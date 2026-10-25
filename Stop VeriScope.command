#!/bin/bash
# ==============================================================================
# VeriScope AI — Safe Shutdown Utility
# ==============================================================================

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -f "$SCRIPT_DIR/app.py" ]; then
    PROJECT_DIR="$SCRIPT_DIR"
elif [ -d "$HOME/Desktop/veritas-ai" ]; then
    PROJECT_DIR="$HOME/Desktop/veritas-ai"
else
    PROJECT_DIR="/Users/saloniganvir/Desktop/veritas-ai"
fi

PORT=8502
LOGS_DIR="$PROJECT_DIR/logs"
PID_FILE="$LOGS_DIR/streamlit.pid"

echo "=========================================================="
echo "  VeriScope AI — Shutdown Utility"
echo "=========================================================="

STOPPED=false

# Method 1: Check recorded PID
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Stopping recorded process PID $PID..."
        kill -TERM "$PID" 2>/dev/null || kill -9 "$PID" 2>/dev/null
        rm -f "$PID_FILE"
        STOPPED=true
        echo "✓ Server process $PID terminated safely."
    fi
fi

# Method 2: Check port 8502 listeners
PIDS=$(lsof -nP -tiTCP:$PORT -sTCP:LISTEN 2>/dev/null || true)
if [ -n "$PIDS" ]; then
    echo "Terminating process listening on port $PORT (PID: $PIDS)..."
    for P in $PIDS; do
        kill -TERM "$P" 2>/dev/null || kill -9 "$P" 2>/dev/null
    done
    STOPPED=true
    echo "✓ Port $PORT released."
fi

if [ "$STOPPED" = true ]; then
    echo "✓ VeriScope AI stopped successfully."
else
    echo "ℹ️  No active VeriScope AI process was running on port $PORT."
fi
