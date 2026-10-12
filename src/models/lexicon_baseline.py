"""
1. Khởi tạo bộ phân loại: Tạo class LoughranMcDonaldClassifier bọc pysentiment2.LM() và hàm predict(text).
2. Nạp dữ liệu: Đọc tập data/processed/test.parquet (gồm 518 mẫu kiểm thử cố định).
3. Dự đoán hàng loạt: Dùng .apply() hoặc vòng lặp để gán nhãn dự đoán (y_pred).
4. Đánh giá & Xuất file:
    Dùng classification_report và accuracy_score của sklearn.metrics để tính Accuracy, Macro F1, Weighted F1.
    In bảng kết quả ra màn hình.
    Lưu kết quả dạng JSON vào reports/metrics/tier1_lexicon.json.
"""

import json 
from pathlib import Path
import pandas as pd  
import pysentiment2 as ps 
from sklearn.metrics import classification_report, accuracy_score, f1_score

class LoughranMcDonaldClassifier:
    """ bộ phân loại cảm xúc tài chính dựa trên từ điển Loughran-McDonal (tier 1 basseline)"""
    def __init__(self, threshold : float = 0.05):
        self.lm = ps.LM()
        self.threshold= threshold
    def predict_single(self, text:str)->int:
        if not text or not isinstance(text, str): return 1 #chuỗi rỗng -> neutral
        tokens = self.lm.tokenize(text)
        score = self.lm.get_score(tokens)
        
        pos = score["Positive"]
        neg = score["Negative"]
        polarity = score["Polarity"]

        #nếu không chứa từ nào trong từ điển -> neutral
        if pos ==0 and neg ==0:
            return 1
        if polarity > self.threshold: return 2 #postivie
        elif polarity < - self.threshold: return 0 #negative
        else: return 1 #neutral
    
    def predict(self, texts:list[str])->list[int]:
        return [self.predict_single(t) for t in texts]


def run_evaluation():
    #1. path 
    test_path = Path("data/processed/test.parquet")
    output_dir = Path("reports/metrics")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "tier1_lexicon.json"

    print(f"dang tai du lieu de kiem thu : {test_path}")
    df_test  = pd.read_parquet(test_path)
    
    y_true = df_test["label"].tolist()
    sentences = df_test["sentence"].tolist()

    #2. predict
    clf = LoughranMcDonaldClassifier(threshold=0.05)
    y_pred = clf.predict(sentences)
    
    #3. metrics
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro")
    weighted_f1 = f1_score(y_true, y_pred, average="weighted")
    
    target_names = ["Negative (0)","Neutral (1)" , "Positive (2)"]
    report_dict = classification_report(y_true, y_pred, target_names=target_names, output_dict=True)
    report_text = classification_report(y_true, y_pred, target_names=target_names, digits=4)

    print(report_text)
    print(f"Accuracy   : {acc:.4f} ({acc*100:.2f}%)")
    print(f"Macro F1   : {macro_f1:.4f} ({macro_f1*100:.2f}%)")
    print(f"Weighted F1: {weighted_f1:.4f} ({weighted_f1*100:.2f}%)")

    # 4. Xuất kết quả JSON
    metrics_summary = {
        "model_name": "Loughran-McDonald Lexicon Baseline",
        "threshold": 0.05,
        "total_samples": len(y_true),
        "accuracy": acc,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "classification_report": report_dict
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=4)
        
    print(f"[+] Báo cáo đã được lưu vào: {output_file}\n")



if __name__ == "__main__":
    run_evaluation()