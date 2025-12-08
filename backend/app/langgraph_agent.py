from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph
from pydantic import BaseModel
import httpx

from .config import settings
from .services.text_cleaner import clean_transcript
from .services.speaker_parser import parse_speakers
from .services.fallback_parser import parse_transcript_fallback

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
        "stream": False
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.OLLAMA_HOST}/api/generate", json=payload
        )
        response.raise_for_status()
        # Parse the JSON response
        data = response.json()
        return data.get("response", "").strip()

# ----------- Node Definitions -----------

async def node_clean_transcript(state: MinutesState) -> MinutesState:
    cleaned = clean_transcript(state["raw_transcript"])
    return {**state, "cleaned_transcript": cleaned}

async def node_parse_speakers(state: MinutesState) -> MinutesState:
    segments = parse_speakers(state["cleaned_transcript"])
    return {**state, "speaker_segments": segments}

def build_structuring_prompt(segments: List[Dict[str, Any]]) -> str:
    transcript_blocks = "\n".join(
        f"[{seg['speaker']}]: {seg['text']}" for seg in segments
    )

    # Extract all unique speakers
    speakers_list = list(set(seg['speaker'] for seg in segments))
    speakers_str = ", ".join(speakers_list)

    return f"""You are an AI meeting minutes analyzer. Extract structured information from this transcript.

TRANSCRIPT:
{transcript_blocks}

SPEAKERS: {speakers_str}

OUTPUT - Return VALID JSON (no markdown, no code blocks):
{{
  "executive_summary": ["Key point 1", "Key point 2"],
  "action_items": [
    {{"description": "Task", "owner": "Name or Unassigned", "due_date": "YYYY-MM-DD or null", "priority": "High|Medium|Low", "status": "Pending"}}
  ],
  "decisions": [
    {{"decision": "What", "rationale": "Why", "owner": "Who", "context": "Background"}}
  ],
  "risks": [
    {{"risk": "Issue", "impact": "High|Medium|Low", "mitigation": "How", "owner": "Who"}}
  ],
  "speaker_spotlight": [
    {{"speaker": "Name", "role": "PM|Developer|QA|Designer", "contribution_count": 1, "key_points": ["point"]}}
  ],
  "metadata": {{"transcript_length_words": 0, "processing_method": "llm", "detected_dates": [], "confidence_score": "High"}}
}}

RULES:
1. Owner: Use EXACT names from SPEAKERS list. If "I will" assign that speaker
2. Dates: Convert "tomorrow", "Friday", "next week" to YYYY-MM-DD
3. Priority: "urgent"=High, "eventually"=Low, else Medium
4. Roles: PM (plans), Developer (code), QA (testing), Designer (UI)
5. Extract top 3-5 summary points

Return ONLY JSON object, no text before or after.""".strip()

async def node_llm_minutes(state: MinutesState) -> MinutesState:
    prompt = build_structuring_prompt(state["speaker_segments"])
    raw_response = await call_ollama(prompt)
    return {**state, "structured_minutes": raw_response, "llm_trace": {"prompt": prompt, "raw_response": raw_response}}

async def node_validate_structure(state: MinutesState) -> MinutesState:
    """Validate and post-process the LLM output, add warnings"""
    import json
    import re
    from datetime import datetime

    raw_json = state["structured_minutes"]
    processing_method = "llm"

    # Extract JSON from markdown or surrounding text
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_json, re.DOTALL)
    if json_match:
        raw_json = json_match.group(1)
    elif not raw_json.strip().startswith('{'):
        json_match = re.search(r'\{.*\}', raw_json, re.DOTALL)
        if json_match:
            raw_json = json_match.group(0)

    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        print(f"LLM JSON parse failed: {raw_json[:500]}")
        print(f"Using fallback parser...")
        parsed = parse_transcript_fallback(
            state.get("raw_transcript", ""),
            state.get("speaker_segments", [])
        )
        processing_method = "fallback"

    # Post-processing and validation
    warnings = []

    # Validate and enhance action items
    if "action_items" in parsed:
        for idx, action in enumerate(parsed["action_items"]):
            # Check for missing owner
            if not action.get("owner") or action["owner"] == "Unassigned":
                warnings.append({
                    "type": "missing_owner",
                    "message": f"Action item #{idx+1} has no assigned owner",
                    "context": action.get("description", "")[:50]
                })

            # Check for missing due date
            if not action.get("due_date"):
                warnings.append({
                    "type": "missing_due_date",
                    "message": f"Action item #{idx+1} has no due date",
                    "context": action.get("description", "")[:50]
                })

            # Ensure status field exists
            if "status" not in action:
                action["status"] = "Pending"

    # Validate decisions
    if "decisions" in parsed:
        for idx, decision in enumerate(parsed["decisions"]):
            if not decision.get("owner"):
                warnings.append({
                    "type": "missing_decision_owner",
                    "message": f"Decision #{idx+1} has no owner assigned",
                    "context": decision.get("decision", "")[:50]
                })

    # Validate risks
    if "risks" in parsed:
        for idx, risk in enumerate(parsed["risks"]):
            if not risk.get("mitigation"):
                warnings.append({
                    "type": "missing_mitigation",
                    "message": f"Risk #{idx+1} has no mitigation strategy",
                    "context": risk.get("risk", "")[:50]
                })

    # Ensure all required keys exist
    if "executive_summary" not in parsed:
        parsed["executive_summary"] = ["No summary generated"]
    if "action_items" not in parsed:
        parsed["action_items"] = []
    if "decisions" not in parsed:
        parsed["decisions"] = []
    if "risks" not in parsed:
        parsed["risks"] = []
    if "speaker_spotlight" not in parsed:
        parsed["speaker_spotlight"] = []

    # Add warnings to output
    parsed["warnings"] = warnings

    # Enhanced metadata
    raw_transcript = state.get("raw_transcript", "")
    speakers = state.get("speaker_segments", [])

    parsed["metadata"] = {
        "transcript_length_words": len(raw_transcript.split()),
        "transcript_length_chars": len(raw_transcript),
        "speaker_count": len(set(seg["speaker"] for seg in speakers)),
        "processing_method": processing_method,
        "detected_dates": extract_dates_from_transcript(raw_transcript),
        "confidence_score": "High" if processing_method == "llm" and not warnings else "Medium"
    }

    return {**state, "structured_minutes": parsed}


def extract_dates_from_transcript(text: str) -> List[str]:
    """Extract all date mentions from transcript"""
    import re
    from datetime import datetime, timedelta

    dates = []

    # Pattern for explicit dates
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',  # 2024-12-04
        r'\d{1,2}/\d{1,2}/\d{4}',  # 12/4/2024
        r'[A-Z][a-z]+ \d{1,2},? \d{4}',  # December 4, 2024
    ]

    # Pattern for relative dates
    relative = r'\b(today|tomorrow|yesterday|next week|next month|this week|this month|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'

    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates.extend(matches)

    relative_matches = re.findall(relative, text, re.IGNORECASE)
    dates.extend([m.capitalize() for m in relative_matches])

    return list(set(dates))[:10]  # Return up to 10 unique dates

# ----------- Graph Construction -----------

graph_builder = StateGraph(MinutesState)

graph_builder.add_node("clean_transcript", node_clean_transcript)
graph_builder.add_node("parse_speakers", node_parse_speakers)
graph_builder.add_node("llm_minutes", node_llm_minutes)
graph_builder.add_node("validate_structure", node_validate_structure)

graph_builder.set_entry_point("clean_transcript")
graph_builder.add_edge("clean_transcript", "parse_speakers")
graph_builder.add_edge("parse_speakers", "llm_minutes")
graph_builder.add_edge("llm_minutes", "validate_structure")
graph_builder.set_finish_point("validate_structure")

minutes_graph = graph_builder.compile()

# ----------- Entry Point -----------

async def generate_minutes(transcript_text: str) -> Dict[str, Any]:
    initial_state: MinutesState = {"raw_transcript": transcript_text}
    final_state = await minutes_graph.ainvoke(initial_state)
    return {
        "minutes": final_state["structured_minutes"],
        "llm_trace": final_state.get("llm_trace"),
    }