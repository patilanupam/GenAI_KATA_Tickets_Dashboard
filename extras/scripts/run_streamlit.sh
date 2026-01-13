#!/bin/bash

# ClarifyMeet AI - Streamlit Launcher
# This script checks prerequisites and launches the Streamlit app

echo "🤖 ClarifyMeet AI - Streamlit Launcher"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python is installed"

# Check if Ollama is running
echo "🔍 Checking Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Warning: Ollama is not accessible at http://localhost:11434"
    echo "   Please make sure Ollama is installed and running:"
    echo "   1. Install from: https://ollama.ai/download"
    echo "   2. Run: ollama serve"
    echo "   3. Pull model: ollama pull tinyllama"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
if python3 -c "import streamlit" 2>/dev/null || python -c "import streamlit" 2>/dev/null; then
    echo "✅ Dependencies are installed"
else
    echo "⚠️  Dependencies not found. Installing..."
    if command -v python3 &> /dev/null; then
        python3 -m pip install -r requirements.txt
    else
        python -m pip install -r requirements.txt
    fi
fi

# Launch Streamlit
echo ""
echo "🚀 Launching ClarifyMeet AI..."
echo "   Access the app at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

if command -v python3 &> /dev/null; then
    python3 -m streamlit run streamlit_app.py
else
    python -m streamlit run streamlit_app.py
fi
