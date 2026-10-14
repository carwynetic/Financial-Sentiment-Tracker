import ast
import urllib.request
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

SENTFIN_URL = "https://raw.githubusercontent.com/pyRis/SEntFiN/main/SEntFiN.csv"
RAW_FILE = RAW_DIR / "SEntFiN.csv"

LABEL_MAP = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}


def download_raw_sentfin():
    """Tải file SEntFiN.csv từ GitHub chính thức nếu chưa có."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if not RAW_FILE.exists():
        print(f"[*] Đang tải SEntFiN.csv từ {SENTFIN_URL}...")
        urllib.request.urlretrieve(SENTFIN_URL, RAW_FILE)
        print(f"[+] Đã tải xong và lưu tại: {RAW_FILE}")
    else:
        print(f"[*] Đã tìm thấy file thô tại: {RAW_FILE}")


def parse_and_flatten_entities(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Bóc tách cột Decisions dạng dict: {'Entity': 'sentiment'}
    thành các mẫu huấn luyện độc lập: (headline_id, entity, headline, label).
    """
    records = []
    skipped_count = 0

    for idx, row in df_raw.iterrows():
        headline = str(row["Title"]).strip()
        decisions_str = str(row["Decisions"]).strip()

        try:
            # Parse chuỗi dict an toàn bằng ast.literal_eval
            decisions_dict = ast.literal_eval(decisions_str)
        except Exception:
            skipped_count += 1
            continue

        if not isinstance(decisions_dict, dict):
            continue

        for entity, sentiment in decisions_dict.items():
            sent_clean = str(sentiment).strip().lower()
            if sent_clean in LABEL_MAP:
                records.append({
                    "headline_id": idx,  # Khóa bảo vệ chống rò rỉ tiêu đề
                    "entity": str(entity).strip(),
                    "headline": headline,
                    "label_name": sent_clean,
                    "label": LABEL_MAP[sent_clean]
                })

    df_flat = pd.DataFrame(records)
    print(f"[*] Đã bóc tách thành công: {len(df_flat)} cặp (Entity, Headline). Bỏ qua {skipped_count} dòng lỗi format.")
    return df_flat


def split_and_save_leakage_free(df_flat: pd.DataFrame, seed: int = 42):
    """
    Chia 70% Train - 15% Val - 15% Test bảo đảm KHÔNG RÒ RỈ tiêu đề:
    Tất cả thực thể của cùng 1 headline_id phải cùng thuộc 1 tập dữ liệu.
    """
    unique_headlines = df_flat[["headline_id"]].drop_duplicates()

    # Chia ở cấp độ headline_id
    train_hids, temp_hids = train_test_split(unique_headlines, test_size=0.30, random_state=seed)
    val_hids, test_hids = train_test_split(temp_hids, test_size=0.50, random_state=seed)

    train_ids = set(train_hids["headline_id"])
    val_ids = set(val_hids["headline_id"])
    test_ids = set(test_hids["headline_id"])

    # Xác minh khoa học: Giao tập bằng 0
    assert len(train_ids & val_ids) == 0, "LỖI RÒ RỈ DỮ LIỆU: Train và Val trùng tiêu đề!"
    assert len(train_ids & test_ids) == 0, "LỖI RÒ RỈ DỮ LIỆU: Train và Test trùng tiêu đề!"
    assert len(val_ids & test_ids) == 0, "LỖI RÒ RỈ DỮ LIỆU: Val và Test trùng tiêu đề!"
    print("[+] XÁC MINH AN TOÀN: Độ giao thoa tiêu đề giữa 3 tập = 0 (Hoàn toàn không rò rỉ)!")

    # Lọc các bản ghi theo headline_id tương ứng
    train_df = df_flat[df_flat["headline_id"].isin(train_ids)].reset_index(drop=True)
    val_df = df_flat[df_flat["headline_id"].isin(val_ids)].reset_index(drop=True)
    test_df = df_flat[df_flat["headline_id"].isin(test_ids)].reset_index(drop=True)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for name, split_df in [("sentfin_train", train_df), ("sentfin_val", val_df), ("sentfin_test", test_df)]:
        parquet_path = PROCESSED_DIR / f"{name}.parquet"
        csv_path = PROCESSED_DIR / f"{name}.csv"

        split_df.to_parquet(parquet_path, index=False)
        split_df.to_csv(csv_path, index=False, encoding="utf-8")

        print(f"\n[+] Tập {name.upper()}: {len(split_df)} mẫu")
        dist = split_df["label_name"].value_counts(normalize=True) * 100
        for l, p in dist.items():
            print(f"    - {l:<8}: {p:.2f}%")


def main():
    download_raw_sentfin()
    df_raw = pd.read_csv(RAW_FILE)
    print(f"[*] Tổng số dòng thô ban đầu: {len(df_raw)}")
    df_flat = parse_and_flatten_entities(df_raw)
    split_and_save_leakage_free(df_flat, seed=42)
    print("\n[+] HOÀN TẤT BƯỚC 1: Dữ liệu SEntFiN đã sẵn sàng tại data/processed/!")


if __name__ == "__main__":
    main()