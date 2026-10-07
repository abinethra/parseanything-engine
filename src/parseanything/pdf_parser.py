"""Digital PDF extractor using PyMuPDF (fitz)."""

import fitz  # PyMuPDF
from typing import List
from parseanything.schema import Page, Block, BlockType, BBox
from parseanything.exceptions import ParseError, ErrorCode


def extract_digital_pdf(file_path: str) -> List[Page]:
    """Extracts structured text blocks and bounding boxes from a native digital PDF."""
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise ParseError(
            code=ErrorCode.CORRUPT_FILE,
            message=f"Failed to open PDF file: {str(e)}"
        )

    pages: List[Page] = []

    for page_idx, page in enumerate(doc):
        page_num = page_idx + 1
        page_rect = page.rect
        width = float(page_rect.width)
        height = float(page_rect.height)

        # Extract structured text blocks: (x0, y0, x1, y1, "text", block_no, block_type)
        text_blocks = page.get_text("blocks")
        parsed_blocks: List[Block] = []

        for b_idx, b in enumerate(text_blocks):
            x0, y0, x1, y1, text_content, block_no, b_type = b
            text = text_content.strip()

            if not text:
                continue

            bbox = BBox(
                x0=round(float(x0), 2),
                y0=round(float(y0), 2),
                x1=round(float(x1), 2),
                y1=round(float(y1), 2)
            )

            block = Block(
                block_id=f"p{page_num}_b{b_idx + 1}",
                block_type=BlockType.PARAGRAPH,
                text=text,
                page_number=page_num,
                bbox=bbox,
                confidence=1.0,
                flags=[]
            )
            parsed_blocks.append(block)

        # Check if page is essentially scanned (contains images but zero/minimal text)
        is_scanned = len(parsed_blocks) == 0 and len(page.get_images()) > 0

        page_obj = Page(
            page_number=page_num,
            width=width,
            height=height,
            blocks=parsed_blocks,
            is_scanned=is_scanned
        )
        pages.append(page_obj)

    doc.close()
    return pages