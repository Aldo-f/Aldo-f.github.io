# Phase 0 Research: Deployable Orchestrator

## Decision 1: Base image

- **Decision**: `python:3.11-slim` (tag-pinned), no extra packages.
- **Rationale**: The orchestrator uses only stdlib; the legacy pino-node
  Dockerfile installed `requests` it barely needed. slim ≈ 50 MB on arm64,
  well within budget. Alpine would be smaller but risks musl/ARM quirks for
  zero practical gain here.
- **Alternatives**: `python:3.11-alpine` (smaller, musl risk);
  distroless python (harder to `docker exec` debug on a Pi).

## Decision 2: Pinning the dashboard image

- **Decision**: `traefik/whoami` pinned by sha256 digest, not tag.
- **Rationale**: Constitution V forbids `:latest`; whoami's only moving tags
  are rolling ones (`latest`, `v1.8`), so a digest is the only stable pin.
- **Alternatives**: pin a versioned tag like `v1.8.7` (exists upstream but
  multi-arch coverage must be checked at pull time — digest sidesteps that).
- **Note**: exact digest resolved at build time on this host (arm64) and
  recorded in docker-compose.yml.

## Decision 3: Placeholder credential semantics

- **Decision**: A provider is "not configured" if ANY required field is
  missing, empty, or matches `^your-` / equals `CHANGE_ME` /
  contains "here"/"example.com" placeholder patterns.
- **Rationale**: Existing placeholders ("your-email@example.com",
  "your-password-here") must never reach real providers. One helper,
  `is_placeholder()`, is the single implementation (DRY).
- **Alternatives**: explicit sentinel value comparison only (too brittle if
  users type partial values).

## Decision 4: Registry-driven handler dispatch

- **Decision**: Keep per-provider functions but route them through one
  registry-driven loop: `for name, spec in registry: if enabled and
  configured: HANDLERS[name](...)`. Adding a provider = registry entry + one
  function + one dict entry.
- **Rationale**: Preserves readability of per-provider logic while removing
  the hardcoded name lists (the bug that made traffmonetizer unreachable).
- **Alternatives**: fully generic container-spec compiler from JSON
  (rejected: over-engineered for 5 providers, violates KISS).

## Decision 5: Docker access from inside the orchestrator container

- **Decision**: Mount `/var/run/docker.sock` and call the `docker` CLI via
  subprocess; install docker-cli in the image.
- **Rationale**: Matches existing code shape (subprocess), avoids the Docker
  SDK pip dependency entirely (stdlib-only constraint). docker-cli adds ~60MB… 
  actually significant: use static docker-cli binary (~20 MB compressed,
  ~50 MB unpacked) copied into the slim image in the same stage.
- **Alternatives**: Docker SDK for Python (pip dep — rejected); talking to the
  socket with raw HTTP over unix socket via stdlib (possible but ~80 lines of
  fragile HTTP plumbing — rejected as less simple than shipping docker-cli).

## Legacy asset audit

- `~/dev/passive-income/providers/provider.json`: adopt structure verbatim as
  the base (names/images/schema), extend with credentials mapping notes.
- `~/dev/passive-income/tests/test_dashboard.*`: superseded by
  tests/run_tests.py (their compose path assumptions no longer apply).
- `~/dev/pino-node-clone/Dockerfile`: adopted as starting point, minus the
  unnecessary `requests` install, plus docker-cli.
