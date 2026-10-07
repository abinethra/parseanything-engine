"""Tests for table parser and Markdown converter."""

from parseanything.table_parser import table_to_markdown


def test_table_to_markdown_formatting():
    raw_table = [
        ["Line Item", "Q1 2024", "Q2 2024"],
        ["Revenue", "$100M", "$120M"],
        ["EBITDA", "$25M", "$30M"]
    ]

    md_output = table_to_markdown(raw_table)

    assert "| Line Item | Q1 2024 | Q2 2024 |" in md_output
    assert "| --- | --- | --- |" in md_output
    assert "| Revenue | $100M | $120M |" in md_output
    assert "| EBITDA | $25M | $30M |" in md_output


def test_empty_table_to_markdown():
    assert table_to_markdown([]) == ""
    assert table_to_markdown([[]]) == ""