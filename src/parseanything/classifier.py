"""Semantic classification of text blocks using layout heuristics."""

import re
from typing import List
from parseanything.schema import Block, BlockType

# Bullet point patterns
BULLET_PATTERN = re.compile(r"^([\u2022\u25e6\u25aa\u25cf\u2212\-*]|\d+[\.\)])\s+")


def classify_block(block: Block, median_font_size: float = 10.0) -> Block:
    """Classifies a single text block into heading, list_item, or paragraph."""
    # Skip if already classified as header/footer or table/figure
    if block.block_type in (BlockType.HEADER_FOOTER, BlockType.TABLE, BlockType.FIGURE, BlockType.EQUATION):
        return block

    text = block.text.strip()
    if not text:
        return block

    font_size = block.metadata.get("font_size", median_font_size)
    is_bold = block.metadata.get("is_bold", False)

    # Rule 1: Bullet or numbered list item
    if BULLET_PATTERN.match(text):
        block.block_type = BlockType.LIST_ITEM
        return block

    # Rule 2: Heading based on font size or bold style + shortness
    is_significantly_larger = font_size >= median_font_size * 1.2
    is_short_title = len(text) < 120 and not text.endswith(".")

    if (is_significantly_larger or (is_bold and is_short_title)) and len(text.splitlines()) <= 2:
        block.block_type = BlockType.HEADING
        return block

    # Rule 3: Default to paragraph
    block.block_type = BlockType.PARAGRAPH
    return block


def classify_page_blocks(blocks: List[Block]) -> List[Block]:
    """Calculates median font size across a page and classifies all text blocks."""
    font_sizes = [
        b.metadata.get("font_size", 10.0)
        for b in blocks
        if b.metadata.get("font_size") is not None
    ]
    
    median_size = 10.0
    if font_sizes:
        sorted_sizes = sorted(font_sizes)
        median_size = sorted_sizes[len(sorted_sizes) // 2]

    for block in blocks:
        classify_block(block, median_font_size=median_size)

    return blocks