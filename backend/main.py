from fastapi import FastAPI, UploadFile, File
from agent.langgraph_agent import process_transcript
from models.minutes import Minutes

app = FastAPI()

@app.post("/upload_transcript")
async def upload_transcript(file: UploadFile = File(...)):
    if not file.filename.endswith('.txt'):
        return {"error": "Only .txt files are allowed."}
    content = await file.read()
    minutes = process_transcript(content.decode())
    return minutes.dict()