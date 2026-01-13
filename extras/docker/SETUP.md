# ClarifyMeet AI - Setup Guide

This guide will walk you through setting up ClarifyMeet AI, a meeting minutes generation tool powered by LangGraph and Ollama.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Ollama Setup](#ollama-setup)
3. [Project Setup](#project-setup)
4. [Running the Application](#running-the-application)
5. [Testing the Application](#testing-the-application)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
  - Download: https://www.docker.com/products/docker-desktop
  - Verify: `docker --version` and `docker-compose --version`

- **Git** (optional, for cloning)
  - Download: https://git-scm.com/downloads
  - Verify: `git --version`

- **Ollama** (for local LLM inference)
  - See [Ollama Setup](#ollama-setup) section below

---

## Ollama Setup

Ollama must be running on your **host machine** (not inside Docker) for the application to work.

### Step 1: Install Ollama

#### Windows
1. Download Ollama from: https://ollama.ai/download/windows
2. Run the installer (`OllamaSetup.exe`)
3. Ollama will start automatically as a Windows service

#### macOS
```bash
# Using Homebrew
brew install ollama

# Or download from: https://ollama.ai/download/mac
```

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Verify Ollama Installation

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# You should see a JSON response with available models
```

### Step 3: Download the TinyLlama Model

```bash
# Pull the tinyllama model (required for the application)
ollama pull tinyllama

# Verify the model is downloaded
ollama list
```

**Expected Output:**
```
NAME            ID              SIZE    MODIFIED
tinyllama:latest  bcf49c8f7c88   637 MB  X minutes ago
```

### Step 4: Test the Model

```bash
# Test if the model works
ollama run tinyllama "Hello, how are you?"

# You should get a response from the model
# Press Ctrl+D to exit the interactive mode
```

---

## Project Setup

### Step 1: Project Structure

Ensure your project directory looks like this:

```
ClarifyMeetAI/
├── backend/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── langgraph_agent.py
│   │   └── prompts.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── minutes.py
│   └── utils/
│       ├── __init__.py
│       └── transcript_parser.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── docker-compose.yml
├── SETUP.md
└── sample_transcripts/
    └── (your test transcripts)
```

### Step 2: Verify Configuration

Check that your `docker-compose.yml` has the correct Ollama URL:

```yaml
environment:
  - OLLAMA_BASE_URL=http://host.docker.internal:11434
  - OLLAMA_MODEL=tinyllama
```

**Note:**
- On **Windows/Mac**: Use `host.docker.internal`
- On **Linux**: You may need to use `host-gateway` or your host's IP address

---

## Running the Application

### Step 1: Ensure Ollama is Running

```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# If not running, start Ollama:
# Windows: Ollama runs as a service automatically
# Mac/Linux: Run `ollama serve` in a separate terminal
```

### Step 2: Build and Start Docker Containers

```bash
# Navigate to project root
cd ClarifyMeetAI

# Build and start the application
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

### Step 3: Wait for Services to Start

Watch the logs for:
```
clarifymeet-app | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
clarifymeet-app | INFO:     Application startup complete.
```

### Step 4: Verify the Application

Open your browser and navigate to:

1. **Frontend UI**: http://localhost:8000
2. **API Documentation**: http://localhost:8000/docs
3. **Health Check**: http://localhost:8000/health

**Expected Health Check Response:**
```json
{
  "status": "healthy",
  "ollama_status": "connected",
  "ollama_model": "tinyllama"
}
```

---

## Testing the Application

### Step 1: Prepare a Test Transcript

Create a file named `test_transcript.txt` with the following content:

```
John: Good morning everyone. Let's start our sprint planning meeting.

Sarah: I'll work on the login page redesign. I can finish it by Friday.

Mike: I'll handle the backend API for authentication. Due date is next Monday.

John: Great. Decision: We will use JWT tokens for authentication.

Sarah: One risk - the design needs approval from stakeholders first.

Mike: I'll also prepare the test cases. High priority.
```

### Step 2: Upload the Transcript

1. Open http://localhost:8000 in your browser
2. Drag and drop `test_transcript.txt` or click "Browse Files"
3. Enter meeting details:
   - **Meeting Title**: Sprint Planning
   - **Meeting Date**: Today's date
4. Click "Process Transcript"

### Step 3: Verify Results

You should see:
- **Summary** tab with a meeting overview
- **Action Items** tab with extracted tasks (2-3 actions)
- **Decisions** tab showing the JWT decision
- **Risks** tab with the stakeholder approval risk
- **Speakers** tab listing John, Sarah, and Mike

### Step 4: Test API Directly (Optional)

```bash
# Using curl
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@test_transcript.txt" \
  -F "meeting_title=Sprint Planning" \
  -F "meeting_date=2024-12-05"

# You should receive a JSON response with structured meeting minutes
```

---

## Troubleshooting

### Issue 1: "Ollama connection failed"

**Symptoms:**
- Health check shows `ollama_status: "disconnected"`
- Error: "Connection refused to http://host.docker.internal:11434"

**Solutions:**

1. **Verify Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **On Linux, update docker-compose.yml:**
   ```yaml
   environment:
     - OLLAMA_BASE_URL=http://172.17.0.1:11434  # Use Docker bridge IP
   ```

3. **Check firewall settings:**
   - Ensure port 11434 is not blocked
   - On Windows, allow Docker in firewall rules

4. **Restart Ollama:**
   ```bash
   # Mac/Linux
   pkill ollama
   ollama serve

   # Windows: Restart Ollama from Task Manager or Services
   ```

### Issue 2: "Model not found: tinyllama"

**Solutions:**

1. **Pull the model:**
   ```bash
   ollama pull tinyllama
   ```

2. **Verify model is available:**
   ```bash
   ollama list
   ```

### Issue 3: "Port 8000 already in use"

**Solutions:**

1. **Stop conflicting services:**
   ```bash
   # Find process using port 8000
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F

   # Mac/Linux
   lsof -ti:8000 | xargs kill -9
   ```

2. **Or change the port in docker-compose.yml:**
   ```yaml
   ports:
     - "8080:8000"  # Use port 8080 instead
   ```

### Issue 4: Frontend shows 404 errors

**Solutions:**

1. **Verify volume mounts in docker-compose.yml:**
   ```yaml
   volumes:
     - ./backend:/app
     - ./frontend:/app/static
   ```

2. **Check static files exist:**
   ```bash
   ls frontend/
   # Should show: index.html, style.css, app.js
   ```

3. **Restart containers:**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### Issue 5: "File upload failed" or "Processing timeout"

**Solutions:**

1. **Check file format:**
   - Only `.txt` files are supported
   - File must contain speaker format: `Name: text`

2. **Verify transcript format:**
   ```
   Speaker1: This is the text
   Speaker2: Another line
   ```

3. **Check Ollama logs:**
   ```bash
   # View Ollama logs to see if model is responding
   # The response time can be slow for large transcripts
   ```

4. **Increase timeout in langgraph_agent.py:**
   ```python
   # In backend/agent/langgraph_agent.py, line ~80
   timeout=300  # Increase from 120 to 300 seconds
   ```

### Issue 6: Docker build fails

**Solutions:**

1. **Clear Docker cache:**
   ```bash
   docker-compose down
   docker system prune -a
   docker-compose up --build
   ```

2. **Check Python dependencies:**
   - Ensure `backend/requirements.txt` is present
   - Verify no syntax errors in Python files

3. **View build logs:**
   ```bash
   docker-compose up --build 2>&1 | tee build.log
   ```

---

## Stopping the Application

```bash
# Stop containers (keeps data)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

---

## Development Tips

### Hot Reload

The application supports hot reload for both backend and frontend:

1. **Backend changes**: Modify files in `backend/` - uvicorn auto-reloads
2. **Frontend changes**: Modify files in `frontend/` - refresh browser

### View Logs

```bash
# All logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f clarifymeet-app

# Last 100 lines
docker-compose logs --tail=100
```

### Access Container Shell

```bash
# Interactive shell
docker-compose exec clarifymeet-app bash

# Run commands
docker-compose exec clarifymeet-app python -c "import fastapi; print(fastapi.__version__)"
```

### Test Backend Directly

```bash
# Install httpie (better than curl)
pip install httpie

# Make API request
http -f POST http://localhost:8000/api/process \
  file@test_transcript.txt \
  meeting_title="Test Meeting" \
  meeting_date="2024-12-05"
```

---

## Production Deployment Notes

If deploying to production, consider:

1. **Use a production ASGI server:**
   - Already configured: `uvicorn` with proper settings
   - For high traffic, use Gunicorn + Uvicorn workers

2. **Add environment variable management:**
   - Use `.env` files (not committed to git)
   - Store secrets in environment variables

3. **Configure CORS if needed:**
   ```python
   # In main.py
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(CORSMiddleware, ...)
   ```

4. **Add authentication:**
   - Implement API key authentication
   - Use OAuth2 for user authentication

5. **Use persistent storage:**
   - Replace in-memory sessions with Redis or database
   - Store uploaded files in object storage (S3, etc.)

6. **Monitor and log:**
   - Add structured logging
   - Integrate with monitoring tools (Prometheus, Grafana)

---

## Support and Resources

- **Ollama Documentation**: https://ollama.ai/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **LangChain/LangGraph**: https://python.langchain.com/docs/langgraph
- **Docker Documentation**: https://docs.docker.com

---

## Next Steps

After successful setup, you can:

1. Test with your own meeting transcripts
2. Customize prompts in `backend/agent/prompts.py`
3. Add more features (PDF export, email notifications, etc.)
4. Integrate with calendar apps or video conferencing tools
5. Deploy to a cloud platform (AWS, GCP, Azure)

---

**Happy Meeting Minutes Generation! 🚀**
