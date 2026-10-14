import os
import pandas as pd
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.generate_benchmark_table import load_metrics, build_benchmark_dataframe

def test_load_metrics_files_exist():
    """Kiểm tra các file json metrics đầu vào có đầy đủ không."""
    metrics_dir = "reports/metrics"
    required_files = [
        "tier1_lexicon.json",
        "tier2_classical_ml.json",
        "finbert_zero_shot.json",
        "finbert_fine_tuned.json",
        "finbert_entity_aware.json"
    ]
    for fname in required_files:
        assert os.path.exists(os.path.join(metrics_dir, fname)), f"Thiếu file: {fname}"

def test_build_benchmark_dataframe():
    """Kiểm tra DataFrame được tạo ra có đúng định dạng và chỉ số hợp lệ."""
    df = build_benchmark_dataframe("reports/metrics")
    
    # Kiểm tra các cột bắt buộc
    expected_cols = ["Paradigm", "Model", "Accuracy", "Macro Precision", "Macro Recall", "Macro F1", "Weighted F1"]
    for col in expected_cols:
        assert col in df.columns, f"Thiếu cột: {col}"
        
    # Kiểm tra số lượng mô hình tối thiểu (1 Lexicon + 3 Classical ML + 2 Zero-shot + 1 Fine-tuned + 1 Entity-aware = 8 hàng)
    assert len(df) >= 7, f"Số lượng mô hình chưa đủ, hiện có: {len(df)}"
    
    # Kiểm tra giá trị các chỉ số phải nằm trong [0.0, 1.0]
    metric_cols = ["Accuracy", "Macro Precision", "Macro Recall", "Macro F1", "Weighted F1"]
    for col in metric_cols:
        assert (df[col] >= 0.0).all() and (df[col] <= 1.0).all(), f"Giá trị cột {col} nằm ngoài [0, 1]"