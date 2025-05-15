#!/bin/bash

set -e  # Exit on error

# Navigate to the root of the project
cd "$(dirname "$0")/.."

VENV_DIR="./venv"
REQ_FILE="./requirements.txt"

echo "🔧 Creating Python virtual environment at $VENV_DIR ..."
python -m venv "$VENV_DIR"

echo "✅ Virtual environment created"

echo "📦 Activating virtual environment and installing requirements..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip

if [ -f "$REQ_FILE" ]; then
  pip install -r "$REQ_FILE"
  echo "✅ Requirements installed from $REQ_FILE"
else
  echo "⚠️ No requirements.txt found, skipping install."
fi

echo "🎉 Done. Run: source venv/bin/activate to start using your virtual environment."
