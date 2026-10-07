"""Schema definitions and data models for ParseAnything engine."""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ParseError(Exception):
    """Custom exception raised when document parsing or format detection fails."""
    pass


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    detail: Optional[str] = None


class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    LIST_ITEM = "list_item"
    TABLE = "table"
    HEADER = "header"
    FOOTER = "footer"


class BBox(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float


class Block(BaseModel):
    block_id: str
    page_number: int
    text: str
    block_type: BlockType = BlockType.PARAGRAPH
    bbox: BBox = Field(default_factory=lambda: BBox(x0=0.0, y0=0.0, x1=0.0, y1=0.0))
    flags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Page(BaseModel):
    page_number: int
    width: float
    height: float
    blocks: List[Block] = Field(default_factory=list)
    is_scanned: bool = False


class ParsedDocument(BaseModel):
    file_name: str
    file_type: str = "pdf"
    num_pages: int
    pages: List[Page] = Field(default_factory=list)