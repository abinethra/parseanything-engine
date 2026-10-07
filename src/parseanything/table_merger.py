from typing import Any, Dict, List

def should_merge_tables(table1: Dict[str, Any], table2: Dict[str, Any]) -> bool:
    """
    Check if table2 on page N+1 is a continuation of table1 on page N.
    """
    if table2.get("page_number") != table1.get("page_number") + 1:
        return False
    
    rows1 = table1.get("rows", [])
    rows2 = table2.get("rows", [])
    
    if not rows1 or not rows2:
        return False
    
    # Check if column counts match
    col_count1 = len(rows1[0]) if rows1 else 0
    col_count2 = len(rows2[0]) if rows2 else 0
    
    return col_count1 > 0 and col_count1 == col_count2

def merge_cross_page_tables(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Iterate through blocks and merge consecutive table blocks across pages.
    """
    merged_blocks = []
    idx = 0
    
    while idx < len(blocks):
        current = blocks[idx]
        
        if current.get("block_type") == "table" and idx + 1 < len(blocks):
            nxt = blocks[idx + 1]
            if nxt.get("block_type") == "table" and should_merge_tables(current, nxt):
                # Combine table rows
                combined_rows = current.get("rows", []) + nxt.get("rows", [])
                
                # Rebuild merged Markdown
                markdown_lines = []
                headers = [str(cell or "").strip() for cell in combined_rows[0]]
                markdown_lines.append("| " + " | ".join(headers) + " |")
                markdown_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                
                for row in combined_rows[1:]:
                    cells = [str(cell or "").strip().replace("\n", " ") for cell in row]
                    markdown_lines.append("| " + " | ".join(cells) + " |")
                
                merged_table = current.copy()
                merged_table["text"] = "\n".join(markdown_lines)
                merged_table["rows"] = combined_rows
                merged_table["flags"] = current.get("flags", []) + ["merged_cross_page"]
                
                merged_blocks.append(merged_table)
                idx += 2  # Skip the next table as it was merged
                continue
        
        merged_blocks.append(current)
        idx += 1
        
    return merged_blocks
