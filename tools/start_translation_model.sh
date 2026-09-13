#!/usr/bin/env bash
# Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell
set -euo pipefail

# This helper is for disposable GitHub-hosted Linux runners, never a user's PC.
test "${GITHUB_ACTIONS:-}" = true
test "${RUNNER_OS:-}" = Linux
archive="$RUNNER_TEMP/ollama.tar.zst"
curl --fail --location --retry 3 \
  https://github.com/ollama/ollama/releases/download/v0.34.0/ollama-linux-amd64.tar.zst \
  --output "$archive"
echo "cf95886728959aa09910bb34de5cca1cc5a8f68003b5597197d3f2c2d57c0804  $archive" | sha256sum --check
mkdir -p "$RUNNER_TEMP/ollama-runtime"
tar --zstd -xf "$archive" -C "$RUNNER_TEMP/ollama-runtime"
export PATH="$RUNNER_TEMP/ollama-runtime/bin:$PATH"
export OLLAMA_HOST=127.0.0.1:11434
export OLLAMA_MODELS="$RUNNER_TEMP/translation-models"
export OLLAMA_NO_CLOUD=1
ollama serve > "$RUNNER_TEMP/translation-model.log" 2>&1 &
for attempt in $(seq 1 30); do
  if curl --fail --silent http://127.0.0.1:11434/api/tags >/dev/null; then break; fi
  sleep 1
done
ollama pull translategemma:4b
python - <<'PY'
import json, sys, urllib.request
sys.path.insert(0, 'tools')
from translate_docs import MODEL, MODEL_DIGEST
with urllib.request.urlopen('http://127.0.0.1:11434/api/tags') as response:
    models = json.load(response)['models']
assert any(m['name'] == MODEL and m['digest'] == MODEL_DIGEST for m in models), 'Model digest changed; review the new model before use'
print('Pinned local translation model verified; no cloud inference')
PY
