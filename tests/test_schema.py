"""Tests for Pydantic data schemas."""

from parseanything.schema import BBox, Block, BlockType, ParsedDocument, ErrorResponse


def test_bbox_creation():
    bbox = BBox(x0=10.0, y0=20.0, x1=100.0, y1=200.0)
    assert bbox.x0 == 10.0
    assert bbox.x1 == 100.0


def test_block_defaults():
    block = Block(block_id="p1_b1", page_number=1, text="Hello World")
    assert block.block_type == BlockType.PARAGRAPH
    assert block.confidence == 1.0
    assert block.flags == []


def test_error_response():
    err = ErrorResponse(code="UNSUPPORTED_FORMAT", message="File extension .xyz is not supported")
    assert err.status == "error"
    assert err.code == "UNSUPPORTED_FORMAT"