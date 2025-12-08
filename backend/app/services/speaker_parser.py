"""
Speaker parsing utilities for transcript segmentation with role inference
"""
import re
from typing import List, Dict, Any


def infer_speaker_role(speaker_name: str, text_content: str) -> str:
    """
    Infer speaker role based on name and content.

    Args:
        speaker_name: Name of the speaker
        text_content: Combined text from all their contributions

    Returns:
        Inferred role string
    """
    text_lower = text_content.lower()

    # Role indicators in speech patterns
    pm_keywords = ["roadmap", "timeline", "stakeholder", "deadline", "priority", "schedule", "deliverable", "scope"]
    dev_keywords = ["code", "implement", "deploy", "bug", "api", "database", "backend", "frontend", "technical debt"]
    qa_keywords = ["test", "testing", "quality", "regression", "automation", "bug report", "test case"]
    designer_keywords = ["design", "mockup", "prototype", "ui", "ux", "interface", "wireframe", "user experience"]
    manager_keywords = ["team", "resource", "budget", "escalate", "approve", "review meeting"]

    # Count keyword matches
    scores = {
        "Project Manager": sum(1 for kw in pm_keywords if kw in text_lower),
        "Developer": sum(1 for kw in dev_keywords if kw in text_lower),
        "QA Engineer": sum(1 for kw in qa_keywords if kw in text_lower),
        "Designer": sum(1 for kw in designer_keywords if kw in text_lower),
        "Manager": sum(1 for kw in manager_keywords if kw in text_lower),
    }

    # Get role with highest score
    max_score = max(scores.values())
    if max_score > 0:
        return max(scores, key=scores.get)

    # Default based on common name patterns
    if any(word in speaker_name.lower() for word in ["pm", "product", "manager"]):
        return "Project Manager"
    elif any(word in speaker_name.lower() for word in ["dev", "engineer", "developer"]):
        return "Developer"
    elif any(word in speaker_name.lower() for word in ["qa", "test", "quality"]):
        return "QA Engineer"
    elif any(word in speaker_name.lower() for word in ["design", "ux", "ui"]):
        return "Designer"

    return "Team Member"


def parse_speakers(transcript: str) -> List[Dict[str, Any]]:
    """
    Parse transcript into speaker segments with enhanced detection.

    Supports formats:
    - [Speaker Name] text...
    - Speaker Name: text...
    - Speaker Name - text...

    Args:
        transcript: Cleaned transcript text

    Returns:
        List of speaker segments with speaker name, text, and inferred role
    """
    segments = []

    # Pattern 1: [Speaker Name] text
    pattern1 = r'\[([^\]]+)\]\s*([^\[]+)'
    matches1 = re.findall(pattern1, transcript, re.MULTILINE)

    if matches1:
        for speaker, text in matches1:
            speaker = speaker.strip()
            segments.append({
                "speaker": speaker,
                "text": text.strip(),
                "role": None  # Will be inferred later
            })
        _add_roles_to_segments(segments)
        return segments

    # Pattern 2: Speaker Name: text or Speaker Name - text
    pattern2 = r'^([A-Za-z\s]+)[\:\-]\s*(.+)$'
    lines = transcript.split('\n')

    current_speaker = None
    current_text = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(pattern2, line)
        if match:
            # Save previous segment
            if current_speaker and current_text:
                segments.append({
                    "speaker": current_speaker,
                    "text": " ".join(current_text).strip(),
                    "role": None
                })

            # Start new segment
            current_speaker = match.group(1).strip()
            text_part = match.group(2).strip()
            if text_part:
                current_text = [text_part]
            else:
                current_text = []
        elif current_speaker and line:
            # Continue current segment (multi-line speech)
            current_text.append(line)

    # Save last segment
    if current_speaker and current_text:
        segments.append({
            "speaker": current_speaker,
            "text": " ".join(current_text).strip(),
            "role": None
        })

    # If segments found, infer roles
    if segments:
        _add_roles_to_segments(segments)
        return segments

    # Fallback: treat entire transcript as single segment
    segments.append({
        "speaker": "Unknown Speaker",
        "text": transcript.strip(),
        "role": "Team Member"
    })

    return segments


def _add_roles_to_segments(segments: List[Dict[str, Any]]) -> None:
    """Add inferred roles to speaker segments in-place"""
    # Aggregate text by speaker for role inference
    speaker_texts = {}
    for seg in segments:
        speaker = seg["speaker"]
        if speaker not in speaker_texts:
            speaker_texts[speaker] = []
        speaker_texts[speaker].append(seg["text"])

    # Infer roles
    speaker_roles = {}
    for speaker, texts in speaker_texts.items():
        combined_text = " ".join(texts)
        speaker_roles[speaker] = infer_speaker_role(speaker, combined_text)

    # Assign roles to segments
    for seg in segments:
        seg["role"] = speaker_roles.get(seg["speaker"], "Team Member")

