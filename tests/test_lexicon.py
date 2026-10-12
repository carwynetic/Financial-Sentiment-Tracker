import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from src.models.lexicon_baseline import LoughranMcDonaldClassifier

@pytest.fixture
def classifier():
    return LoughranMcDonaldClassifier(threshold=0.05)


def test_positive_sentence(classifier):
    text = "The company reported record profit and outstanding earnings growth."
    pred = classifier.predict_single(text)
    assert pred == 2, f"Kỳ vọng nhãn 2 (Positive), nhưng nhận được {pred}"


def test_negative_sentence(classifier):
    text = "The business suffered severe loss, debt default and bankruptcy."
    pred = classifier.predict_single(text)
    assert pred == 0, f"Kỳ vọng nhãn 0 (Negative), nhưng nhận được {pred}"


def test_neutral_sentence(classifier):
    text = "The meeting was held at the headquarters on Monday."
    pred = classifier.predict_single(text)
    assert pred == 1, f"Kỳ vọng nhãn 1 (Neutral), nhưng nhận được {pred}"


def test_edge_cases(classifier):
    assert classifier.predict_single("") == 1
    assert classifier.predict_single(None) == 1
    assert classifier.predict_single("12345 67890") == 1


def test_batch_prediction(classifier):
    texts = [
        "Record profit and growth.",
        "Loss and bankruptcy.",
        "The committee meets today."
    ]
    preds = classifier.predict(texts)
    assert len(preds) == 3
    assert preds == [2, 0, 1]