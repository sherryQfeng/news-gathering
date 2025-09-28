#!/bin/bash

# 🌟 Animal Crossing News Hub - Easy Start Script 🌟

echo "🌟 Starting Animal Crossing News Hub! 🌟"
echo "🦝 Tom Nook is preparing your cozy news corner..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "🔧 Please run ./setup.sh first!"
    exit 1
fi

# Activate virtual environment and run the app
source .venv/bin/activate && python run.py
