"""Reading order and layout analysis module."""

from typing import List
from parseanything.schema import Page, Block, BlockType


def sort_blocks_reading_order(blocks: List[Block], page_width: float = 600.0) -> List[Block]:
    """Sorts blocks in multi-column reading order (left-to-right columns, top-to-bottom)."""
    midpoint = page_width / 2.0
    left_col = [b for b in blocks if (b.bbox.x0 + b.bbox.x1) / 2.0 < midpoint]
    right_col = [b for b in blocks if (b.bbox.x0 + b.bbox.x1) / 2.0 >= midpoint]

    left_col.sort(key=lambda b: (b.bbox.y0, b.bbox.x0))
    right_col.sort(key=lambda b: (b.bbox.y0, b.bbox.x0))

    return left_col + right_col


# Alias to maintain compatibility with pipeline imports
sort_blocks_in_reading_order = sort_blocks_reading_order


def tag_headers_and_footers(pages: List[Page], header_threshold: float = 50.0, footer_offset: float = 50.0) -> List[Page]:
    """Tags blocks appearing near top or bottom page margins as HEADER_FOOTER."""
    for page in pages:
        for block in page.blocks:
            if block.bbox.y0 <= header_threshold or block.bbox.y1 >= (page.height - footer_offset):
                block.block_type = BlockType.HEADER_FOOTER
    return pages
