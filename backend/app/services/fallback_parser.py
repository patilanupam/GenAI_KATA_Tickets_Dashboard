"""
Fallback parser for extracting meeting information from transcripts
when LLM fails to produce valid JSON.
"""
import re
from typing import List, Dict, Any
from datetime import datetime, timedelta


def parse_transcript_fallback(transcript: str, speaker_segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract meeting information using rule-based parsing.

    Args:
        transcript: Raw transcript text
        speaker_segments: Parsed speaker segments

    Returns:
        Structured meeting minutes dictionary
    """
    # Extract action items
    action_items = []
    action_patterns = [
        r"(?:I'll|I will|I'm going to)\s+(.+?)(?:\s+by\s+|\s+before\s+|\s+on\s+)?(tomorrow|today|next \w+|end of \w+|\w+day|\d{4}-\d{2}-\d{2})?(?:\.|$)",
        r"(?:action item|action|task|todo|to do)[:\s]+(.+?)(?:\.|$)",
    ]

    for segment in speaker_segments:
        speaker = segment.get("speaker", "Unknown")
        text = segment.get("text", "")

        # Skip non-person speakers
        if speaker in ["Decision", "Risk", "Action", "Unknown"]:
            continue

        for pattern in action_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                description = match.group(1).strip()
                due_date = None
                if len(match.groups()) > 1 and match.group(2):
                    due_date = match.group(2).strip()

                # Clean up description (remove trailing conjunctions)
                description = re.sub(r'\s+(and|but|so|then)\s*$', '', description, flags=re.IGNORECASE).strip()

                if description and len(description) > 5:  # Filter out very short matches
                    action_items.append({
                        "description": description,
                        "owner": speaker,
                        "due_date": parse_due_date(due_date) if due_date else None,
                        "priority": infer_priority(description)
                    })

    # Extract decisions
    decisions = []
    decision_patterns = [
        r"(?:decision|decided|we will|we'll|let's|agreed)[:\s\-]+(.+?)(?:\.|$)",
        r"(?:we will|we'll)\s+(.+?)(?:\.|$)",
    ]

    for segment in speaker_segments:
        speaker = segment.get("speaker", "Unknown")
        text = segment.get("text", "")

        for pattern in decision_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                decision = match.group(1).strip()
                # Clean up the decision text
                decision = re.sub(r'^\s*[-:]\s*', '', decision)
                if decision and len(decision) > 10:
                    decisions.append({
                        "decision": decision,
                        "rationale": None,
                        "owner": speaker if speaker not in ["Decision", "Risk", "Action"] else "Team"
                    })

    # Extract risks
    risks = []
    risk_patterns = [
        r"(?:risk|concern|issue|problem)[:\s]+(.+?)(?:\.|$)",
        r"(?:if not\s+\w+|may affect|could impact|potential issue)\s+(.+?)(?:\.|$)",
    ]

    for segment in speaker_segments:
        speaker = segment.get("speaker", "Unknown")
        text = segment.get("text", "")

        for pattern in risk_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                risk = match.group(1).strip()
                # Clean up the risk text
                risk = re.sub(r'^\s*[-:]\s*', '', risk)
                if risk and len(risk) > 10 and "this week" not in risk[:20]:  # Avoid partial matches
                    risks.append({
                        "risk": risk,
                        "impact": infer_impact(risk),
                        "mitigation": None,
                        "owner": speaker if speaker not in ["Decision", "Risk", "Action"] else "Unassigned"
                    })

    # Create executive summary
    executive_summary = []
    if action_items:
        executive_summary.append(f"{len(action_items)} action item(s) identified")
    if decisions:
        executive_summary.append(f"{len(decisions)} decision(s) made")
    if risks:
        executive_summary.append(f"{len(risks)} risk(s) identified")

    # Add key points from transcript
    sentences = re.split(r'[.!?]+', transcript)
    important_sentences = [s.strip() for s in sentences if len(s.strip()) > 20][:3]
    executive_summary.extend(important_sentences)

    # Create speaker spotlight
    speaker_spotlight = []
    speaker_counts = {}
    for segment in speaker_segments:
        speaker = segment.get("speaker", "Unknown")
        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1

    for speaker, count in speaker_counts.items():
        speaker_spotlight.append({
            "speaker": speaker,
            "speaking_time_estimate": f"~{count} contribution(s)",
            "notable_points": []
        })

    # Extract dates mentioned
    date_patterns = [
        r'(?:on|by|before)?\s*([A-Z][a-z]+day,?\s+\w+\s+\d{1,2})',
        r'(?:on|by|before)?\s*(\d{4}-\d{2}-\d{2})',
        r'(tomorrow|today|next week|next month)',
    ]

    detected_dates = []
    for pattern in date_patterns:
        matches = re.finditer(pattern, transcript, re.IGNORECASE)
        detected_dates.extend([m.group(1) for m in matches])

    return {
        "executive_summary": executive_summary[:5] if executive_summary else ["Meeting minutes extracted using fallback parser"],
        "action_items": action_items,
        "decisions": decisions,
        "risks": risks,
        "speaker_spotlight": speaker_spotlight,
        "metadata": {
            "transcript_length_words": len(transcript.split()),
            "detected_date": detected_dates[0] if detected_dates else None,
            "confidence_notes": "Parsed using rule-based fallback parser (LLM output was invalid)"
        }
    }


def parse_due_date(date_str: str) -> str:
    """Convert relative dates to ISO format."""
    if not date_str:
        return None

    date_str = date_str.lower().strip()
    today = datetime.now()

    if "tomorrow" in date_str:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "today" in date_str:
        return today.strftime("%Y-%m-%d")
    elif "monday" in date_str:
        days_ahead = 0 - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    elif "friday" in date_str:
        days_ahead = 4 - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    elif "next week" in date_str:
        return (today + timedelta(days=7)).strftime("%Y-%m-%d")
    elif "end of day" in date_str or "eod" in date_str:
        return today.strftime("%Y-%m-%d")

    return date_str


def infer_priority(description: str) -> str:
    """Infer priority level from action item description."""
    description_lower = description.lower()

    # High priority indicators
    if any(word in description_lower for word in ["urgent", "asap", "critical", "immediately", "blocker"]):
        return "High"

    # Low priority indicators
    if any(word in description_lower for word in ["eventually", "nice to have", "consider", "optional"]):
        return "Low"

    # Default to medium
    return "Medium"


def infer_impact(risk: str) -> str:
    """Infer impact level from risk description."""
    risk_lower = risk.lower()

    # High impact indicators
    if any(word in risk_lower for word in ["affect the release", "block", "critical", "major"]):
        return "High"

    # Low impact indicators
    if any(word in risk_lower for word in ["minor", "small", "trivial"]):
        return "Low"

    # Default to medium
    return "Medium"
