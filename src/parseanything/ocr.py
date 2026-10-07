from typing import Any, Dict, List
import pytesseract
from PIL import Image

def is_scanned_page(page_text: str, threshold: int = 50) -> bool:
    """
    Determines if a page is scanned based on extracted digital text length.
    """
    clean_text = page_text.strip() if page_text else ""
    return len(clean_text) < threshold

def extract_text_via_ocr(image_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text blocks with bounding boxes and word-level confidence using Tesseract OCR.
    """
    extracted_blocks = []
    try:
        image = Image.open(image_path)
        ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        n_boxes = len(ocr_data['text'])
        line_text = []
        confidences = []
        
        for i in range(n_boxes):
            text = ocr_data['text'][i].strip()
            conf = int(ocr_data['conf'][i])
            
            if text:
                line_text.append(text)
                if conf > 0:
                    confidences.append(conf)
            
            # Group into line-level blocks when a newline/block breaks
            if (ocr_data['text'][i] == '' or i == n_boxes - 1) and line_text:
                combined_text = " ".join(line_text)
                avg_conf = round(sum(confidences) / len(confidences) / 100.0, 2) if confidences else 0.50
                
                extracted_blocks.append({
                    "block_id": f"ocr_b{len(extracted_blocks) + 1}",
                    "text": combined_text,
                    "block_type": "paragraph",
                    "bbox": {
                        "x0": ocr_data['left'][i],
                        "y0": ocr_data['top'][i],
                        "x1": ocr_data['left'][i] + ocr_data['width'][i],
                        "y1": ocr_data['top'][i] + ocr_data['height'][i],
                    },
                    "confidence": avg_conf,
                    "flags": ["ocr_extracted"]
                })
                line_text = []
                confidences = []
                
    except Exception as e:
        print(f"Error during OCR extraction: {e}")
        
    return extracted_blocks
