#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="/data/models"
MODEL_PATH="$MODEL_DIR/model.gguf"
mkdir -p "$MODEL_DIR"

if [ ! -s "$MODEL_PATH" ]; then
  echo "Downloading GGUF model..."
  curl --location --fail --show-error --retry 5 --retry-delay 5 --retry-all-errors \
    --output "$MODEL_PATH" "$MODEL_URL"
  test -s "$MODEL_PATH"
fi

exec /app/llama.cpp/build/bin/llama-server \
  --model "$MODEL_PATH" \
  --host 0.0.0.0 \
  --port 8080 \
  --ctx-size "${CTX_SIZE:-4096}" \
  --threads "${THREADS:-4}" \
  --parallel "${PARALLEL:-1}" \
  --cors "*"
