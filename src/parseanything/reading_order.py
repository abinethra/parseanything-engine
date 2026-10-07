"""Reading order reconstruction and running header/footer filtering."""

from typing import List
from parseanything.schema import Page, Block, BlockType


def sort_blocks_reading_order(blocks: List[Block], page_width: float) -> List[Block]:
    """Sorts blocks into natural reading order, handling multi-column layouts."""
    if not blocks:
        return []

    # Detect if page likely has a multi-column layout (blocks split horizontally across middle)
    mid_x = page_width / 2.0
    left_blocks = [b for b in blocks if b.bbox and b.bbox.x1 <= mid_x + 20]
    right_blocks = [b for b in blocks if b.bbox and b.bbox.x0 >= mid_x - 20]

    # If substantial content exists on both sides, sort column-by-column
    if len(left_blocks) > 0 and len(right_blocks) > 0 and (len(left_blocks) + len(right_blocks)) >= len(blocks) * 0.7:
        left_sorted = sorted(left_blocks, key=lambda b: (b.bbox.y0 if b.bbox else 0))
        right_sorted = sorted(right_blocks, key=lambda b: (b.bbox.y0 if b.bbox else 0))
        
        # Capture any full-width blocks (spanning middle) sorted by vertical position
        full_width_blocks = [b for b in blocks if b not in left_blocks and b not in right_blocks]
        full_width_sorted = sorted(full_width_blocks, key=lambda b: (b.bbox.y0 if b.bbox else 0))
        
        # Combine left column, right column, and full-width blocks by vertical position
        combined = left_sorted + right_sorted + full_width_sorted
        return sorted(combined, key=lambda b: (0 if b in left_sorted else 1, b.bbox.y0 if b.bbox else 0))

    # Standard single-column sort: top-to-bottom, left-to-right
    return sorted(blocks, key=lambda b: (b.bbox.y0 if b.bbox else 0, b.bbox.x0 if b.bbox else 0))


def tag_headers_and_footers(pages: List[Page]) -> List[Page]:
    """Identifies and tags top/bottom margin running headers and footers."""
    for page in pages:
        if not page.blocks or page.height == 0:
            continue

        top_margin_threshold = page.height * 0.08    # Top 8% of page
        bottom_margin_threshold = page.height * 0.92 # Bottom 8% of page

        for block in page.blocks:
            if not block.bbox:
                continue

            # Check if block resides entirely in top or bottom margin
            is_top = block.bbox.y1 <= top_margin_threshold
            is_bottom = block.bbox.y0 >= bottom_margin_threshold

            if is_top or is_bottom:
                block.block_type = BlockType.HEADER_FOOTER
                block.flags.append("header_footer")

    return pages