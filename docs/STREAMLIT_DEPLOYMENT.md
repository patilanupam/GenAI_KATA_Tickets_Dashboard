# Streamlit Deployment Guide for ClarifyMeet AI

## 📋 Overview

This guide explains how to deploy ClarifyMeet AI on Streamlit Cloud or run it locally with Streamlit.

## 🚀 Local Deployment

### Prerequisites

1. **Python 3.11+**
2. **Ollama installed and running**
   ```bash
   # Install Ollama: https://ollama.ai/download
   
   # Pull the TinyLlama model
   ollama pull tinyllama
   ```

### Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure Ollama is running:**
   ```bash
   # Ollama should be running on http://localhost:11434
   # Verify with:
   curl http://localhost:11434/api/tags
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the app:**
   - Open your browser to: http://localhost:8501

## ☁️ Streamlit Cloud Deployment

### Important Note about Ollama

Streamlit Cloud doesn't support running Ollama locally. You have two options:

#### Option 1: Use a Hosted Ollama Instance

1. Deploy Ollama on a cloud server (AWS, DigitalOcean, etc.)
2. Make it accessible via a public URL with proper security
3. Update the `.streamlit/secrets.toml` with your Ollama host URL

#### Option 2: Switch to a Cloud LLM Service (Recommended)

Replace Ollama with OpenAI, Anthropic, or Hugging Face:

**For OpenAI:**

1. Update `backend/app/config.py`:
   ```python
   # Add OpenAI settings
   OPENAI_API_KEY: str = ""
   USE_OPENAI: bool = True
   ```

2. Update `backend/app/langgraph_agent.py`:
   ```python
   from openai import AsyncOpenAI
   
   async def call_llm(prompt: str) -> str:
       if settings.USE_OPENAI:
           client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
           response = await client.chat.completions.create(
               model="gpt-3.5-turbo",
               messages=[{"role": "user", "content": prompt}],
               temperature=0.2
           )
           return response.choices[0].message.content
       else:
           # Existing Ollama code
           ...
   ```

3. Add to `requirements.txt`:
   ```
   openai==1.10.0
   ```

### Deployment Steps

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Streamlit deployment"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `streamlit_app.py`
   - Click "Deploy"

3. **Configure Secrets:**
   - In Streamlit Cloud dashboard, go to your app settings
   - Navigate to "Secrets"
   - Add your configuration:
   ```toml
   [ollama]
   host = "YOUR_OLLAMA_HOST_URL"
   model = "tinyllama"
   
   # OR for OpenAI
   [openai]
   api_key = "your-openai-api-key"
   use_openai = true
   ```

## 🔧 Configuration

### Environment Variables

You can configure the app using `.streamlit/secrets.toml` or environment variables:

- `OLLAMA_HOST`: Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model name (default: tinyllama)
- `MAX_TRANSCRIPT_SIZE_MB`: Maximum upload size (default: 10)

### Custom Themes

Edit `.streamlit/config.toml` to customize the appearance:

```toml
[theme]
primaryColor = "#6264A7"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#262730"
```

## 📝 Differences from FastAPI Version

### What Changed

1. **Frontend Integration**: HTML/CSS/JS frontend replaced with Streamlit Python UI
2. **Single Application**: Combined frontend and backend into one `streamlit_app.py`
3. **No FastAPI Server**: Streamlit handles the web server
4. **Simplified Deployment**: One-click deployment to Streamlit Cloud

### What Stayed the Same

1. **Backend Logic**: All LangGraph agent code remains unchanged
2. **AI Processing**: Same Ollama/LLM integration
3. **Features**: All analysis features (summary, action items, decisions, risks, speakers)
4. **Output Format**: Same JSON structure

## 🐛 Troubleshooting

### Ollama Connection Issues

If you get "Connection refused" errors:

1. Verify Ollama is running:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. Check if the model is downloaded:
   ```bash
   ollama list
   ```

3. Ensure the Ollama host is accessible from your deployment environment

### Memory Issues

If processing large transcripts fails:

1. Reduce `MAX_TRANSCRIPT_SIZE_MB` in settings
2. Consider using a smaller model
3. Implement chunking for large transcripts

### Streamlit Cloud Limitations

- **Memory**: Limited to 1GB RAM on free tier
- **CPU**: Shared resources
- **Network**: Ollama must be publicly accessible
- **Timeout**: Long-running requests may timeout

Consider upgrading to Streamlit Cloud Teams for better resources.

## 🔐 Security Considerations

1. **API Keys**: Always use Streamlit secrets for sensitive data
2. **File Upload**: Validate and sanitize user uploads
3. **Ollama Access**: Secure your Ollama endpoint with authentication
4. **HTTPS**: Streamlit Cloud provides HTTPS by default

## 📊 Performance Tips

1. **Use Caching**: Streamlit's `@st.cache_data` for expensive operations
2. **Async Processing**: Maintain async operations for better performance
3. **Progress Indicators**: Show users processing status
4. **Error Handling**: Implement robust error handling and user feedback

## 🆘 Support

For issues:
- Check the [Streamlit documentation](https://docs.streamlit.io)
- Review the [Ollama documentation](https://ollama.ai/docs)
- Open an issue in the project repository

## 🎉 Success!

Once deployed, your app will be available at:
- **Local**: http://localhost:8501
- **Streamlit Cloud**: https://your-app-name.streamlit.app

Enjoy your AI-powered meeting minutes analyzer! 🤖
