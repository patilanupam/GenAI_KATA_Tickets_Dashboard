from utils.transcript_parser import extract_speakers
from agent.prompts import MINUTES_PROMPT
import requests

def process_transcript(transcript: str):
    speakers = extract_speakers(transcript)
    payload = {
        "prompt": MINUTES_PROMPT.format(transcript=transcript, speakers=speakers),
        "model": "tiny-llama/llama-2"
    }
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    return Minutes.parse_raw(response.text)