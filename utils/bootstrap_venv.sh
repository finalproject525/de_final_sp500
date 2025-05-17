#!/bin/bash
set -e

VENV_PATH="/project/workspace/sp500/.venv"
REQ_FILE="/project/workspace/sp500/requirements.txt"

echo "🔧 Checking for Python virtual environment at $VENV_PATH ..."

# Force recreate if broken
if [ ! -f "$VENV_PATH/bin/activate" ]; then
  echo "🔧 Creating Python virtual environment..."
  rm -rf "$VENV_PATH"
  python3 -m venv "$VENV_PATH"
  echo "✅ Virtual environment created at $VENV_PATH"
else
  echo "✅ Virtual environment already exists"
fi

echo "📦 Activating virtual environment..."
if [ -f "$VENV_PATH/bin/activate" ]; then
  source "$VENV_PATH/bin/activate"
else
  echo "❌ Failed to activate virtualenv — file not found: $VENV_PATH/bin/activate"
  exit 1
fi

# Wait for requirements.txt if needed
for i in {1..10}; do
  if [ -f "$REQ_FILE" ]; then
    echo "📦 Found requirements.txt"
    break
  fi
  echo "⏳ Waiting for requirements.txt to appear..."
  sleep 1
done

# Install dependencies
if [ -f "$REQ_FILE" ]; then
  echo "📦 Installing Python dependencies..."
  pip install --upgrade pip
  pip install -r "$REQ_FILE"
else
  echo "⚠️ No requirements.txt found — skipping installation."
fi

echo "🎉 Environment is ready. Run: source .venv/bin/activate to use it."
