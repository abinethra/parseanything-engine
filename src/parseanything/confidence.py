from typing import Any, Dict, List

def calculate_block_confidence(block: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates block attributes and text characteristics to score parsing confidence
    and assign diagnostic ambiguity flags.
    """
    text = block.get("text", "")
    block_type = block.get("block_type", "paragraph")
    flags = block.get("flags", [])
    
    score = block.get("confidence", 1.0)
    new_flags = list(flags)

    # Flag low text length or empty blocks
    if not text.strip():
        score = 0.0
        if "empty_block" not in new_flags:
            new_flags.append("empty_block")
    
    # Flag potential OCR noise (high proportion of non-alphanumeric chars)
    elif len(text) > 10:
        non_alpha = sum(1 for c in text if not c.isalnum() and not c.isspace())
        ratio = non_alpha / len(text)
        if ratio > 0.35 and block_type != "table" and "equation" not in block_type:
            score -= 0.25
            if "potential_ocr_noise" not in new_flags:
                new_flags.append("potential_ocr_noise")

    # Flag table formatting ambiguities
    if block_type == "table":
        if "---" not in text:
            score -= 0.15
            if "malformed_table_headers" not in new_flags:
                new_flags.append("malformed_table_headers")

    # Flag OCR fallback extractions
    if "ocr_extracted" in new_flags:
        score = min(score, 0.75)
        if "requires_manual_review" not in new_flags and score < 0.70:
            new_flags.append("requires_manual_review")

    # Clamp confidence between 0.0 and 1.0
    final_score = round(max(0.0, min(1.0, score)), 2)

    block["confidence"] = final_score
    block["flags"] = new_flags
    return block


def apply_confidence_scoring(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Applies confidence scoring and ambiguity flagging across all extracted blocks.
    """
    return [calculate_block_confidence(block) for block in blocks]
