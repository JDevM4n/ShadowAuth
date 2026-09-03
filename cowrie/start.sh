#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT_DIR"

if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found."
    echo "Run:"
    echo
    echo "    bash bootstrap.sh"
    echo
    exit 1
fi

source venv/bin/activate

echo
echo "=============================================="
echo "        Starting ShadowAuth Honeypot"
echo "=============================================="
echo

python -m cowrie.scripts.cowrie start

echo
python -m cowrie.scripts.cowrie status
echo