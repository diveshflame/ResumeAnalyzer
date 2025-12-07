@echo off
echo ================================================
echo AI Resume Feedback System - Setup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo √ Python found
python --version
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo √ Dependencies installed successfully!
) else (
    echo X Failed to install dependencies.
    pause
    exit /b 1
)

echo.

REM Check if .env exists
if exist .env (
    echo √ .env file already exists
) else (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo WARNING: Edit .env file and add your Gemini API key!
    echo.
    echo To get your API key:
    echo 1. Visit: https://makersuite.google.com/app/apikey
    echo 2. Sign in and create an API key
    echo 3. Edit .env and replace 'your_gemini_api_key_here' with your actual key
)

echo.
echo ================================================
echo √ Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env file and add your Gemini API key
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
echo Need help? Check README.md for detailed instructions.
echo.
pause