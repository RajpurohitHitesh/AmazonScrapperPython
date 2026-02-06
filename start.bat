@echo off
REM Quick Start Script for Amazon Scraper API
REM This script helps you quickly set up and run the scraper

echo ========================================
echo Amazon Scraper API - Quick Start
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

REM Install dependencies
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Setup environment file
echo [3/4] Setting up environment...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo .env file created! Please edit it and set your API_KEY
        echo Opening .env file...
        notepad .env
    ) else (
        echo WARNING: .env.example not found
    )
) else (
    echo .env file already exists
)
echo.

REM Start server
echo [4/4] Starting server...
echo.
echo ========================================
echo Server is starting...
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python api_server.py

pause
