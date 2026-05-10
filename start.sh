#!/bin/bash

###############################################################################
# Smart Budget Planner - START SCRIPT
# This script handles:
# - Checking dependencies
# - Initializing database
# - Starting the Flask application
###############################################################################

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    🚀 Smart Budget Planner - Startup Script${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# ============================================================================
# STEP 1: Check if Python is installed
# ============================================================================
echo -e "${YELLOW}[1/5]${NC} Checking Python installation..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi
echo ""

# ============================================================================
# STEP 2: Build and prepare project
# ============================================================================
echo -e "${YELLOW}[2/5]${NC} Building and preparing project..."

# Create necessary directories
mkdir -p "$SCRIPT_DIR/templates" 2>/dev/null
mkdir -p "$SCRIPT_DIR/static/css" 2>/dev/null
mkdir -p "$SCRIPT_DIR/static/js" 2>/dev/null

# Verify frontend files exist
FRONTEND_FILES=(
    "$SCRIPT_DIR/templates/index.html"
    "$SCRIPT_DIR/static/css/style.css"
    "$SCRIPT_DIR/static/js/script.js"
)

MISSING_FILES=0
for file in "${FRONTEND_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗${NC} Missing: $(basename $file)"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -gt 0 ]; then
    echo -e "${RED}✗${NC} Frontend files are incomplete!"
    echo "Required files:"
    echo "  - templates/index.html"
    echo "  - static/css/style.css"
    echo "  - static/js/script.js"
    exit 1
fi

# Verify core application files
if [ ! -f "$SCRIPT_DIR/app.py" ]; then
    echo -e "${RED}✗${NC} app.py not found!"
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/database.py" ]; then
    echo -e "${RED}✗${NC} database.py not found!"
    exit 1
fi

echo -e "${GREEN}✓${NC} Project structure verified"
echo -e "${GREEN}✓${NC} All frontend files present"
echo -e "${GREEN}✓${NC} Core application files found"
echo ""

# ============================================================================
# STEP 3: Check and install dependencies
# ============================================================================
echo -e "${YELLOW}[3/5]${NC} Checking Python dependencies..."

# Check if requirements.txt exists
if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo -e "${RED}✗${NC} requirements.txt not found!"
    exit 1
fi

# Check if dependencies are installed
$PYTHON_CMD -c "import flask, pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠${NC} Installing required packages..."
    
    # Try to install requirements
    if $PYTHON_CMD -m pip install -r "$SCRIPT_DIR/requirements.txt" &> /dev/null; then
        echo -e "${GREEN}✓${NC} Dependencies installed successfully"
    else
        echo -e "${RED}✗${NC} Failed to install dependencies"
        echo "Try running: pip install -r requirements.txt"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} All dependencies are installed"
fi
echo ""

# ============================================================================
# STEP 4: Initialize database
# ============================================================================
echo -e "${YELLOW}[4/5]${NC} Initializing database..."

if [ ! -f "$SCRIPT_DIR/database.db" ]; then
    echo -e "${YELLOW}⚠${NC} Database not found. Creating..."
    
    if $PYTHON_CMD "$SCRIPT_DIR/database.py" &> /dev/null; then
        echo -e "${GREEN}✓${NC} Database initialized successfully"
    else
        echo -e "${RED}✗${NC} Failed to initialize database"
        echo "Try running manually: python database.py"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} Database already exists"
fi
echo ""

# ============================================================================
# STEP 5: Start the Flask application
# ============================================================================
echo -e "${YELLOW}[5/5]${NC} Starting Flask application..."
echo ""

# Check if port 5000 is already in use
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${RED}✗${NC} Port 5000 is already in use!"
    echo ""
    echo "Options:"
    echo "1. Kill the process: lsof -ti:5000 | xargs kill -9"
    echo "2. Use a different port by editing app.py"
    exit 1
fi

# Start the application
echo -e "${GREEN}✓${NC} Starting application..."
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✨ Smart Budget Planner is running!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "📱 Open your browser and navigate to:"
echo -e "   ${GREEN}http://localhost:5000${NC}"
echo ""
echo -e "⏹️  To stop the application, press: ${YELLOW}Ctrl + C${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Change to script directory before running
cd "$SCRIPT_DIR"

# Run the Flask app
$PYTHON_CMD app.py
