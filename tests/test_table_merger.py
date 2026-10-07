"""Tests for cross-page table merging."""

from parseanything.schema import Page, Block, BlockType, BBox
from parseanything.table_merger import merge_cross_page_tables


def test_cross_page_table_merging():
    raw_tbl1 = [
        ["Metric", "2023", "2024"],
        ["Revenue", "$500M", "$620M"]
    ]
    raw_tbl2 = [
        ["Metric", "2023", "2024"],
        ["Net Income", "$80M", "$105M"]
    ]

    b1 = Block(
        block_id="p1_tbl1", page_number=1, block_type=BlockType.TABLE,
        text="| Metric | 2023 | 2024 |\n| --- | --- | --- |\n| Revenue | $500M | $620M |",
        bbox=BBox(x0=50, y0=500, x1=550, y1=700),
        metadata={"raw_table": raw_tbl1}
    )

    b2 = Block(
        block_id="p2_tbl1", page_number=2, block_type=BlockType.TABLE,
        text="| Metric | 2023 | 2024 |\n| --- | --- | --- |\n| Net Income | $80M | $105M |",
        bbox=BBox(x0=50, y0=50, x1=550, y1=200),
        metadata={"raw_table": raw_tbl2}
    )

    page1 = Page(page_number=1, width=600, height=800, blocks=[b1])
    page2 = Page(page_number=2, width=600, height=800, blocks=[b2])

    processed_pages = merge_cross_page_tables([page1, page2])

    # Check that second page table was merged into first page
    assert len(processed_pages[0].blocks) == 1
    assert len(processed_pages[1].blocks) == 0
    assert "Net Income" in processed_pages[0].blocks[0].text
    assert "merged_cross_page" in processed_pages[0].blocks[0].flags