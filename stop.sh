#!/bin/bash

###############################################################################
# Smart Budget Planner - STOP SCRIPT
# This script handles:
# - Finding the Flask process running on port 5000
# - Gracefully shutting down the application
###############################################################################

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    ⏹️  Smart Budget Planner - Shutdown Script${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# ============================================================================
# Check if anything is running on port 5000
# ============================================================================
echo -e "${YELLOW}[1/2]${NC} Checking for running processes on port 5000..."

# Try to find process on port 5000
PID=$(lsof -ti:5000)

if [ -z "$PID" ]; then
    echo -e "${YELLOW}⚠${NC} No process found running on port 5000"
    echo "Application may not be running, or running on a different port"
    echo ""
    echo "To find processes on other ports:"
    echo "  lsof -i -P -n | grep LISTEN"
    echo ""
    exit 0
fi

echo -e "${GREEN}✓${NC} Found process (PID: $PID) on port 5000"
echo ""

# ============================================================================
# Stop the process
# ============================================================================
echo -e "${YELLOW}[2/2]${NC} Stopping the application..."
echo ""

# Try graceful shutdown first
kill $PID 2>/dev/null

# Give it a moment to shut down gracefully
sleep 2

# Check if process still exists
if ps -p $PID > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠${NC} Process did not stop gracefully, forcing shutdown..."
    kill -9 $PID 2>/dev/null
    sleep 1
fi

# Verify process is stopped
if ! ps -p $PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Process stopped successfully"
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✨ Smart Budget Planner has been shut down${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "To start again, run: ./start.sh"
    echo ""
else
    echo -e "${RED}✗${NC} Failed to stop process (PID: $PID)"
    echo "Try manual shutdown:"
    echo "  kill -9 $PID"
    exit 1
fi
