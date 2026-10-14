// Khởi tạo Context Menu khi cài đặt extension
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "analyzeFinBertSentiment",
        title: "⚡ Phân tích cảm xúc với FinBERT",
        contexts: ["selection"]
    });
});

// Khi người dùng bấm vào menu chuột phải
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "analyzeFinBertSentiment" && info.selectionText) {
        // Lưu tạm văn bản vừa bôi đen vào storage của Chrome
        chrome.storage.local.set({ selectedText: info.selectionText }, () => {
            // Mở popup hoặc gửi thông báo
            chrome.action.openPopup();
        });
    }
});