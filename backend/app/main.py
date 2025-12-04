"""
FastAPI application entry point for ClarifyMeet AI
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
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

@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "model": settings.OLLAMA_MODEL}

def validate_file(file: UploadFile) -> None:
    """Validate uploaded file"""
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt transcripts are accepted.")
    size = file.spool_max_size
    if size and size > settings.MAX_TRANSCRIPT_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large.")

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

