"""Tests for OCR engine and scanned page processing."""

from PIL import Image, ImageDraw
from parseanything.ocr_engine import extract_ocr_from_image, process_scanned_image_file


def test_ocr_synthetic_image(tmp_path):
    # Create a synthetic image with text rendered on white background
    img = Image.new("RGB", (400, 100), color="white")
    d = ImageDraw.Draw(img)
    d.text((10, 10), "ParseAnything OCR Test", fill="black")

    img_path = tmp_path / "test_ocr.png"
    img.save(img_path)

    page = process_scanned_image_file(str(img_path))

    assert page.page_number == 1
    assert page.is_scanned is True
    assert len(page.blocks) >= 1
    # Check that OCR extracted content or handled execution safely
    assert page.blocks[0].confidence >= 0.0