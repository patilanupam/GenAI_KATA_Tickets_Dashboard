# ClarifyMeetAI

flowchart TD
    A[Upload Transcript (.txt)] --> B[Validate & Extract Text]
    B --> C[Identify Speakers/Actors]
    C --> D[Summarize Meeting]
    D --> E[Extract Action Items]
    E --> F[Extract Decisions]
    F --> G[Identify Risks]
    G --> H[Format Structured Minutes (JSON)]
    H --> I[Return to Frontend]

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
│   ├── static/
│   │   ├── style.css          # Responsive CSS
│   ├── templates/
│   │   └── index.html         # Main UI
│   └── app.js                 # Frontend logic (optional)
│
├── docs/
│   ├── flow_diagram.md        # Flow diagram (mermaid)
│   └── README.md              # Project documentation
│
└── .env                       # Ollama API keys/config
