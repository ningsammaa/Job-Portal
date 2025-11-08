from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from ai.resume_parser import ResumeParser

app = FastAPI(title="AI Resume Parser API", version="1.0.0")
parser = ResumeParser()

@app.get("/")
async def root():
    return {
        "message": "AI Resume Parser API",
        "status": "active",
        "endpoints": {
            "parse_resume": "/parse-resume (POST)",
            "docs": "/docs"
        }
    }

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save uploaded file
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Parse the resume
        extracted_text = parser.extract_text(file_path)
        
        return {
            "filename": file.filename,
            "extracted_text": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            "size": len(content)
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)