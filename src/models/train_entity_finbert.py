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


# 1. DATASET PHÂN LOẠI CẶP CÂU (SENTENCE-PAIR DATASET)
class EntityFinancialDataset(Dataset):
    def __init__(self, entities, headlines, labels, tokenizer, max_len=128):
        self.entities = entities
        self.headlines = headlines
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.entities)

    def __getitem__(self, idx):
        entity = str(self.entities[idx])
        headline = str(self.headlines[idx])
        label = self.labels[idx]

        # ĐIỂM CỐT LÕI: Nạp cặp (Entity, Headline) vào Tokenizer
        encoding = self.tokenizer(
            text=entity,
            text_pair=headline,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "token_type_ids": encoding.get("token_type_ids", torch.zeros_like(encoding["input_ids"])).squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long)
        }


# 2. HÀM ĐÁNH GIÁ (VALIDATION & TEST)
def evaluate(model, dataloader, device):
    model.eval()
    all_preds = []
    all_targets = []

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            token_type_ids = batch["token_type_ids"].to(device)
            labels = batch["labels"].to(device)

            with torch.amp.autocast("cuda"):
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    token_type_ids=token_type_ids
                )
                logits = outputs.logits

            preds = torch.argmax(logits, dim=1).cpu().tolist()
            all_preds.extend(preds)
            all_targets.extend(labels.cpu().tolist())

    acc = accuracy_score(all_targets, all_preds)
    macro_f1 = f1_score(all_targets, all_preds, average="macro")
    weighted_f1 = f1_score(all_targets, all_preds, average="weighted")
    return acc, macro_f1, weighted_f1, all_preds, all_targets


# 3. TRAINING LOOP CHO ENTITY-AWARE FINBERT
def train():
    MODEL_NAME = "yiyanghkust/finbert-tone"
    BATCH_SIZE = 32  # Tối ưu cho RTX 3050 6GB
    MAX_LEN = 128
    EPOCHS = 3
    LEARNING_RATE = 2e-5
    WEIGHT_DECAY = 0.01

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Thiết bị huấn luyện: {device} ({torch.cuda.get_device_name(0)})")

    # Đọc dữ liệu SEntFiN
    train_df = pd.read_parquet("data/processed/sentfin_train.parquet")
    val_df = pd.read_parquet("data/processed/sentfin_val.parquet")
    test_df = pd.read_parquet("data/processed/sentfin_test.parquet")
    print(f"[*] Dữ liệu SEntFiN: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")

    # Nạp Tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    except Exception:
        tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

    # Khởi tạo Dataloaders
    train_dataset = EntityFinancialDataset(train_df["entity"].tolist(), train_df["headline"].tolist(), train_df["label"].tolist(), tokenizer, MAX_LEN)
    val_dataset = EntityFinancialDataset(val_df["entity"].tolist(), val_df["headline"].tolist(), val_df["label"].tolist(), tokenizer, MAX_LEN)
    test_dataset = EntityFinancialDataset(test_df["entity"].tolist(), test_df["headline"].tolist(), test_df["label"].tolist(), tokenizer, MAX_LEN)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    # Nạp Model
    id2label = {0: "negative", 1: "neutral", 2: "positive"}
    label2id = {"negative": 0, "neutral": 1, "positive": 2}

    print(f"[*] Đang nạp mô hình: {MODEL_NAME}...")
    model = BertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True
    ).to(device)

    # Cross-Entropy Loss
    loss_fn = nn.CrossEntropyLoss()

    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    total_steps = len(train_loader) * EPOCHS
    warmup_steps = int(0.1 * total_steps)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=total_steps)

    scaler = torch.amp.GradScaler("cuda")

    best_val_macro_f1 = 0.0
    models_dir = Path("models/finbert_entity_best")
    models_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*20} BẮT ĐẦU FINE-TUNING ENTITY-AWARE ({EPOCHS} Epochs) {'='*20}")

    for epoch in range(1, EPOCHS + 1):
        model.train()
        total_train_loss = 0.0

        for step, batch in enumerate(train_loader, 1):
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            token_type_ids = batch["token_type_ids"].to(device)
            labels = batch["labels"].to(device)

            optimizer.zero_grad()

            with torch.amp.autocast("cuda"):
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    token_type_ids=token_type_ids
                )
                loss = loss_fn(outputs.logits, labels)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()

            total_train_loss += loss.item()

        avg_train_loss = total_train_loss / len(train_loader)
        val_acc, val_f1, val_weighted_f1, _, _ = evaluate(model, val_loader, device)

        print(f"Epoch {epoch}/{EPOCHS} | Train Loss: {avg_train_loss:.4f} | Val Acc: {val_acc*100:.2f}% | Val Macro F1: {val_f1*100:.2f}%")

        if val_f1 > best_val_macro_f1:
            best_val_macro_f1 = val_f1
            print(f"  [+] Đạt kỷ lục Val Macro F1 mới ({val_f1*100:.2f}%)! Lưu checkpoint vào {models_dir}...")
            model.save_pretrained(models_dir)
            tokenizer.save_pretrained(models_dir)

    print(f"\n{'='*20} HUẤN LUYỆN HOÀN TẤT {'='*20}")

    # 4. ĐÁNH GIÁ TRÊN TẬP TEST SENTFIN
    print(f"[*] Đang đánh giá checkpoint tối ưu trên SENTFIN_TEST ({len(test_df)} mẫu)...")
    best_model = BertForSequenceClassification.from_pretrained(models_dir).to(device)
    test_acc, test_macro_f1, test_weighted_f1, test_preds, test_targets = evaluate(best_model, test_loader, device)

    target_names = ["Negative (0)", "Neutral (1)", "Positive (2)"]
    report = classification_report(test_targets, test_preds, target_names=target_names, digits=4, output_dict=True)

    print("\n--- KẾT QUẢ ĐÁNH GIÁ TRÊN SENTFIN TEST SET ---")
    print(classification_report(test_targets, test_preds, target_names=target_names, digits=4))
    print(f"Test Accuracy    : {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"Test Macro F1    : {test_macro_f1:.4f} ({test_macro_f1*100:.2f}%)")
    print(f"Test Weighted F1 : {test_weighted_f1:.4f} ({test_weighted_f1*100:.2f}%)")

    # Lưu metrics vào reports/metrics/finbert_entity_aware.json
    metrics_path = Path("reports/metrics/finbert_entity_aware.json")
    results = {
        "benchmark": "SEntFiN 1.0 (Entity-Aware)",
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