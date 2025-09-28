#!/bin/bash

# 🌟 Animal Crossing News Hub - Quick Setup Script 🌟
# This script will help you get started quickly!

echo "🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟"
echo ""
echo "     🏠 Animal Crossing News Hub Setup 🏠"
echo ""
echo "🦝 Tom Nook says: \"Let's get your news site ready!\""
echo "🐕 Isabelle adds: \"This will only take a moment!\""
echo ""
echo "🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟✨🌟"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first!"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your email configuration!"
else
    echo "✅ Environment file already exists"
fi

echo ""
echo "🎉 Setup complete! Here's what to do next:"
echo ""
echo "1. 📧 Edit your .env file with email settings (optional):"
echo "   nano .env"
echo ""
echo "2. 🚀 Start your news hub:"
echo "   source .venv/bin/activate"
echo "   python run.py"
echo ""
echo "   OR use the quick start command:"
echo "   .venv/bin/python run.py"
echo ""
echo "3. 🌐 Open http://localhost:8000 in your browser"
echo ""
echo "💡 Pro tip: The virtual environment needs to be activated!"
echo "🦝 Tom Nook says: \"Happy news reading!\" 🌟"
