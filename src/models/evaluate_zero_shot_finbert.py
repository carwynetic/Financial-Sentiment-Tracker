import json
from pathlib import Path
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    BertTokenizer, 
    BertForSequenceClassification
)
from sklearn.metrics import classification_report, accuracy_score, f1_score


# 1. HỆ QUY CHIẾU NHÃN CHUẨN CỦA DỰ ÁN
PROJECT_LABEL_MAP = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}
TARGET_NAMES = ["Negative (0)", "Neutral (1)", "Positive (2)"]


# 2. DATASET TỐI ƯU CHO PYTORCH
class FinancialTestDataset(Dataset):
    def __init__(self, sentences):
        self.sentences = sentences

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        return str(self.sentences[idx])


def build_hf_to_project_mapping(model_config):
    """
    Giải quyết bẫy Lệch Nhãn:
    Ánh xạ từ id2label của Hugging Face sang [0, 1, 2] chuẩn của dự án.
    """
    id2label = getattr(model_config, "id2label", None)
    
    # Fallback cho checkpoint cũ nếu không có id2label trong config
    if not id2label or "LABEL_0" in str(id2label):
        # Theo chuẩn công bố của yiyanghkust/finbert-tone: 0: Neutral, 1: Positive, 2: Negative
        return {0: 1, 1: 2, 2: 0}

    hf_to_project = {}
    for hf_id, label_str in id2label.items():
        clean_str = str(label_str).strip().lower()
        if clean_str in PROJECT_LABEL_MAP:
            hf_to_project[int(hf_id)] = PROJECT_LABEL_MAP[clean_str]
        else:
            raise ValueError(f"Nhãn lạ từ model: '{label_str}' không nằm trong {PROJECT_LABEL_MAP}")
    return hf_to_project


def evaluate_model(model_name: str, sentences: list, y_true: list, device: torch.device, batch_size: int = 32):
    print(f"\n{'='*25} ĐANG ĐÁNH GIÁ: {model_name} {'='*25}")
    print(f"[*] Đang tải Tokenizer & Model từ Hugging Face Hub...")
    
    # 1. Tải Tokenizer (Fallback AutoTokenizer -> BertTokenizer)
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except Exception:
        print(f"[!] AutoTokenizer gặp hạn chế config cũ, chuyển sang BertTokenizer chuẩn...")
        tokenizer = BertTokenizer.from_pretrained(model_name)

    # 2. Tải Model (Fallback AutoModel -> BertForSequenceClassification)
    try:
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
    except Exception:
        print(f"[!] AutoModel gặp hạn chế config cũ, chuyển sang BertForSequenceClassification chuẩn...")
        model = BertForSequenceClassification.from_pretrained(model_name)

    model.to(device)
    model.eval()  # Chuyển sang chế độ đánh giá (tắt Dropout)

    # 3. Xây dựng bảng ánh xạ nhãn
    hf_to_project = build_hf_to_project_mapping(model.config)
    print(f"[*] Bảng ánh xạ nhãn phát hiện được -> {hf_to_project}")

    dataset = FinancialTestDataset(sentences)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    all_preds = []
    print(f"[*] Đang chạy suy luận trên GPU ({device})...")
    
    # Chống rò rỉ VRAM: bắt buộc torch.no_grad()
    with torch.no_grad():
        for batch_texts in dataloader:
            inputs = tokenizer(
                list(batch_texts),
                padding=True,
                truncation=True,
                max_length=128,
                return_tensors="pt"
            ).to(device)

            outputs = model(**inputs)
            logits = outputs.logits
            batch_hf_preds = torch.argmax(logits, dim=1).cpu().tolist()
            batch_project_preds = [hf_to_project[p] for p in batch_hf_preds]
            all_preds.extend(batch_project_preds)

    # 4. Tính toán các chỉ số khoa học
    acc = accuracy_score(y_true, all_preds)
    macro_f1 = f1_score(y_true, all_preds, average="macro")
    weighted_f1 = f1_score(y_true, all_preds, average="weighted")
    report = classification_report(y_true, all_preds, target_names=TARGET_NAMES, digits=4, output_dict=True)

    print(f"\n--- KẾT QUẢ CHO {model_name} ---")
    print(classification_report(y_true, all_preds, target_names=TARGET_NAMES, digits=4))
    print(f"Test Accuracy    : {acc:.4f} ({acc*100:.2f}%)")
    print(f"Test Macro F1    : {macro_f1:.4f} ({macro_f1*100:.2f}%)")
    print(f"Test Weighted F1 : {weighted_f1:.4f} ({weighted_f1*100:.2f}%)")

    # Giải phóng VRAM GPU sau khi xong mỗi model
    del model
    del tokenizer
    torch.cuda.empty_cache()

    return {
        "accuracy": float(acc),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "classification_report": report
    }


def main():
    # 1. Tải tập test
    test_path = Path("data/processed/test.parquet")
    if not test_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {test_path}")

    test_df = pd.read_parquet(test_path)
    sentences = test_df["sentence"].tolist()
    y_true = test_df["label"].tolist()
    print(f"[*] Đã tải tập Test: {len(sentences)} mẫu.")

    # 2. Thiết lập phần cứng
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Thiết bị suy luận: {device} ({torch.cuda.get_device_name(0)})")

    # 3. Danh sách mô hình FinBERT cần benchmark Zero-Shot
    candidate_models = [
        "ProsusAI/finbert",
        "yiyanghkust/finbert-tone"
    ]

    all_results = {}
    for model_name in candidate_models:
        all_results[model_name] = evaluate_model(
            model_name=model_name,
            sentences=sentences,
            y_true=y_true,
            device=device,
            batch_size=32
        )

    # 4. Lưu kết quả vào reports/metrics/finbert_zero_shot.json
    output_dir = Path("reports/metrics")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "finbert_zero_shot.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)

    print(f"\n[+] ĐÃ HOÀN TẤT & LƯU KẾT QUẢ TẠI: {output_file}")


if __name__ == "__main__":
    main()