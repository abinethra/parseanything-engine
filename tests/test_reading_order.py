"""Tests for reading order sorting and header/footer tagging."""

from parseanything.schema import Page, Block, BBox, BlockType
from parseanything.reading_order import sort_blocks_reading_order, tag_headers_and_footers


def test_multi_column_sorting():
    # Left column block
    b_left = Block(block_id="b1", page_number=1, text="Left Column Text", bbox=BBox(x0=50, y0=200, x1=250, y1=250))
    # Right column block positioned higher on y-axis
    b_right = Block(block_id="b2", page_number=1, text="Right Column Text", bbox=BBox(x0=350, y0=100, x1=550, y1=150))

    sorted_blocks = sort_blocks_reading_order([b_right, b_left], page_width=600)
    
    # Left column block should come first despite having larger y0
    assert sorted_blocks[0].block_id == "b1"
    assert sorted_blocks[1].block_id == "b2"


def test_tag_headers_and_footers():
    header = Block(block_id="h1", page_number=1, text="Page 1 of 10", bbox=BBox(x0=50, y0=10, x1=100, y1=30))
    body = Block(block_id="b1", page_number=1, text="Main content body", bbox=BBox(x0=50, y0=200, x1=500, y1=300))
    footer = Block(block_id="f1", page_number=1, text="CONFIDENTIAL", bbox=BBox(x0=50, y0=750, x1=200, y1=780))

    page = Page(page_number=1, width=600, height=800, blocks=[header, body, footer])
    processed_pages = tag_headers_and_footers([page])

    assert processed_pages[0].blocks[0].block_type == BlockType.HEADER_FOOTER
    assert processed_pages[0].blocks[1].block_type == BlockType.PARAGRAPH
    assert processed_pages[0].blocks[2].block_type == BlockType.HEADER_FOOTER