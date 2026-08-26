# Implementation Plan: Make Passive Income Orchestrator Deployable and Verified

**Branch**: `001-make-passive-income` | **Date**: 2026-08-22 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-make-passive-income/spec.md`

## Summary

Turn the skeleton repo into a working one-command deployment: add the missing
Dockerfile, restore `providers/provider.json` as the single registry, rewrite
docker-compose.yml (two services, pinned images, no fake Traefik route), fix
orchestrator bugs (registry gate for all providers, DRY JSONC parsing,
placeholder-aware credential checks), and prove it on the real Docker runtime
before merging.

## Technical Context

**Language/Version**: Python 3.11 (orchestrator), pinned `python:3.11-slim` base image

**Primary Dependencies**: None — stdlib only (`json`, `subprocess`, `logging`,
`time`, `re`). Docker CLI accessed via mounted socket + `docker` binary inside
the container.

**Storage**: N/A (stateless reconcile loop; Docker itself is the state store)

**Testing**: `tests/run_tests.py`, plain `python3`, stdlib assertions only

**Target Platform**: Raspberry Pi 5 (ARM64, Ubuntu), Docker Engine + compose v2

**Project Type**: containerized background service + tiny static dashboard

**Performance Goals**: reconcile loop tick < 2s; negligible idle CPU between ticks

**Constraints**: ≤ ~50 MB orchestrator image; no pip packages; secrets never in
git (Constitution III); every image pinned by tag/digest (Constitution V)

**Scale/Scope**: 1 host, ≤ 6 providers, 2 containers total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Simplicity First | PASS | No new frameworks/deps; one file per concern |
| II. Single Source of Truth | PASS | provider.json restored as sole registry; compose derives nothing else |
| III. Secrets Never Enter Git | PASS | Placeholders only in git; `.gitignore` blocks local credential overrides |
| IV. Verify Against Real Runtime | GATED | Implementation not done until E2E evidence captured (US1 scenarios) |
| V. Pinned, Minimal Images | PASS | python:3.11-slim tag; whoami by digest; zero `:latest` |

Post-design re-check: no violations introduced. Contracts dir intentionally
skipped — purely internal tool (no external API surface beyond /health).

## Project Structure

### Documentation (this feature)

```
specs/001-make-passive-income/
├── spec.md          # completed
├── plan.md          # this file
├── research.md      # Phase 0 decisions
└── quickstart.md    # Phase 1 validation guide
```

### Source Code (repository root)

```
Dockerfile                    # NEW: pinned base, CMD python -u orchestrator.py
docker-compose.yml            # REWRITE: 2 services, digest-pinned whoami, no traefik labels
providers/provider.json       # RESTORE from legacy ~/dev/passive-income (adapted)
orchestrator.py               # FIX: registry gate, DRY parse_jsonc, placeholder checks
credentials.jsonc             # keep placeholders; becomes gitignored pattern source
.gitignore                    # NEW: credentials.local.jsonc etc.
tests/run_tests.py            # NEW: static contract tests (plain python3)
README.md                     # REWRITE to reality
CONTRIBUTING.md               # NEW incl. credential rotation path
```

## Key Decisions (see research.md for detail)

1. Stdlib-only container (no `requests`) → smaller image, fewer CVEs.
2. whoami pinned by sha256 digest (rolling upstream tags violate Constitution V).
3. Placeholder detection centralized in one `is_placeholder()` helper used by
   all handlers (DRY).
4. Registry gate applies to EVERY provider uniformly — one code path.
