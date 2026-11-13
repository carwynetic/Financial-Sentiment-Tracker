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

TEMPLATE_PATH = Path(r"c:\Users\CARWYN\Downloads\presentation_backup.pptx")
DEST_DOWNLOADS = Path(r"c:\Users\CARWYN\Downloads\presentation.pptx")
DEST_DOWNLOADS_ALT = Path(r"c:\Users\CARWYN\Downloads\presentation_hoan_chinh.pptx")
DEST_DRIVE = Path(r"G:\My Drive\Study\FPT University AI\Kì 5\Text Mining (TMG301)\Project\presentation_hoan_chinh.pptx")
DEST_DRIVE_ALT = Path(r"G:\My Drive\Study\FPT University AI\Kì 5\Text Mining (TMG301)\Project\presentation.pptx")

prs = pptx.Presentation(str(TEMPLATE_PATH))

SLIDES_CONTENT = {
    # Slide 1: Title
    1: {
        "type": "title",
        "title": "HỆ THỐNG PHÂN TÍCH CẢM XÚC TIN TỨC TÀI CHÍNH THEO THỰC THỂ",
        "presenter": "Nhóm 4 (AI Batch 19): Nguyễn Đoàn Bảo Phúc (Lead), Nguyễn Phú Triệu, Ngô Công Minh, Nguyễn Công Minh",
        "supervisor": "Giảng viên hướng dẫn: ThS. Vũ Hà Anh — Môn học: Text Mining (TMG301)",
        "link": "https://github.com/carwynetic/Financial-Sentiment-Tracker"
    },

    # Slide 2: Outline
    2: {
        "type": "outline",
        "title": "Lộ Trình Báo Cáo 10 Phút Chuẩn Bảo Vệ (Theo Sơ Đồ Pipeline)",
        "bullets": [
            ("I. Introduction (1m - 1m30s):", " Bối cảnh (Context: Topic & Situation) -> 3 Cạm bẫy NLP -> Solutions & Thành tựu nổi bật"),
            ("II. Related Work (2m - 2m30s):", " 4 Bài báo nền tảng -> Trả lời câu hỏi trọng tâm 'Liên quan gì?' -> Khoảng trống nghiên cứu"),
            ("III. Contribution & Pipeline (3m):", " Problem Formulation -> Overall Architecture -> 3 Đóng góp cốt lõi (Rationale) -> Train & Test Strategy"),
            ("IV. Experiments & Results (2m):", " Datasets & Configs -> Master Benchmark Matrix -> Trả lời 'What problems solved?' & McNemar (p < 0.01)"),
            ("V. Discussion & Ablation (1m):", " 'Tháo gỡ component để thấy vai trò' (Inverse Class Weights, Cross-Attention) -> Error Taxonomy (6 dạng lỗi)"),
            ("VI. Conclusion & Future (1m):", " Solution Summary -> Đóng gói 3 phân hệ (FastAPI, React, Chrome Ext) -> Mở rộng VN-Index (PhoBERT)")
        ]
    },

    # Slide 3: Divider - I. Introduction
    3: {
        "type": "divider",
        "title": "I. Introduction\n(Bối Cảnh, 3 Cạm Bẫy NLP & Giải Pháp)"
    },

    # Slide 4: Context
    4: {
        "type": "content",
        "title": "I. Introduction: Context (Bối Cảnh Nghiên Cứu)",
        "bullets": [
            ("[Topic - Chủ đề nghiên cứu]:", " Tự động hóa phân tích cảm xúc tin tức tài chính thích ứng miền (Domain-Adapted Financial Sentiment Analysis) với mô hình FinBERT."),
            ("[Situation - Thực trạng thị trường]:", " Thị trường tài chính vận hành ở quy mô mili-giây. Dòng vốn hàng nghìn tỷ USD phản ứng tức thì trước tin tức báo chí, thông cáo và hồ sơ SEC (10-K, 10-Q)."),
            ("[Information Overload - Bùng nổ thông tin]:", " Hàng chục nghìn bài báo xuất bản mỗi ngày, vượt quá hoàn toàn khả năng đọc hiểu và tổng hợp thủ công của các chuyên viên phân tích."),
            ("[Nhu cầu cấp thiết]:", " Xây dựng hệ sinh thái AI phân tích cảm xúc tin tức với độ chính xác cao và độ trễ thấp (<20ms) để cảnh báo rủi ro danh mục và hỗ trợ giao dịch thuật toán.")
        ]
    },

    # Slide 5: Challenge
    5: {
        "type": "content",
        "title": "I. Introduction: Challenge (3 Điểm Nghẽn Khiến NLP Thất Bại)",
        "bullets": [
            ("1. Xung đột từ vựng kế toán (Vocabulary Collision):", " Loughran & McDonald (2011) chứng minh từ điển ngôn ngữ thông thường gán sai 73.8% từ tiêu cực (những từ bình thường như liability, cost, tax, capital bị coi là xấu)."),
            ("2. Phủ định kép & Đảo chiều phức hợp (Turnaround Nuance):", " Câu 'pretax loss narrowed' (khoản lỗ thu hẹp = tin tốt/bước ngoặt) bị các mô hình đếm từ gán nhãn Tiêu cực do thấy chữ 'loss'."),
            ("3. Xung đột đa thực thể trái chiều (Multi-Entity Conflict):", " Câu chứa 2 thực thể đối lập ('Gold extends gains on festive buying, weak rupee') khiến phân loại cấp câu bị triệt tiêu tín hiệu."),
            ("[Rationale Link]:", " Cả 3 điểm nghẽn này đòi hỏi kiến trúc Transformer hiểu sâu ngữ cảnh chuyên ngành và cơ chế Cross-Attention hướng đối tượng.")
        ]
    },

    # Slide 6: Solutions & Key Achievements
    6: {
        "type": "content",
        "title": "I. Introduction: Solutions & Key Achievements",
        "bullets": [
            ("[Summary - Tóm tắt giải pháp]:", " Xây dựng hệ thống Financial Sentiment Tracker với FinBERT thích ứng miền, tích hợp Inverse Class Weighting trong hàm mất mát và Sentence-Pair Cross-Attention phân giải thực thể."),
            ("[Achievement 1 - Quán quân Benchmark]:", " Macro-F1 đạt 89.76% trên Financial PhraseBank, vượt trội Linear SVM (+8.47%) và Loughran-McDonald Lexicon (+46.24%)."),
            ("[Achievement 2 - Phân định đa thực thể]:", " Giải quyết dứt điểm câu đa ticker với F1 đạt 84.11% trên tập kiểm thử chuẩn SEntFiN 1.0 (2,169 mẫu)."),
            ("[Achievement 3 - Ý nghĩa thống kê & Phần mềm]:", " Kiểm định McNemar đạt p = 0.0021 < 0.01; đóng gói trọn vẹn 3 phân hệ: FastAPI GPU Microservice, React Cyber Terminal 2.0, Chrome Extension V3.")
        ]
    },

    # Slide 7: Divider - II. Related Work
    7: {
        "type": "divider",
        "title": "II. Related Work\n(4 Bài Báo Nền Tảng & Khoảng Trống Nghiên Cứu)"
    },

    # Slide 8: Related work
    8: {
        "type": "content",
        "title": "II. Related Work: 4 Nghiên Cứu Nền Tảng (Trả lời: 'Liên quan gì?')",
        "bullets": [
            ("1. Loughran & McDonald (2011) [JOF]:", " Tạo từ điển tài chính 347 Pos / 2,345 Neg -> [Liên quan gì?]: Nhóm dùng dựng mốc đối chuẩn yếu nhất (Tier 1 Lexicon Baseline). [Hạn chế]: Bag-of-Words, mù ngữ cảnh."),
            ("2. Araci (2019) & Huang et al. (2023) [CAR]:", " Tiền huấn luyện BERT trên báo cáo 10-K/10-Q -> [Liên quan gì?]: Nền tảng trọng số thích ứng miền cho Tier 3 Transformer. [Hạn chế]: Chỉ xử lý cấp câu đơn thuần."),
            ("3. Sinha et al. (2022) [SEntFiN 1.0]:", " Đặt bài toán cảm xúc hướng thực thể -> [Liên quan gì?]: Cung cấp dữ liệu để nhóm xây dựng Sentence-Pair Cross-Attention; nhóm đóng góp thêm Headline-Level Split chống rò rỉ dữ liệu."),
            ("4. Malo et al. (2014) [PhraseBank]:", " Bộ ngữ liệu chuẩn 3,453 câu (75% agreement) -> [Liên quan gì?]: Bộ benchmark trung tâm để nhóm đối chuẩn 8 mô hình thuộc 3 tầng công nghệ.")
        ]
    },

    # Slide 9: Divider - III. Contribution
    9: {
        "type": "divider",
        "title": "III. Contribution & Methodology\n(Định Nghĩa Bài Toán, Pipeline & 3 Đóng Góp Cốt Lõi)"
    },

    # Slide 10: Problem formulation
    10: {
        "type": "content",
        "title": "III. Contribution: (1) Problem Formulation (Định Nghĩa Toán Học)",
        "bullets": [
            ("[Input & Output - Cấp câu (Sentence-Level)]:", " Cho câu s = (w1, ..., wL). Ánh xạ cực đại hóa xác suất: ŷ = argmax_{c ∈ {0,1,2}} ℙ(Y = c | s; θ) với Y = {0: Negative, 1: Neutral, 2: Positive}."),
            ("[Input & Output - Cấp thực thể (Entity-Level)]:", " Cho tiêu đề s chứa tập thực thể E. Ánh xạ có điều kiện thực thể e_target: ŷ_e = argmax_{c} ℙ(Y = c | e_target, s; θ)."),
            ("[Cấu trúc Sequence-Pair]:", " Chuỗi đầu vào ghép nối: x = [CLS] ⊕ e_target ⊕ [SEP] ⊕ s_headline ⊕ [SEP] với Token Type IDs (0...0, 1...1) xử lý đồng thời qua ma trận Cross-Attention."),
            ("[Mục tiêu tối ưu hóa]:", " Tối thiểu hóa hàm mất mát Weighted Cross-Entropy Loss có phạt trọng số nghịch đảo tần suất lớp.")
        ]
    },

    # Slide 11: Overall architecture
    11: {
        "type": "content",
        "title": "III. Contribution: (2) Overall Architecture (Kiến Trúc 4 Tầng)",
        "bullets": [
            ("Tầng 1 (Ingestion & Preprocessing):", " Thu nạp tin tức trực tiếp; xử lý chuyên biệt qua cleaner.py bảo tồn 100% định lượng, tiền tệ, %, từ báo lỗ; cố định max_seq_length = 64 tokens."),
            ("Tầng 2 (Model Hierarchy):", " Bậc thang đối chuẩn 3 tầng công nghệ: Tier 1 Lexicon (Loughran-McDonald) -> Tier 2 Classical ML (Multinomial NB, Logistic Regression, Linear SVM) -> Tier 3 Transformer."),
            ("Tầng 3 (Optimization & Disambiguation):", " Hàm mất mát Inverse Class Weighting (bù trừ mất cân bằng lớp 5.1:1) + Sentence-Pair Cross-Attention phân giải thực thể."),
            ("Tầng 4 (Deployment Ecosystem):", " Đóng gói hoàn chỉnh: REST API (FastAPI, độ trễ 18.2ms), Giao diện Cyber Terminal 2.0 (React SPA) và Chrome Extension Manifest V3 duyệt tin live.")
        ]
    },

    # Slide 12: Contribution 1
    12: {
        "type": "content",
        "title": "III. Contribution: (3) Đóng Góp 1 - Financial Text Cleaner",
        "bullets": [
            ("[Rationale: Liệu có giải quyết xác đáng Problem chưa?]:", " Text cleaner thông thường xóa hết số và ký tự, phá hủy hoàn toàn tín hiệu tài chính. Module của nhóm bảo tồn 100% thông tin định lượng sống còn."),
            ("Bảo tồn định lượng 100%:", " Giữ nguyên vẹn ký hiệu tiền tệ ($ € VND), tỷ lệ %, số liệu tăng trưởng và chỉ số biên lợi nhuận."),
            ("Bảo tồn cấu trúc phủ định & bước ngoặt:", " Không lược bỏ các từ ngữ báo lỗ và đảo ngược ngữ cảnh như 'loss', 'narrowed', 'dropped', 'plunged'."),
            ("Tối ưu hóa GPU VRAM:", " Cố định max_seq_length = 64 tokens cho tập câu đơn, tiết kiệm 75% VRAM trên GPU RTX 3050 Laptop, triệt tiêu nguy cơ tràn bộ nhớ CUDA OOM.")
        ]
    },

    # Slide 13: Contribution 2
    13: {
        "type": "content",
        "title": "III. Contribution: (3) Đóng Góp 2 - Inverse Class Weighting",
        "bullets": [
            ("[Rationale: Liệu có giải quyết xác đáng Problem chưa?]:", " Tập Train bị lệch nghiêm trọng: Neutral chiếm 62.14%, Negative chỉ 12.16% (lệch 5.1 : 1). Mô hình thông thường sẽ đoán vẹt Neutral để tối ưu Accuracy bề mặt."),
            ("Công thức Trọng số Phạt Nghịch đảo Lớp:", " w_c = N / (C × N_c) => w_neg = 2.7404 (phạt nặng nhất), w_neu = 0.5364, w_pos = 1.2974."),
            ("Hàm mất mát Weighted Cross-Entropy Loss:", " L_WCE = - ∑_{c=1}^C w_c · y_c log(ŷ_c). Phạt nặng gấp 5.1 lần (2.7404 / 0.5364) khi mô hình đoán sai mẫu rủi ro Negative."),
            ("Hiệu quả thực tế:", " Nâng Negative Recall từ 74.2% lên 88.5%, bảo vệ nhà đầu tư khỏi rủi ro bỏ lọt tin xấu.")
        ]
    },

    # Slide 14: Contribution 3
    14: {
        "type": "content",
        "title": "III. Contribution: (3) Đóng Góp 3 - Sentence-Pair Cross-Attention",
        "bullets": [
            ("[Rationale: Liệu có giải quyết xác đáng Problem chưa?]:", " Giải quyết dứt điểm Cạm bẫy 3: Tiêu đề chứa 2 thực thể đối lập ('Gold extends gains, weak rupee'). Mô hình cấp câu bị triệt tiêu tín hiệu."),
            ("Cấu trúc mã hóa cặp câu:", " [CLS] ⊕ e_target ⊕ [SEP] ⊕ s_headline ⊕ [SEP] với Segment IDs (0...0, 1...1)."),
            ("Cơ chế Cross-Attention:", " Ma trận Attention(Q, K, V) = softmax(Q K^T / √d_k) V với Q xuất phát từ e_target, hướng sự chú ý liên kết thực thể mục tiêu trực tiếp với từ ngữ cảm xúc bổ nghĩa cho nó."),
            ("Kết quả thực nghiệm:", " Đạt F1 84.11% trên 2,169 mẫu SEntFiN test set, phân định chính xác Gold (+) và rupee (-) trong cùng một câu.")
        ]
    },

    # Slide 15: Training strategy
    15: {
        "type": "content",
        "title": "III. Contribution: (4) Train & Test Strategy (Zero Data Leakage)",
        "bullets": [
            ("Nguyên tắc Chống rò rỉ dữ liệu (Zero Data Leakage):", " Với SEntFiN (14,405 cặp), phân tách Stratified Split 70/15/15 ở cấp Headline ID, tuyệt đối không tách ngẫu nhiên ở cấp cặp câu."),
            ("Chuẩn hóa Feature Extraction ML:", " TF-IDF Vectorizer chỉ gọi .fit_transform() trên Train, chỉ dùng .transform() trên Val/Test để ngăn ngừa từ vựng test rò rỉ vào train."),
            ("Tối ưu hóa GPU Phần cứng:", " PyTorch Automatic Mixed Precision (AMP fp16), AdamW (lr = 2e-5, weight decay = 0.01), batch size 16, Linear Warmup 10%."),
            ("Checkpoint Selection:", " Lưu checkpoint mô hình tối ưu dựa trên đỉnh Validation Macro-F1 để chống hiện tượng over-fitting.")
        ]
    },

    # Slide 16: Divider - IV. Experiments
    16: {
        "type": "divider",
        "title": "IV. Experiments & Results\n(Bộ Dữ Liệu, Cấu Hình & Bảng Đối Chuẩn Tổng Thể)"
    },

    # Slide 17: Dataset
    17: {
        "type": "content",
        "title": "IV. Experiments: Dataset & Môi Trường Thực Nghiệm",
        "bullets": [
            ("1. Financial PhraseBank (Malo et al., 2014):", " 3,453 câu tài chính (75% agreement subset). Train: 2,417 (70%), Val: 518 (15%), Test: 518 (15%). Lớp: Neutral 62.14%, Positive 25.69%, Negative 12.16%."),
            ("2. SEntFiN 1.0 (Sinha et al., 2022):", " 14,405 cặp entity-headline tin tức tài chính. Train: 10,083 (70%), Val: 2,161 (15%), Test: 2,161 (15%)."),
            ("3. Môi trường phần cứng máy trạm:", " NVIDIA GeForce RTX 3050 6GB Laptop GPU (Tensor Cores), CUDA 13.0, cuDNN 9.1, PyTorch 2.13.0, Python 3.14."),
            ("Minh bạch học thuật:", " Cố định 100% random seed = 42 trên toàn bộ thư viện, đảm bảo khả năng tái lập độc lập kết quả 100%.")
        ]
    },

    # Slide 18: Configuration
    18: {
        "type": "content",
        "title": "IV. Experiments: Cấu Hình Thực Nghiệm & 8 Mô Hình Đối Chuẩn",
        "bullets": [
            ("Tier 1: Lexicon Baseline:", " Loughran-McDonald Financial Dictionary (2011/2025) (347 Pos, 2,345 Neg)."),
            ("Tier 2: Classical Machine Learning:", " Multinomial Naive Bayes (alpha=1.0), Logistic Regression (class_weight='balanced'), Linear SVM (C=1.0, max_iter=2000)."),
            ("Tier 3: Transformer Zero-Shot:", " yiyanghkust/finbert-tone và ProsusAI/finbert."),
            ("Tier 3: Transformer Fine-Tuned (Proposed):", " FinBERT Fine-Tuned (PhraseBank) & Entity-Aware FinBERT (SEntFiN 1.0) huấn luyện với Inverse Class Weights.")
        ]
    },

    # Slide 19: Result
    19: {
        "type": "content",
        "title": "IV. Experiments: Results (Master Benchmark Matrix & McNemar)",
        "bullets": [
            ("Tier 1 (Lexicon):", " Loughran-McDonald đạt Acc 56.18%, Macro-F1 43.52% (Mù ngữ pháp và cấu trúc câu đảo chiều)."),
            ("Tier 2 (Classical ML):", " Linear SVM là quán quân Tier 2 với Acc 86.49%, Macro-F1 81.29% nhờ biên phân tách tối đa."),
            ("Tier 3 (FinBERT Fine-Tuned):", " Quán quân toàn diện với Acc 89.96%, Macro P 89.88%, Macro R 89.65%, Macro-F1 89.76% (Vượt trội Linear SVM +8.47%, vượt Lexicon +46.24%)."),
            ("Entity-Aware FinBERT:", " F1 đạt 84.11% trên SEntFiN test set, giải quyết trọn vẹn câu đa thực thể đối lập."),
            ("Kiểm định ý nghĩa thống kê McNemar:", " b = 39, c = 15 => χ² = (|39-15|-1)² / (39+15) = 9.80 > 6.635, p = 0.0021 < 0.01 (Độ tin cậy 99%).")
        ]
    },

    # Slide 20: Divider - V. Discussion & Ablation
    20: {
        "type": "divider",
        "title": "V. Discussion & Ablation\n('Tháo Gỡ Component' & Phân Loại Lỗi Ngôn Ngữ Học)"
    },

    # Slide 21: Discussion & Ablation
    21: {
        "type": "content",
        "title": "V. Discussion & Ablation: 'Tháo Gỡ Component Để Thấy Vai Trò'",
        "bullets": [
            ("Mục tiêu phản biện Rationale:", " Tháo gỡ từng component để chứng minh vai trò không thể thay thế đối với độ chính xác toàn hệ thống:"),
            ("1. Tháo Inverse Class Weighting:", " Macro-F1 giảm từ 89.76% xuống 85.34%. Đặc biệt Negative Recall sụp đổ từ 88.5% xuống 74.2% (-14.3%), chứng minh vai trò ngăn chặn bỏ lọt rủi ro."),
            ("2. Tháo Entity Cross-Attention:", " Khả năng phân định câu đa thực thể đối lập sụp đổ về ~50% (đoán ngẫu nhiên), chứng minh vai trò sống còn của cơ chế liên kết Q, K, V hướng đối tượng."),
            ("3. Tháo Financial Text Cleaner:", " Độ trễ suy luận tăng gấp 4 lần, nhiễu ký tự phá hỏng token embeddings, Macro-F1 giảm -3.12%.")
        ]
    },

    # Slide 22: Error Taxonomy
    22: {
        "type": "content",
        "title": "V. Discussion: Error Taxonomy (Phân Loại 6 Dạng Lỗi Ngôn Ngữ)",
        "bullets": [
            ("Bóc tách 41 ca dự đoán sai (tỷ lệ lỗi 7.92% trên 518 mẫu test):", ""),
            ("Neutral -> Positive (31.7%, 13 ca):", " Báo cáo mở rộng thông thường chứa từ tăng doanh số ('sales grew by 9%')."),
            ("Positive -> Neutral (29.3%, 12 ca):", " Hợp đồng thương mại dùng văn phong ngoại giao thận trọng, ước tính ('aim is to double turnover')."),
            ("Positive -> Negative (14.6%, 6 ca):", " Cấu trúc hồi sinh độc lạ ('survived near liquidation', 'narrowed loss')."),
            ("Negative -> Neutral (12.2%, 5 ca) & Neutral -> Negative (7.3%, 3 ca):", " Báo cáo tuân thủ pháp lý, tổn thất gián tiếp."),
            ("Negative -> Positive (4.9%, 2 ca):", " Khoản lỗ thu hẹp nhưng giá trị lỗ tuyệt đối vẫn quá lớn.")
        ]
    },

    # Slide 23: Divider - VI. Conclusion & Future work
    23: {
        "type": "divider",
        "title": "VI. Conclusion & Future Work\n(Tổng Kết Đóng Góp & Mở Rộng Thị Trường Việt Nam)"
    },

    # Slide 24: Conclusion & Future work
    24: {
        "type": "content",
        "title": "VI. Conclusion & Future Work (Tổng Kết & Mở Rộng VN-Index)",
        "bullets": [
            ("[Solution Summary - Tổng kết giải pháp]:", " Hoàn thành hệ thống Financial Sentiment Tracker giải quyết trọn vẹn 3 cạm bẫy NLP (Xung đột từ vựng, ngữ cảnh đảo chiều, đa thực thể)."),
            ("[Achievements - Thành tựu cốt lõi]:", " Macro-F1 89.76%, McNemar p = 0.0021 < 0.01, Entity F1 84.11%, 3 phân hệ phần mềm (FastAPI độ trễ 18.2ms, React Terminal 2.0, Chrome Extension V3), 34/34 tests passed."),
            ("[Future Work 1 - Mở rộng thị trường Việt Nam]:", " Thách thức tách từ ghép tài chính ('thu nhập ròng', 'cổ tức') và tiếng lóng F0 ('úp bô', 'bắt đáy', 'múa bên trăng'). Tiếp tục tiền huấn luyện PhoBERT-base trên 500,000 bài báo CafeF, Vietstock và báo cáo tài chính sàn HOSE/HNX."),
            ("[Future Work 2 - Giao dịch định lượng]:", " Tích hợp chỉ số cảm xúc thời gian thực vào các thuật toán backtest giao dịch định lượng (Quantitative Trading) trên rổ chỉ số VN30.")
        ]
    },

    # Slide 25: References & Thank you
    25: {
        "type": "thankyou",
        "title": "Cảm Ơn Thầy/Cô Và Hội Đồng Đã Lắng Nghe!",
        "subtitle": "Nhóm 4 sẵn sàng cho Phiên Hỏi & Đáp (Q&A Session)",
        "presenter": "Nhóm 4: Nguyễn Đoàn Bảo Phúc (Lead), Nguyễn Phú Triệu, Ngô Công Minh, Nguyễn Công Minh",
        "demo": "Live Demo Hệ Sinh Thái: http://127.0.0.1:8000 (React Terminal + Chrome Extension V3)"
    },

    # Slide 26: Appendix
    26: {
        "type": "content",
        "title": "Phụ Lục: Cấu Hình Siêu Tham Số & Môi Trường Phần Cứng",
        "bullets": [
            ("Kiến trúc mạng nơ-ron lõi:", " bert-base-uncased (12 layers, 768 hidden dimension, 12 attention heads, 110M parameters)."),
            ("Tham số huấn luyện Fine-Tuning:", " Thuật toán AdamW, Learning Rate = 2e-5, Weight Decay = 0.01, Linear Warmup 10%, Batch Size = 16, Epochs = 5."),
            ("Tăng tốc phần cứng GPU:", " PyTorch Automatic Mixed Precision (AMP fp16) trên NVIDIA GeForce RTX 3050 Laptop GPU (6GB VRAM, Tensor Cores)."),
            ("Độ trễ suy luận thời gian thực (Inference Latency):", " Đơn mẫu = 18.2 ms | Lô 5 mẫu = 42.6 ms | Cào tin yfinance + chấm điểm ticker = 145 ms."),
            ("Mã nguồn & Kiểm thử:", " 100% mã nguồn mở trên GitHub, vượt qua 34/34 bài unit test tự động (PyTest).")
        ]
    }
}

def set_text_box_content(shape, bullets):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.clear()
    
    for idx, (prefix, text) in enumerate(bullets):
        p = tf.add_paragraph() if idx > 0 else tf.paragraphs[0]
        p.space_after = Pt(7)
        p.line_spacing = 1.15
        
        if prefix:
            r1 = p.add_run()
            r1.text = prefix
            r1.font.bold = True
            r1.font.name = "Arial"
            r1.font.size = Pt(13)
            r1.font.color.rgb = RGBColor(30, 41, 59)
            
        if text:
            r2 = p.add_run()
            r2.text = text
            r2.font.bold = False
            r2.font.name = "Arial"
            r2.font.size = Pt(12.5)
            r2.font.color.rgb = RGBColor(51, 65, 85)

for slide_idx, slide in enumerate(prs.slides, start=1):
    data = SLIDES_CONTENT.get(slide_idx)
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
                        s.text_frame.paragraphs[0].font.size = Pt(21)
                        s.text_frame.paragraphs[0].font.bold = True
                elif "Presenter" in txt:
                    s.text = data["presenter"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(11.5)
                elif "Supervisor" in txt:
                    s.text = data["supervisor"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(11.5)
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
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(20)
                        s.text_frame.paragraphs[0].font.bold = True
                elif "I. Introduction" in txt or "Lorem" in txt:
                    set_text_box_content(s, data["bullets"])

    elif stype == "divider":
        # Slide 3, 7, 9, 16, 20, 23
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text.strip()
                if not txt.isdigit() and len(txt) > 0:
                    s.text = data["title"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(26)
                        s.text_frame.paragraphs[0].font.bold = True
                        s.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    elif stype == "content":
        title_shape = None
        body_shape = None
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text.strip()
                if "Lorem ipsum" in txt:
                    body_shape = s
                elif len(txt) > 0 and not txt.isdigit():
                    title_shape = s
        
        if title_shape is not None:
            title_shape.text = data["title"]
            if len(title_shape.text_frame.paragraphs) > 0:
                title_shape.text_frame.paragraphs[0].font.bold = True
                title_shape.text_frame.paragraphs[0].font.size = Pt(19)
        
        if body_shape is not None:
            set_text_box_content(body_shape, data["bullets"])
        else:
            # Nếu slide chưa có body text box (như Slide 11), thêm mới
            new_box = slide.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(8.8), Inches(5.2))
            set_text_box_content(new_box, data["bullets"])

    elif stype == "thankyou":
        # Slide 25
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text.strip()
                if "Thank you" in txt:
                    s.text = data["title"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(24)
                        s.text_frame.paragraphs[0].font.bold = True
                elif "Presenter" in txt:
                    s.text = data["presenter"] + "\n\n" + data["demo"]
                    if len(s.text_frame.paragraphs) > 0:
                        s.text_frame.paragraphs[0].font.size = Pt(12)

# Lưu lần lượt vào các đích đến
for dest_path in [DEST_DOWNLOADS, DEST_DOWNLOADS_ALT, DEST_DRIVE, DEST_DRIVE_ALT]:
    try:
        prs.save(str(dest_path))
        print(f"[✓] Đã lưu thành công presentation tại: {dest_path}")
    except Exception as e:
        print(f"[!] Lỗi khi lưu tại {dest_path}: {e}")

