import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import numpy as np
from src.evaluation.error_analysis import compute_normalized_confusion_matrix, extract_misclassified_cases

def test_compute_normalized_confusion_matrix():
    """Kiểm tra ma trận nhầm lẫn chuẩn hóa theo hàng phải có tổng mỗi hàng bằng 1.0."""
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([0, 1, 1, 1, 2, 0])
    
    cm_norm = compute_normalized_confusion_matrix(y_true, y_pred, num_classes=3)
    row_sums = cm_norm.sum(axis=1)
    
    for s in row_sums:
        assert pytest.approx(s, 1e-5) == 1.0, f"Tổng hàng phải bằng 1.0, nhận được: {s}"

def test_extract_misclassified_cases():
    """Kiểm tra trích xuất đúng các ca đoán sai kèm metadata."""
    sentences = ["Bad news", "Stable market", "Great profit"]
    y_true = np.array([0, 1, 2])
    y_pred = np.array([1, 1, 0])
    
    errors = extract_misclassified_cases(sentences, y_true, y_pred)
    assert len(errors) == 2
    assert errors[0]["sentence"] == "Bad news"
    assert errors[0]["true_label"] == 0
    assert errors[0]["pred_label"] == 1
    assert errors[1]["sentence"] == "Great profit"
    assert errors[1]["true_label"] == 2
    assert errors[1]["pred_label"] == 0