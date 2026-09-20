# PROJECT KNOWLEDGE BASE – rag

**Generated:** 2026-09-20

## OVERVIEW
RAG (retrieval‑augmented generation) helpers that power the documentation site search and AI‑assisted content.

## STRUCTURE
```
06-apps-aldo-f-github-io/
└── rag/
    ├── __init__.py        # Public package interface
    ├── okf_rag_serve.py   # API entry point (run with `python -m rag.okf_rag_serve`)
    └── utils.py           # Shared retrieval utilities
```

## WHERE TO LOOK
| File | Purpose |
|------|---------|
| `okf_rag_serve.py` | Starts the local RAG HTTP server |
| `utils.py` | Vector store loading, query handling |

## CONVENTIONS
- RAG server runs on localhost with a configurable port (default 8000).
- All data files live under `rag/data/` (ignored by Git).

## ANTI‑PATTERNS (THIS PROJECT)
- Do not commit large vector‑store binaries – keep them out of the repo.

## COMMANDS
```bash
# Start the RAG service
python -m rag.okf_rag_serve
```
