"""Table extraction module using pdfplumber."""

import pdfplumber
from typing import List, Dict, Any
from parseanything.schema import Block, BlockType, BBox


def table_to_markdown(table_data: List[List[Any]]) -> str:
    """Converts a 2D list of table cells into a clean Markdown table string."""
    if not table_data or not table_data[0]:
        return ""

    # Replace None values with empty string and remove line breaks within cells
    cleaned_rows = []
    for row in table_data:
        cleaned_row = [str(cell or "").replace("\n", " ").strip() for cell in row]
        cleaned_rows.append(cleaned_row)

    if not cleaned_rows:
        return ""

    headers = cleaned_rows[0]
    md_lines = []
    
    # Header row
    md_lines.append("| " + " | ".join(headers) + " |")
    # Separator row
    md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    # Data rows
    for row in cleaned_rows[1:]:
        # Pad row if columns don't match header length
        while len(row) < len(headers):
            row.append("")
        md_lines.append("| " + " | ".join(row[:len(headers)]) + " |")

    return "\n".join(md_lines)


def extract_tables_from_pdf(file_path: str, page_number: int) -> List[Block]:
    """Extracts tables from a specific page in a PDF using pdfplumber."""
    blocks: List[Block] = []

    try:
        with pdfplumber.open(file_path) as pdf:
            if page_number > len(pdf.pages):
                return blocks

            pdf_page = pdf.pages[page_number - 1]
            tables = pdf_page.find_tables()

            for t_idx, table in enumerate(tables):
                extracted_data = table.extract()
                if not extracted_data:
                    continue

                md_text = table_to_markdown(extracted_data)
                if not md_text:
                    continue

                x0, y0, x1, y1 = table.bbox
                bbox = BBox(
                    x0=round(float(x0), 2),
                    y0=round(float(y0), 2),
                    x1=round(float(x1), 2),
                    y1=round(float(y1), 2)
                )

                block = Block(
                    block_id=f"p{page_number}_tbl{t_idx + 1}",
                    block_type=BlockType.TABLE,
                    text=md_text,
                    page_number=page_number,
                    bbox=bbox,
                    confidence=0.95,
                    metadata={
                        "raw_table": extracted_data,
                        "num_rows": len(extracted_data),
                        "num_cols": len(extracted_data[0]) if extracted_data else 0
                    }
                )
                blocks.append(block)
    except Exception:
        # Fallback cleanly if pdfplumber encounters an error on this page
        pass

    return blocks