import concurrent.futures
import os
from typing import Any, Dict, List
from parseanything.tables import extract_tables_from_page
from parseanything.figures import extract_figures_from_page
import fitz

def _process_single_page(args: tuple) -> List[Dict[str, Any]]:
    """Helper worker function to process a single PDF page in parallel."""
    file_path, page_num = args
    page_blocks = []
    
    try:
        doc = fitz.open(file_path)
        page = doc[page_num - 1]
        text = page.get_text()
        
        if text.strip():
            page_blocks.append({
                "block_id": f"p{page_num}_b1",
                "page_number": page_num,
                "text": text.strip(),
                "block_type": "paragraph",
                "bbox": {"x0": 0.0, "y0": 0.0, "x1": 0.0, "y1": 0.0},
                "confidence": 1.0,
                "flags": []
            })
            
        page_table_blocks = extract_tables_from_page(file_path, page_num)
        page_figure_blocks = extract_figures_from_page(file_path, page_num)
        
        page_blocks.extend(page_table_blocks)
        page_blocks.extend(page_figure_blocks)
    except Exception as e:
        print(f"Error processing page {page_num} in parallel worker: {e}")
        
    return page_blocks

def parse_pdf_parallel(file_path: str, max_workers: int = 4) -> List[Dict[str, Any]]:
    """Extracts blocks from PDF pages concurrently using process/thread pools."""
    doc = fitz.open(file_path)
    total_pages = len(doc)
    doc.close()
    
    page_args = [(file_path, page_num) for page_num in range(1, total_pages + 1)]
    all_blocks = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(_process_single_page, page_args)
        for page_blocks in results:
            all_blocks.extend(page_blocks)
            
    return all_blocks
