#!/bin/bash

echo "🚀 Starting Data Strategy Bot - Complete End-to-End Application"
echo ""
echo "This script will start both the backend API and frontend React app"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the frontend directory."
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Check if backend is running
if check_port 8000; then
    echo "✅ Backend API is already running on port 8000"
else
    echo "⚠️  Backend API is not running on port 8000"
    echo "   Please start the backend first:"
    echo "   cd ../src/api && python main.py"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "🌐 Starting React development server..."
echo ""
echo "Frontend will be available at:"
echo "  📱 Local:   http://localhost:5173"
echo "  🌍 Network: http://localhost:5173"
echo ""
echo "Backend API endpoints:"
echo "  📖 API Docs: http://localhost:8000/docs"
echo "  🏥 Health:   http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the development server"
echo ""

# Start the React development server
npm run dev

