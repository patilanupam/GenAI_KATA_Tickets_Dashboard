@echo off
REM Verify Streamlit Cloud Deployment Readiness

echo.
echo ========================================
echo Streamlit Cloud Deployment Verification
echo ========================================
echo.

set "allGood=true"

REM Check required files
echo Checking required files...
echo.

if exist "streamlit_app.py" (
    echo [32m✅ streamlit_app.py[0m
) else (
    echo [31m❌ streamlit_app.py MISSING[0m
    set "allGood=false"
)

if exist "requirements.txt" (
    echo [32m✅ requirements.txt[0m
) else (
    echo [31m❌ requirements.txt MISSING[0m
    set "allGood=false"
)

if exist ".streamlit\config.toml" (
    echo [32m✅ .streamlit\config.toml[0m
) else (
    echo [31m❌ .streamlit\config.toml MISSING[0m
    set "allGood=false"
)

if exist "packages.txt" (
    echo [32m✅ packages.txt[0m
) else (
    echo [31m❌ packages.txt MISSING[0m
    set "allGood=false"
)

if exist "backend" (
    echo [32m✅ backend\ folder[0m
) else (
    echo [31m❌ backend\ folder MISSING[0m
    set "allGood=false"
)

echo.
echo ========================================
echo.

if "%allGood%"=="true" (
    echo [32m🎉 All required files present![0m
    echo [32mReady for Streamlit Cloud deployment.[0m
    echo.
    echo Next steps:
    echo 1. git add .
    echo 2. git commit -m "Deploy to Streamlit Cloud"
    echo 3. git push origin main
    echo 4. Go to share.streamlit.io and deploy
) else (
    echo [31m⚠️  Some files are missing![0m
    echo Please create the missing files before deploying.
)

echo.
echo ========================================
echo Git Status:
echo ========================================
git status

echo.
pause
