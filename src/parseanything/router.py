import os
from typing import Any, Dict, List
from parseanything.office import parse_docx, parse_pptx, parse_xlsx
from parseanything.tables import extract_tables_from_page
from parseanything.table_merger import merge_cross_page_tables
from parseanything.equations import process_equation_blocks
from parseanything.figures import extract_figures_from_page
from parseanything.confidence import apply_confidence_scoring
import fitz

def parse(file_path: str) -> Dict[str, Any]:
    """
    Unified entry point for ParseAnything engine.
    Detects file type, routes to extractors, applies math/table merging,
    calculates confidence scores, and returns a structured document payload.
    """
    if not os.path.exists(file_path):
        return {"status": "error", "code": "FILE_NOT_FOUND", "message": f"File '{file_path}' does not exist."}

    ext = os.path.splitext(file_path)[1].lower()
    raw_blocks = []

    try:
        if ext in [".pdf"]:
            doc = fitz.open(file_path)
            for page_num in range(1, len(doc) + 1):
                page = doc[page_num - 1]
                text = page.get_text()
                if text.strip():
                    raw_blocks.append({
                        "block_id": f"p{page_num}_b1",
                        "page_number": page_num,
                        "text": text.strip(),
                        "block_type": "paragraph",
                        "bbox": {"x0": 0.0, "y0": 0.0, "x1": 0.0, "y1": 0.0},
                        "confidence": 1.0,
                        "flags": []
                    })
                
                # Table Extraction
                page_table_blocks = extract_tables_from_page(file_path, page_num)
                # Figure Detection
                page_figure_blocks = extract_figures_from_page(file_path, page_num)
                
                raw_blocks.extend(page_table_blocks)
                raw_blocks.extend(page_figure_blocks)

        elif ext in [".docx"]:
            raw_blocks = parse_docx(file_path)
        elif ext in [".pptx"]:
            raw_blocks = parse_pptx(file_path)
        elif ext in [".xlsx", ".csv"]:
            raw_blocks = parse_xlsx(file_path)
        else:
            return {"status": "error", "code": "UNSUPPORTED_FORMAT", "message": f"Extension '{ext}' is not supported."}

        # Post-Processing Pipeline
        blocks_with_math = process_equation_blocks(raw_blocks)
        merged_blocks = merge_cross_page_tables(blocks_with_math)
        final_blocks = apply_confidence_scoring(merged_blocks)

        return {
            "status": "success",
            "file_name": os.path.basename(file_path),
            "total_blocks": len(final_blocks),
            "blocks": final_blocks
        }

    except Exception as e:
        return {"status": "error", "code": "PARSING_FAILED", "message": str(e)}
