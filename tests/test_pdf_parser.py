"""Tests for PyMuPDF digital PDF parser."""

import pytest
import fitz
from parseanything.pdf_parser import extract_digital_pdf


def test_extract_digital_pdf(tmp_path):
    # Create a synthetic 1-page PDF using PyMuPDF
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text((50, 100), "Hello World - Line 1")
    page.insert_text((50, 150), "Financial Report Executive Summary")
    doc.save(str(pdf_path))
    doc.close()

    pages = extract_digital_pdf(str(pdf_path))

    assert len(pages) == 1
    assert pages[0].page_number == 1
    assert pages[0].width == 612.0
    assert pages[0].height == 792.0
    assert len(pages[0].blocks) >= 1
    
    all_text = " ".join([b.text for b in pages[0].blocks])
    assert "Hello World" in all_text
    assert "Financial Report" in all_text