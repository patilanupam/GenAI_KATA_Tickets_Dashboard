# ClarifyMeet AI 🤖

> Transform meeting conversations into actionable insights using AI

ClarifyMeet AI is an intelligent meeting minutes generation tool that automatically extracts structured information from meeting transcripts using LangGraph and Ollama.

![Status](https://img.shields.io/badge/status-ready-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688)
![Docker](https://img.shields.io/badge/docker-ready-2496ED)

## 📊 Workflow

<pre> ```mermaid graph TD A["Upload Transcript (.txt)"] --> B["Validate & Extract Text"] B --> C["Identify Speakers / Actors"] C --> D["Summarize Meeting"] D --> E["Extract Action Items"] E --> F["Extract Decisions"] F --> G["Identify Risks"] G --> H["Format Structured Minutes (JSON)"] H --> I["Return to Frontend"] ``` </pre>


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

## ✨ Features

- 📤 **Easy Upload**: Drag-and-drop `.txt` transcript files
- 🤖 **AI-Powered Extraction**: Uses LangGraph + Ollama (TinyLlama) for intelligent parsing
- 📋 **Structured Output**: Extracts Summary, Action Items, Decisions, Risks, and Speakers
- 🎯 **Smart Inference**: Automatically identifies task owners, due dates, and priorities
- 💬 **ChatGPT-like UI**: Modern, responsive interface with dark theme
- 🔄 **In-Session Management**: Edit and manage action items in real-time
- 📊 **Confidence Scoring**: AI confidence levels for extracted information
- ⚡ **Fast & Local**: All processing happens locally with no external API calls
- 🐳 **Docker Ready**: Single-command deployment with Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Ollama installed and running on host machine

### Installation

1. **Install Ollama and download the model:**
   ```bash
   # Install Ollama: https://ollama.ai/download

   # Pull TinyLlama model
   ollama pull tinyllama
   ```

2. **Clone and start the application:**
   ```bash
   # Navigate to project directory
   cd ClarifyMeetAI

   # Build and start with Docker Compose
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

📖 **For detailed setup instructions, see [SETUP.md](SETUP.md)**

## 📁 Project Structure

```
ClarifyMeetAI/
├── backend/                  # FastAPI Backend
│   ├── main.py              # Application entry point
│   ├── agent/               # LangGraph agent logic
│   │   ├── langgraph_agent.py
│   │   └── prompts.py
│   ├── models/              # Pydantic schemas
│   │   └── minutes.py
│   ├── utils/               # Utility functions
│   │   └── transcript_parser.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Static Frontend
│   ├── index.html          # Main UI
│   ├── style.css           # Styling
│   └── app.js              # JavaScript logic
├── docker-compose.yml      # Docker orchestration
├── SETUP.md               # Detailed setup guide
└── README.md              # This file
```

## 💡 Usage Example

### 1. Prepare a Transcript

Create a `.txt` file with speaker-based format:

```
John: Good morning everyone. Let's start our sprint planning.

Sarah: I'll work on the login page redesign. I can finish it by Friday.

Mike: I'll handle the backend API for authentication. Due date is next Monday.

John: Decision: We will use JWT tokens for authentication.

Sarah: One risk - the design needs approval from stakeholders first.
```

### 2. Upload and Process

1. Open http://localhost:8000
2. Drag and drop your transcript file
3. Enter meeting title and date
4. Click "Process Transcript"

### 3. View Results

The AI will extract:

- **Summary**: Brief overview of the meeting
- **Action Items**: Tasks with owners, due dates, priorities, and confidence scores
- **Decisions**: Key decisions made during the meeting
- **Risks**: Identified risks and open questions
- **Speakers**: List of participants with their roles

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.11, FastAPI 0.109.0 |
| **AI/Agent** | LangGraph 0.0.20, LangChain 0.1.0 |
| **LLM** | Ollama + TinyLlama (local inference) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Deployment** | Docker, Docker Compose, Uvicorn |
| **Storage** | In-memory (stateless, session-based) |

## 🎯 What Gets Extracted

### Action Items
- **Description**: What needs to be done
- **Owner**: Who is responsible (auto-inferred from "I'll" statements)
- **Due Date**: When it's due (converts relative dates like "tomorrow")
- **Priority**: LOW, MEDIUM, or HIGH
- **Status**: PENDING, IN_PROGRESS, DONE, CANCELLED
- **Confidence**: AI confidence level (LOW, MEDIUM, HIGH)

### Decisions
- **Description**: What was decided
- **Source**: Original utterance from transcript

### Risks & Open Questions
- **Type**: RISK or OPEN_QUESTION
- **Description**: The risk or question identified
- **Source**: Original utterance from transcript

### Speakers
- **Name**: Speaker name
- **Role**: Auto-inferred from context (Developer, QA, PM, etc.)
- **Action Count**: Number of actions assigned to them

## 🔧 API Reference

### POST `/api/process`

Process a meeting transcript and extract structured information.

**Request:**
- `file`: .txt file (multipart/form-data)
- `meeting_title`: String
- `meeting_date`: ISO date string (YYYY-MM-DD)

**Response:**
```json
{
  "session_id": "uuid",
  "meeting_title": "Sprint Planning",
  "meeting_date": "2024-12-05",
  "summary": "Team discussed...",
  "actions": [...],
  "decisions": [...],
  "risks": [...],
  "speakers": [...],
  "warnings": [...]
}
```

### GET `/health`

Check application and Ollama connection health.

**Response:**
```json
{
  "status": "healthy",
  "ollama_status": "connected",
  "ollama_model": "tinyllama"
}
```

## 🐛 Troubleshooting

### Ollama Connection Issues

```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama if needed
ollama serve
```

### Port Already in Use

```bash
# Change port in docker-compose.yml
ports:
  - "8080:8000"  # Use 8080 instead
```

### Model Not Found

```bash
# Pull the required model
ollama pull tinyllama

# Verify it's available
ollama list
```

For more troubleshooting, see [SETUP.md](SETUP.md#troubleshooting).

## 🔐 Security Notes

- **Local Processing**: All data is processed locally, no external API calls
- **In-Memory Storage**: Sessions are stored in memory (no persistent database)
- **No Authentication**: Current version has no auth (add for production use)
- **File Validation**: Only `.txt` files accepted, max 10MB

## 🚧 Roadmap / Future Enhancements

- [ ] PDF/DOCX export functionality
- [ ] Persistent storage (Redis/PostgreSQL)
- [ ] User authentication & multi-tenancy
- [ ] Real-time collaboration features
- [ ] Integration with video conferencing tools (Zoom, Teams, Meet)
- [ ] Multi-language support
- [ ] Advanced analytics and insights
- [ ] Email notifications for action items
- [ ] Calendar integration for due dates
- [ ] Support for audio file transcription

## 📝 Customization

### Modify Extraction Prompts

Edit `backend/agent/prompts.py` to customize how the AI extracts information:

```python
def build_minutes_prompt(transcript, speakers, meeting_date, meeting_title):
    # Customize the prompt template here
    prompt = f"""Your custom instructions..."""
    return prompt
```

### Change LLM Model

In `docker-compose.yml`:
```yaml
environment:
  - OLLAMA_MODEL=llama2  # Or any other Ollama model
```

### Adjust UI Theme

Edit `frontend/style.css` to change colors and styling:
```css
:root {
    --bg-primary: #0f172a;    /* Dark background */
    --accent-primary: #3b82f6; /* Blue accent */
    /* ... more variables ... */
}
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🙏 Acknowledgments

- **Ollama** for local LLM inference
- **LangChain/LangGraph** for agent orchestration
- **FastAPI** for the modern Python web framework
- **TinyLlama** for the efficient language model

## 📞 Support

For issues, questions, or suggestions:

1. Check the [SETUP.md](SETUP.md) for detailed instructions
2. Review the [Troubleshooting](SETUP.md#troubleshooting) section
3. Open an issue on GitHub (if applicable)

---

**Built with ❤️ using LangGraph, Ollama, and FastAPI**

**Status**: Production-ready ✅ | Last Updated: December 2025
