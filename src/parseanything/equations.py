import re
from typing import Any, Dict, List

# Unicode math symbols, operators, and basic algebraic patterns
MATH_SYMBOLS_REGEX = re.compile(
    r'[\u2200-\u22FF\u2A00-\u2AFF\u2190-\u21FF]|=|'
    r'\+|\-|\*|\/|\^|\_|\±|\×|\÷|\√|\∫|\∑|\∏'
)

EQUATION_HEURISTICS = re.compile(
    r'(\b[a-zA-Z]\s*[\=\+\-\*\/]\s*[0-9a-zA-Z\(\)]+)|'
    r'(\b(sum|lim|int|sqrt|log|ln|sin|cos|tan)\b)|'
    r'(\d+\s*[\+\-\*\/\=]\s*\d+)'
)

def is_equation_block(text: str) -> bool:
    """
    Determines if a block text is a mathematical equation based on heuristics.
    """
    clean_text = text.strip() if text else ""
    if not clean_text:
        return False
    
    symbol_matches = MATH_SYMBOLS_REGEX.findall(clean_text)
    heuristic_matches = EQUATION_HEURISTICS.search(clean_text)
    
    if len(symbol_matches) >= 2 or heuristic_matches:
        return True
    return False

def convert_to_latex(text: str) -> str:
    """
    Converts plain-text mathematical expressions into basic LaTeX formatting.
    """
    latex_str = text.strip() if text else ""
    latex_str = re.sub(r'√\((.*?)\)', r'\\sqrt{\1}', latex_str)
    latex_str = re.sub(r'√(\w+)', r'\\sqrt{\1}', latex_str)
    latex_str = re.sub(r'∫', r'\\int ', latex_str)
    latex_str = re.sub(r'∑', r'\\sum ', latex_str)
    latex_str = re.sub(r'±', r'\\pm ', latex_str)
    latex_str = re.sub(r'×', r'\\times ', latex_str)
    latex_str = re.sub(r'÷', r'\\div ', latex_str)
    
    return f"$${latex_str}$$"

def process_equation_blocks(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scans document blocks, identifies equations, and updates block type and text to LaTeX.
    """
    for block in blocks:
        if block.get("block_type") in ["paragraph", "text"] and is_equation_block(block.get("text", "")):
            block["block_type"] = "equation"
            block["text"] = convert_to_latex(block["text"])
            block["flags"] = block.get("flags", []) + ["equation_detected"]
            block["confidence"] = 0.90
            
    return blocks
