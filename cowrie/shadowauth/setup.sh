#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

CFG="$ROOT_DIR/etc/cowrie.cfg"
DIST="$ROOT_DIR/src/cowrie/data/etc/cowrie.cfg.dist"

echo "[*] Configuring ShadowAuth honeypot..."

# Create configuration directory
mkdir -p "$ROOT_DIR/etc"

# Create cowrie.cfg from the default template if it doesn't exist
if [ ! -f "$CFG" ]; then
    cp "$DIST" "$CFG"
fi

#############################################
# contents_path
#############################################

if grep -q "^contents_path" "$CFG"; then
    sed -i 's|^contents_path.*|contents_path = honeyfs|' "$CFG"
else
    sed -i '/^#sensor_name/a contents_path = honeyfs' "$CFG"
fi

#############################################
# hostname
#############################################

if grep -q "^hostname" "$CFG"; then
    sed -i 's|^hostname.*|hostname = auth-node-01|' "$CFG"
else
    echo "hostname = auth-node-01" >> "$CFG"
fi

#############################################
# filesystem
#############################################

if grep -q "^filesystem" "$CFG"; then
    sed -i 's|^filesystem.*|filesystem = shadowauth/fs-banco-andino.pickle|' "$CFG"
else
    sed -i '/# File in the Python pickle format containing the virtual filesystem./a filesystem = shadowauth/fs-banco-andino.pickle' "$CFG"
fi

#############################################
# Summary
#############################################

echo
echo "[✓] ShadowAuth configured successfully."
echo
echo "Current configuration:"
grep -E "^(contents_path|hostname|filesystem)" "$CFG"

echo
echo "Next steps:"
echo
echo "1. Create the virtual environment (only the first time):"
echo "   python3 -m venv venv"
echo
echo "2. Activate it:"
echo "   source venv/bin/activate"
echo
echo "3. Install Cowrie:"
echo "   pip install -U pip"
echo "   pip install -e ."
echo
echo "4. Start the honeypot:"
echo "   python -m cowrie.scripts.cowrie start"