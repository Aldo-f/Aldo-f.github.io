# Tasks: Make Orchestrator Deployable and Verified

**Input**: Design documents from `/specs/001-make-passive-income/`
**Prerequisites**: spec.md ✅, plan.md ✅, research.md ✅, quickstart.md ✅
(Contracts dir skipped: internal tool, no external API surface.)

## Phase 1: Setup

- [ ] T001 [P] Create `.gitignore` (credentials.local.jsonc, __pycache__, *.log)
- [ ] T002 [P] Restore `providers/provider.json` from legacy `~/dev/passive-income`, adapted (5 providers, enabled:false, image tags noted for pinning)

## Phase 2: Foundational (blocking)

- [ ] T003 [US3] Write `tests/run_tests.py` FIRST (compose parses; zero `:latest`; every compose image exists in registry or is whoami digest-pinned; credentials.jsonc placeholders-only; provider.json valid JSON with schema fields). Run it → capture RED output against current repo.
- [ ] T004 Create `Dockerfile`: FROM python:3.11-slim (tag pin), install docker-cli static binary into /usr/local/bin, copy orchestrator.py, CMD ["python","-u","orchestrator.py"]

**Checkpoint**: foundation ready

## Phase 3: US1 — One-command deploy (P1) 🎯 MVP

- [ ] T005 Rewrite `docker-compose.yml`: service `pino-orchestrator` (build:., docker.sock mount, ./credentials.jsonc ro-mount, restart: unless-stopped) + `dashboard` (traefik/whoami@sha256 digest, 4747:80, user 1000:1000, NO traefik labels); drop bogus portainer_data volume; drop `version:` key
- [ ] T006 Run quickstart.md evidence block A: build, up -d, docker ps both Up, curl :4747 → 200, logs show safe idle, second up -d idempotent

**Checkpoint**: US1 independently verifiable

## Phase 4: US2 — Registry+credential driven providers (P2)

- [ ] T007 Fix `orchestrator.py`: single `parse_jsonc()` helper; `is_placeholder()` helper; uniform registry gate (enabled AND configured) for ALL providers incl. traffmonetizer/earnapp; HANDLERS dict dispatch; logging to stdout only; keep 60s loop + error backoff
- [ ] T008 Runtime behavior evidence: logs show per-provider decisions in placeholder state; smoke-test container management via a harmless whoami container created by the same code path (`manage_container`), then removed

**Checkpoint**: US2 verifiable without real provider accounts

## Phase 5: US3 — Honest docs & tests (P3)

- [ ] T009 Rewrite README.md to match reality exactly (file list, quickstart, provider matrix)
- [ ] T010 Write CONTRIBUTING.md (spec-kit workflow pointer, KISS/DRY rules, test command, **credential rotation procedure**)
- [ ] T011 Re-run `python3 tests/run_tests.py` → GREEN (exit 0); negative test: temp `:latest` edit → exit 1 → revert

## Phase 6: Polish & Integration

- [ ] T012 Commit feature on master (single-repo flow), push origin master
- [ ] T013 Bump gitlink in `~/dev`, commit + push dev main; fresh-clone submodule init verification
- [ ] T014 Consolidation: archive legacy dirs' unique assets, remove `pino-node-clone` submodule mapping from ~/dev, note `~/dev/passive-income` removal

## Dependencies

T003 before T004/T005 (RED first); T004→T006; T007 after T002 (registry exists);
T011 gates T012; T012→T013→T014.

## Validation Strategy

Every checkpoint uses plain `python3` + real docker commands on this Pi 5 host.
No venv-only verification (Constitution IV).
