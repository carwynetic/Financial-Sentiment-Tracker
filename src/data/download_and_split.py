"""
File này thực hiện:

Tải dataset financial_phrasebank (sentences_75agree) từ Hugging Face.
Ánh xạ nhãn: 0: negative, 1: neutral, 2: positive.
Chia Stratified Split chuẩn: 70% Train - 15% Val - 15% Test (random_state=42).
Kiểm tra kiểm định: Kiểm tra rò rỉ dữ liệu (zero ID overlap) và so sánh tỷ lệ phân phối nhãn giữa 3 tập.
Lưu ra cả định dạng .parquet (chuẩn pipeline) và .csv (để dễ mở xem).
"""
import os
import zipfile
from pathlib import Path
import pandas as pd
from huggingface_hub import hf_hub_download
from sklearn.model_selection import train_test_split

#1. config path
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
LABEL_NAME_TO_ID = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}

def load_benchmark_data(subset_filename: str = "Sentences_75Agree.txt") -> pd.DataFrame:
    zip_path = hf_hub_download(
        repo_id="takala/financial_phrasebank",
        filename="data/FinancialPhraseBank-v1.0.zip",
        repo_type="dataset"
    )
    
    print(f"[*] Đang đọc tập dữ liệu: {subset_filename}...")
    records = []
    with zipfile.ZipFile(zip_path, "r") as z:
        with z.open(f"FinancialPhraseBank-v1.0/{subset_filename}") as f:
            for line in f:
                text = line.decode("iso-8859-1").strip()
                if "@" in text:
                    sentence, label_str = text.rsplit("@", 1)
                    sentence = sentence.strip()
                    label_str = label_str.strip()
                    records.append({
                        "sentence": sentence,
                        "label_name": label_str,
                        "label": LABEL_NAME_TO_ID[label_str]
                    })
    df = pd.DataFrame(records)
    df["id"] = df.index  # ID duy nhất để kiểm định rò rỉ dữ liệu
    # Lưu bản raw backup
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / "financial_phrasebank_75agree.csv"
    df.to_csv(raw_path, index=False, encoding="utf-8")
    print(f"[+] Đã lưu dữ liệu thô tại: {raw_path} ({len(df)} dòng)")
    return df
    
def split_and_freeze_data(df : pd.DataFrame, seed : int = 42):
    #70 : 15 : 15 - train/valid/test
    train_df, temp_df = train_test_split(
        df,
        test_size=0.30,
        random_state=seed,
        stratify=df["label"]
    )
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        random_state=seed,
        stratify=temp_df["label"]
    )
    #integrity check
    train_ids = set(train_df["id"])
    val_ids = set(val_df["id"])
    test_ids = set(test_df["id"])

    assert len(train_ids & val_ids)==0, "dataleakage: train & val"
    assert len(train_ids & test_ids)==0, "dataleakage: train & test"
    assert len(val_ids & test_ids)==0, "dataleakage: val & test"
    print("No data leakage between 3 set")

    #4. xuat file vao data/processed
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for name, split_df in [("train", train_df), ("val", val_df), ("test", test_df)]:
        parquet_path = PROCESSED_DIR / f"{name}.parquet"
        csv_path = PROCESSED_DIR / f"{name}.csv"
        
        split_df.to_parquet(parquet_path, index=False)
        split_df.to_csv(csv_path, index=False, encoding="utf-8")

        print(f"\n[+] Tập {name.upper()}: {len(split_df)} mẫu")
        dist = split_df["label_name"].value_counts(normalize=True) * 100
        for label, pct in dist.items():
            print(f"    - {label:<8}: {pct:.2f}%")


if __name__ == "__main__":
    df = load_benchmark_data()
    split_and_freeze_data(df, seed=42)