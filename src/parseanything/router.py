import os
from typing import Any, Dict, List
from parseanything.office import parse_docx, parse_pptx, parse_xlsx
from parseanything.table_merger import merge_cross_page_tables
from parseanything.equations import process_equation_blocks
from parseanything.confidence import apply_confidence_scoring
from parseanything.models import ParsedDocument
from parseanything.parallel import parse_pdf_parallel

def parse(file_path: str, use_parallel: bool = True) -> Dict[str, Any]:
    """
    Unified entry point for ParseAnything engine with optional concurrent page parsing.
    """
    if not os.path.exists(file_path):
        return {"status": "error", "code": "FILE_NOT_FOUND", "message": f"File '{file_path}' does not exist."}

    ext = os.path.splitext(file_path)[1].lower()
    raw_blocks = []

    try:
        if ext in [".pdf"]:
            if use_parallel:
                raw_blocks = parse_pdf_parallel(file_path)
            else:
                import fitz
                from parseanything.tables import extract_tables_from_page
                from parseanything.figures import extract_figures_from_page
                
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
                    raw_blocks.extend(extract_tables_from_page(file_path, page_num))
                    raw_blocks.extend(extract_figures_from_page(file_path, page_num))

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
        scored_blocks = apply_confidence_scoring(merged_blocks)

        # Validate with Pydantic
        document_model = ParsedDocument(
            status="success",
            file_name=os.path.basename(file_path),
            total_blocks=len(scored_blocks),
            blocks=scored_blocks
        )

        return document_model.model_dump()

    except Exception as e:
        return {"status": "error", "code": "PARSING_FAILED", "message": str(e)}
