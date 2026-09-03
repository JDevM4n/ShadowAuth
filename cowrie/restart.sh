#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT_DIR"

if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found."
    exit 1
fi

source venv/bin/activate

echo
echo "Restarting ShadowAuth..."
echo

python -m cowrie.scripts.cowrie restart

echo

python -m cowrie.scripts.cowrie status

echo