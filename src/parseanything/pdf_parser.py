"""PDF parsing module using PyMuPDF (fitz)."""

import fitz  # PyMuPDF
from typing import List
from parseanything.schema import Page, Block, BlockType, BBox


def extract_digital_pdf(file_path: str) -> List[Page]:
    """Extracts pages and text blocks with bounding boxes and metadata from a PDF file."""
    doc = fitz.open(file_path)
    pages: List[Page] = []

    for page_idx, page in enumerate(doc):
        page_num = page_idx + 1
        width = page.rect.width
        height = page.rect.height

        page_dict = page.get_text("dict")
        blocks: List[Block] = []

        block_counter = 1
        for b in page_dict.get("blocks", []):
            if b.get("type") == 0:
                lines = b.get("lines", [])
                full_text_lines = []
                font_sizes = []
                is_bold_flags = []

                for line in lines:
                    line_text = ""
                    for span in line.get("spans", []):
                        span_text = span.get("text", "")
                        line_text += span_text
                        font_sizes.append(span.get("size", 10.0))

                        flags = span.get("flags", 0)
                        font_name = str(span.get("font", "")).lower()
                        if (flags & 16) or ("bold" in font_name) or ("black" in font_name):
                            is_bold_flags.append(True)

                    if line_text.strip():
                        full_text_lines.append(line_text.strip())

                text_content = "\n".join(full_text_lines)
                if not text_content.strip():
                    continue

                bbox = BBox(
                    x0=round(b["bbox"][0], 2),
                    y0=round(b["bbox"][1], 2),
                    x1=round(b["bbox"][2], 2),
                    y1=round(b["bbox"][3], 2),
                )

                avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 10.0
                is_bold = any(is_bold_flags)

                block = Block(
                    block_id=f"p{page_num}_b{block_counter}",
                    block_type=BlockType.PARAGRAPH,
                    text=text_content,
                    page_number=page_num,
                    bbox=bbox,
                    metadata={
                        "font_size": round(avg_font_size, 2),
                        "is_bold": is_bold,
                    },
                )
                blocks.append(block)
                block_counter += 1

        is_scanned = len(blocks) == 0
        pages.append(Page(
            page_number=page_num,
            width=width,
            height=height,
            blocks=blocks,
            is_scanned=is_scanned,
        ))

    doc.close()
    return pages


extract_pdf_pages = extract_digital_pdf