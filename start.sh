#!/bin/bash
# Quick Start Script for Amazon Scraper API
# This script helps you quickly set up and run the scraper

echo "========================================"
echo "Amazon Scraper API - Quick Start"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ first"
    exit 1
fi

echo "[1/5] Checking Python installation..."
python3 --version
echo ""

# Install dependencies
echo "[2/5] Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
python3 -m playwright install chromium
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Playwright browsers"
    exit 1
fi
echo ""

# Setup environment file
echo "[3/5] Setting up environment..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo ".env file created! Please edit it and set your API_KEY"
        echo "Opening .env file..."
        ${EDITOR:-nano} .env
    else
        echo "WARNING: .env.example not found"
    fi
else
    echo ".env file already exists"
fi
echo ""

# Start server
echo "[5/5] Starting server..."
echo ""
echo "========================================"
echo "Server is starting..."
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python3 api_server.py
