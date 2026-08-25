<!--
SYNC IMPACT REPORT
Version change: (none) → 1.0.0
Modified principles: n/a (initial ratification)
Added sections: Core Principles (I–V), Security & Secrets, Development Workflow, Governance
Removed sections: none
Follow-up TODOs: none
-->

# Passive Income Orchestrator Constitution

## Core Principles

### I. Simplicity First (KISS)

The system MUST remain a small set of plain files a single person can fully
understand in one sitting. No frameworks, no databases, no queues: one Python
orchestrator, one JSONC credential file, one provider registry, one compose
file. A feature that adds a dependency or an abstraction layer MUST justify
itself against the simplest alternative that works.

### II. Single Source of Truth (DRY)

Every fact about providers lives in exactly one place:
`providers/provider.json` is the only registry of supported providers and their
images; `credentials.jsonc` is the only store of secrets; `docker-compose.yml`
is the only deployment description. Duplicating any of these into scripts,
docs, or code is a defect.

### III. Secrets Never Enter Git

Real credentials MUST NOT appear in tracked files. `credentials.jsonc` ships
only with placeholder values; operators fill it locally. `.gitignore` MUST keep
any file containing real secrets untracked. Provider credentials belong in the
credential file or Docker secrets — never in environment variables committed
to the repo, never in logs.

### IV. Verify Against Real Runtime

A change is done when it has been exercised on the actual Docker runtime of
this host — containers built and started, health endpoint curled, management
actions observed — not merely syntax-checked or run inside a virtualenv.
Static checks (`docker compose config`, JSON parsing) are necessary but never
sufficient.

### V. Pinned, Minimal Images

Docker images MUST be pinned by tag (or digest for rolling images); `:latest`
is forbidden. Base images MUST be the smallest that satisfy the function.
Every added image increases attack surface and update burden on the Pi 5 and
MUST earn its place.

## Security & Secrets

- The orchestrator holds a mounted Docker socket; it therefore effectively has
  root-equivalent access on the host. Its code MUST be minimal, readable, and
  reviewed with that in mind.
- Dashboard/health endpoints MUST stay LAN-local (bound port, not routed
  through Traefik publicly) unless explicitly protected later.
- Credential rotation instructions belong in CONTRIBUTING.md so leaks have a
  documented response path.

## Development Workflow

1. Spec-driven: features are specified under `specs/<NNN>-<name>/` before code
   changes; the spec states goal, constraints, and out-of-scope items.
2. Test-first where testable without live provider accounts: static contract
   tests (compose validity, registry consistency, credential placeholders)
   run via `tests/run_tests.py` with plain `python3`.
3. Runtime verification per Principle IV before merging to `master`.
4. Every commit keeps README honest: documented behavior = actual behavior.

## Governance

This constitution supersedes ad-hoc practice. Amendments require: a written
rationale in the commit message, a semver bump of this document (MAJOR =
principle removed/redefined, MINOR = new principle/section, PATCH = wording),
and a Sync Impact Report prepended as an HTML comment. Compliance is checked
during review of every PR; complexity that cannot cite a principle is rejected.

**Version**: 1.0.0 | **Ratified**: 2026-08-22 | **Last Amended**: 2026-08-22
