"""
FastAPI application entry point for ClarifyMeet AI
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse, FileResponse
from pathlib import Path
from .config import settings
from .langgraph_agent import generate_minutes
from .schemas import MinutesResponse

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML"""
    frontend_file = frontend_path / "index.html"
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    return {"message": "Frontend not found", "path": str(frontend_path)}

@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "model": settings.OLLAMA_MODEL}

@app.get("/health")
async def health():
    """Alternative health check endpoint"""
    return {"status": "ok", "model": settings.OLLAMA_MODEL}

def validate_file(file: UploadFile) -> None:
    """Validate uploaded file"""
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt transcripts are accepted.")
    # Note: Size validation happens during read, FastAPI handles max size via config

@app.post(f"{settings.API_PREFIX}/analyze", response_model=MinutesResponse)
async def analyze_transcript(file: UploadFile = File(...)):
    """
    Analyze transcript and generate meeting minutes.

    Args:
        file: Uploaded transcript file (.txt format)

    Returns:
        MinutesResponse containing structured meeting minutes
    """
    validate_file(file)
    transcript_bytes = await file.read()
    try:
        transcript_text = transcript_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Transcript must be UTF-8 encoded.")

    result = await generate_minutes(transcript_text)
    return JSONResponse(content=result)

@app.post("/process")
async def process_transcript(file: UploadFile = File(...)):
    """
    Process transcript endpoint that matches frontend expectations.

    Args:
        file: Uploaded transcript file (.txt format)

    Returns:
        JSON response with structured meeting minutes
    """
    validate_file(file)
    transcript_bytes = await file.read()
    try:
        transcript_text = transcript_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Transcript must be UTF-8 encoded.")

    try:
        result = await generate_minutes(transcript_text)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

