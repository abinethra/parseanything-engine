"""Reading order utilities."""

def sort_blocks_in_reading_order(blocks):
    if not blocks:
        return []
    def get_y(b):
        if isinstance(b, dict):
            return b.get("bbox", [0, 0, 0, 0])[1]
        return getattr(b, "y0", getattr(b, "top", 0))
    return sorted(blocks, key=get_y)

def tag_headers_and_footers(page, height=None):
    blocks = getattr(page, "blocks", page if isinstance(page, (list, tuple)) else [page])
    page_height = height or getattr(page, "height", None) or 1000
    for block in blocks:
        if isinstance(block, dict):
            bbox = block.get("bbox", [0, 0, 0, 0])
            y0, y1 = bbox[1], bbox[3]
        else:
            y0 = getattr(block, "y0", getattr(block, "top", 0))
            y1 = getattr(block, "y1", getattr(block, "bottom", 0))
        if y0 < page_height * 0.08:
            if hasattr(block, "type"):
                setattr(block, "type", "header")
            elif isinstance(block, dict):
                block["type"] = "header"
        elif y1 > page_height * 0.92:
            if hasattr(block, "type"):
                setattr(block, "type", "footer")
            elif isinstance(block, dict):
                block["type"] = "footer"
    return blocks

def detect_headers_footers(page, height=None):
    return tag_headers_and_footers(page, height=height)
