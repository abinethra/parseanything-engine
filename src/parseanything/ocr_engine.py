"""OCR extraction module using pytesseract and Pillow/OpenCV for scanned pages and images."""

import os
from typing import List, Tuple
from PIL import Image
import pytesseract
from parseanything.schema import Block, BlockType, BBox, Page

# Configure Tesseract path for standard Windows installation if not in PATH
DEFAULT_WIN_TESSERACT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(DEFAULT_WIN_TESSERACT):
    pytesseract.pytesseract.tesseract_cmd = DEFAULT_WIN_TESSERACT


def extract_ocr_from_image(image: Image.Image, page_number: int = 1) -> Tuple[List[Block], float]:
    """Runs OCR on a PIL Image object and returns extracted blocks and average page confidence."""
    width, height = image.size

    # Get word-level data including bounding boxes and confidence scores
    try:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    except Exception as e:
        # Fallback if Tesseract binary is not installed on system
        return [
            Block(
                block_id=f"p{page_number}_ocr_err",
                block_type=BlockType.PARAGRAPH,
                text="[OCR engine unavailable or Tesseract not installed]",
                page_number=page_number,
                bbox=BBox(x0=0, y0=0, x1=float(width), y1=float(height)),
                confidence=0.0,
                flags=["ocr_failed"]
            )
        ], 0.0

    blocks: List[Block] = []
    n_boxes = len(data["text"])

    current_text_words = []
    current_confidences = []
    x0, y0, x1, y1 = float("inf"), float("inf"), 0.0, 0.0

    total_conf = 0.0
    valid_words_count = 0

    for i in range(n_boxes):
        text = data["text"][i].strip()
        conf = float(data["conf"][i])

        if conf > 0:
            total_conf += conf
            valid_words_count += 1

        if text:
            left = float(data["left"][i])
            top = float(data["top"][i])
            w = float(data["width"][i])
            h = float(data["height"][i])

            current_text_words.append(text)
            current_confidences.append(max(0.0, conf) / 100.0)

            x0 = min(x0, left)
            y0 = min(y0, top)
            x1 = max(x1, left + w)
            y1 = max(y1, top + h)

        # Create block at line break or paragraph end
        if (data["block_num"][i] != data["block_num"][i - 1] if i > 0 else False) or (i == n_boxes - 1):
            if current_text_words and x0 < x1 and y0 < y1:
                block_text = " ".join(current_text_words)
                avg_conf = sum(current_confidences) / len(current_confidences) if current_confidences else 0.5
                
                flags = []
                if avg_conf < 0.6:
                    flags.append("low_confidence_ocr")

                bbox = BBox(
                    x0=round(x0, 2),
                    y0=round(y0, 2),
                    x1=round(x1, 2),
                    y1=round(y1, 2)
                )

                block = Block(
                    block_id=f"p{page_number}_ocr_{len(blocks) + 1}",
                    block_type=BlockType.PARAGRAPH,
                    text=block_text,
                    page_number=page_number,
                    bbox=bbox,
                    confidence=round(avg_conf, 2),
                    flags=flags,
                    metadata={"source": "ocr"}
                )
                blocks.append(block)

            current_text_words = []
            current_confidences = []
            x0, y0, x1, y1 = float("inf"), float("inf"), 0.0, 0.0

    avg_page_conf = (total_conf / valid_words_count / 100.0) if valid_words_count > 0 else 0.0
    return blocks, round(avg_page_conf, 2)


def process_scanned_image_file(file_path: str) -> Page:
    """Processes a standalone PNG or JPG image file with OCR."""
    image = Image.open(file_path)
    width, height = image.size
    blocks, _ = extract_ocr_from_image(image, page_number=1)

    return Page(
        page_number=1,
        width=float(width),
        height=float(height),
        blocks=blocks,
        is_scanned=True
    )