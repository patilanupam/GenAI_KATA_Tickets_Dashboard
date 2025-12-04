# ClarifyMeetAI



# ClarifyMeetAI

ClarifyMeetAI is an intelligent meeting transcription analysis tool that transforms raw meeting transcripts into structured, actionable meeting minutes. The application extracts key information including summaries, action items, decisions, and potential risks.

## System Architecture

```mermaid 
flowchart TD
    A[Upload Transcript (.txt)] --> B[Validate & Extract Text]
    B --> C[Identify Speakers/Actors]
    C --> D[Summarize Meeting]
    D --> E[Extract Action Items]
    E --> F[Extract Decisions]
    F --> G[Identify Risks]
    G --> H[Format Structured Minutes (JSON)]
    H --> I[Return to Frontend]
```

## Features

- **Transcript Analysis**: Processes raw meeting transcripts in text format
- **Speaker Identification**: Automatically detects and labels different speakers
- **Meeting Summarization**: Creates concise summaries of discussion topics
- **Action Item Extraction**: Identifies and lists tasks assigned during the meeting
- **Decision Tracking**: Captures key decisions made during discussions
- **Risk Assessment**: Highlights potential risks or issues mentioned
- **Structured Output**: Delivers organized meeting minutes in JSON format

## Project Structure

```
clarifymeet-ai/
│
├── backend/
│   ├── main.py                # FastAPI app entrypoint
│   ├── agent/
│   │   ├── langgraph_agent.py # LangGraph agent logic
│   │   └── prompts.py         # LLM prompt templates
│   ├── models/
│   │   └── minutes.py         # Pydantic models for output
│   ├── utils/
│   │   └── transcript_parser.py # Speaker extraction, validation
│   └── requirements.txt
│
├── frontend/
│   ├── style.css              # Responsive CSS
│   ├── index.html             # Main UI
│   └── app.js                 # Frontend logic
│
├── docs/
│   ├── flow_diagram.md        # Flow diagram (mermaid)
│   └── README.md              # Project documentation
│
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Multi-container setup
├── .dockerignore              # Docker build exclusions
├── .gitignore                 # Git exclusions
└── .env                       # Environment configuration
```
