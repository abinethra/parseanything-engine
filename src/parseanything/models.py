from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    x0: float = 0.0
    y0: float = 0.0
    x1: float = 0.0
    y1: float = 0.0

class DocumentBlock(BaseModel):
    block_id: str
    page_number: int = 1
    text: str
    block_type: str = Field(description="paragraph, heading, table, figure, or equation")
    bbox: BoundingBox = Field(default_factory=BoundingBox)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    flags: List[str] = Field(default_factory=list)
    rows: Optional[List[List[Any]]] = None

class ParsedDocument(BaseModel):
    status: str = "success"
    file_name: str
    total_blocks: int
    blocks: List[DocumentBlock]

    def to_markdown(self) -> str:
        """Export document text blocks as unified Markdown."""
        md_lines = [f"# {self.file_name}\n"]
        for block in self.blocks:
            if block.block_type == "heading":
                md_lines.append(f"## {block.text}\n")
            elif block.block_type == "equation":
                md_lines.append(f"{block.text}\n")
            else:
                md_lines.append(f"{block.text}\n")
        return "\n".join(md_lines)
