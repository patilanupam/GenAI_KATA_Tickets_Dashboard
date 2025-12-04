"""
Transcript parsing utilities
This module provides utilities for parsing and processing meeting transcripts.
"""
import re
from typing import List, Dict, Any, Optional


def parse_transcript(transcript: str) -> List[Dict[str, str]]:
    """
    Parse transcript into structured segments.

    Supports multiple formats:
    - [Speaker Name] text
    - Speaker Name: text

    Args:
        transcript: Raw transcript text

    Returns:
        List of dictionaries with 'speaker' and 'text' keys
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


def extract_speakers(transcript: str) -> List[str]:
    """
    Extract unique speaker names from transcript.

    Args:
        transcript: Raw transcript text

    Returns:
        List of unique speaker names
    """
    segments = parse_transcript(transcript)
    speakers = list(set(seg["speaker"] for seg in segments))
    return sorted(speakers)


def clean_transcript_text(text: str) -> str:
    """
    Clean and normalize transcript text.

    Args:
        text: Raw transcript text

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Remove excessive whitespace
    cleaned = re.sub(r'\s+', ' ', text)

    # Remove special characters but keep punctuation
    cleaned = re.sub(r'[^\w\s\[\]:,!?\-\'\"]', '', cleaned)

    # Normalize line breaks
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

    # Strip leading/trailing whitespace
    cleaned = cleaned.strip()

    return cleaned


def segment_by_speaker(transcript: str) -> Dict[str, List[str]]:
    """
    Group all text segments by speaker.

    Args:
        transcript: Raw transcript text

    Returns:
        Dictionary mapping speaker names to list of their text segments
    """
    segments = parse_transcript(transcript)
    speaker_map: Dict[str, List[str]] = {}

    for segment in segments:
        speaker = segment["speaker"]
        text = segment["text"]

        if speaker not in speaker_map:
            speaker_map[speaker] = []

        speaker_map[speaker].append(text)

    return speaker_map


def get_transcript_stats(transcript: str) -> Dict[str, Any]:
    """
    Get statistics about the transcript.

    Args:
        transcript: Raw transcript text

    Returns:
        Dictionary with transcript statistics
    """
    segments = parse_transcript(transcript)
    speaker_map = segment_by_speaker(transcript)

    total_words = sum(len(seg["text"].split()) for seg in segments)

    speaker_stats = {}
    for speaker, texts in speaker_map.items():
        word_count = sum(len(text.split()) for text in texts)
        speaker_stats[speaker] = {
            "segments": len(texts),
            "word_count": word_count,
            "percentage": round(word_count / total_words * 100, 2) if total_words > 0 else 0
        }

    return {
        "total_segments": len(segments),
        "total_words": total_words,
        "unique_speakers": len(speaker_map),
        "speaker_stats": speaker_stats
    }

 