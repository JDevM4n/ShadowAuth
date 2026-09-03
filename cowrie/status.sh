#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT_DIR"

if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found."
    exit 1
fi

source venv/bin/activate

python -m cowrie.scripts.cowrie status