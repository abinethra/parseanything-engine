from typing import Any, Dict, List
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_figures_from_page(doc_path: str, page_number: int) -> List[Dict[str, Any]]:
    """
    Detects visual figures/charts on a page, extracts bounding boxes,
    and performs OCR on embedded chart text.
    Page numbers are 1-indexed.
    """
    figure_blocks = []
    
    try:
        doc = fitz.open(doc_path)
        if page_number < 1 or page_number > len(doc):
            return []
            
        page = doc[page_number - 1]
        image_list = page.get_images(full=True)
        
        for idx, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Load image for OCR processing
            image = Image.open(io.BytesIO(image_bytes))
            chart_text = pytesseract.image_to_string(image).strip()
            
            # Find rect/bbox of image on page if available
            image_rects = page.get_image_rects(xref)
            if image_rects:
                rect = image_rects[0]
                bbox = {
                    "x0": round(rect.x0, 2),
                    "y0": round(rect.y0, 2),
                    "x1": round(rect.x1, 2),
                    "y1": round(rect.y1, 2),
                }
            else:
                bbox = {"x0": 0.0, "y0": 0.0, "x1": 0.0, "y1": 0.0}
                
            figure_blocks.append({
                "block_id": f"p{page_number}_fig{idx + 1}",
                "page_number": page_number,
                "text": f"[FIGURE/CHART] Extracted text: {chart_text}" if chart_text else "[FIGURE/CHART]",
                "block_type": "figure",
                "bbox": bbox,
                "confidence": 0.85,
                "flags": ["figure_detected", f"format_{image_ext}"]
            })
            
    except Exception as e:
        print(f"Error extracting figures on page {page_number}: {e}")
        
    return figure_blocks
