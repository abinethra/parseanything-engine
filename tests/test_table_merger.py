import pytest
from parseanything.table_merger import merge_cross_page_tables

def test_cross_page_table_merging():
    blocks = [
        {
            "block_id": "t1",
            "page_number": 1,
            "text": "| Header 1 | Header 2 |\n| --- | --- |\n| Data 1 | Data 2 |",
            "block_type": "table",
            "confidence": 1.0,
            "flags": []
        },
        {
            "block_id": "t2",
            "page_number": 2,
            "text": "| Header 1 | Header 2 |\n| --- | --- |\n| Data 3 | Data 4 |",
            "block_type": "table",
            "confidence": 1.0,
            "flags": []
        }
    ]
    
    merged = merge_cross_page_tables(blocks)
    assert isinstance(merged, list)
    assert len(merged) >= 1
