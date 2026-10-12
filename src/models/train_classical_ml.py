import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score, f1_score


def load_datasets():
    """Tải 3 tập dữ liệu cố định: Train, Val, Test."""
    train_df = pd.read_parquet("data/processed/train.parquet")
    val_df = pd.read_parquet("data/processed/val.parquet")
    test_df = pd.read_parquet("data/processed/test.parquet")
    
    print(f"[*] Kích thước dữ liệu: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
    return train_df, val_df, test_df


def train_and_evaluate():
    train_df, val_df, test_df = load_datasets()

    X_train_raw = train_df["sentence"].tolist()
    y_train = train_df["label"].tolist()

    X_val_raw = val_df["sentence"].tolist()
    y_val = val_df["label"].tolist()

    X_test_raw = test_df["sentence"].tolist()
    y_test = test_df["label"].tolist()

    # 1. Trích xuất đặc trưng TF-IDF (TUYỆT ĐỐI CHỈ FIT TRÊN TRAIN)
    print("\n[*] Đang fit TfidfVectorizer trên tập Train (ngram_range=(1,2), max_features=10000)...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=10000,
        sublinear_tf=True
    )
    X_train = vectorizer.fit_transform(X_train_raw)
    X_val = vectorizer.transform(X_val_raw)
    X_test = vectorizer.transform(X_test_raw)
    print(f"[+] Số lượng đặc trưng TF-IDF trích xuất: {X_train.shape[1]}")

    # Tạo thư mục lưu mô hình và báo cáo
    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir = Path("reports/metrics")
    metrics_dir.mkdir(parents=True, exist_ok=True)

    # Lưu lại vectorizer để dùng cho suy luận sau này
    joblib.dump(vectorizer, models_dir / "tfidf_vectorizer.joblib")

    # 2. Định nghĩa danh sách 3 mô hình
    models = {
        "Multinomial_Naive_Bayes": MultinomialNB(alpha=1.0),
        "Logistic_Regression": LogisticRegression(C=1.0, class_weight="balanced", max_iter=1000, random_state=42),
        "Linear_SVM": LinearSVC(C=0.5, class_weight="balanced", random_state=42)
    }

    results = {}
    target_names = ["Negative (0)", "Neutral (1)", "Positive (2)"]

    # 3. Huấn luyện và đánh giá từng mô hình
    for name, model in models.items():
        print(f"\n{'='*20} Đang huấn luyện: {name} {'='*20}")
        model.fit(X_train, y_train)

        # Lưu model đã huấn luyện
        model_file = models_dir / f"baseline_{name.lower()}.joblib"
        joblib.dump(model, model_file)
        print(f"[+] Đã lưu mô hình tại: {model_file}")

        # Đánh giá trên tập Validation
        val_preds = model.predict(X_val)
        val_macro_f1 = f1_score(y_val, val_preds, average="macro")

        # Đánh giá trên tập Test
        test_preds = model.predict(X_test)
        acc = accuracy_score(y_test, test_preds)
        macro_f1 = f1_score(y_test, test_preds, average="macro")
        weighted_f1 = f1_score(y_test, test_preds, average="weighted")
        report_dict = classification_report(y_test, test_preds, target_names=target_names, output_dict=True)

        print(f"--- KẾT QUẢ TEST CHO {name} ---")
        print(classification_report(y_test, test_preds, target_names=target_names, digits=4))
        print(f"Validation Macro F1 : {val_macro_f1:.4f}")
        print(f"Test Accuracy       : {acc:.4f} ({acc*100:.2f}%)")
        print(f"Test Macro F1       : {macro_f1:.4f} ({macro_f1*100:.2f}%)")
        print(f"Test Weighted F1    : {weighted_f1:.4f} ({weighted_f1*100:.2f}%)")

        results[name] = {
            "val_macro_f1": float(val_macro_f1),
            "test_accuracy": float(acc),
            "test_macro_f1": float(macro_f1),
            "test_weighted_f1": float(weighted_f1),
            "classification_report": report_dict
        }

    # 4. Xuất kết quả tổng hợp ra JSON
    output_json = metrics_dir / "tier2_classical_ml.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"\n[+] Toàn bộ kết quả Tier 2 đã được lưu vào: {output_json}\n")


if __name__ == "__main__":
    train_and_evaluate()