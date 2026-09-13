# PROJECT KNOWLEDGE BASE – .github/workflows

**Generated:** 2026-09-13
**Commit:** {{short_sha}}
**Branch:** {{branch}}

## OVERVIEW
GitHub Actions workflows for CI/CD, testing, and deployment.

## STRUCTURE
```
.github/workflows/
├── deploy.yml                  # Main deploy: build EN/NL sites on push to main
├── coverage.yml                # Plugin test coverage (codecov)
├── publish-mkdocs-raw-markdown.yml  # Publish raw-markdown plugin to PyPI
└── rag-tests.yml               # RAG API and mem0 integration tests
```

## WHERE TO LOOK
| Workflow | Purpose |
|----------|---------|
| `deploy.yml` | Triggers on push to `main`; builds EN site (root) and NL site (`/nl/`) |
| `coverage.yml` | Runs plugin tests with coverage; uploads to Codecov |
| `rag-tests.yml` | Runs RAG API tests; requires `MEM0_API_KEY` secret |
| `publish-mkdocs-raw-markdown.yml` | Publishes raw-markdown plugin to PyPI on tag |

## CONVENTIONS
- Deploy workflow uses `--strict` builds to catch warnings.
- NL site is served at `/nl/` path.
- Secrets stored in GitHub repo settings, not in workflow files.
- Coverage upload requires `CODECOV_TOKEN` secret.

## ANTI‑PATTERNS
- Do not add new workflows without updating `requirements.txt` if deps change.
- Do not commit `site/` output — it's generated.
- Do not hardcode secrets in workflow files.

## COMMANDS
```bash
# Trigger manual workflow run
gh workflow run deploy.yml
gh workflow run rag-tests.yml
```
