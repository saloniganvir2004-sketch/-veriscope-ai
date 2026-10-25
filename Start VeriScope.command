#!/bin/bash
# ==============================================================================
# VeriScope AI — Intelligence Beyond the Headline
# Automated macOS Launcher
# ==============================================================================

set -e

# Robust directory resolution
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -f "$SCRIPT_DIR/app.py" ]; then
    PROJECT_DIR="$SCRIPT_DIR"
elif [ -d "$HOME/Desktop/veritas-ai" ]; then
    PROJECT_DIR="$HOME/Desktop/veritas-ai"
else
    PROJECT_DIR="/Users/saloniganvir/Desktop/veritas-ai"
fi

cd "$PROJECT_DIR"

PORT=8502
URL="http://localhost:$PORT"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
LOGS_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOGS_DIR/server.log"
PID_FILE="$LOGS_DIR/streamlit.pid"

mkdir -p "$LOGS_DIR"

echo "=========================================================="
echo "  VeriScope AI — Intelligence Beyond the Headline"
echo "  Production Launcher"
echo "=========================================================="
echo "Project Path : $PROJECT_DIR"
echo "Target Port  : $PORT ($URL)"
echo ""

# 1. Environment and file checks
if [ ! -f "$PROJECT_DIR/app.py" ]; then
    echo "❌ Error: app.py not found in $PROJECT_DIR"
    exit 1
fi

if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Error: Virtual environment python not found at $VENV_PYTHON"
    exit 1
fi

PYTHON_VER=$("$VENV_PYTHON" --version 2>&1 || true)
echo "✓ Interpreter: $PYTHON_VER ($VENV_PYTHON)"

# 2. Duplicate-instance protection & port inspection
IS_PORT_LISTENING=false
if lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; then
    IS_PORT_LISTENING=true
fi

if [ "$IS_PORT_LISTENING" = true ]; then
    echo "ℹ️  Port $PORT is currently active. Verifying VeriScope AI status..."
    # Probe whether port is serving Streamlit / VeriScope
    SERVER_RESP=$("$VENV_PYTHON" -c "
import urllib.request, sys
try:
    with urllib.request.urlopen('$URL', timeout=3) as resp:
        content = resp.read(2048).decode('utf-8', errors='ignore')
        if 'streamlit' in content.lower() or 'veriscope' in content.lower() or resp.status == 200:
            sys.exit(0)
except Exception:
    pass
sys.exit(1)
" 2>/dev/null && echo "HEALTHY" || echo "UNKNOWN")

    if [ "$SERVER_RESP" = "HEALTHY" ]; then
        echo "✓ VeriScope AI is already active and healthy at $URL"
        echo "✓ Reusing existing instance (preventing duplicate server processes)."
        echo "Opening $URL in your default browser..."
        open "$URL" 2>/dev/null || true
        echo ""
        echo "VeriScope AI remains active. You can safely close this terminal window."
        exit 0
    fi

    # Fallback inspection: if local socket is restricted by environment sandbox,
    # verify whether the listening process is a Python Streamlit instance
    if lsof -nP -iTCP:$PORT -sTCP:LISTEN 2>/dev/null | grep -qi "Python"; then
        echo "✓ VeriScope AI server process detected on port $PORT."
        echo "✓ Reusing existing healthy instance."
        open "$URL" 2>/dev/null || true
        echo "Opening $URL in your default browser."
        exit 0
    fi

    echo "⚠️  Port $PORT is responding, but not from the expected VeriScope instance."
        echo "    Active process on port $PORT:"
        lsof -nP -iTCP:$PORT -sTCP:LISTEN || true
        echo ""
        echo "Starting VeriScope AI on alternate port 8503..."
        PORT=8503
        URL="http://localhost:$PORT"
    fi

# 3. Clean launch in background
echo "🚀 Starting Streamlit server on port $PORT..."
nohup "$VENV_PYTHON" -m streamlit run "$PROJECT_DIR/app.py" \
    --server.port "$PORT" \
    --server.headless true \
    > "$LOG_FILE" 2>&1 &

APP_PID=$!
echo "$APP_PID" > "$PID_FILE"
echo "✓ Server process started (PID: $APP_PID). Logs: $LOG_FILE"

# 4. Wait for server readiness (up to 12 seconds)
echo -n "Waiting for application readiness..."
READY=false
for i in {1..24}; do
    if lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; then
        READY=true
        break
    fi
    echo -n "."
    sleep 0.5
done
echo ""

if [ "$READY" = true ]; then
    echo "=========================================================="
    echo "✓ VeriScope AI is ONLINE at $URL"
    echo "=========================================================="
    open "$URL" 2>/dev/null || true
    echo "Opening $URL in default browser."
else
    echo "⚠️  Application is initializing in background."
    echo "    Check $LOG_FILE for startup progress."
fi
