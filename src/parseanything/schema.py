"""Data schemas for ParseAnything document elements and parsing results."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BlockType(str, Enum):
    """Supported semantic block types."""
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    TABLE = "table"
    FIGURE = "figure"
    EQUATION = "equation"
    HEADER_FOOTER = "header_footer"
    UNKNOWN = "unknown"


class BBox(BaseModel):
    """Bounding box coordinates on a page (x0, y0, x1, y1 in points/pixels)."""
    x0: float = Field(..., description="Top-left x coordinate")
    y0: float = Field(..., description="Top-left y coordinate")
    x1: float = Field(..., description="Bottom-right x coordinate")
    y1: float = Field(..., description="Bottom-right y coordinate")


class Block(BaseModel):
    """A single semantic block of content extracted from a document."""
    block_id: str = Field(..., description="Unique identifier for the block")
    block_type: BlockType = Field(default=BlockType.PARAGRAPH)
    text: str = Field(default="", description="Cleaned extracted text content")
    page_number: int = Field(..., description="1-based page index")
    bbox: Optional[BBox] = Field(default=None, description="Bounding box on the page")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    flags: List[str] = Field(default_factory=list, description="Quality or ambiguity flags (e.g., 'low_confidence')")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata (e.g., font size, row/col info)")


class Page(BaseModel):
    """Represents a single processed page."""
    page_number: int = Field(..., description="1-based page index")
    width: float = Field(..., description="Page width in points/pixels")
    height: float = Field(..., description="Page height in points/pixels")
    blocks: List[Block] = Field(default_factory=list, description="Ordered semantic blocks on this page")
    is_scanned: bool = Field(default=False, description="True if page was identified as scanned/image-only")


class ParsedDocument(BaseModel):
    """The master output object for a parsed document."""
    file_name: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="Detected file extension or MIME category")
    total_pages: int = Field(default=0, description="Total page count")
    pages: List[Page] = Field(default_factory=list, description="Extracted pages")
    reading_order_blocks: List[Block] = Field(default_factory=list, description="Global re-ordered list of all blocks")
    processing_time_seconds: float = Field(default=0.0, description="Total execution time in seconds")


class ErrorResponse(BaseModel):
    """Standard error response format for failed parses or invalid files."""
    status: str = Field(default="error")
    code: str = Field(..., description="Standardized error code e.g. UNSUPPORTED_FORMAT")
    message: str = Field(..., description="Human-readable error explanation")
    details: Optional[Dict[str, Any]] = Field(default=None)