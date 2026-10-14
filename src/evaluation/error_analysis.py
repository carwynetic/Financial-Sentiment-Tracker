import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

CLASS_NAMES = ["Negative", "Neutral", "Positive"]
LABEL_MAP = {0: "Negative", 1: "Neutral", 2: "Positive"}


def compute_normalized_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int = 3) -> np.ndarray:
    """Tính ma trận nhầm lẫn chuẩn hóa theo hàng (Row-normalized / Recall từng lớp)."""
    cm = confusion_matrix(y_true, y_pred, labels=list(range(num_classes)))
    with np.errstate(divide="ignore", invalid="ignore"):
        cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    return np.nan_to_num(cm_norm)


def plot_comparative_confusion_matrices(y_true: np.ndarray, predictions: dict[str, np.ndarray], output_dir: Path):
    """Vẽ lưới 2x2 ma trận nhầm lẫn chuẩn hóa chuẩn ấn phẩm IEEE."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    models_to_plot = [
        ("Loughran_McDonald", "Tier 1: Loughran-McDonald"),
        ("Logistic_Regression", "Tier 2: Logistic Regression"),
        ("Linear_SVM", "Tier 2: Linear SVM (Best Baseline)"),
        ("FinBERT_Fine_Tuned", "Tier 3: FinBERT Fine-Tuned (Proposed)")
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for idx, (m_key, title) in enumerate(models_to_plot):
        ax = axes[idx]
        y_pred = predictions[m_key]
        cm_raw = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
        cm_norm = compute_normalized_confusion_matrix(y_true, y_pred, num_classes=3)

        # Chú thích: Tỷ lệ Recall kèm số đếm thực tế
        annot_matrix = np.empty_like(cm_norm, dtype=object)
        for i in range(3):
            for j in range(3):
                annot_matrix[i, j] = f"{cm_norm[i, j]:.2f}\n({cm_raw[i, j]})"

        sns.heatmap(
            cm_norm,
            annot=annot_matrix,
            fmt="",
            cmap="Blues",
            cbar=False,
            ax=ax,
            vmin=0.0,
            vmax=1.0,
            xticklabels=CLASS_NAMES,
            yticklabels=CLASS_NAMES,
            annot_kws={"size": 11, "weight": "bold"}
        )

        ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
        ax.set_xlabel("Predicted Label", fontsize=10, fontweight="bold")
        ax.set_ylabel("True Label", fontsize=10, fontweight="bold")

    plt.suptitle("Normalized Confusion Matrices Across Model Tiers (Test Split N=518)", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout()

    # Xuất cả vector PDF và PNG 300 DPI
    pdf_path = output_dir / "confusion_matrices_all_models.pdf"
    png_path = output_dir / "confusion_matrices_all_models.png"
    plt.savefig(pdf_path, dpi=300, bbox_inches="tight")
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[✓] Đã xuất biểu đồ Confusion Matrix:\n - {pdf_path}\n - {png_path}")


def extract_misclassified_cases(sentences: list[str], y_true: np.ndarray, y_pred: np.ndarray) -> list[dict]:
    """Trích xuất danh sách các ca dự đoán sai."""
    errors = []
    for idx, (sent, t, p) in enumerate(zip(sentences, y_true, y_pred)):
        if t != p:
            errors.append({
                "sample_idx": idx,
                "sentence": sent,
                "true_label": int(t),
                "true_name": LABEL_MAP[int(t)],
                "pred_label": int(p),
                "pred_name": LABEL_MAP[int(p)],
                "error_type": f"{LABEL_MAP[int(t)]} -> {LABEL_MAP[int(p)]}"
            })
    return errors


def generate_error_taxonomy_report(errors: list[dict], output_file: Path):
    """Xuất báo cáo phân loại lỗi sang Markdown."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_err = pd.DataFrame(errors)
    type_counts = df_err["error_type"].value_counts()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Qualitative Failure Mode Analysis & Error Taxonomy (FinBERT Fine-Tuned)\n\n")
        f.write(f"- **Tổng số ca kiểm thử**: 518\n")
        f.write(f"- **Tổng số ca FinBERT đoán sai**: {len(errors)} ({len(errors)/518*100:.2f}%)\n")
        f.write(f"- **Độ chính xác toàn cục**: {(518-len(errors))/518*100:.2f}%\n\n")

        f.write("## 1. Thống kê phân bố các dạng lỗi nhầm lẫn\n\n")
        f.write("| Error Mode (True -> Pred) | Count | Percentage of Errors |\n")
        f.write("| :--- | :---: | :---: |\n")
        for mode, count in type_counts.items():
            f.write(f"| `{mode}` | {count} | {count/len(errors)*100:.1f}% |\n")

        f.write("\n## 2. Phân tích chi tiết các mẫu câu lỗi tiêu biểu\n\n")
        for mode in type_counts.index:
            subset = df_err[df_err["error_type"] == mode].head(3)
            f.write(f"### Dạng lỗi: `{mode}`\n\n")
            for _, row in subset.iterrows():
                f.write(f"- **Sentence**: *\"{row['sentence']}\"*\n")
                f.write(f"  - **Ground Truth**: `{row['true_name']}` | **FinBERT Prediction**: `{row['pred_name']}`\n")
            f.write("\n")

    print(f"[✓] Đã xuất báo cáo Error Taxonomy tại: {output_file}")


def run_error_analysis():
    cache_path = Path("reports/metrics/test_predictions.json")
    if not cache_path.exists():
        raise FileNotFoundError(f"Chưa tìm thấy {cache_path}. Hãy chạy src/evaluation/mcnemar_test.py trước!")

    with open(cache_path, "r", encoding="utf-8") as f:
        cache = json.load(f)

    y_true = np.array(cache["y_true"])
    predictions = {k: np.array(v) for k, v in cache["predictions"].items()}

    test_df = pd.read_parquet("data/processed/test.parquet")
    sentences = test_df["sentence"].tolist()

    figures_dir = Path("reports/figures")
    plot_comparative_confusion_matrices(y_true, predictions, figures_dir)

    errors = extract_misclassified_cases(sentences, y_true, predictions["FinBERT_Fine_Tuned"])
    taxonomy_file = Path("reports/tables/error_taxonomy.md")
    generate_error_taxonomy_report(errors, taxonomy_file)


if __name__ == "__main__":
    run_error_analysis()