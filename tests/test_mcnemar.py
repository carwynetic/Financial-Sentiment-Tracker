import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import numpy as np
from src.evaluation.mcnemar_test import compute_mcnemar_statistic, build_contingency_table

def test_mcnemar_statistic_symmetry():
    """Khi hai mô hình sai khác nhau đối xứng (b == c), p-value phải xấp xỉ 1.0 (không có ý nghĩa)."""
    # b = 15, c = 15
    table = np.array([[300, 15], 
                      [15, 50]])
    chi2, p_val = compute_mcnemar_statistic(table)
    assert p_val > 0.05, f"p-value phải lớn hơn 0.05 khi đối xứng, nhận được: {p_val}"

def test_mcnemar_statistic_significant_difference():
    """Khi Model A vượt trội rõ rệt (b >> c), p-value phải rất nhỏ (< 0.001)."""
    # Model A đúng 40 ca mà Model B sai; Model B chỉ đúng 5 ca mà Model A sai
    table = np.array([[400, 40], 
                      [5, 30]])
    chi2, p_val = compute_mcnemar_statistic(table)
    assert chi2 > 10.0, f"Chi2 phải lớn khi chênh lệch lớn: {chi2}"
    assert p_val < 0.001, f"p-value phải < 0.001, nhận được: {p_val}"

def test_build_contingency_table():
    """Kiểm tra việc lập bảng 2x2 từ vector nhãn đúng/sai."""
    y_true = np.array([0, 1, 2, 1, 0])
    pred_a = np.array([0, 1, 2, 0, 0]) # Đúng: 0, 1, 2, 4 (4 ca đúng)
    pred_b = np.array([0, 2, 2, 1, 1]) # Đúng: 0, 2, 3 (3 ca đúng)

    # Ca 0: A đúng, B đúng -> n00
    # Ca 1: A đúng, B sai   -> n01 (b)
    # Ca 2: A đúng, B đúng -> n00
    # Ca 3: A sai,   B đúng -> n10 (c)
    # Ca 4: A đúng, B sai   -> n01 (b)
    # Kỳ vọng: n00=2, n01=2, n10=1, n11=0
    table = build_contingency_table(y_true, pred_a, pred_b)
    assert table[0, 0] == 2
    assert table[0, 1] == 2
    assert table[1, 0] == 1
    assert table[1, 1] == 0