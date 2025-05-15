#!/bin/bash

set -e

VENV_PATH="/project/workspace/sp500/.venv"
REQ_FILE="/project/workspace/sp500/requirements.txt"

echo "🔧 Checking for Python virtual environment at $VENV_PATH ..."

if [ ! -d "$VENV_PATH" ]; then
  echo "🔧 Creating Python virtual environment at ./.venv ..."
  python3 -m venv "$VENV_PATH"
  echo "✅ Virtual environment created"
else
  echo "✅ Virtual environment already exists"
fi

echo "📦 Activating virtual environment and checking for requirements..."

# Activate the virtual environment in this script context
source "$VENV_PATH/bin/activate"

# Wait for requirements.txt to be mounted (in case of delay)
for i in {1..10}; do
  if [ -f "$REQ_FILE" ]; then
    echo "📦 Found requirements.txt"
    break
  fi
  echo "⏳ Waiting for requirements.txt to appear..."
  sleep 1
done

# Install dependencies if the file exists
if [ -f "$REQ_FILE" ]; then
  echo "📦 Installing Python dependencies..."
  pip install --upgrade pip
  pip install -r "$REQ_FILE"
else
  echo "⚠️ No requirements.txt found — skipping installation."
fi

echo "🎉 Environment is ready. Run: source .venv/bin/activate to use it."

# Execute the main Docker command (e.g., sshd -D)
exec "$@"
