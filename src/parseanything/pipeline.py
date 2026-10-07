"""Master pipeline orchestrator for ParseAnything engine."""

import os
from typing import List
from parseanything.schema import ParsedDocument, Page, Block, BlockType
from parseanything.pdf_parser import extract_digital_pdf
from parseanything.reading_order import tag_headers_and_footers as detect_headers_footers
from parseanything.classifier import classify_page_blocks
from parseanything.reading_order import sort_blocks_in_reading_order
from parseanything.table_parser import extract_tables_from_pdf
from parseanything.table_merger import merge_cross_page_tables
from parseanything.ocr_engine import process_scanned_image_file


class ParseAnythingEngine:
    """Master engine orchestrating multi-format document parsing."""

    def __init__(self, use_ocr: bool = True):
        self.use_ocr = use_ocr

    def parse_file(self, file_path: str) -> ParsedDocument:
        """Parses a PDF or image file into a structured ParsedDocument."""
        ext = os.path.splitext(file_path)[1].lower()

        if ext in (".png", ".jpg", ".jpeg", ".tiff", ".bmp"):
            page = process_scanned_image_file(file_path)
            return ParsedDocument(
                file_name=os.path.basename(file_path),
                file_type=ext.lstrip("."),
                num_pages=1,
                pages=[page]
            )

        if ext == ".pdf":
            return self._parse_pdf(file_path)

        raise ValueError(f"Unsupported file format: {ext}")

    def _parse_pdf(self, file_path: str) -> ParsedDocument:
        raw_pages = extract_digital_pdf(file_path)
        pages: List[Page] = []

        for p in raw_pages:
            page_num = p.page_number
            width = p.width
            height = p.height
            text_blocks: List[Block] = p.blocks

            table_blocks = extract_tables_from_pdf(file_path, page_num)
            all_blocks = text_blocks + table_blocks

            all_blocks = detect_headers_footers(all_blocks, page_height=height)
            all_blocks = [b for b in all_blocks if b.block_type not in (BlockType.HEADER, BlockType.FOOTER)]

            all_blocks = classify_page_blocks(all_blocks)
            all_blocks = sort_blocks_in_reading_order(all_blocks)

            pages.append(Page(
                page_number=page_num,
                width=width,
                height=height,
                blocks=all_blocks,
                is_scanned=p.is_scanned
            ))

        pages = merge_cross_page_tables(pages)

        return ParsedDocument(
            file_name=os.path.basename(file_path),
            file_type="pdf",
            num_pages=len(pages),
            pages=pages
        )

    @staticmethod
    def document_to_markdown(doc: ParsedDocument) -> str:
        """Converts a ParsedDocument into a clean, LLM-ready Markdown string."""
        md_lines = [f"# Document: {doc.file_name}\n"]

        for page in doc.pages:
            md_lines.append(f"--- Page {page.page_number} ---\n")
            for block in page.blocks:
                if block.block_type == BlockType.HEADING:
                    md_lines.append(f"\n## {block.text}\n")
                elif block.block_type == BlockType.LIST_ITEM:
                    md_lines.append(f"{block.text}")
                elif block.block_type == BlockType.TABLE:
                    md_lines.append(f"\n{block.text}\n")
                else:
                    md_lines.append(f"\n{block.text}\n")

        return "\n".join(md_lines)