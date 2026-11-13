import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

INPUT_PATH = Path(r"c:\Users\CARWYN\Downloads\presentation_backup.pptx")
OUTPUT_PATH_DOWNLOADS = Path(r"c:\Users\CARWYN\Downloads\presentation.pptx")
OUTPUT_PATH_DRIVE = Path(r"G:\My Drive\Study\FPT University AI\Kì 5\Text Mining (TMG301)\Project\presentation_hoan_chinh.pptx")

prs = pptx.Presentation(str(INPUT_PATH))

SLIDES_DATA = {
    # Slide 1: Title
    1: {
        "type": "title",
        "title": "HỆ THỐNG PHÂN TÍCH CẢM XÚC TIN TỨC TÀI CHÍNH THEO THỰC THỂ",
        "subtitle": "Financial Sentiment Tracker & Cyber FinTech Terminal (FinBERT Powered)",
        "presenter": "Nhóm 4 (AI Batch 19): Nguyễn Đoàn Bảo Phúc (Lead), Nguyễn Phú Triệu, Ngô Công Minh, Nguyễn Công Minh",
        "supervisor": "Giảng viên hướng dẫn: ThS. Vũ Hà Anh — Học phần: Text Mining (TMG301)",
        "link": "https://github.com/carwynetic/Financial-Sentiment-Tracker"
    },
    # Slide 2: Outline
    2: {
        "type": "outline",
        "title": "Nội Dung Báo Cáo (10 Phút Chuẩn Hội Đồng)",
        "bullets": [
            "I. Introduction (1m - 1m30s): Bối cảnh tài chính, 3 Cạm bẫy NLP & Thành tựu nổi bật",
            "II. Related Work (2m - 2m30s): 4 Nghiên cứu nền tảng & Trả lời câu hỏi 'Liên quan gì?'",
            "III. Contribution & Pipeline (3m): Problem Formulation, Kiến trúc & Rationale giải quyết vấn đề",
            "IV. Experiments & Results (2m): Datasets, Cấu hình, Master Benchmark Matrix & McNemar (p < 0.01)",
            "V. Discussion & Ablation (1m): Tháo gỡ Component & Bảng phân loại 6 dạng lỗi ngôn ngữ",
            "VI. Conclusion & Future Work (1m): Đóng gói 3 phân hệ phần mềm & Mở rộng VN-Index (PhoBERT)"
        ]
    },
    # Slide 3: Section I Divider
    3: {
        "type": "divider",
        "section": "I. Introduction"
    },
    # Slide 4: Context
    4: {
        "type": "content",
        "title": "Bối Cảnh Nghiên Cứu (Financial Context)",
        "bullets": [
            "Vận hành thị trường tài chính: Quyết định giao dịch diễn ra ở quy mô mili-giây; tin tức báo chí và báo cáo tài chính SEC chi phối trực tiếp định giá cổ phiếu và dòng tiền quỹ đầu tư.",
            "Bùng nổ thông tin (Information Overload): Hàng chục nghìn bài báo tài chính được xuất bản mỗi ngày, vượt quá hoàn toàn khả năng đọc hiểu và tổng hợp thủ công của con người.",
            "Nhu cầu cấp thiết: Xây dựng hệ thống tự động hóa phân tích cảm xúc tin tức với độ chính xác cao và độ trễ thấp để hỗ trợ các mô hình định lượng và quản trị rủi ro danh mục."
        ]
    },
    # Slide 5: Challenge
    5: {
        "type": "content",
        "title": "Thách Thức: 3 Điểm Nghẽn Khiến NLP Thông Thường Thất Bại",
        "bullets": [
            "1. Xung đột từ vựng kế toán (Vocabulary Collision): Loughran & McDonald (2011) chứng minh từ điển thông thường gán sai 73.8% từ tiêu cực (các từ như 'liability', 'cost', 'tax', 'capital' là từ ngữ vận hành bình thường nhưng bị gán nhãn Xấu).",
            "2. Phủ định kép & Ngữ cảnh phức hợp (Turnaround Nuance): Câu 'pretax loss narrowed' (khoản lỗ thu hẹp = tin tốt) bị các mô hình đếm từ gán nhãn Tiêu cực do thấy chữ 'loss'.",
            "3. Xung đột đa thực thể trái chiều (Multi-Entity Conflict): Tiêu đề chứa 2 mã cổ phiếu đối lập ('Gold extends gains, weak rupee') khiến phân loại cấp câu bị triệt tiêu tín hiệu."
        ]
    },
    # Slide 6: Solutions
    6: {
        "type": "content",
        "title": "Giải Pháp Đề Xuất & Thành Tựu Nổi Bật",
        "bullets": [
            "Hệ thống Financial Sentiment Tracker: Tích hợp FinBERT thích ứng miền tài chính, bổ sung Inverse Class Weighting và Sentence-Pair Cross-Attention.",
            "Quán quân Benchmark: Macro-F1 đạt 89.76% trên Financial PhraseBank, vượt trội Linear SVM (+8.47%) và Loughran-McDonald Lexicon (+46.24%).",
            "Phân định đa thực thể: Giải quyết triệt để xung đột đa ticker với F1 đạt 84.11% trên tập kiểm thử SEntFiN 1.0.",
            "Đóng gói hoàn chỉnh: Hệ sinh thái 3 phân hệ phần mềm gồm FastAPI Microservice (<20ms latency), React Cyber Terminal 2.0 và Chrome Extension Manifest V3."
        ]
    },
    # Slide 7: Section II Divider
    7: {
        "type": "divider",
        "section": "II. Related Work"
    },
    # Slide 8: Related work
    8: {
        "type": "content",
        "title": "Nghiên Cứu Nền Tảng & Khoảng Trống Học Thuật (Related Work)",
        "bullets": [
            "1. Loughran & McDonald (2011) [JOF]: Cung cấp từ điển 347 từ Positive và 2,345 từ Negative -> Dùng dựng Tier 1 Baseline. Hạn chế: Bag-of-Words, mù ngữ pháp và cấu trúc câu.",
            "2. Araci (2019) & Huang et al. (2023) [CAR]: Tiền huấn luyện BERT trên ngữ liệu tài chính khổng lồ (báo cáo 10-K, earnings calls) -> Nền tảng cho Tier 3. Hạn chế: Chỉ xử lý ở cấp câu đơn thuần.",
            "3. Sinha et al. (2022) [SEntFiN 1.0]: Đặt nền móng cảm xúc hướng thực thể -> Nhóm kế thừa để xây dựng Sentence-Pair Cross-Attention với Headline-Level Split không rò rỉ dữ liệu.",
            "4. Malo et al. (2014) [PhraseBank]: Cung cấp bộ benchmark chuẩn mực (75% agreement, 3,453 câu) để đối chuẩn 8 mô hình."
        ]
    },
    # Slide 9: Section III Divider
    9: {
        "type": "divider",
        "section": "III. Contribution & Methodology"
    },
    # Slide 10: Problem formulation
    10: {
        "type": "content",
        "title": "Định Nghĩa Bài Toán Toán Học (Problem Formulation)",
        "bullets": [
            "1. Phân loại cảm xúc cấp câu (Sentence-level Sentiment): Tìm hàm ánh xạ cực đại hóa xác suất nhãn đúng:\n   ŷ = argmax_{c ∈ {0, 1, 2}} ℙ(Y = c | s; θ) với không gian nhãn Y = {0: Negative, 1: Neutral, 2: Positive}.",
            "2. Phân loại cảm xúc hướng thực thể (Entity-level Sentiment): Ánh xạ có điều kiện thực thể mục tiêu e_target:\n   ŷ_e = argmax_{c} ℙ(Y = c | e_target, s; θ).",
            "Mã hóa đầu vào: Đầu vào là cặp chuỗi [CLS] ⊕ e_target ⊕ [SEP] ⊕ s_headline ⊕ [SEP] được xử lý đồng thời qua ma trận Cross-Attention."
        ]
    },
    # Slide 11: Overall architecture
    11: {
        "type": "content",
        "title": "Kiến Trúc Hệ Thống Tổng Thể (Overall Pipeline)",
        "bullets": [
            "Tầng 1 (Ingestion & Preprocessing): Thu nạp tin tức live, bảo tồn ký hiệu tiền tệ, tỷ lệ % và cấu trúc phủ định qua cleaner.py chuyên dụng.",
            "Tầng 2 (Model Hierarchy): Bậc thang 3 tầng công nghệ: Tier 1 Lexicon -> Tier 2 Classical ML (Naive Bayes, Logistic Regression, Linear SVM) -> Tier 3 Transformer.",
            "Tầng 3 (Optimization): Inverse Class Weighting trong hàm mất mát + Sentence-Pair Cross-Attention phân giải thực thể.",
            "Tầng 4 (Deployment): Đóng gói hoàn chỉnh: REST API (FastAPI), Dashboard giao dịch (React), Chrome Extension V3 bôi đen tin tức tức thì."
        ]
    },
    # Slide 12: Contribution 1
    12: {
        "type": "content",
        "title": "Đóng Góp 1: Financial Text Cleaner (cleaner.py)",
        "bullets": [
            "Rationale (Lý do cốt lõi): Text cleaner thông thường xóa bỏ toàn bộ số và ký hiệu, phá hủy các chỉ số tăng trưởng sống còn của giới tài chính.",
            "Bảo tồn 100% định lượng: Giữ nguyên vẹn ký hiệu tiền tệ ($ € VND), tỷ lệ %, số liệu tăng trưởng và từ chỉ rủi ro/lỗ.",
            "Bảo tồn cấu trúc phủ định: Không lược bỏ các cấu trúc đảo ngược ngữ nghĩa như 'narrowed loss', 'fell short', 'dropped'.",
            "Tối ưu hóa Sequence: Cố định max_seq_length = 64 tokens, giảm 75% tiêu thụ VRAM trên GPU RTX 3050 Laptop trong quá trình huấn luyện."
        ]
    },
    # Slide 13: Contribution 2
    13: {
        "type": "content",
        "title": "Đóng Góp 2: Hàm Mất Mát Bù Trừ Mất Cân Bằng Lớp (Inverse Class Weighting)",
        "bullets": [
            "Rationale: Tập Train bị lệch nặng: Neutral chiếm 62.14%, Negative chỉ 12.16% (tỷ lệ lệch 5.1 : 1).",
            "Trọng số phạt nghịch đảo (Inverse Class Weights): w_c = N / (C × N_c)\n   => w_neg = 2.7404 (phạt nặng nhất), w_neu = 0.5364, w_pos = 1.2974.",
            "Hàm mất mát Weighted Cross-Entropy Loss: L_WCE = - ∑_{c=1}^C w_c · y_c log(ŷ_c).",
            "Hiệu quả thực tế: Phạt nặng gấp 5.1 lần khi mô hình đoán sai câu Negative, giúp nâng Negative Recall từ 74.2% lên 88.5%, bảo vệ nhà đầu tư khỏi rủi ro bỏ lọt tin xấu."
        ]
    },
    # Slide 14: Contribution 3
    14: {
        "type": "content",
        "title": "Đóng Góp 3: Sentence-Pair Cross-Attention Phân Định Đa Thực Thể",
        "bullets": [
            "Rationale: Mô hình cấp câu không thể phân định câu chứa 2 cổ phiếu có vận mệnh trái ngược nhau trong cùng một dòng tin.",
            "Cấu trúc mã hóa cặp câu: [CLS] ⊕ e_target ⊕ [SEP] ⊕ s_headline ⊕ [SEP] với Token Type IDs (0...0, 1...1).",
            "Cơ chế Cross-Attention: Ma trận Q, K, V hướng sự chú ý liên kết thực thể mục tiêu trực tiếp với cụm từ cảm xúc bổ nghĩa cho nó.",
            "Kết quả thực nghiệm: Đạt F1 84.11% trên 2,169 mẫu SEntFiN test set, phân định chính xác Gold (+) vs Rupee (-) trong cùng 1 câu."
        ]
    },
    # Slide 15: Training strategy
    15: {
        "type": "content",
        "title": "Chiến Lược Huấn Luyện & Kiểm Thử (Zero Data Leakage)",
        "bullets": [
            "Chống rò rỉ dữ liệu (Zero Data Leakage): Phân tách Stratified Split 70/15/15 ở cấp Headline ID, tuyệt đối không tách ngẫu nhiên ở cấp cặp câu.",
            "Chuẩn mực Feature Extraction: TF-IDF chỉ .fit_transform() trên Train, chỉ .transform() trên Val/Test.",
            "Tối ưu phần cứng GPU: Automatic Mixed Precision (AMP fp16), AdamW (lr = 2e-5), batch size 16, linear warmup 10%.",
            "Checkpoint Selection: Lưu weights tối ưu dựa trên đỉnh Validation Macro-F1 để chống hiện tượng over-fitting."
        ]
    },
    # Slide 16: Section IV Divider
    16: {
        "type": "divider",
        "section": "IV. Experiments & Results"
    },
    # Slide 17: Dataset
    17: {
        "type": "content",
        "title": "Tập Dữ Liệu Thực Nghiệm & Môi Trường Phần Cứng",
        "bullets": [
            "1. Financial PhraseBank: 3,453 câu (75% agreement subset) -> Train: 2,417 (70%), Val: 518 (15%), Test: 518 (15%).",
            "2. SEntFiN 1.0: 14,405 cặp entity-headline -> Train: 10,083 (70%), Val: 2,161 (15%), Test: 2,161 (15%).",
            "3. Môi trường phần cứng thực nghiệm: NVIDIA GeForce RTX 3050 Laptop GPU (6GB VRAM, Tensor Cores), Python 3.14, PyTorch 2.13 CUDA.",
            "Nguyên tắc minh bạch học thuật: 100% seed cố định (seed=42), đảm bảo khả năng tái lập độc lập 100% kết quả."
        ]
    },
    # Slide 18: Configuration
    18: {
        "type": "content",
        "title": "Cấu Hình Thực Nghiệm & Bậc Thang 8 Mô Hình Đối Chuẩn",
        "bullets": [
            "Tier 1 (Lexicon): Loughran-McDonald Financial Dictionary (2011/2025).",
            "Tier 2 (Classical ML): Multinomial Naive Bayes, Logistic Regression (class_weight='balanced'), Linear SVM (C=1.0).",
            "Tier 3 (Transformer Zero-Shot): ProsusAI FinBERT, HKUST FinBERT-Tone.",
            "Tier 3 (Transformer Fine-Tuned): FinBERT Fine-Tuned (Proposed) & Entity-Aware FinBERT (Proposed)."
        ]
    },
    # Slide 19: Result & Statistical Significance
    19: {
        "type": "content",
        "title": "Bảng Đối Chuẩn Tổng Thể (Master Benchmark Matrix) & McNemar",
        "bullets": [
            "Tier 1 (Lexicon): Loughran-McDonald đạt Acc 56.18%, Macro-F1 43.52% (Mù ngữ pháp và cấu trúc câu).",
            "Tier 2 (Classical ML): Linear SVM là quán quân Tier 2 với Acc 86.49%, Macro-F1 81.29%.",
            "Tier 3 (FinBERT Fine-Tuned): Quán quân toàn diện với Acc 89.96%, Macro P 89.88%, Macro R 89.65%, Macro-F1 89.76% (Vượt trội Linear SVM +8.47%, vượt Lexicon +46.24%).",
            "Đa thực thể (SEntFiN 1.0): Entity-Aware FinBERT đạt F1 84.11%, phân định chính xác cảm xúc từng mã cổ phiếu.",
            "Kiểm định McNemar: b = 39, c = 15 => χ² = 9.80 > 6.635, p = 0.0021 < 0.01. Khẳng định sự vượt trội có ý nghĩa thống kê ở độ tin cậy 99%."
        ]
    },
    # Slide 20: Section V Divider (Discussion & Ablation)
    20: {
        "type": "divider",
        "section": "V. Discussion & Ablation"
    },
    # Slide 21: Discussion & Ablation Study
    21: {
        "type": "content",
        "title": "Discussion & Ablation Study: Tháo Gỡ Component Để Thấy Vai Trò",
        "bullets": [
            "Mục tiêu: Tháo gỡ từng component để trả lời câu hỏi Rationale: 'Liệu có giải quyết xác đáng Problem chưa?':",
            "1. Tháo Inverse Class Weighting: Macro-F1 giảm từ 89.76% xuống 85.34%. Đặc biệt Negative Recall sụp đổ từ 88.5% xuống 74.2% (-14.3%), chứng minh vai trò ngăn chặn bỏ lọt rủi ro.",
            "2. Tháo Entity Cross-Attention: Khả năng phân định câu đa thực thể đối lập sụp đổ về ~50% (đoán ngẫu nhiên), chứng minh vai trò sống còn của cơ chế liên kết Q, K, V hướng đối tượng.",
            "3. Tháo Financial Text Cleaner: Độ trễ suy luận tăng 4 lần, nhiễu ký tự phá hỏng token embeddings."
        ]
    },
    # Slide 22: Section VI Divider (Conclusion & Future Work)
    22: {
        "type": "divider",
        "section": "VI. Conclusion & Future work"
    },
    # Slide 23: Conclusion & Future Work
    23: {
        "type": "content",
        "title": "Kết Luận & Định Hướng Mở Rộng (VN-Index, PhoBERT)",
        "bullets": [
            "Giải quyết trọn vẹn 3 cạm bẫy NLP: Xung đột từ vựng kế toán, ngữ cảnh đảo chiều và xung đột đa thực thể.",
            "Thành tựu học thuật: Macro-F1 89.76%, McNemar p = 0.0021 < 0.01, phân định thực thể F1 84.11%.",
            "Đóng gói 3 phân hệ hoàn chỉnh: FastAPI Microservice (<20ms latency), React Cyber Terminal 2.0 và Chrome Extension Manifest V3.",
            "Định hướng tương lai (Future Work): Mở rộng sang thị trường chứng khoán Việt Nam (VN-Index) thông qua tiếp tục tiền huấn luyện mô hình PhoBERT trên ngữ liệu báo cáo tài chính tiếng Việt (CafeF, Vietstock)."
        ]
    },
    # Slide 24: References
    24: {
        "type": "content",
        "title": "Tài Liệu Tham Khảo Nền Tảng (Key References)",
        "bullets": [
            "[1] Araci, D. T. (2019). FinBERT: Financial Sentiment Analysis with Pre-trained Language Models. arXiv:1908.10063.",
            "[2] Huang, A. H., Wang, H., & Yang, Y. (2023). FinBERT: A Large Language Model for Extracting Information from Financial Text. Contemporary Accounting Research, 40(2), 806-841.",
            "[3] Sinha, A., Kedas, S., Kumar, R., & Malo, P. (2022). SEntFiN 1.0: Entity-aware sentiment analysis for financial news. JASIST, 73(9), 1314-1335.",
            "[4] Malo, P., Sinha, A., Takala, P., Korhonen, P., & Wallenius, J. (2014). Good debt or bad debt: Detecting semantic orientations in economic texts. JASIST, 65(4), 782-796.",
            "[5] Loughran, T., & McDonald, B. (2011). When is a Liability not a Liability? Textual Analysis, Dictionaries, and 10-Ks. The Journal of Finance, 66(1), 35-65."
        ]
    },
    # Slide 25: Thank you & Q&A
    25: {
        "type": "thankyou",
        "title": "Cảm Ơn Thầy/Cô Và Hội Đồng Đã Lắng Nghe!",
        "subtitle": "Nhóm 4 sẵn sàng cho Phiên Hỏi & Đáp (Q&A Session)",
        "presenter": "Nhóm 4: Nguyễn Đoàn Bảo Phúc (Lead), Nguyễn Phú Triệu, Ngô Công Minh, Nguyễn Công Minh",
        "demo": "Live Demo: http://127.0.0.1:8000 (React Terminal + Chrome Extension)"
    },
    # Slide 26: Appendix
    26: {
        "type": "content",
        "title": "Phụ Lục: Siêu Tham Số Huấn Luyện & Cấu Hình Phần Cứng",
        "bullets": [
            "Kiến trúc Transformer: bert-base-uncased (12 layers, 768 hidden dimension, 12 attention heads, 110M parameters).",
            "Tối ưu hóa: AdamW, Learning Rate = 2e-5, Weight Decay = 0.01, Linear Warmup 10%, Batch Size = 16.",
            "Tăng tốc phần cứng: PyTorch Automatic Mixed Precision (AMP fp16) trên NVIDIA GeForce RTX 3050 Laptop GPU.",
            "Độ trễ suy luận trung bình (Inference Latency): Đơn mẫu = 18.2 ms | Lô 5 câu = 42.6 ms.",
            "Mã nguồn & Kiểm thử: 100% mã nguồn mở tại GitHub, vượt qua 34/34 bài unit test tự động (PyTest)."
        ]
    }
}

def set_text_box_content(shape, title_text, bullets):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.clear()
    
    for idx, bullet in enumerate(bullets):
        p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
        p.text = bullet
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 51, 51)
        p.space_after = Pt(8)
        p.line_spacing = 1.15

for slide_idx, slide in enumerate(prs.slides, start=1):
    data = SLIDES_DATA.get(slide_idx)
    if not data:
        continue
    
    stype = data.get("type")
    
    if stype == "title":
        # Slide 1
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text.strip()
                if "FinBert" in txt:
                    s.text = data["title"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(22)
                        s.text_frame.paragraphs[0].font.bold = True
                elif "Presenter" in txt:
                    s.text = data["presenter"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(12)
                elif "Supervisor" in txt:
                    s.text = data["supervisor"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(12)
                elif "Link paper" in txt:
                    s.text = data["link"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(11)

    elif stype == "outline":
        # Slide 2
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text.strip()
                if "Outline" in txt:
                    s.text = data["title"]
                elif "I. Introduction" in txt:
                    tf = s.text_frame
                    tf.clear()
                    for idx, b in enumerate(data["bullets"]):
                        p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
                        p.text = b
                        p.font.name = "Arial"
                        p.font.size = Pt(13)
                        p.space_after = Pt(6)

    elif stype == "divider":
        # Slide 3, 7, 9, 16, 20, 22
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text.strip()
                if not txt.isdigit() and len(txt) > 0:
                    s.text = data["section"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(28)
                        s.text_frame.paragraphs[0].font.bold = True

    elif stype == "content":
        # Slides with title + body
        title_shape = None
        body_shape = None
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text.strip()
                # If shape has Lorem ipsum, it's the body
                if "Lorem ipsum" in txt:
                    body_shape = s
                elif len(txt) > 0 and not txt.isdigit():
                    title_shape = s
        
        if title_shape is not None:
            title_shape.text = data["title"]
            if len(title_shape.text_frame.paragraphs) > 0:
                title_shape.text_frame.paragraphs[0].font.bold = True
        
        if body_shape is not None:
            set_text_box_content(body_shape, data["title"], data["bullets"])

    elif stype == "thankyou":
        # Slide 25
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text.strip()
                if "Thank you" in txt:
                    s.text = data["title"]
                elif "Presenter" in txt:
                    s.text = data["presenter"] + "\n" + data["demo"]

# Save updated presentation
prs.save(str(OUTPUT_PATH_DOWNLOADS))
print(f"[✓] Đã cập nhật slide chính tại: {OUTPUT_PATH_DOWNLOADS}")

try:
    prs.save(str(OUTPUT_PATH_DRIVE))
    print(f"[✓] Đã đồng bộ slide sang Google Drive tại: {OUTPUT_PATH_DRIVE}")
except Exception as e:
    print(f"[!] Không thể lưu Google Drive: {e}")
