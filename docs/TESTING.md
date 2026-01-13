# Test Configuration for ClarifyMeet AI

This file helps verify your setup before running the full application.

## Quick Test

Run this in PowerShell or Terminal:

```bash
python -c "import streamlit; import langgraph; import httpx; print('✅ All dependencies installed!')"
```

## Verify Ollama

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check if tinyllama is available
curl http://localhost:11434/api/show -d '{"name": "tinyllama"}'
```

## Test Transcript Example

Save this as `test_meeting.txt`:

```text
John: Good morning team. Let's discuss the Q1 roadmap.

Sarah: I'll work on the new dashboard. I can have it ready by next Friday.

Mike: I'll handle the API integration. The deadline is January 20th.

John: Decision: We're going with the microservices architecture.

Sarah: One concern - we might need additional design resources.

Mike: I agree. I'll also write comprehensive unit tests.
```

## Expected Output Structure

After analysis, you should see:

### Executive Summary
- 3-5 key points about the meeting

### Action Items
```json
{
  "description": "Work on the new dashboard",
  "owner": "Sarah",
  "due_date": "2026-01-17",
  "priority": "Medium",
  "status": "Pending"
}
```

### Decisions
```json
{
  "decision": "Going with microservices architecture",
  "rationale": "...",
  "owner": "John"
}
```

### Risks
```json
{
  "risk": "Might need additional design resources",
  "impact": "Medium",
  "mitigation": "...",
  "owner": "..."
}
```

## Troubleshooting Tests

### Test 1: Python Version
```bash
python --version
# Should be 3.11 or higher
```

### Test 2: Ollama Connection
```bash
curl http://localhost:11434/api/tags
# Should return JSON with available models
```

### Test 3: Dependencies
```bash
pip list | grep streamlit
pip list | grep langgraph
pip list | grep httpx
# All should be present
```

### Test 4: Simple LLM Call
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "tinyllama",
  "prompt": "Say hello",
  "stream": false
}'
# Should return a response
```

## Performance Benchmarks

### Expected Processing Times
- Small transcript (<1000 words): 10-30 seconds
- Medium transcript (1000-3000 words): 30-60 seconds  
- Large transcript (3000-5000 words): 60-120 seconds

### Resource Usage
- RAM: 2-4 GB (including Ollama)
- CPU: Moderate during processing
- Disk: 1 GB for model

## Common Issues

### Issue: ModuleNotFoundError
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Connection refused (Ollama)
**Solution:**
```bash
# Windows: Check Ollama in system tray
# Mac/Linux: 
ollama serve
```

### Issue: Port already in use
**Solution:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Issue: Slow processing
**Solution:**
- First run takes longer (model loading)
- Reduce transcript size
- Close other applications

## Success Indicators

✅ Python 3.11+ installed  
✅ Ollama running on port 11434  
✅ TinyLlama model downloaded  
✅ All Python dependencies installed  
✅ Streamlit launches without errors  
✅ Can upload and analyze test transcript  
✅ Results display in all tabs  
✅ Can download JSON output  

## Next Steps

Once all tests pass:
1. Try with your own meeting transcripts
2. Experiment with different meeting formats
3. Review the warnings and metadata
4. Export results to JSON
5. Consider deploying to Streamlit Cloud

## Support

If tests fail:
1. Review error messages carefully
2. Check [QUICKSTART_STREAMLIT.md](QUICKSTART_STREAMLIT.md)
3. See [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md)
4. Verify all prerequisites are met
