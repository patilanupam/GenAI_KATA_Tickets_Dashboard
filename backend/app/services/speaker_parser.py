"""
Speaker parsing utilities for transcript segmentation
"""
import re
from typing import List, Dict, Any


def parse_speakers(transcript: str) -> List[Dict[str, Any]]:
    """
    Parse transcript into speaker segments.

    Expects format like:
    [Speaker Name] text...
    or
    Speaker Name: text...

    Args:
        transcript: Cleaned transcript text

    Returns:
        List of speaker segments with speaker name and text
    """
    segments = []

    # Pattern 1: [Speaker Name] text
    pattern1 = r'\[([^\]]+)\]\s*([^\[]+)'
    matches1 = re.findall(pattern1, transcript, re.MULTILINE)

    if matches1:
        for speaker, text in matches1:
            segments.append({
                "speaker": speaker.strip(),
                "text": text.strip()
            })
        return segments

    # Pattern 2: Speaker Name: text
    pattern2 = r'^([A-Za-z\s]+):\s*(.+)$'
    lines = transcript.split('\n')

    current_speaker = None
    current_text = []

    for line in lines:
        match = re.match(pattern2, line.strip())
        if match:
            # Save previous segment
            if current_speaker and current_text:
                segments.append({
                    "speaker": current_speaker,
                    "text": " ".join(current_text).strip()
                })

            # Start new segment
            current_speaker = match.group(1).strip()
            current_text = [match.group(2).strip()]
        elif current_speaker and line.strip():
            # Continue current segment
            current_text.append(line.strip())

    # Save last segment
    if current_speaker and current_text:
        segments.append({
            "speaker": current_speaker,
            "text": " ".join(current_text).strip()
        })

    # If no patterns matched, treat entire transcript as single segment
    if not segments:
        segments.append({
            "speaker": "Unknown",
            "text": transcript.strip()
        })

    return segments

