#!/bin/bash

###############################################################################
# Smart Budget Planner - UNIVERSAL CONTROL SCRIPT
# Usage: ./run.sh [start|stop|restart|status]
###############################################################################

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Default command
COMMAND="${1:-help}"

# ============================================================================
# FUNCTION: Display help
# ============================================================================
show_help() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}    Smart Budget Planner - Control Script${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Usage: ./run.sh [command]"
    echo ""
    echo "Commands:"
    echo -e "  ${GREEN}start${NC}      - Start the application"
    echo -e "  ${GREEN}stop${NC}       - Stop the application"
    echo -e "  ${GREEN}restart${NC}    - Restart the application"
    echo -e "  ${GREEN}status${NC}     - Check application status"
    echo -e "  ${GREEN}help${NC}       - Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run.sh start       # Start the app"
    echo "  ./run.sh stop        # Stop the app"
    echo "  ./run.sh restart     # Restart the app"
    echo "  ./run.sh status      # Check if running"
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
}

# ============================================================================
# FUNCTION: Start the application
# ============================================================================
start_app() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}    🚀 Starting Smart Budget Planner${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Check if already running
    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${YELLOW}⚠${NC} Application is already running on port 5000"
        echo ""
        echo "Open your browser: http://localhost:5000"
        echo ""
        return 0
    fi
    
    # Run start script
    if [ -f "$SCRIPT_DIR/start.sh" ]; then
        chmod +x "$SCRIPT_DIR/start.sh"
        "$SCRIPT_DIR/start.sh"
    else
        echo -e "${RED}✗${NC} start.sh not found"
        exit 1
    fi
}

# ============================================================================
# FUNCTION: Stop the application
# ============================================================================
stop_app() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}    ⏹️  Stopping Smart Budget Planner${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Run stop script
    if [ -f "$SCRIPT_DIR/stop.sh" ]; then
        chmod +x "$SCRIPT_DIR/stop.sh"
        "$SCRIPT_DIR/stop.sh"
    else
        echo -e "${RED}✗${NC} stop.sh not found"
        exit 1
    fi
}

# ============================================================================
# FUNCTION: Restart the application
# ============================================================================
restart_app() {
    echo -e "${BLUE}Restarting application...${NC}"
    echo ""
    stop_app
    sleep 2
    echo ""
    start_app
}

# ============================================================================
# FUNCTION: Check application status
# ============================================================================
status_app() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}    📊 Smart Budget Planner - Status${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Check if process is running on port 5000
    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        PID=$(lsof -ti:5000)
        echo -e "${GREEN}✓${NC} Application is ${GREEN}RUNNING${NC}"
        echo ""
        echo "Details:"
        echo "  Process ID: $PID"
        echo "  Port: 5000"
        echo "  URL: http://localhost:5000"
        echo ""
        echo -e "Stop command: ${YELLOW}./run.sh stop${NC}"
    else
        echo -e "${RED}✗${NC} Application is ${RED}STOPPED${NC}"
        echo ""
        echo "Start command: ${YELLOW}./run.sh start${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
}

# ============================================================================
# MAIN: Process command
# ============================================================================
case "$COMMAND" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    status)
        status_app
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

exit 0
