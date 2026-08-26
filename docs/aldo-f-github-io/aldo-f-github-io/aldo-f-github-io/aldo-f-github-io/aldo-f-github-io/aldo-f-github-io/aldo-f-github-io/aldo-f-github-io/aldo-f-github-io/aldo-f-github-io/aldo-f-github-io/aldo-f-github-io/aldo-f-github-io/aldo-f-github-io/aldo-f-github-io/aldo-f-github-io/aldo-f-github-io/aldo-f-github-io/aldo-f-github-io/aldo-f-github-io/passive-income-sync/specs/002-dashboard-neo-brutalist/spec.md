# Feature Specification: Dashboard v3 — Neo-brutalist UI, Full CRUD, Multi-node

**Branch**: `002-dashboard-neo-brutalist` | **Created**: 2026-08-23 | **Status**: Implemented

## Problem
The v2 dashboard is read-mostly: credentials can be set, but providers can't be
created/edited/removed, containers can't be controlled, pi3 isn't visible, and
the styling is generic dark-mode.

## User Stories

### US1 — Provider CRUD from the browser (P1)
Operator creates, edits, and deletes providers in the UI. Writes land in a
host-local **registry overlay** (`~/.config/pino/providers.local.jsonc`,
shallow per-provider merge over the tracked `providers/provider.json`) so they
survive `deploy.sh`'s `git reset --hard` on children. Image pins validated:
`:latest` and unpinned images rejected.

### US2 — Clear stored credential fields (P2)
Any saved field can be cleared per provider+field; clearing returns it to
"missing" without touching other fields.

### US3 — Container control (P3)
Start / Stop / Purge per managed container. Stop sets a per-provider
`suspended` flag (overlay) so the reconcile loop doesn't fight the operator;
Start clears it. Purge removes the container and suspends.

### US4 — All nodes, one pane (P2)
`nodes.json` lists nodes (self + remotes). `/` aggregates every node's status
(3s timeout, graceful offline card). Action/CRUD forms post directly to each
node over the LAN (browser → node), no proxy hop.

### US5 — Neo-brutalist restyle (P3)
Cream paper background, 2px ink borders, hard offset shadows, chunky uppercase
Space Grotesk (system fallback offline), flat state colors (yellow/pink/green),
no gradients/glassmorphism; ≥44px touch targets; confirm-on-delete.

## Constraints
Stdlib only; secrets never rendered; unknown fields rejected; deletes require
confirmation; overlay files atomic 0600.

## Out of scope
Auth/TLS, earnings display, cross-node secret sync (each node holds its own).
