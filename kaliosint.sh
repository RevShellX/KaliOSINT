#!/bin/bash

# KaliOSINT Launcher Script
# Simple script to start KaliOSINT with proper environment

echo "🔍 Starting KaliOSINT - Advanced OSINT Terminal Tool"
echo "=================================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "kaliosint.py" ]; then
    echo "❌ kaliosint.py not found. Please run this script from the KaliOSINT directory."
    exit 1
fi

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
fi

# Check for required packages
echo "📦 Checking dependencies..."
python3 -c "import requests, rich, whois, dns.resolver, phonenumbers, shodan, nmap" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some dependencies are missing. Installing..."
    pip3 install -r requirements.txt
fi

# Create config directory if it doesn't exist
mkdir -p ~/.kaliosint/results ~/.kaliosint/logs

# Check for updates (optional)
if command -v git &> /dev/null && [ -d ".git" ]; then
    echo "🔄 Checking for updates..."
    git fetch origin main --quiet
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse @{u} 2>/dev/null)
    
    if [ "$LOCAL" != "$REMOTE" ] && [ ! -z "$REMOTE" ]; then
        echo "📢 Updates available! Run 'git pull' to update."
    fi
fi

echo "🚀 Launching KaliOSINT..."
echo ""

# Start the application
python3 kaliosint.py "$@"

# Exit message
echo ""
echo "👋 KaliOSINT session ended. Thank you for using KaliOSINT!"
