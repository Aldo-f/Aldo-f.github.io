#!/usr/bin/env bash
# Run the OKF RAG API (bundle root must be the working directory's parent).
set -euo pipefail
BUNDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "${PYTHON:-python3}" -m uvicorn rag_api:app --host 127.0.0.1 --port 8000 --app-dir "$BUNDLE_DIR/rag"
