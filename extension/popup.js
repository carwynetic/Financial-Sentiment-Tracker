const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", async () => {
    const inputText = document.getElementById("inputText");
    const targetEntity = document.getElementById("targetEntity");
    const btnAnalyze = document.getElementById("btnAnalyze");
    const btnFetchSelection = document.getElementById("btnFetchSelection");
    const resultBox = document.getElementById("resultBox");
    const targetEntityDisplay = document.getElementById("targetEntityDisplay");
    const sentimentBadge = document.getElementById("sentimentBadge");
    const confidenceText = document.getElementById("confidenceText");
    const latencyText = document.getElementById("latencyText");
    const posBar = document.getElementById("posBar");
    const negBar = document.getElementById("negBar");
    const neuBar = document.getElementById("neuBar");
    const posVal = document.getElementById("posVal");
    const negVal = document.getElementById("negVal");
    const neuVal = document.getElementById("neuVal");

    // 1. Kiểm tra kết nối API Backend
    checkBackendHealth();

    // 2. Tự động kiểm tra xem có văn bản bôi đen từ context menu không
    chrome.storage.local.get(["selectedText"], (res) => {
        if (res.selectedText && res.selectedText.trim()) {
            inputText.value = res.selectedText.trim();
            chrome.storage.local.remove(["selectedText"]);
            analyzeSentiment(inputText.value, targetEntity.value.trim());
        } else {
            // Nếu không, thử lấy nội dung bôi đen trực tiếp từ tab đang active
            fetchSelectionFromActiveTab();
        }
    });

    // Nút lấy nội dung bôi đen
    btnFetchSelection.addEventListener("click", () => {
        fetchSelectionFromActiveTab();
    });

    // Nút phân tích
    btnAnalyze.addEventListener("click", () => {
        const text = inputText.value.trim();
        if (!text) {
            alert("Vui lòng nhập hoặc bôi đen văn bản cần phân tích!");
            return;
        }
        analyzeSentiment(text, targetEntity.value.trim());
    });

    async function checkBackendHealth() {
        try {
            const res = await fetch(`${API_URL}/health`);
            if (res.ok) {
                const data = await res.json();
                const entityReady = data.entity_model_loaded ? " + Entity-Aware" : "";
                document.getElementById("statusIndicator").innerHTML = `<span class="status-dot"></span> <span style="font-size:11px; color:#22c55e;">GPU Online${entityReady}</span>`;
            }
        } catch (e) {
            document.getElementById("statusIndicator").innerHTML = '<span class="status-dot status-offline"></span> <span style="font-size:11px; color:#ef4444;">Offline</span>';
        }
    }

    function fetchSelectionFromActiveTab() {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (!tabs || !tabs[0] || !tabs[0].id) return;
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                func: () => window.getSelection().toString()
            }, (results) => {
                if (results && results[0] && results[0].result && results[0].result.trim()) {
                    inputText.value = results[0].result.trim();
                    analyzeSentiment(inputText.value, targetEntity.value.trim());
                }
            });
        });
    }

    async function analyzeSentiment(text, entity) {
        btnAnalyze.innerText = "⏳ Đang quét...";
        btnAnalyze.disabled = true;

        try {
            const startTime = performance.now();
            let endpoint = `${API_URL}/predict/sentiment`;
            let payload = { text: text };

            if (entity) {
                endpoint = `${API_URL}/predict/entity-sentiment`;
                payload = { entity: entity, headline: text };
            }

            const res = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const latency = (performance.now() - startTime).toFixed(1);

            if (res.ok) {
                const data = await res.json();
                displayResult(data, latency, entity);
            } else {
                alert("Lỗi phân tích: " + (await res.text()));
            }
        } catch (err) {
            alert("Không thể kết nối FastAPI backend tại http://127.0.0.1:8000. Hãy đảm bảo server đang chạy!");
        } finally {
            btnAnalyze.innerText = "🚀 Phân tích ngay";
            btnAnalyze.disabled = false;
        }
    }

    function displayResult(data, latency, entity) {
        resultBox.style.display = "block";
        const sent = data.sentiment.toLowerCase();

        // Hiển thị thông tin thực thể nếu là entity-aware
        if (entity && targetEntityDisplay) {
            targetEntityDisplay.style.display = "block";
            targetEntityDisplay.innerHTML = `🎯 Target Entity: <span style="color:#ffffff;">${data.entity}</span> <span style="font-size:10px; color:#94a3b8;">(Cross-Attention)</span>`;
        } else if (targetEntityDisplay) {
            targetEntityDisplay.style.display = "none";
        }

        // Thiết lập nhãn cảm xúc
        if (sent === "positive") {
            sentimentBadge.className = "badge positive";
            sentimentBadge.innerText = "🟢 TÍCH CỰC (BULLISH)";
        } else if (sent === "negative") {
            sentimentBadge.className = "badge negative";
            sentimentBadge.innerText = "🔴 TIÊU CỰC (BEARISH)";
        } else {
            sentimentBadge.className = "badge neutral";
            sentimentBadge.innerText = "⚪ TRUNG TÍNH (NEUTRAL)";
        }

        confidenceText.innerText = `Độ tin cậy: ${(data.confidence * 100).toFixed(1)}%`;
        latencyText.innerText = `⚡ Latency: ${latency} ms (FinBERT GPU RTX 3050)`;

        // Cập nhật thanh tiến trình xác suất
        const p = data.probabilities;
        const pPos = (p.positive * 100).toFixed(1);
        const pNeg = (p.negative * 100).toFixed(1);
        const pNeu = (p.neutral * 100).toFixed(1);

        posBar.style.width = pPos + "%";
        negBar.style.width = pNeg + "%";
        neuBar.style.width = pNeu + "%";

        posVal.innerText = pPos + "%";
        negVal.innerText = pNeg + "%";
        neuVal.innerText = pNeu + "%";
    }
});