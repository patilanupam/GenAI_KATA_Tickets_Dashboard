"""
Text cleaning utilities for transcript processing
"""
import re


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

    # Normalize line breaks (reduce excessive blank lines)
    cleaned = re.sub(r'\n{3,}', '\n\n', raw_text)

    # Remove special characters but keep punctuation and newlines
    cleaned = re.sub(r'[^\w\s\[\]:,!?\-\'\"\n]', '', cleaned)

    # Remove excessive spaces (but preserve newlines)
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)

    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in cleaned.split('\n')]
    cleaned = '\n'.join(lines)

    # Strip leading/trailing whitespace from entire text
    cleaned = cleaned.strip()

    return cleaned

