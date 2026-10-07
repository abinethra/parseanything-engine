import os
import shutil
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from parseanything.router import parse

app = FastAPI(
    title="ParseAnything Engine API",
    description="Self-hosted document ingestion engine.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "ParseAnything Engine API is online", "status": "active"}

@app.post("/parse")
async def parse_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF, DOCX, PPTX, XLSX, CSV) and receive structured JSON output.
    """
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        result = parse(temp_file_path)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "Parsing failed."))
            
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
