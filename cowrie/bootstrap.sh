#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo
echo "=============================================="
echo "       ShadowAuth Bootstrap Installer"
echo "=============================================="
echo

#############################################
# Check Python
#############################################

echo "[1/7] Checking Python..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] Python 3 is not installed."
    exit 1
fi

echo "    ✓ Python detected."

#############################################
# Verify location
#############################################

echo
echo "[2/7] Verifying project..."

if [ ! -f "$ROOT_DIR/pyproject.toml" ]; then
    echo "[ERROR] This script must be executed from the Cowrie root directory."
    exit 1
fi

echo "    ✓ Project structure verified."

#############################################
# Configure ShadowAuth
#############################################

echo
echo "[3/7] Configuring ShadowAuth..."

bash "$ROOT_DIR/shadowauth/setup.sh"

#############################################
# Create Virtual Environment
#############################################

echo
echo "[4/7] Preparing virtual environment..."

if [ ! -d "$ROOT_DIR/venv" ]; then
    python3 -m venv "$ROOT_DIR/venv"
    echo "    ✓ Virtual environment created."
else
    echo "    ✓ Virtual environment already exists."
fi

#############################################
# Activate Virtual Environment
#############################################

echo
echo "[5/7] Installing dependencies..."

source "$ROOT_DIR/venv/bin/activate"

python -m pip install --upgrade \
    pip \
    setuptools \
    setuptools-scm \
    wheel

#############################################
# Install Cowrie
#############################################

echo
echo "[6/7] Installing Cowrie..."

pip install -e .

python -c "import cowrie" >/dev/null

echo "    ✓ Cowrie installed successfully."

#############################################
# Check system
#############################################

echo
echo "[7/7] Checking system..."

if command -v ss >/dev/null 2>&1; then

    if ss -ltn | grep -q ":2222 "; then

        echo
        echo "[WARNING] Port 2222 is already in use."
        echo "          Another service is currently listening on this port."
        echo "          ShadowAuth may not start until the port becomes available."

    else

        echo "    ✓ Port 2222 is available."

    fi

elif command -v netstat >/dev/null 2>&1; then

    if netstat -ltn 2>/dev/null | grep -q ":2222 "; then

        echo
        echo "[WARNING] Port 2222 is already in use."
        echo "          Another service is currently listening on this port."
        echo "          ShadowAuth may not start until the port becomes available."

    else

        echo "    ✓ Port 2222 is available."

    fi

else

    echo "    ! Unable to verify port availability (ss/netstat not found)."

fi

#############################################
# Git Information
#############################################

if command -v git >/dev/null 2>&1; then

    COMMIT=$(git -C "$ROOT_DIR" rev-parse --short HEAD 2>/dev/null || true)

    if [ -n "$COMMIT" ]; then
        echo
        echo "Current Git Commit:"
        echo "    $COMMIT"
    fi

fi

#############################################
# Finish
#############################################

echo
echo "=============================================="
echo " ShadowAuth installed successfully!"
echo "=============================================="
echo
echo "Next steps:"
echo
echo "1. Activate the virtual environment:"
echo
echo "   source venv/bin/activate"
echo
echo "2. Start the honeypot:"
echo
echo "   python -m cowrie.scripts.cowrie start"
echo
echo "3. Check status:"
echo
echo "   python -m cowrie.scripts.cowrie status"
echo
echo "4. Stop the honeypot:"
echo
echo "   python -m cowrie.scripts.cowrie stop"
echo
echo "Useful log files:"
echo
echo "   var/log/cowrie/cowrie.log"
echo "   var/log/cowrie/cowrie.json"
echo
echo "ShadowAuth is ready."
echo