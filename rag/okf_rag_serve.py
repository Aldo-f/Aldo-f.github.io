#!/usr/bin/env python3
"""Hermes‑compatible wrapper around the OKF RAG pipeline.
It expects a JSON object on stdin:
{ "question": "...", "k": 3 }
and writes a JSON object on stdout with keys:
answer, confidence, sources.
"""
import sys, json, pathlib

# Append the rag/ dir to import path so rag_query resolves
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from rag_query import OKFRAGPipeline

_pipeline = None
_stamp_path = pathlib.Path(__file__).parent.parent / ".rag_index_stamp"
_last_stamp = None

def get_pipeline():
    global _pipeline, _last_stamp
    current = _stamp_path.stat().st_mtime if _stamp_path.exists() else None
    if _pipeline is None or current != _last_stamp:
        # Re‑load (or build) index
        bundle_root = pathlib.Path(__file__).parent.parent
        _pipeline = OKFRAGPipeline(str(bundle_root))
        _last_stamp = current
    return _pipeline

def main():
    payload = json.load(sys.stdin)
    q = payload.get("question", "")
    k = payload.get("k", 3)
    # rag_query prints progress to stdout; redirect it to stderr so stdout
    # carries only the JSON result.
    real_stdout = sys.stdout
    sys.stdout = sys.stderr
    try:
        result = get_pipeline().query_with_answer(q, k=k)
    finally:
        sys.stdout = real_stdout
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
