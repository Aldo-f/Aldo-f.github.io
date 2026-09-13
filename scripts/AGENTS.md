# PROJECT KNOWLEDGE BASE – scripts

**Generated:** 2026-09-13
**Commit:** {{short_sha}}
**Branch:** {{branch}}

## OVERVIEW
Build automation and utility scripts for the MkDocs documentation hub.

## STRUCTURE
```
scripts/
├── generate_projects.py       # Regenerates projects/ from multirepo config
├── gen_category_index.py      # Generates blog category index pages
├── fix-rag-paths.sh          # Fixes RAG asset paths in built site
├── post_sync.sh              # Post-sync cleanup hook
└── run_rag_api.sh            # Starts RAG API server
```

## WHERE TO LOOK
| Script | Purpose |
|--------|---------|
| `generate_projects.py` | Clone/update imported repos from `mkdocs.yml` multirepo entries |
| `gen_category_index.py` | Generate category overview tables for blog posts |
| `fix-rag-paths.sh` | Fix path references in RAG-generated content |
| `run_rag_api.sh` | Start the RAG FastAPI server |

## CONVENTIONS
- Scripts use the venv Python (`./venv/bin/python`) for consistency.
- Shell scripts have execute permissions (`chmod +x`).
- Output files go to `site/` or current directory, never committed.

## ANTI‑PATTERNS
- Do not commit generated output from these scripts.
- Do not hardcode paths — use relative paths or environment variables.
- Do not add dependencies without updating `requirements.txt`.

## COMMANDS
```bash
# Regenerate projects after mkdocs.yml changes
./venv/bin/python scripts/generate_projects.py

# Generate category indices
./venv/bin/python scripts/gen_category_index.py

# Start RAG API
./scripts/run_rag_api.sh
```
