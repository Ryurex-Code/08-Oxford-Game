@echo off
echo ================================
echo Oxford Vocabulary Trainer Setup
echo ================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo Python found!

echo.
echo [2/4] Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo [3/4] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from template
) else (
    echo .env file already exists
)

echo.
echo [4/4] Running quick test...
python main.py --test

echo.
echo ================================
echo Setup completed!
echo ================================
echo.
echo Next steps:
echo 1. Get a free Groq API key from: https://console.groq.com
echo 2. Edit .env file and add your API key
echo 3. Run: python main.py
echo.
pause
