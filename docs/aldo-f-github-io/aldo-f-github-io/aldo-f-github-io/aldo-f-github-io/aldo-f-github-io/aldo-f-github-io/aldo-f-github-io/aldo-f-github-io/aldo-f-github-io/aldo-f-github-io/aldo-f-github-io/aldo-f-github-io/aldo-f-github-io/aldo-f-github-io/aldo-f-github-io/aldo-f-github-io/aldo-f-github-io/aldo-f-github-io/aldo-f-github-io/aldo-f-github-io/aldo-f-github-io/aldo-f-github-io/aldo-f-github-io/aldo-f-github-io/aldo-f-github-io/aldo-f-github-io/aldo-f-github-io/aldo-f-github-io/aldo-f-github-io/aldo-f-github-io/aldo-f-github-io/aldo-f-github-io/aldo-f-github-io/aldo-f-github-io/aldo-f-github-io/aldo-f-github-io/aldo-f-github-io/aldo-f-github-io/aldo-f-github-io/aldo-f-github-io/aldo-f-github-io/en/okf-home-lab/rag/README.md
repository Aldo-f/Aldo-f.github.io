---
type: Directory
title: OKF Home Lab RAG
description: Integration of a minimal Retrieval‑Augmented Generation pipeline for querying the OKF knowledge bundle.
resource: ./rag/
tags: [RAG, retrieval, vector-search, knowledge-graph]
sources:
  - id: rag-pipeline-source
    resource: ./rag/rag_query.py
    title: RAG pipeline script
    author: human:aldo
    usage_count: 1
    last_modified: 2026-08-25T09:15:00Z
generated:
  by: human:aldo
  at: 2026-08-25T09:15:00Z
verified:
  - by: human:aldo
    at: 2026-08-25T09:15:00Z
status: stable
stale_after: 2027-02-25T09:15:00Z
---

# RAG Pipeline Documentation

## Overview
This directory contains a minimal Retrieval‑Augmented Generation (RAG) pipeline that enables natural‑language queries over the OKF home‑lab knowledge bundle.

- **Embedding model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector store**: FAISS (or fallback to NumPy similarity if FAISS unavailable)
- **Query interface**: Simple Python function `query_with_answer`
- **Use case**: Quickly retrieve documentation excerpts and generate concise answers for agents.

## Installation
```bash
# From the OKF home‑lab repo root
cd rag
pip install -r requirements.txt
```

## Running a query
```python
from rag_query import OKFRAGPipeline
pipeline = OKFRAGPipeline('..')  # Path to the OKF bundle root
result = pipeline.query_with_answer('What is the Jellyfin health‑check command?')
print(result['answer'])
```

## Expected output (example)
```
Answer:
Based on the documentation:
curl -fsS -m 5 http://127.0.0.1:8096/health

Confidence: 0.92
Sources:
1. Jellyfin Health Check (Attested Computation)
```

## Limitations & Future Work
- Currently returns the most relevant snippet as the answer.  
- Future versions could integrate an LLM (e.g., Ollama, llama.cpp) for richer generation.
- Support for incremental indexing as new documentation is added.

## Verification
- Run `python -m okf.validate okf-bundle/` (a custom validation script you may implement) to ensure every concept file contains valid front‑matter and required fields.
- Execute the script and verify it returns a non-empty answer with a confidence score.

## Provider switching & RAG API

The pipeline reads `hermes config get memory.provider` at startup:

- `mem0` → documents are indexed into the Mem0 Platform (collection `okf_rag`;
  requires `MEM0_API_KEY` in the env or `~/.hermes/.env`). Search runs server-side
  via `rag/mem0_store.py`.
- anything else → local FAISS index.

Switch providers:

```bash
hermes config set memory.provider mem0   # or faiss
```

Remote API (FastAPI, port 8000):

```bash
./scripts/run_rag_api.sh
curl -s -X POST http://127.0.0.1:8000/search \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is the Jellyfin health-check command?", "k": 3}'
```

Tests: `pytest -q tests/rag/test_mem0_integration.py tests/api/test_rag_api.py`
(CI runs these via `.github/workflows/rag-tests.yml`; set the `MEM0_API_KEY`
repo secret to enable the Mem0 test there.)

See `INDEXING.md`: new markdown anywhere in the bundle is picked up on the next run.
