import pytest
from parseanything.confidence import apply_confidence_scoring
from parseanything.equations import is_equation_block, convert_to_latex
from parseanything.models import DocumentBlock, ParsedDocument
from parseanything.router import parse

def test_equation_detection():
    assert is_equation_block("y = mx + c") == True
    assert is_equation_block("Just a normal sentence.") == False
    assert convert_to_latex("√(x)") == "$$\\sqrt{x}$$"

def test_confidence_scoring():
    blocks = [
        {"block_id": "b1", "text": "Clean standard legal paragraph content text.", "block_type": "paragraph", "confidence": 1.0, "flags": []},
        {"block_id": "b2", "text": "@#$%^&*!!@#$%^&*!!@#$%^&*!!", "block_type": "paragraph", "confidence": 1.0, "flags": []}
    ]
    scored = apply_confidence_scoring(blocks)
    assert scored[0]["confidence"] == 1.0
    assert scored[1]["confidence"] < 1.0

def test_pydantic_models():
    doc = ParsedDocument(
        status="success",
        file_name="test.pdf",
        total_blocks=1,
        blocks=[
            DocumentBlock(
                block_id="p1_b1",
                page_number=1,
                text="Sample Text",
                block_type="paragraph"
            )
        ]
    )
    assert doc.status == "success"
    assert len(doc.blocks) == 1

def test_router_nonexistent_file():
    result = parse("non_existent_file.pdf")
    assert result["status"] == "error"
    assert result["code"] == "FILE_NOT_FOUND"
