MINUTES_PROMPT = """
You are a professional meeting assistant. Given the following transcript and speakers, generate structured meeting minutes in JSON with:
- summary
- action_items
- decisions
- risks
- speakers (with roles if possible)

Transcript:
{transcript}

Speakers:
{speakers}

Format output as:
{
  "summary": "...",
  "action_items": [...],
  "decisions": [...],
  "risks": [...],
  "speakers": [{ "name": "...", "role": "..." }]
}
"""