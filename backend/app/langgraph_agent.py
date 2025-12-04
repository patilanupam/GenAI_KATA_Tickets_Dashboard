from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
import httpx

from .config import settings
from .services.text_cleaner import clean_transcript
from .services.speaker_parser import parse_speakers

# ----------- State Definition -----------

class MinutesState(TypedDict, total=False):
    raw_transcript: str
    cleaned_transcript: str
    speaker_segments: List[Dict[str, Any]]
    structured_minutes: Dict[str, Any]
    llm_trace: Dict[str, Any]

# ----------- Helper: Ollama LLM Call -----------

async def call_ollama(prompt: str) -> str:
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": prompt,
        "temperature": 0.2,
        "top_p": 0.95,
        "repeat_penalty": 1.1,
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.OLLAMA_HOST}/api/generate", json=payload
        )
        response.raise_for_status()
        # ollama returns streaming chunks; we accumulate to string
        output = ""
        for chunk in response.iter_lines():
            if chunk:
                data = httpx.Response(200, content=chunk).json()
                output += data.get("response", "")
        return output.strip()

# ----------- Node Definitions -----------

async def node_clean_transcript(state: MinutesState) -> MinutesState:
    cleaned = clean_transcript(state["raw_transcript"])
    return {**state, "cleaned_transcript": cleaned}

async def node_parse_speakers(state: MinutesState) -> MinutesState:
    segments = parse_speakers(state["cleaned_transcript"])
    return {**state, "speaker_segments": segments}

def build_structuring_prompt(segments: List[Dict[str, Any]]) -> str:
    transcript_blocks = "\n".join(
        f"[{seg['speaker']}] {seg['text']}" for seg in segments
    )
    return f"""
You are an enterprise meeting-minutes generator. Analyze the meeting transcript and produce structured minutes in JSON.

Transcript:
{transcript_blocks}

Return JSON with keys:
- executive_summary: bullet list capturing main points (max 5 bullets).
- action_items: list of objects with fields:
    description, owner (speaker/person), due_date (if inferable), priority (High/Medium/Low).
- decisions: list with {{"decision", "rationale", "owner"}}
- risks: list with {{"risk", "impact", "mitigation", "owner"}}
- speaker_spotlight: array summarizing each speaker: {{"speaker", "speaking_time_estimate", "notable_points"}}
- metadata: include {{"transcript_length_words", "detected_date" (if mentioned), "confidence_notes"}}

Use professional tone, infer logical owners/priorities if possible, else "Unassigned".
JSON only, no markdown.
    """.strip()

async def node_llm_minutes(state: MinutesState) -> MinutesState:
    prompt = build_structuring_prompt(state["speaker_segments"])
    raw_response = await call_ollama(prompt)
    return {**state, "structured_minutes": raw_response, "llm_trace": {"prompt": prompt}}

async def node_validate_structure(state: MinutesState) -> MinutesState:
    # Optionally validate JSON, ensure all keys exist
    import json
    try:
        parsed = json.loads(state["structured_minutes"])
    except json.JSONDecodeError as exc:
        parsed = {
            "executive_summary": ["LLM parsing error: " + str(exc)],
            "action_items": [],
            "decisions": [],
            "risks": [],
            "speaker_spotlight": [],
            "metadata": {"confidence_notes": "Failed to parse JSON output from LLM."},
        }
    return {**state, "structured_minutes": parsed}

# ----------- Graph Construction -----------

graph_builder = StateGraph(MinutesState)

graph_builder.add_node("clean_transcript", node_clean_transcript)
graph_builder.add_node("parse_speakers", node_parse_speakers)
graph_builder.add_node("llm_minutes", node_llm_minutes)
graph_builder.add_node("validate_structure", node_validate_structure)

graph_builder.add_edge(START, "clean_transcript")
graph_builder.add_edge("clean_transcript", "parse_speakers")
graph_builder.add_edge("parse_speakers", "llm_minutes")
graph_builder.add_edge("llm_minutes", "validate_structure")
graph_builder.add_edge("validate_structure", END)

minutes_graph = graph_builder.compile()

# ----------- Entry Point -----------

async def generate_minutes(transcript_text: str) -> Dict[str, Any]:
    initial_state: MinutesState = {"raw_transcript": transcript_text}
    final_state = await minutes_graph.ainvoke(initial_state)
    return {
        "minutes": final_state["structured_minutes"],
        "llm_trace": final_state.get("llm_trace"),
    }