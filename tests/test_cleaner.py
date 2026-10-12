"""
Module: test_cleaner.py
Bộ kiểm thử đơn vị (Unit Tests) cho module làm sạch văn bản tài chính.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pytest
from src.preprocessing.cleaner import clean_financial_text, FinancialTextCleaner


def test_clean_html_and_urls():
    raw = "<p>Check out the earnings report at https://bloomberg.com/news &amp; details.</p>"
    cleaned = clean_financial_text(raw)
    assert "<p>" not in cleaned
    assert "https://" not in cleaned
    assert "&" in cleaned
    assert "Check out the earnings report at & details." == cleaned


def test_preserve_financial_entities():
    """Kiểm tra xem hàm có vô tình xóa mất ký hiệu $, €, % hay số liệu không."""
    raw = "Net sales increased by 15.5 % to EUR 205.5 mn, compared to $ 180 mn."
    cleaned = clean_financial_text(raw)
    assert "%" in cleaned
    assert "EUR" in cleaned
    assert "$" in cleaned
    assert "205.5" in cleaned
    assert "mn" in cleaned


def test_preserve_negation_and_losses():
    """Kiểm tra xem các từ phủ định và báo lỗ có được giữ nguyên không."""
    raw = "The firm did not report a profit, incurring an operating loss down 20%."
    cleaned = clean_financial_text(raw)
    assert "not" in cleaned
    assert "operating loss" in cleaned
    assert "down" in cleaned


def test_edge_cases():
    """Kiểm tra các trường hợp biên: chuỗi rỗng, None, nhiều khoảng trắng."""
    assert clean_financial_text("") == ""
    assert clean_financial_text(None) == ""
    assert clean_financial_text("   Lots    of   spaces   ") == "Lots of spaces"


def test_cleaner_class():
    """Kiểm tra class FinancialTextCleaner."""
    cleaner = FinancialTextCleaner(lowercase=True)
    batch = ["PROFIT OF EUR 10 MN.", "Loss of $5 Mn."]
    result = cleaner.transform(batch)
    assert result == ["profit of eur 10 mn.", "loss of $5 mn."]