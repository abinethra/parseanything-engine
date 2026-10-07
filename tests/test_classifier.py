"""Tests for semantic block classifier."""

from parseanything.schema import Block, BlockType
from parseanything.classifier import classify_block, classify_page_blocks


def test_classify_list_item():
    block = Block(block_id="b1", page_number=1, text="• First key takeaway for investment")
    classified = classify_block(block)
    assert classified.block_type == BlockType.LIST_ITEM

    block_num = Block(block_id="b2", page_number=1, text="1. Secondary objective")
    classified_num = classify_block(block_num)
    assert classified_num.block_type == BlockType.LIST_ITEM


def test_classify_heading():
    block = Block(
        block_id="b3",
        page_number=1,
        text="EXECUTIVE SUMMARY",
        metadata={"font_size": 16.0, "is_bold": True}
    )
    classified = classify_block(block, median_font_size=10.0)
    assert classified.block_type == BlockType.HEADING


def test_classify_paragraph():
    block = Block(
        block_id="b4",
        page_number=1,
        text="This is a standard paragraph containing financial performance metrics.",
        metadata={"font_size": 10.0, "is_bold": False}
    )
    classified = classify_block(block, median_font_size=10.0)
    assert classified.block_type == BlockType.PARAGRAPH