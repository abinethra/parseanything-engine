"""Cross-page table detection and merging logic."""

from typing import List
from parseanything.schema import Page, Block, BlockType
from parseanything.table_parser import table_to_markdown


def should_merge_tables(tbl1: Block, tbl2: Block) -> bool:
    """Heuristic check to determine if two tables across consecutive pages should be merged."""
    if tbl1.block_type != BlockType.TABLE or tbl2.block_type != BlockType.TABLE:
        return False

    # Check if pages are consecutive
    if tbl2.page_number != tbl1.page_number + 1:
        return False

    raw1 = tbl1.metadata.get("raw_table", [])
    raw2 = tbl2.metadata.get("raw_table", [])

    if not raw1 or not raw2:
        return False

    # Check if column counts match
    cols1 = len(raw1[0]) if raw1 else 0
    cols2 = len(raw2[0]) if raw2 else 0

    if cols1 > 0 and cols1 == cols2:
        return True

    return False


def merge_cross_page_tables(pages: List[Page]) -> List[Page]:
    """Iterates across pages and merges eligible cross-page tables."""
    if len(pages) < 2:
        return pages

    for i in range(len(pages) - 1):
        p1 = pages[i]
        p2 = pages[i + 1]

        if not p1.blocks or not p2.blocks:
            continue

        # Look for table at end of page 1 and table at start of page 2
        p1_tables = [b for b in p1.blocks if b.block_type == BlockType.TABLE]
        p2_tables = [b for b in p2.blocks if b.block_type == BlockType.TABLE]

        if not p1_tables or not p2_tables:
            continue

        last_tbl_p1 = p1_tables[-1]
        first_tbl_p2 = p2_tables[0]

        if should_merge_tables(last_tbl_p1, first_tbl_p2):
            raw1 = last_tbl_p1.metadata.get("raw_table", [])
            raw2 = first_tbl_p2.metadata.get("raw_table", [])

            # Merge raw cell arrays (skipping redundant header in second table if identical)
            if raw1 and raw2 and raw1[0] == raw2[0]:
                merged_raw = raw1 + raw2[1:]
            else:
                merged_raw = raw1 + raw2

            merged_md = table_to_markdown(merged_raw)

            # Update first table block with merged data
            last_tbl_p1.text = merged_md
            last_tbl_p1.metadata["raw_table"] = merged_raw
            last_tbl_p1.metadata["num_rows"] = len(merged_raw)
            last_tbl_p1.flags.append("merged_cross_page")

            # Remove merged table block from second page
            p2.blocks.remove(first_tbl_p2)

    return pages