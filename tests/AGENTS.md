# PROJECT KNOWLEDGE BASE – tests

**Generated:** 2026-09-20

## OVERVIEW
Test suite for RAG, site utilities, and MkDocs hooks. Uses pytest with subdirectories for different test types.

## STRUCTURE
```
tests/
├── __init__.py
├── test_abbreviations_hook.py   # Hook unit tests
├── test_asset_paths.py          # Asset path verification
├── test_watcher_map.py          # Project watcher tests
├── verify_blog.py               # Blog verification harness
├── e2e/
│   └── test_404_dungeon_multilingual.py  # Playwright E2E tests
├── api/
│   └── test_rag_api.py          # RAG API tests
└── rag/
    └── test_mem0_integration.py # Mem0 storage tests
```

## WHERE TO LOOK
| File | Purpose |
|------|---------|
| `test_abbreviations_hook.py` | Abbreviation hook parsing tests |
| `verify_blog.py` | Blog content validation (run after adding posts) |
| `e2e/test_404_dungeon_multilingual.py` | 404 dungeon language detection tests |
| `api/test_rag_api.py` | RAG HTTP API endpoint tests |
| `rag/test_mem0_integration.py` | Mem0 vector store integration tests |

## CONVENTIONS
- Tests use pytest with `pytest -q` for quick runs.
- E2E tests require `playwright` installed and a browser available.
- RAG tests need `MEM0_API_KEY` env var for Mem0 integration tests.
- Blog verification harness fails if category index is stale.

## ANTI‑PATTERNS
- Do not add test data that bloats the repository — use fixtures.
- Do not run E2E tests in CI without `playwright` installed.
- Do not hardcode paths — use relative paths from test directory.

## COMMANDS
```bash
# Run all tests
pytest tests/ -q

# Run specific test file
pytest tests/test_abbreviations_hook.py -v

# Run E2E tests (requires playwright)
pytest tests/e2e/test_404_dungeon_multilingual.py -v

# Run blog verification
./venv/bin/python tests/verify_blog.py
```
