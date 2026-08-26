# Feature Specification: Make Passive Income Orchestrator Deployable and Verified

**Feature Branch**: `001-make-passive-income`

**Created**: 2026-08-22

**Status**: Draft

**Input**: User description: "Make the orchestrator actually runnable end-to-end on
the Pi 5: add the missing Dockerfile and provider registry, fix docker-compose
(pinned images, no fake Traefik route), fix orchestrator bugs, and verify against
the real Docker runtime before calling it done."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One-command deploy (Priority: P1)

An operator clones this repo on the Pi 5, runs `docker compose up -d --build`,
and gets a running orchestrator container plus a dashboard endpoint that answers
on `http://localhost:4747/health`. No manual file creation, no editing code,
no missing-build-context errors.

**Why this priority**: The repo currently cannot start at all (`build: .` with no
Dockerfile). Until one command works, nothing else has value.

**Independent Test**: Run `docker compose up -d --build` in a clean checkout;
`docker ps` shows both containers Up; `curl localhost:4747/health` returns 200.

**Acceptance Scenarios**:

1. **Given** a fresh clone with placeholder credentials, **When**
   `docker compose up -d --build`, **Then** `pino_orchestrator` and
   `passive-income-dashboard` are both Up within 60 seconds.
2. **Given** containers are Up, **When** `curl http://localhost:4747/health`,
   **Then** HTTP 200 with a body naming the node and enabled providers.
3. **Given** containers are Up with placeholder credentials, **When** reading
   orchestrator logs, **Then** it logs each provider as "not configured" and
   stays alive (no crash loop) — placeholders must be safe, not fatal.

---

### User Story 2 - Providers controlled by registry + credentials (Priority: P2)

The operator enables or disables providers by editing exactly two files:
`providers/provider.json` (`enabled: true/false`) and `credentials.jsonc`
(real values). The orchestrator starts only providers that are both enabled in
the registry AND have non-placeholder credentials. Adding a new supported
provider means adding a registry entry plus one handler function — no compose
edits.

**Why this priority**: This is the core behavior that makes it an *orchestrator*
rather than a hand-edited compose file.

**Independent Test**: With honeygain marked enabled but credentials still
placeholders, logs show "honeygain: not configured (placeholder)" and no
honeygain container exists; flipping credentials to dummy-real values and
restarting creates the container.

**Acceptance Scenarios**:

1. **Given** provider.json has `honeygain.enabled = false`, **When** the
   orchestrator runs, **Then** no `honeygain_node` container is created.
2. **Given** honeygain enabled + placeholder credentials, **When** the loop
   runs, **Then** it logs "not configured" and does not create a container.
3. **Given** honeygain enabled + filled credentials, **When** the loop runs,
   **Then** `docker ps` shows `honeygain_node` started with the configured
   device name.
4. **Given** any configuration, **When** the orchestrator restarts, **Then**
   already-running correct containers are left untouched (idempotent).

---

### User Story 3 - Honest documentation and tests (Priority: P3)

README describes only what exists. A test script run with plain `python3`
validates the static contracts: compose parses, every image is pinned (no
`:latest`), provider.json entries match handlers, credentials.jsonc contains
only placeholders in git.

**Why this priority**: Prevents regression to the previous state where docs
promised nine nonexistent files.

**Independent Test**: `python3 tests/run_tests.py` exits 0 on the finished repo;
deliberately re-adding `:latest` makes it exit 1.

**Acceptance Scenarios**:

1. **Given** the finished repo, **When** `python3 tests/run_tests.py`, **Then**
   all checks pass with exit code 0.
2. **Given** someone changes an image tag to `:latest`, **When** tests run,
   **Then** the pin check fails with exit code 1.

## Requirements

### Functional Requirements

- **FR-1**: A Dockerfile MUST build the orchestrator image from a pinned
  python:3.11-slim base with zero pip dependencies.
- **FR-2**: docker-compose.yml MUST define exactly two services:
  `pino-orchestrator` (built locally) and `dashboard` (whoami, pinned digest).
- **FR-3**: The dashboard service MUST NOT carry Traefik labels; exposure is
  LAN-local port 4747 only.
- **FR-4**: The orchestrator MUST read `providers/provider.json` for enable
  state and `credentials.jsonc` for secrets, treating any value starting with
  "your-" or equal to known placeholders as not-configured.
- **FR-5**: Container management (create/start) MUST be idempotent: existing
  healthy containers with the expected image are reused.
- **FR-6**: All logging goes to stdout/stderr (visible via `docker logs`);
  no host filesystem writes.
- **FR-7**: `.gitignore` MUST exclude any local override of credentials so
  real secrets can never be committed.

### Key Entities

- **Provider registry** (`providers/provider.json`): name → {enabled, image,
  config_schema}; single source of truth for what can run.
- **Credentials** (`credentials.jsonc`): system block (nodeName) + per-provider
  secret blocks; placeholders in git, real values local only.
- **Orchestrator**: stateless 60s reconcile loop comparing desired state
  (registry × credentials) to actual Docker state.

### Out of Scope

- Real provider accounts / earnings (operator supplies their own).
- Traefik routing, TLS, or public exposure.
- Earnings analytics, persistence, dashboards beyond whoami health.
- Windows/macOS hosts; anything beyond this Pi 5 Docker runtime.

## Success Criteria

- `docker compose up -d --build` works on a clean clone (US1 evidence).
- Orchestrator log shows correct per-provider decisions for all three
  credential states (off / placeholder / configured).
- `python3 tests/run_tests.py` passes; README matches reality file-for-file.
