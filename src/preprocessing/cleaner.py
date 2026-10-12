r"""
bắt đầu task1.3:
- theo phát hiện ở D:\Vscode-luyện code\TMG\notebooks\01_exploratory_data_analysis.ipynb
    + ta sẽ xóa htmll, đường dẫn url và kí tự điều khiển lạ, khoảng trắng thùaw
    + giữa các kí hiệu đặc biệt tiền tệ, phần trăm, các con số doanh thu, quý, các từ chỉ quy mô mn,bn và từ phủ định thua lỗ (not, loss,down)
"""


"""
Module: cleaner.py
Task 1.3: Module tiền xử lý và chuẩn hóa văn bản tài chính.
Thiết kế dựa trên các phát hiện thực nghiệm từ EDA (Cell 6):
- Loại bỏ rác định dạng (HTML, URLs, khoảng trắng thừa).
- Bảo tồn chữ số, ký hiệu tài chính ($, €, %) và từ phủ định.
"""

import html
import re
from typing import Optional

def clean_financial_text(text : Optional[str], lowercase: bool = False) ->str:
    """
    Hàm làm sạch và chuẩn hóa một chuỗi văn bản tài chính.
    Args:
        text (str): Chuỗi văn bản thô đầu vào.
        lowercase (bool): Có chuyển về chữ thường hay không (mặc định False
                          để bảo toàn mã cổ phiếu như AAPL, MSFT, EUR).
    Returns:
        str: Chuỗi văn bản đã được làm sạch chuẩn hóa.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    
    # 1. Giải mã các thực thể HTML (ví dụ &amp; -> &, &nbsp; -> khoảng trắng)
    text =  html.unescape(text)

    #2. xóa các thẻ html ví dụ <p>, <br>,..
    text = re.sub(r"<[^>]+>", " ",text)
    
    #3. Xóa đường dẫn urls (https://, http://, www.)
    text = re.sub(r'https?://\S+|www\.\S+'," ", text)

    #4. chuẩn hóa dẫu nháy đơn, nháy kép và gạch ngang đăc biệt
    text = re.sub(r"[\u2018\u2019\u201A\u201B]", "'", text)
    text = re.sub(r"[\u201C\u201D\u201E\u201F]", '"', text)
    text = re.sub(r"[\u2013\u2014]", "-", text)

    #5. chuẩn hóa khoảng cách trắng quanh kí hiệu tiền tệ và số liueuej
    # Giữ nguyên $100, €50, 10.5%, EUR 1.5 mn
    text = re.sub(r"\s+", " ", text)

    #6. chuyển chữ thường nếu được yêu cầu cho Classical ML
    if lowercase:
        text = text.lower()

    return text.strip()

class FinancialTextCleaner:
    """Class bọc phục vụ áp dụng hàng loạt trên dataframe hoặc pipelin"""

    def __init__(self, lowercase:bool = False):
        self.lowercase  =lowercase

    def transform(self, texts):
        return [clean_financial_text(t, lowercase=self.lowercase) for t in texts]
    
    def __call__(self, text:str)->str:
        return clean_financial_text(text, lowercase=self.lowercase)
