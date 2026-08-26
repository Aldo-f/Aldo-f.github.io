# Implementation Plan: Dashboard v3

**Branch**: `002-dashboard-neo-brutalist` | **Date**: 2026-08-23 | **Spec**: [spec.md](./spec.md)

## Summary
Split the monolith: `webui.py` (presentation + HTTP API) beside `orchestrator.py`
(reconcile core), sharing helpers. New `nodes.json`, overlay registry layer,
per-node aggregated rendering, neo-brutalist stylesheet.

## Technical Context
Same as v2 (Python 3.11 stdlib-only, arm64 Pi Docker). New module `webui.py`;
new tracked config `nodes.json`; new static asset `static/style.css`.

## Constitution Check
| Principle | Status |
|---|---|
| I. Simplicity | PASS — one extra module + one css file, no frameworks |
| II. Source of truth | PASS — tracked registry stays canonical; overlay = documented host-local delta |
| III. Secrets | PASS — same 0600 atomic writer; values never rendered |
| IV. Real runtime | GATED until E2E evidence |
| V. Pinned images | ENFORDED by new CRUD validation (no :latest) |

## Key decisions
1. Overlay merge is shallow per-provider (`_deleted` tombstones) — base stays canonical.
2. `suspended` flag reconciles "operator stopped this on purpose" with the loop.
3. Browser posts directly to node URLs (LAN-trust, no server-side proxy).
4. Neo-brutalism per house style: hard shadows/borders, flat state colors,
   Space Grotesk with system fallback (offline-safe).

See [tasks.md](./tasks.md) for the task breakdown.
