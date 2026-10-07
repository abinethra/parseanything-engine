"""Integration tests for ParseAnything pipeline engine."""

from parseanything.schema import Block, BlockType, Page, ParsedDocument
from parseanything.pipeline import ParseAnythingEngine


def test_document_to_markdown_conversion():
    b1 = Block(block_id="b1", page_number=1, block_type=BlockType.HEADING, text="FINANCIAL HIGHLIGHTS")
    b2 = Block(block_id="b2", page_number=1, block_type=BlockType.PARAGRAPH, text="Revenue grew 15% year over year.")
    
    page = Page(page_number=1, width=600, height=800, blocks=[b1, b2])
    doc = ParsedDocument(file_name="sample.pdf", num_pages=1, pages=[page])

    md = ParseAnythingEngine.document_to_markdown(doc)

    assert "# Document: sample.pdf" in md
    assert "## FINANCIAL HIGHLIGHTS" in md
    assert "Revenue grew 15% year over year." in md