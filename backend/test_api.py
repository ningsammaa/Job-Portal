from fastapi import FastAPI, UploadFile, File, Form
import uvicorn
import os
from database.db_connection import init_database
from ai.ai_service import ai_service

app = FastAPI(title="AI Resume Parser API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print("🚀 Initializing AI Test API...")
    init_database()

@app.get("/")
async def root():
    return {"message": "AI Test API - Data & AI Module", "status": "active"}

@app.post("/test/parse-resume")
async def test_parse_resume(
    user_id: int = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save uploaded file
        file_path = f"uploads/test_{user_id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Test AI processing
        success, message = ai_service.process_resume(user_id, file_path)
        
        return {
            "success": success,
            "message": message,
            "file_processed": file_path
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/test/candidates/{job_id}")
async def test_get_candidates(job_id: int):
    """Test endpoint for candidate matching."""
    success, candidates = ai_service.get_recommended_candidates(job_id)
    return {
        "success": success,
        "job_id": job_id,
        "candidates": candidates if success else []
    }

@app.get("/test/database-status")
async def test_database_status():
    try:
        from database.db_connection import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Count records in each table
        tables = ['Users', 'Jobs', 'Resumes', 'Applications']
        counts = {}
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            counts[table] = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            "success": True,
            "database_status": "connected",
            "record_counts": counts
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("Starting AI Test API on http://localhost:8000")
    print("Available endpoints:")
    print("  GET  / - API status")
    print("  POST /test/parse-resume - Test resume parsing")
    print("  GET  /test/candidates/{job_id} - Test candidate matching")
    print("  GET  /test/database-status - Check database")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)