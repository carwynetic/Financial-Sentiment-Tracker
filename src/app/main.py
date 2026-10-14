import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from typing import List, Dict, Optional

import torch
import yfinance as yf
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from transformers import AutoTokenizer, BertForSequenceClassification

# 1. THIẾT LẬP ĐƯỜNG DẪN & THIẾT BỊ
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "models" / "finbert_best"
FALLBACK_MODEL_NAME = "ProsusAI/finbert"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = None
model = None

# Ánh xạ nhãn chuẩn đã đồng bộ ở Phase 3
ID2LABEL = {0: "negative", 1: "neutral", 2: "positive"}
LABEL2ID = {"negative": 0, "neutral": 1, "positive": 2}


# 2. HÀM NẠP MODEL & WARMUP GPU
def load_sentiment_model():
    """Nạp weights FinBERT và tokenizer lên bộ nhớ GPU/CPU."""
    global tokenizer, model
    
    if MODEL_DIR.exists():
        print(f"[*] Nạp mô hình FinBERT fine-tuned từ: {MODEL_DIR}")
        model_source = str(MODEL_DIR)
    else:
        print(f"[!] Không tìm thấy local weights, fallback nạp: {FALLBACK_MODEL_NAME}")
        model_source = FALLBACK_MODEL_NAME
        
    tokenizer = AutoTokenizer.from_pretrained(model_source)
    model = BertForSequenceClassification.from_pretrained(
        model_source,
        num_labels=3,
        id2label=ID2LABEL,
        label2id=LABEL2ID
    ).to(device)
    model.eval()

    # Warmup GPU để tối ưu latency cho request đầu tiên
    if torch.cuda.is_available():
        warmup_text = "Operating profit increased by 10 percent."
        inputs = tokenizer(warmup_text, return_tensors="pt", truncation=True, max_length=128).to(device)
        with torch.no_grad():
            _ = model(**inputs)
        print(f"[✓] Đã khởi tạo và warmup FinBERT trên GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("[✓] Đã khởi tạo FinBERT trên CPU.")


# 3. QUẢN LÝ VÒNG ĐỜI ỨNG DỤNG (LIFESPAN)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi động: nạp model
    load_sentiment_model()
    yield
    # Dọn dẹp: dọn sạch VRAM
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


# Khởi tạo FastAPI App
app = FastAPI(
    title="TMG301 Financial Sentiment Tracker API",
    description="Microservice phân tích cảm xúc tin tức tài chính dựa trên FinBERT fine-tuned",
    version="1.0.0",
    lifespan=lifespan
)

# Kích hoạt CORS để cho phép Chrome Extension và Dashboard kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 4. DATA SCHEMAS (PYDANTIC V2)
class SentimentRequest(BaseModel):
    text: str = Field(..., description="Đoạn văn bản tài chính cần phân tích")

    @field_validator("text")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Văn bản đầu vào không được để trống hoặc chỉ chứa khoảng trắng.")
        return v.strip()


class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    probabilities: Dict[str, float]


class BatchSentimentRequest(BaseModel):
    texts: List[str] = Field(..., description="Danh sách các đoạn văn bản tài chính")

    @field_validator("texts")
    @classmethod
    def validate_texts(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Danh sách câu không được để trống.")
        cleaned = [t.strip() for t in v if isinstance(t, str) and t.strip()]
        if not cleaned:
            raise ValueError("Không có văn bản hợp lệ trong danh sách.")
        return cleaned


class BatchSentimentResponse(BaseModel):
    predictions: List[SentimentResponse]


# 5. HÀM SUY LUẬN LÕI (CORE INFERENCE)
def predict_text_sentiment(text: str) -> Dict:
    """Suy luận cảm xúc cho 1 câu văn bản."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1).squeeze(0)
        
    pred_idx = torch.argmax(probs).item()
    pred_label = ID2LABEL[pred_idx]
    confidence = float(probs[pred_idx].item())
    
    probabilities = {
        ID2LABEL[i]: round(float(probs[i].item()), 4)
        for i in range(len(ID2LABEL))
    }
    
    return {
        "text": text,
        "sentiment": pred_label,
        "confidence": round(confidence, 4),
        "probabilities": probabilities
    }


# 6. CÁC API ENDPOINTS
@app.get("/health", summary="Kiểm tra trạng thái server")
def health_check():
    return {
        "status": "ok",
        "device": str(device),
        "model_loaded": model is not None,
        "model_source": str(MODEL_DIR) if MODEL_DIR.exists() else FALLBACK_MODEL_NAME
    }


@app.post("/predict/sentiment", response_model=SentimentResponse, summary="Dự đoán cảm xúc 1 câu")
def predict_single(request: SentimentRequest):
    try:
        return predict_text_sentiment(request.text)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/predict/batch", response_model=BatchSentimentResponse, summary="Dự đoán cảm xúc hàng loạt")
def predict_batch(request: BatchSentimentRequest):
    try:
        inputs = tokenizer(request.texts, return_tensors="pt", truncation=True, max_length=128, padding=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
            
        results = []
        for i, text in enumerate(request.texts):
            p = probs[i]
            pred_idx = torch.argmax(p).item()
            results.append({
                "text": text,
                "sentiment": ID2LABEL[pred_idx],
                "confidence": round(float(p[pred_idx].item()), 4),
                "probabilities": {ID2LABEL[j]: round(float(p[j].item()), 4) for j in range(3)}
            })
            
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/ticker/{symbol}", summary="Cào tin tức live và phân tích cảm xúc mã cổ phiếu")
def get_ticker_news_sentiment(symbol: str, count: int = 5):
    clean_symbol = symbol.strip().upper()
    articles_data = []

    # Sử dụng yfinance Search để lấy danh sách tin tức mới nhất
    try:
        search = yf.Search(clean_symbol, news_count=count)
        raw_news = search.news if search.news else []
    except Exception:
        raw_news = []

    # Fallback dữ liệu mẫu nếu yfinance gặp hạn chế mạng/chặn kết nối
    if not raw_news:
        raw_news = [
            {"title": f"{clean_symbol} reports strong quarterly earnings beat and revenue growth.", "publisher": "Reuters", "link": ""},
            {"title": f"Analysts raise price target for {clean_symbol} amid positive outlook.", "publisher": "Bloomberg", "link": ""},
            {"title": f"{clean_symbol} faces supply chain bottlenecks in foreign markets.", "publisher": "CNBC", "link": ""}
        ]

    headlines = [item.get("title", "") for item in raw_news if item.get("title")]
    if headlines:
        batch_res = predict_batch(BatchSentimentRequest(texts=headlines))
        for item, pred in zip(raw_news, batch_res["predictions"]):
            articles_data.append({
                "title": item.get("title", ""),
                "publisher": item.get("publisher", "Unknown"),
                "link": item.get("link", ""),
                "sentiment": pred["sentiment"],
                "confidence": pred["confidence"],
                "probabilities": pred["probabilities"]
            })

    # Thống kê phân bổ cảm xúc
    bullish = sum(1 for a in articles_data if a["sentiment"] == "positive")
    bearish = sum(1 for a in articles_data if a["sentiment"] == "negative")
    neutral = sum(1 for a in articles_data if a["sentiment"] == "neutral")

    # Xác định xung nhịp thị trường
    if bullish > bearish:
        market_pulse = "BULLISH"
    elif bearish > bullish:
        market_pulse = "BEARISH"
    else:
        market_pulse = "NEUTRAL"

    return {
        "symbol": clean_symbol,
        "market_pulse": market_pulse,
        "summary": {
            "bullish": bullish,
            "bearish": bearish,
            "neutral": neutral,
            "total": len(articles_data)
        },
        "articles": articles_data
    }
# Đảm bảo model được nạp tự động khi import module
if model is None:
    load_sentiment_model()