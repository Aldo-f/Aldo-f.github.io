---
title: Building Nocturna — The Hermes Kanban Control Center
date: 2026-09-14
categories:
  - Home Lab
  - AI Agents
tags:
  - nocturna
  - hermes
  - kanban
  - automation
projects:
  - nocturna
---

# Building Nocturna — The Hermes Kanban Control Center

After months of running Hermes Agent for home-lab automation, I needed a visual way to track, manage, and replay tasks. Nocturna was born: a React + Express kanban board that connects to Hermes in two modes — **Gateway** (HTTP API to a remote instance) or **Local CLI** (spawns the `hermes` binary directly).

<!-- more -->

## Why a separate UI?

Hermes' web UI is great for chat, but automation tasks have lifecycle states (pending → running → complete/blocked) that benefit from a board view. Nocturna adds:

- **Board-scoped tasks**: each board maps to a Hermes kanban board (default: `nocturna`)
- **Instance management**: add SSH, LAN, Gateway, or Local CLI instances
- **Real-time polling**: 3s interval with idle detection
- **Action lifecycle**: complete, block, promote, reopen via single click

## Architecture highlights

| Component | Tech | Purpose |
|-----------|------|---------|
| Backend | Express 5 + TypeScript (ESM) | API routes, auth, instance runner |
| Frontend | React 19 + Vite + Tailwind v4 | Board, columns, cards, drawers |
| Database | node:sqlite (no ORM) | Users, instances, tasks, runs, boards |
| Hermes link | Gateway HTTP / CLI spawn | Two execution modes |

The critical branching: every server route checks `isGatewayActive(instance)` and calls either `gatewayFetch()` (HTTP) or `runCliJson()` (spawns `hermes` binary).

## Development workflow

```bash
npm run dev      # Vite + tsx hot reload
npm run build    # Vite + esbuild → dist/
npm test         # Vitest (unit/integration)
npm run test:e2e # Playwright (starts dev server)
npm run lint     # tsc --noEmit
```

Tests mock the CLI via `NOCTURNA_HERMES_BIN=tests/fake-hermes` pointing to a shell shim.

## Next steps

- [ ] Board templates (scrum, kanban, custom columns)
- [ ] Webhook receiver for external triggers
- [ ] Mobile-responsive board view
- [ ] Export/import board JSON

---

*This post is linked to the **Nocturna** project — click the project link in the sidebar to see all related posts.*