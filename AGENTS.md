# PROJECT KNOWLEDGE BASE

**Generated:** 2026-09-13
**Commit:** {{short_sha}}
**Branch:** {{branch}}

## OVERVIEW
Personal documentation hub built with MkDocs Material, aggregating multiple repositories via multirepo plugin. Deployed to https://aldo-f.github.io via GitHub Pages.

## STRUCTURE
```
06-apps-aldo-f-github-io/
├── docs/{en,nl}/        # EN/NL documentation sources
├── plugins/             # Custom MkDocs plugins
├── projects/            # Imported external docs (multirepo)
├── hooks/               # Build hooks & utilities
├── rag/                 # Retrieval‑augmented generation helpers
├── tests/               # Test suite for RAG and site utilities
├── overrides/           # MkDocs HTML overrides
├── scripts/             # Build and utility scripts
├── .github/workflows/   # CI workflows
└── ...
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Docs | `docs/` | EN/NL content, blog posts |
| Plugins | `plugins/` | Custom MkDocs extensions |
| Imported docs | `projects/` | Multirepo imports |
| CI | `.github/workflows/` | Deploy pipeline |
| RAG helpers | `rag/` | Retrieval‑augmented generation code |
| Tests | `tests/` | Unit, E2E, and integration tests |
| Scripts | `scripts/` | Build automation, category generation |
| Overrides | `overrides/` | MkDocs template customizations |

## CODE MAP
| Symbol | Type | Location | Refs | Role |
|--------|------|----------|------|------|
| `on_config` | function | `hooks/*.py` | 10+ | MkDocs config hook |
| `on_page_markdown` | function | `hooks/*.py` | 15+ | Page markdown hook |
| `PivotTablePlugin` | class | `plugins/mkdocs_pivot_table/` | 1 | Interactive table plugin |
| `OKFRAGPipeline` | class | `rag/okf_rag_serve.py` | 5 | RAG pipeline entry |
| `_parse_abbreviation` | function | `hooks/abbreviations.py` | 3 | Abbreviation parser |

## CONVENTIONS
- Use `mkdocs.{en,nl}.yml` to build language‑specific sites.
- All configuration lives in `mkdocs.base.yml` and is inherited.
- Documentation files use front‑matter `title:` and optional `draft: true`.
- Blog posts live in `docs/<lang>/blog/posts/`; mirroring = same filename across languages.
- Plugin hooks are pure Python, invoked via `mkdocs` config.
- Secrets stored in `credentials.local.jsonc` (gitignored), never committed.

## ANTI‑PATTERNS (THIS PROJECT)
- Direct edits to `site/` — generated output should never be committed.
- Storing secrets in repo files — use `credentials.local.jsonc` outside version control.
- Duplicate top‑level `404.html` — keep only under `overrides/`.
- Committing `venv/`, `__pycache__/`, or imported repo caches to git.
- Using Jekyll/Hugo concepts here — this is MkDocs.

## UNIQUE STYLES
- Multilingual builds with separate `mkdocs.en.yml` / `mkdocs.nl.yml`.
- `plugins/mkdocs_raw_markdown` provides a custom raw‑markdown parser.
- GitHub Pages deployment triggers on push to `main`.

## COMMANDS
```bash
# Build English site
mkdocs build -f mkdocs.en.yml

# Build Dutch site
mkdocs build -f mkdocs.nl.yml

# Run RAG server
python -m rag.okf_rag_serve

# Run tests
pytest tests/ -q

# Generate category index
./venv/bin/python scripts/gen_category_index.py
```

## NOTES
- Remember to run `./venv/bin/python scripts/generate_projects.py` after updating `mkdocs.yml` multirepo entries.
- Keep `requirements.txt` in sync with Python dependencies used by CI.
- Blog post categories require re-running the category generator after changes.
- Remote repos must keep documentation under a top-level `docs/` folder to be importable.
