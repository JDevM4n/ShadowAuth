#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

CFG="$ROOT_DIR/etc/cowrie.cfg"

echo "[*] Configuring ShadowAuth honeypot..."

# Create config if it doesn't exist
if [ ! -f "$CFG" ]; then
    cp "$ROOT_DIR/etc/cowrie.cfg.dist" "$CFG"
fi

# contents_path
if grep -q "^contents_path" "$CFG"; then
    sed -i 's|^contents_path.*|contents_path = honeyfs|' "$CFG"
else
    sed -i '/^#sensor_name/a contents_path = honeyfs' "$CFG"
fi

# hostname
if grep -q "^hostname" "$CFG"; then
    sed -i 's|^hostname.*|hostname = auth-node-01|' "$CFG"
else
    echo "hostname = auth-node-01" >> "$CFG"
fi

# filesystem
if grep -q "^filesystem" "$CFG"; then
    sed -i 's|^filesystem.*|filesystem = shadowauth/fs-banco-andino.pickle|' "$CFG"
else
    sed -i '/# filesystem =/a filesystem = shadowauth/fs-banco-andino.pickle' "$CFG"
fi

echo
echo "[✓] ShadowAuth configured successfully."
echo
echo "Configuration:"
grep -E "^(contents_path|hostname|filesystem)" "$CFG"

echo
echo "Start Cowrie:"
echo "source venv/bin/activate"
echo "python -m cowrie.scripts.cowrie restart"
