"""FastAPI REST service for ParseAnything engine."""

import os
import tempfile
from typing import Dict

from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from parseanything.exceptions import ErrorCode, ParseError
from parseanything.pipeline import ParseAnythingEngine
from parseanything.schema import ErrorResponse, ParsedDocument

app = FastAPI(
    title="ParseAnything Engine API",
    description="REST API for parsing PDFs, images, tables, and structured documents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ParseAnythingEngine()


@app.exception_handler(ParseError)
async def parse_error_handler(request, exc: ParseError) -> JSONResponse:
    status_code = status.HTTP_400_BAD_REQUEST
    if exc.code == ErrorCode.FILE_NOT_FOUND:
        status_code = status.HTTP_404_NOT_FOUND
    elif exc.code == ErrorCode.UNSUPPORTED_FORMAT:
        status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    error_content = ErrorResponse(
        status="error",
        code=exc.code.value if hasattr(exc.code, "value") else str(exc.code),
        message=str(exc),
    ).model_dump()

    return JSONResponse(status_code=status_code, content=error_content)


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception) -> JSONResponse:
    error_content = ErrorResponse(
        status="error",
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred during document parsing.",
        detail=str(exc),
    ).model_dump()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_content,
    )


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "parseanything-engine"}


@app.post(
    "/v1/parse",
    response_model=ParsedDocument,
    status_code=status.HTTP_200_OK,
)
async def parse_document(
    file: UploadFile = File(..., description="Target document/image file to parse"),
    extract_tables: bool = Form(True, description="Enable table detection and extraction"),
    ocr_fallback: bool = Form(True, description="Enable OCR fallback for scanned pages"),
) -> ParsedDocument:
    filename = file.filename or "uploaded_file"
    ext = os.path.splitext(filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        temp_path = temp_file.name
        content = await file.read()
        temp_file.write(content)

    try:
        parsed_doc = engine.parse(
            file_path=temp_path,
            extract_tables=extract_tables,
            ocr_fallback=ocr_fallback,
        )
        parsed_doc.file_name = filename
        return parsed_doc
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
