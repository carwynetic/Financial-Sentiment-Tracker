import json
from pathlib import Path
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AutoTokenizer,
    BertTokenizer,
    BertForSequenceClassification,
    get_linear_schedule_with_warmup
)
from sklearn.metrics import classification_report, accuracy_score, f1_score


# 1. DATASET CHUYÊN BIỆT CHO TRAINING TRANSFORMERS
class FinancialDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long)
        }


# 2. TÍNH TOÁN TRỌNG SỐ LỚP NGHỊCH ĐẢO CHỐNG MẤT CÂN BẰNG
def compute_class_weights(labels, num_classes=3):
    counts = np.bincount(labels, minlength=num_classes)
    total = len(labels)
    # Công thức: w_c = N / (C * N_c)
    weights = total / (num_classes * counts.astype(np.float32))
    # Chuẩn hóa về float32 tensor
    weights_tensor = torch.tensor(weights, dtype=torch.float)
    print(f"[*] Phân phối nhãn Train: Negative={counts[0]}, Neutral={counts[1]}, Positive={counts[2]}")
    print(f"[*] Trọng số Loss tính được: {weights_tensor.tolist()}")
    return weights_tensor


# 3. HÀM ĐÁNH GIÁ (VALIDATION & TEST)
def evaluate(model, dataloader, device):
    model.eval()
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            with torch.cuda.amp.autocast():
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits

            preds = torch.argmax(logits, dim=1).cpu().tolist()
            all_preds.extend(preds)
            all_targets.extend(labels.cpu().tolist())

    acc = accuracy_score(all_targets, all_preds)
    macro_f1 = f1_score(all_targets, all_preds, average="macro")
    weighted_f1 = f1_score(all_targets, all_preds, average="weighted")
    return acc, macro_f1, weighted_f1, all_preds, all_targets


# 4. VÒNG LẶP HUẤN LUYỆN CHÍNH (TRAINING LOOP)
def train():
    # Cấu hình siêu tham số (Hyperparameters)
    MODEL_NAME = "yiyanghkust/finbert-tone"
    BATCH_SIZE = 16
    MAX_LEN = 128
    EPOCHS = 4
    LEARNING_RATE = 2e-5
    WEIGHT_DECAY = 0.01

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Đang chạy trên thiết bị: {device} ({torch.cuda.get_device_name(0)})")

    # Đọc dữ liệu
    train_df = pd.read_parquet("data/processed/train.parquet")
    val_df = pd.read_parquet("data/processed/val.parquet")
    test_df = pd.read_parquet("data/processed/test.parquet")
    print(f"[*] Kích thước dữ liệu: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")

    # Nạp Tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    except Exception:
        tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

    # Khởi tạo Dataloaders
    train_dataset = FinancialDataset(train_df["sentence"].tolist(), train_df["label"].tolist(), tokenizer, MAX_LEN)
    val_dataset = FinancialDataset(val_df["sentence"].tolist(), val_df["label"].tolist(), tokenizer, MAX_LEN)
    test_dataset = FinancialDataset(test_df["sentence"].tolist(), test_df["label"].tolist(), tokenizer, MAX_LEN)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    # Nạp Model với cấu hình 3 nhãn chuẩn
    # Cấu hình ánh xạ chuẩn: 0: Negative, 1: Neutral, 2: Positive
    id2label = {0: "negative", 1: "neutral", 2: "positive"}
    label2id = {"negative": 0, "neutral": 1, "positive": 2}

    print(f"[*] Đang nạp mô hình nền tảng: {MODEL_NAME}...")
    model = BertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True
    ).to(device)

    # Hàm mất mát có bù trọng số lớp
    class_weights = compute_class_weights(train_df["label"].tolist()).to(device)
    loss_fn = nn.CrossEntropyLoss(weight=class_weights)

    # Optimizer & Scheduler
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    total_steps = len(train_loader) * EPOCHS
    warmup_steps = int(0.1 * total_steps)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=total_steps)

    # Bộ tăng tốc Mixed Precision (AMP)
    scaler = torch.cuda.amp.GradScaler()

    best_val_macro_f1 = 0.0
    models_dir = Path("models/finbert_best")
    models_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*20} BẮT ĐẦU FINE-TUNING (Tổng cộng {EPOCHS} Epochs) {'='*20}")

    for epoch in range(1, EPOCHS + 1):
        model.train()
        total_train_loss = 0.0

        for step, batch in enumerate(train_loader, 1):
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            optimizer.zero_grad()

            with torch.cuda.amp.autocast():
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                loss = loss_fn(outputs.logits, labels)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()

            total_train_loss += loss.item()

        avg_train_loss = total_train_loss / len(train_loader)

        # Đánh giá trên Validation set
        val_acc, val_f1, val_weighted_f1, _, _ = evaluate(model, val_loader, device)

        print(f"Epoch {epoch}/{EPOCHS} | Train Loss: {avg_train_loss:.4f} | Val Acc: {val_acc*100:.2f}% | Val Macro F1: {val_f1*100:.2f}%")

        # Lưu checkpoint tốt nhất theo Macro F1
        if val_f1 > best_val_macro_f1:
            best_val_macro_f1 = val_f1
            print(f"  [+] Đạt kỷ lục Val Macro F1 mới ({val_f1*100:.2f}%)! Đang lưu mô hình vào {models_dir}...")
            model.save_pretrained(models_dir)
            tokenizer.save_pretrained(models_dir)

    print(f"\n{'='*20} HUẤN LUYỆN HOÀN TẤT {'='*20}")
    print(f"[*] Kỷ lục Validation Macro F1 tốt nhất: {best_val_macro_f1*100:.2f}%")

    # 5. ĐÁNH GIÁ CUỐI CÙNG TRÊN TẬP TEST BẰNG CHECKPOINT TỐT NHẤT
    print(f"\n[*] Đang nạp lại checkpoint tốt nhất từ {models_dir} để kiểm định Test Set...")
    best_model = BertForSequenceClassification.from_pretrained(models_dir).to(device)
    
    test_acc, test_macro_f1, test_weighted_f1, test_preds, test_targets = evaluate(best_model, test_loader, device)
    target_names = ["Negative (0)", "Neutral (1)", "Positive (2)"]
    report = classification_report(test_targets, test_preds, target_names=target_names, digits=4, output_dict=True)

    print("\n--- KẾT QUẢ ĐÁNH GIÁ CUỐI CÙNG TRÊN TEST SET ---")
    print(classification_report(test_targets, test_preds, target_names=target_names, digits=4))
    print(f"Test Accuracy    : {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"Test Macro F1    : {test_macro_f1:.4f} ({test_macro_f1*100:.2f}%)")
    print(f"Test Weighted F1 : {test_weighted_f1:.4f} ({test_weighted_f1*100:.2f}%)")

    # Lưu metrics vào reports/metrics/finbert_fine_tuned.json
    metrics_path = Path("reports/metrics/finbert_fine_tuned.json")
    results = {
        "model_name": MODEL_NAME,
        "best_val_macro_f1": float(best_val_macro_f1),
        "test_accuracy": float(test_acc),
        "test_macro_f1": float(test_macro_f1),
        "test_weighted_f1": float(test_weighted_f1),
        "classification_report": report
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"[+] Đã lưu kết quả tại: {metrics_path}")


if __name__ == "__main__":
    train()