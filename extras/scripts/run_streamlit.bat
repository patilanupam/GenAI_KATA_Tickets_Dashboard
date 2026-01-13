@echo off
REM ClarifyMeet AI - Streamlit Launcher for Windows
REM This script checks prerequisites and launches the Streamlit app

echo.
echo 🤖 ClarifyMeet AI - Streamlit Launcher
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Check if Ollama is running
echo 🔍 Checking Ollama connection...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Ollama is not accessible at http://localhost:11434
    echo    Please make sure Ollama is installed and running:
    echo    1. Install from: https://ollama.ai/download
    echo    2. The Ollama service should start automatically
    echo    3. Pull model: ollama pull tinyllama
    echo.
    set /p continue="Continue anyway? (y/N): "
    if /i not "%continue%"=="y" exit /b 1
)

echo ✅ Ollama is running

REM Check if requirements are installed
echo 📦 Checking dependencies...
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Dependencies not found. Installing...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies are installed

REM Launch Streamlit
echo.
echo 🚀 Launching ClarifyMeet AI...
echo    Access the app at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

python -m streamlit run streamlit_app.py

pause
