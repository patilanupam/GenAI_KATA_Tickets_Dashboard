"""
Text cleaning utilities for transcript processing
"""
import re
from typing import str


def clean_transcript(raw_text: str) -> str:
    """
    Clean and normalize transcript text.

    Args:
        raw_text: Raw transcript text

    Returns:
        Cleaned transcript text
    """
    if not raw_text:
        return ""

    # Remove excessive whitespace
    cleaned = re.sub(r'\s+', ' ', raw_text)

    # Remove special characters but keep punctuation
    cleaned = re.sub(r'[^\w\s\[\]:,!?\-\'\"]', '', cleaned)

    # Normalize line breaks
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

    # Strip leading/trailing whitespace
    cleaned = cleaned.strip()

    return cleaned

