import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import pytest
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    BertForSequenceClassification
)

from src.models.evaluate_zero_shot_finbert import (
    build_hf_to_project_mapping,
    PROJECT_LABEL_MAP
)


class DummyConfig:
    """Mock config giả lập các kiểu id2label khác nhau của Hugging Face."""
    def __init__(self, id2label):
        self.id2label = id2label


def test_zero_shot_metrics_file_exists():
    """Kiểm tra file kết quả JSON đã tồn tại và chứa đủ số liệu của 2 mô hình."""
    metrics_path = Path("reports/metrics/finbert_zero_shot.json")
    assert metrics_path.exists(), "File finbert_zero_shot.json chưa được tạo!"

    with open(metrics_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "ProsusAI/finbert" in data
    assert "yiyanghkust/finbert-tone" in data

    prosus_f1 = data["ProsusAI/finbert"]["macro_f1"]
    assert 0.0 <= prosus_f1 <= 1.0
    assert prosus_f1 > 0.90, f"ProsusAI FinBERT F1 quá thấp: {prosus_f1}"


def test_label_mapping_alignment():
    """Kiểm tra logic ánh xạ nhãn chống lỗi đảo lộn nhãn."""
    # Giả lập config kiểu ProsusAI: 0: positive, 1: negative, 2: neutral
    mock_config_prosus = DummyConfig({0: "positive", 1: "negative", 2: "neutral"})
    mapping_prosus = build_hf_to_project_mapping(mock_config_prosus)
    assert mapping_prosus == {0: 2, 1: 0, 2: 1}

    # Giả lập config kiểu HKUST: 0: Neutral, 1: Positive, 2: Negative
    mock_config_hkust = DummyConfig({0: "Neutral", 1: "Positive", 2: "Negative"})
    mapping_hkust = build_hf_to_project_mapping(mock_config_hkust)
    assert mapping_hkust == {0: 1, 1: 2, 2: 0}


def test_finbert_prediction_sanity():
    """Kiểm tra độ nhạy suy luận thực tế với 3 câu tài chính rõ ràng."""
    model_name = "ProsusAI/finbert"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    model.eval()

    hf_to_project = build_hf_to_project_mapping(model.config)

    test_samples = [
        ("Net sales decreased significantly and operating loss deepened.", 0),  # Negative
        ("The company will release its third-quarter financial results on Friday.", 1),  # Neutral
        ("Operating profit surged by 45% exceeding market expectations.", 2),  # Positive
    ]

    with torch.no_grad():
        for text, expected_label in test_samples:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=64).to(device)
            outputs = model(**inputs)
            pred_hf_id = torch.argmax(outputs.logits, dim=1).item()
            pred_project_label = hf_to_project[pred_hf_id]

            assert pred_project_label == expected_label, (
                f"Dự đoán sai câu: '{text}'. Dự đoán: {pred_project_label}, Kỳ vọng: {expected_label}"
            )


def test_entity_aware_disambiguation_sanity():
    """Kiểm tra mô hình Entity-Aware phân định được 2 thực thể đối lập trong cùng 1 câu thực tế."""
    model_dir = Path("models/finbert_entity_best")
    if not model_dir.exists():
        pytest.skip("Chưa tìm thấy models/finbert_entity_best")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = BertForSequenceClassification.from_pretrained(model_dir).to(device)
    model.eval()

    # Câu thực tế trong SEntFiN chứa 2 thực thể đối lập: Gold tăng (Positive), rupee suy yếu (Negative)
    headline = "Gold extends gains on festive buying, weak rupee"

    # 1. Dự đoán cho Gold -> Phải là Positive (2)
    inputs_gold = tokenizer("Gold", text_pair=headline, return_tensors="pt", truncation=True, max_length=128).to(device)
    with torch.no_grad():
        out_gold = model(**inputs_gold)
        pred_gold = torch.argmax(out_gold.logits, dim=1).item()

    # 2. Dự đoán cho rupee -> Phải là Negative (0)
    inputs_rupee = tokenizer("rupee", text_pair=headline, return_tensors="pt", truncation=True, max_length=128).to(device)
    with torch.no_grad():
        out_rupee = model(**inputs_rupee)
        pred_rupee = torch.argmax(out_rupee.logits, dim=1).item()

    assert pred_gold == 2, f"Kỳ vọng Gold là Positive (2) nhưng dự đoán: {pred_gold}"
    assert pred_rupee == 0, f"Kỳ vọng rupee là Negative (0) nhưng dự đoán: {pred_rupee}"