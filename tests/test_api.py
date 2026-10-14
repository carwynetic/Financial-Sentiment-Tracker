import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import time
import pytest
from fastapi.testclient import TestClient
from src.app.main import app


# Sử dụng pytest fixture với context manager để kích hoạt đầy đủ lifespan của FastAPI
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    """Kiểm tra endpoint /health xem server và model đã sẵn sàng chưa."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "device" in data
    assert data["model_loaded"] is True


def test_predict_sentiment_positive(client):
    """Kiểm tra dự đoán câu tài chính mang tính tích cực rõ rệt."""
    payload = {"text": "Operating profit increased by 25% due to strong revenue growth across all sectors."}
    response = client.post("/predict/sentiment", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["text"] == payload["text"]
    assert data["sentiment"] == "positive"
    assert 0.0 <= data["confidence"] <= 1.0
    
    probs = data["probabilities"]
    assert "positive" in probs and "negative" in probs and "neutral" in probs
    assert abs(sum(probs.values()) - 1.0) < 1e-3


def test_predict_sentiment_negative(client):
    """Kiểm tra dự đoán câu tài chính mang tính tiêu cực rõ rệt."""
    payload = {"text": "Net income plummeted by 40% amid rising operational expenses and product recalls."}
    response = client.post("/predict/sentiment", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["sentiment"] == "negative"
    assert data["confidence"] > 0.6


def test_predict_sentiment_empty_input(client):
    """Kiểm tra cơ chế Validation của Pydantic khi chuỗi rỗng."""
    payload = {"text": ""}
    response = client.post("/predict/sentiment", json=payload)
    assert response.status_code == 422


def test_predict_batch(client):
    """Kiểm tra suy luận hàng loạt (Batch Inference)."""
    payload = {
        "texts": [
            "Operating profit increased by 25%.",
            "Operating loss widened significantly and revenues dropped by 30%.",
            "The company will publish its interim report next Tuesday."
        ]
    }
    response = client.post("/predict/batch", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "predictions" in data
    assert len(data["predictions"]) == 3
    assert data["predictions"][0]["sentiment"] == "positive"
    assert data["predictions"][1]["sentiment"] == "negative"
    assert data["predictions"][2]["sentiment"] == "neutral"


def test_ticker_news_sentiment(client):
    """Kiểm tra endpoint cào tin tức live và chấm điểm sentiment theo mã cổ phiếu."""
    response = client.get("/ticker/AAPL")
    assert response.status_code == 200
    
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert "market_pulse" in data
    assert "summary" in data
    assert "bullish" in data["summary"]
    assert "bearish" in data["summary"]
    assert "neutral" in data["summary"]
    assert isinstance(data["articles"], list)


def test_api_latency(client):
    """Đo đạc hiệu năng suy luận (Inference Latency) sau warmup."""
    payload = {"text": "Total sales rose to 150 million euros compared to 120 million euros last year."}
    
    # Warmup 1 lần
    client.post("/predict/sentiment", json=payload)
    
    # Đo thời gian request thứ hai
    start_time = time.perf_counter()
    response = client.post("/predict/sentiment", json=payload)
    latency_ms = (time.perf_counter() - start_time) * 1000
    
    assert response.status_code == 200
    print(f"\n[BENCHMARK] Latency đơn mẫu: {latency_ms:.2f} ms")
    assert latency_ms < 100.0, f"Độ trễ quá cao: {latency_ms:.2f} ms"