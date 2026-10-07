from typing import Any, Dict, List, Optional
import pdfplumber

def extract_tables_from_page(pdf_path: str, page_number: int) -> List[Dict[str, Any]]:
    extracted_tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if page_number < 1 or page_number > len(pdf.pages):
                return []
            page = pdf.pages[page_number - 1]
            tables = page.find_tables()
            for idx, table in enumerate(tables):
                data = table.extract()
                if not data:
                    continue
                markdown_lines = []
                headers = [str(cell or "").strip() for cell in data[0]]
                markdown_lines.append("| " + " | ".join(headers) + " |")
                markdown_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                for row in data[1:]:
                    cells = [str(cell or "").strip().replace("\n", " ") for cell in row]
                    markdown_lines.append("| " + " | ".join(cells) + " |")
                markdown_text = "\n".join(markdown_lines)
                bbox = list(table.bbox)
                extracted_tables.append({
                    "block_id": f"p{page_number}_t{idx + 1}",
                    "page_number": page_number,
                    "text": markdown_text,
                    "block_type": "table",
                    "bbox": {
                        "x0": round(bbox[0], 2),
                        "y0": round(bbox[1], 2),
                        "x1": round(bbox[2], 2),
                        "y1": round(bbox[3], 2),
                    },
                    "confidence": 0.95,
                    "rows": data,
                    "flags": []
                })
    except Exception as e:
        print(f"Error extracting tables: {e}")
    return extracted_tables
