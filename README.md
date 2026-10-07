# ⚡ ParseAnything Engine

> **Enterprise Multimodal Document Parsing & Ingestion Infrastructure**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/tests-21%20passed-brightgreen.svg)]()

**ParseAnything Engine** is a high-performance, unified document parsing and extraction framework built in Python. Designed to bridge the gap between unstructured multi-format files and structured AI/ML data pipelines, the engine ingests **PDF, DOCX, PPTX, XLSX, CSV, and MSG** files, standardizes their contents into a single Pydantic schema, and serves them via a FastAPI REST endpoint alongside an interactive Streamlit management dashboard.

---

## 🌟 Key Features

* **Unified Schema Standardization**: Converts all supported formats into a single, structured Pydantic data model (`ParsedDocument` & `DocumentBlock`).
* **Multimodal Support**:
  * 📄 **PDF**: Layout block detection, reading-order extraction, and automatic Tesseract OCR fallback for scanned pages.
  * 📝 **DOCX / PPTX**: Hierarchical section, heading, slide, shape, and table extraction.
  * 📊 **XLSX / CSV**: Row-column tabular data serialization into structured text blocks.
  * ✉️ **MSG**: Email body, header metadata, and attachment extraction.
* **Fast & Resilient**: Execution speed averaging `< 0.25s` per standard document with strict, standardized error handling (`UNSUPPORTED_FORMAT`, `CORRUPTED_FILE`, `FILE_NOT_FOUND`).
* **Interactive Dashboard**: Modern Streamlit Bento Grid UI featuring live document ingestion, JSON/Markdown previewers, and persistent session analytics.

---

## 🏗️ System Architecture

```text
                          [ Client Request / Streamlit UI ]
                                         │
                                         ▼
                          [ FastAPI REST Engine (/parse) ]
                                         │
                                         ▼
                       [ ParseAnything Unified Router ]
                                         │
     ┌──────────────┬──────────────┬─────┴──────────┬──────────────┬──────────────┐
     ▼              ▼              ▼                ▼              ▼              ▼
 [PDF Parser]  [DOCX Parser]  [PPTX Parser]    [XLSX Parser]  [CSV Parser]   [MSG Parser]
 (PyMuPDF/OCR)  (python-docx)  (python-pptx)     (openpyxl)     (pandas)      (extract-msg)
     └──────────────┴──────────────┼────────────────┴──────────────┴──────────────┘
                                   │
                                   ▼
                       [ Unified Pydantic Schema ]
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
           [ Standard JSON Output ]     [ Rendered Markdown Export ]

📁 Repository Structure
Plaintext
parseanything-engine/
├── .streamlit/                 # Streamlit theme configuration (forced light theme)
│   └── config.toml
├── parseanything/              # Core Source Package
│   ├── __init__.py
│   ├── app.py                  # FastAPI Application Server
│   ├── router.py               # Unified Document Routing Engine
│   ├── models.py               # Pydantic Schemas & Markdown Exporters
│   └── parsers/                # Format-Specific Parser Modules
│       ├── pdf_parser.py
│       ├── docx_parser.py
│       ├── pptx_parser.py
│       ├── xlsx_parser.py
│       ├── csv_parser.py
│       └── msg_parser.py
├── tests/                      # Automated Unit & Integration Tests (21 Tests)
├── app_ui.py                   # Custom Streamlit Bento Management Dashboard
├── generate_pdf.py             # PDF Overview Generator Script for Pitching/Judges
├── pyproject.toml              # Build System & Package Distribution Config
└── README.md                   # Project Documentation
🚀 Quick Start
1. Prerequisites
Ensure you have Python 3.10+ installed. Tesseract OCR is optional but recommended for scanned PDF support.

2. Installation
Clone the repository and set up a virtual environment:

Bash
git clone [https://github.com/YOUR_USERNAME/parseanything-engine.git](https://github.com/YOUR_USERNAME/parseanything-engine.git)
cd parseanything-engine

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies in editable mode
pip install -e .
🖥️ Running the Application
Option A: Start the FastAPI Backend
Run the backend engine server using Uvicorn:

Bash
python -m uvicorn parseanything.app:app --reload
API Service Base URL: http://127.0.0.1:8000

Interactive OpenAPI Swagger Docs: http://127.0.0.1:8000/docs

Option B: Start the Streamlit Dashboard UI
Launch the interactive UI dashboard:

Bash
python -m streamlit run app_ui.py
Dashboard Access: http://localhost:8501
