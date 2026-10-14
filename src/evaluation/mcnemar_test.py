import json
import os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from scipy.stats import chi2
import torch
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from src.models.lexicon_baseline import LoughranMcDonaldClassifier


def build_contingency_table(y_true: np.ndarray, pred_a: np.ndarray, pred_b: np.ndarray) -> np.ndarray:
    """Lập bảng tiếp liên 2x2:
        [ [Cả 2 đúng,   A đúng & B sai],
          [A sai & B đúng, Cả 2 cùng sai] ]
    """
    correct_a = (pred_a == y_true)
    correct_b = (pred_b == y_true)

    n00 = np.sum(correct_a & correct_b)
    n01 = np.sum(correct_a & (~correct_b)) # b: A đúng, B sai
    n10 = np.sum((~correct_a) & correct_b) # c: A sai, B đúng
    n11 = np.sum((~correct_a) & (~correct_b))

    return np.array([[n00, n01], 
                     [n10, n11]], dtype=int)


def compute_mcnemar_statistic(table: np.ndarray) -> tuple[float, float]:
    """Tính thống kê Chi2 với hiệu chỉnh liên tục Edwards và p-value."""
    b = float(table[0, 1])
    c = float(table[1, 0])

    if (b + c) == 0:
        return 0.0, 1.0

    # Công thức Edwards' continuity correction
    statistic = ((abs(b - c) - 1.0) ** 2) / (b + c)
    p_value = float(chi2.sf(statistic, df=1))
    return float(statistic), p_value


def get_all_predictions() -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Tải dữ liệu Test và lấy vector dự đoán của 4 mô hình."""
    test_path = Path("data/processed/test.parquet")
    df_test = pd.read_parquet(test_path)
    sentences = df_test["sentence"].tolist()
    y_true = np.array(df_test["label"].tolist())

    predictions = {}

    # 1. Lexicon Baseline
    print("[*] Đang sinh dự đoán cho Loughran-McDonald Lexicon...")
    lexicon_clf = LoughranMcDonaldClassifier(threshold=0.05)
    predictions["Loughran_McDonald"] = np.array(lexicon_clf.predict(sentences))

    # 2. Classical ML (TF-IDF + Linear SVM, Logistic Regression)
    models_dir = Path("models")
    vectorizer = joblib.load(models_dir / "tfidf_vectorizer.joblib")
    X_test_tfidf = vectorizer.transform(sentences)

    print("[*] Đang sinh dự đoán cho Logistic Regression & Linear SVM...")
    logreg = joblib.load(models_dir / "baseline_logistic_regression.joblib")
    svm = joblib.load(models_dir / "baseline_linear_svm.joblib")
    predictions["Logistic_Regression"] = np.array(logreg.predict(X_test_tfidf))
    predictions["Linear_SVM"] = np.array(svm.predict(X_test_tfidf))

    # 3. FinBERT Fine-Tuned (Local checkpoint)
    finbert_path = models_dir / "finbert_best"
    print(f"[*] Đang tải checkpoint FinBERT từ {finbert_path}...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(finbert_path)
    model = AutoModelForSequenceClassification.from_pretrained(finbert_path)
    model.to(device)
    model.eval()

    finbert_preds = []
    batch_size = 32
    print(f"[*] Đang thực hiện inference FinBERT trên {device}...")
    with torch.no_grad():
        for i in range(0, len(sentences), batch_size):
            batch_texts = sentences[i : i + batch_size]
            encoded = tokenizer(batch_texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
            encoded = {k: v.to(device) for k, v in encoded.items()}
            logits = model(**encoded).logits
            preds = torch.argmax(logits, dim=-1).cpu().numpy()
            finbert_preds.extend(preds)

    predictions["FinBERT_Fine_Tuned"] = np.array(finbert_preds)

    # Lưu lại toàn bộ predictions để phục vụ Task 4.3 Error Analysis
    cache_path = Path("reports/metrics/test_predictions.json")
    cache_data = {
        "y_true": y_true.tolist(),
        "predictions": {k: v.tolist() for k, v in predictions.items()}
    }
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, indent=4)
    print(f"[✓] Đã lưu cache dự đoán tại: {cache_path}")

    return y_true, predictions


def run_mcnemar_benchmarks():
    y_true, predictions = get_all_predictions()

    target_model = "FinBERT_Fine_Tuned"
    baselines = [
        ("Linear_SVM", "Linear SVM (Tier 2 Strongest)"),
        ("Logistic_Regression", "Logistic Regression (Tier 2)"),
        ("Loughran_McDonald", "Loughran-McDonald (Tier 1 Lexicon)")
    ]

    results = {}
    print("\n" + "=" * 80)
    print("KẾT QUẢ KIỂM ĐỊNH Ý NGHĨA THỐNG KÊ (McNEMAR'S TEST WITH EDWARDS' CORRECTION)")
    print("=" * 80)

    for base_key, base_name in baselines:
        table = build_contingency_table(y_true, predictions[target_model], predictions[base_key])
        chi2_stat, p_val = compute_mcnemar_statistic(table)
        is_sig = bool(p_val < 0.05)

        b = int(table[0, 1])
        c = int(table[1, 0])

        results[f"{target_model}_vs_{base_key}"] = {
            "model_a": target_model,
            "model_b": base_key,
            "contingency_table": table.tolist(),
            "discordant_pairs": {"a_correct_b_wrong (b)": b, "a_wrong_b_correct (c)": c},
            "chi2_statistic": chi2_stat,
            "p_value": p_val,
            "significant_at_0.05": is_sig
        }

        print(f"\n▶ So sánh: [{target_model}] VS [{base_name}]")
        print(f"   - Bảng 2x2: [[Both Correct: {table[0,0]}, FinBERT win: {b}], [Baseline win: {c}, Both Wrong: {table[1,1]}]]")
        print(f"   - Chi-Square (χ²): {chi2_stat:.4f} (df=1)")
        print(f"   - p-value: {p_val:.4e}")
        print(f"   - Kết luận: {'★ Có ý nghĩa thống kê (p < 0.05)' if is_sig else 'Không có ý nghĩa thống kê (p >= 0.05)'}")

    # Xuất ra JSON
    out_file = Path("reports/metrics/mcnemar_tests.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"\n[✓] Đã xuất kết quả kiểm định tại: {out_file}")


if __name__ == "__main__":
    run_mcnemar_benchmarks()