#!/bin/bash
# GazeAssist Setup Script for Linux/Mac
# Automatically creates virtual environment and installs dependencies

echo ""
echo "====================================================================="
echo "               GazeAssist Smart Setup (Linux/Mac)                   "
echo "====================================================================="
echo ""

# Check Python installation
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python not found!"
    echo "Please install Python 3.9-3.12 from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "Found: $PYTHON_VERSION"

# Extract minor version
if [[ $PYTHON_VERSION =~ Python\ 3\.([0-9]+) ]]; then
    MINOR_VERSION=${BASH_REMATCH[1]}
    
    if [ $MINOR_VERSION -ge 7 ] && [ $MINOR_VERSION -le 12 ]; then
        echo "✅ Python version is compatible!"
    elif [ $MINOR_VERSION -ge 13 ]; then
        echo ""
        echo "❌ WARNING: Python 3.13+ is not supported by MediaPipe!"
        echo "Please install Python 3.11 or 3.12 instead."
        echo "Download from: https://www.python.org/downloads/"
        echo ""
        exit 1
    else
        echo "⚠️  WARNING: Python 3.$MINOR_VERSION is too old. Please use 3.9-3.12"
    fi
fi

echo ""
echo "====================================================================="
echo "Choose installation method:"
echo "  [1] Quick Install (system-wide packages)"
echo "  [2] Virtual Environment (recommended - isolated packages)"
echo "====================================================================="
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "2" ]; then
    echo ""
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created!"
        echo ""
        echo "Activating virtual environment..."
        source venv/bin/activate
        echo "✅ Virtual environment activated!"
        PYTHON_CMD="python"
    else
        echo "❌ Failed to create virtual environment!"
        exit 1
    fi
fi

echo ""
echo "Running smart installer..."
$PYTHON_CMD install_smart.py

if [ $? -eq 0 ]; then
    echo ""
    echo "====================================================================="
    echo "                    Setup Complete!                                  "
    echo "====================================================================="
    echo ""
    
    if [ "$choice" = "2" ]; then
        echo "⚠️  IMPORTANT: Virtual environment is active!"
        echo ""
        echo "To run GazeAssist in the future:"
        echo "  1. Activate environment: source venv/bin/activate"
        echo "  2. Run program: python version1/main.py"
        echo ""
        echo "To deactivate: deactivate"
    else
        echo "To run GazeAssist:"
        echo "  Version 1: python3 version1/main.py"
        echo "  Version 2: python3 version2/enhanced_tracker.py"
    fi
    echo ""
    echo "First time? Test your camera:"
    echo "  python scripts/test_camera.py"
    echo ""
else
    echo ""
    echo "❌ Setup failed! Check errors above."
    echo ""
    exit 1
fi
