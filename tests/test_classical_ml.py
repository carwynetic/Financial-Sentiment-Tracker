"""
Module: test_classical_ml.py
Mục đích: Kiểm thử tự động (Unit Test) cho các mô hình Machine Learning cổ điển (Tier 2).
Đảm bảo các artifact .joblib đã lưu tải lên chuẩn xác và dự đoán ổn định.
"""

import sys
from pathlib import Path

# Thêm thư mục gốc vào sys.path để Python tìm thấy các package trong dự án
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import joblib

# Đường dẫn đến thư mục chứa các mô hình đã đóng gói
MODELS_DIR = Path("models")


@pytest.fixture(scope="module")
def artifacts():
    """
    Fixture này chạy 1 lần duy nhất: Nạp vectorizer và 3 mô hình từ đĩa vào bộ nhớ.
    Nếu thiếu bất kỳ file nào, bài kiểm tra sẽ báo lỗi ngay lập tức.
    """
    vectorizer_path = MODELS_DIR / "tfidf_vectorizer.joblib"
    nb_path = MODELS_DIR / "baseline_multinomial_naive_bayes.joblib"
    logreg_path = MODELS_DIR / "baseline_logistic_regression.joblib"
    svm_path = MODELS_DIR / "baseline_linear_svm.joblib"

    # Kiểm tra file vật lý có tồn tại trên ổ đĩa hay không
    assert vectorizer_path.exists(), "Thiếu file tfidf_vectorizer.joblib!"
    assert nb_path.exists(), "Thiếu file baseline_multinomial_naive_bayes.joblib!"
    assert logreg_path.exists(), "Thiếu file baseline_logistic_regression.joblib!"
    assert svm_path.exists(), "Thiếu file baseline_linear_svm.joblib!"

    # Nạp các artifact vào dictionary để tái sử dụng trong các hàm test
    return {
        "vectorizer": joblib.load(vectorizer_path),
        "nb": joblib.load(nb_path),
        "logreg": joblib.load(logreg_path),
        "svm": joblib.load(svm_path)
    }


def test_vectorizer_transformation(artifacts):
    """
    Kiểm tra xem TfidfVectorizer có biến đổi văn bản thành ma trận đúng 10,000 đặc trưng không.
    """
    sample_text = ["Operating profit increased by 10% to EUR 50 million."]
    # Biến đổi văn bản sang vector đặc trưng TF-IDF
    X_vec = artifacts["vectorizer"].transform(sample_text)
    
    # Kiểm tra số cột (features) phải đúng 10,000 như lúc huấn luyện
    assert X_vec.shape[1] == 10000, f"Kỳ vọng 10000 features, nhưng nhận {X_vec.shape[1]}"


def test_models_prediction_valid_labels(artifacts):
    """
    Kiểm tra cả 3 mô hình có trả về nhãn hợp lệ trong tập {0: Negative, 1: Neutral, 2: Positive} không.
    """
    sample_texts = [
        "Net sales increased significantly.",   # Câu tích cực
        "The company went bankrupt.",           # Câu tiêu cực
        "The annual general meeting was held."  # Câu trung lập
    ]
    # Trích xuất đặc trưng cho 3 câu mẫu
    X_sample = artifacts["vectorizer"].transform(sample_texts)

    valid_labels = {0, 1, 2}

    # Lặp qua từng mô hình để kiểm tra nhãn dự đoán
    for model_name in ["nb", "logreg", "svm"]:
        model = artifacts[model_name]
        preds = model.predict(X_sample)

        # Kiểm tra độ dài mảng dự đoán phải khớp với số câu đầu vào (3 câu)
        assert len(preds) == 3, f"Mô hình {model_name} trả về sai số lượng dự đoán"

        # Kiểm tra từng nhãn trả về phải nằm trong {0, 1, 2}
        for p in preds:
            assert int(p) in valid_labels, f"Mô hình {model_name} trả về nhãn không hợp lệ: {p}"


def test_linear_svm_sensible_predictions(artifacts):
    """
    Kiểm tra riêng mô hình quán quân Linear SVM trên các trường hợp rõ ràng.
    """
    vectorizer = artifacts["vectorizer"]
    svm = artifacts["svm"]

    pos_text = ["Profit surged to record high with strong revenue growth."]
    neg_text = ["The operating profit fell dramatically due to severe losses."]

    # Dự đoán nhãn
    pos_pred = svm.predict(vectorizer.transform(pos_text))[0]
    neg_pred = svm.predict(vectorizer.transform(neg_text))[0]

    # Câu tích cực phải ra nhãn 2, câu tiêu cực phải ra nhãn 0
    assert pos_pred == 2, f"Linear SVM dự đoán sai câu tích cực, nhận được: {pos_pred}"
    assert neg_pred == 0, f"Linear SVM dự đoán sai câu tiêu cực, nhận được: {neg_pred}"