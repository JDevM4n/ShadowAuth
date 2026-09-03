#!/bin/bash

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$ROOT_DIR"

tail -f var/log/cowrie/cowrie.log