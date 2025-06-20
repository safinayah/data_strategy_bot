#!/bin/bash

# Data Strategy Bot Installation and Setup Script

echo "🎯 Data Strategy Bot - Installation Script"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies."
    exit 1
fi

# Install package in development mode
echo "🔧 Installing package in development mode..."
pip3 install -e .

if [ $? -ne 0 ]; then
    echo "❌ Failed to install package."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before running the bot."
else
    echo "✅ .env file already exists."
fi

# Run basic tests
echo "🧪 Running basic tests..."
python3 -m pytest tests/ -v

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - OPENAI_API_KEY=your_openai_key"
echo "   - QDRANT_API_KEY=your_qdrant_key" 
echo "   - QDRANT_URL=your_qdrant_url"
echo ""
echo "2. Initialize the knowledge base:"
echo "   data-strategy-bot setup"
echo ""
echo "3. Generate recommendations:"
echo "   data-strategy-bot recommend"
echo ""
echo "4. Test the system:"
echo "   data-strategy-bot test"

