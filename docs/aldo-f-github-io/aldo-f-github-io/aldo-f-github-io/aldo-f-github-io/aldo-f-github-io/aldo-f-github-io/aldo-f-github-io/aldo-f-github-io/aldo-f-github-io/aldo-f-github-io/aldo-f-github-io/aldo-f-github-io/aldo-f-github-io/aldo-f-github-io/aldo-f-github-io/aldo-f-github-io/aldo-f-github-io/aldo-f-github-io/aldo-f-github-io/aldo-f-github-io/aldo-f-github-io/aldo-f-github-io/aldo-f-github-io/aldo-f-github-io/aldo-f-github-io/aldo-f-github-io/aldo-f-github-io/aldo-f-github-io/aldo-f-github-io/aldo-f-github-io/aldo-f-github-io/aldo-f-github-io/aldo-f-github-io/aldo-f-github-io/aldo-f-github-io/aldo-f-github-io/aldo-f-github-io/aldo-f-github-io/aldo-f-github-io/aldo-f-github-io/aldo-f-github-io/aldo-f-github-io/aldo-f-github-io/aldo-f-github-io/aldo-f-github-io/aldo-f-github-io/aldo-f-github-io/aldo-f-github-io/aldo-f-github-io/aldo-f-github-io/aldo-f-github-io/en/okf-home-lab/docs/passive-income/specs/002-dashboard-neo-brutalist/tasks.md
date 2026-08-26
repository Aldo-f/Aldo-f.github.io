# Tasks: Dashboard v3

- [ ] T001 [US4] `nodes.json` (tracked): pi5-local + pi3 entries; loader with validation
- [ ] T002 [US1] Registry overlay layer: PINO_REGISTRY_OVERLAY (default ~/.config/pino/providers.local.jsonc), shallow per-provider merge, atomic writer
- [ ] T003 [US1] CRUD API: POST /api/providers, POST /api/providers/<name> (update), POST /api/providers/<name>/delete (+purge-container flag); image-pin validation; allow-listed fields only
- [ ] T004 [US2] POST /api/credentials/clear (provider+field) — deletes one field from overlay creds
- [ ] T005 [US3] POST /api/container/<name>/<start|stop|restart> via docker CLI; state refreshed immediately
- [ ] T006 [US4] Node aggregation: fetch sibling /api/status with 3s timeout; graceful offline cards; action proxying = redirect POST to selected node's endpoint
- [ ] T007 [US5] Neo-brutalist CSS + UI rewrite: node tabs, ALL matrix, CRUD forms/modals, confirm-on-delete, ≥44px targets, Space Grotesk w/ fallback
- [ ] T008 Extend tests/run_tests.py: nodes.json valid, overlay merge unit check, endpoints exist in source scan; GREEN + negative (bad image pin rejected)
- [ ] T009 Runtime verify pi5: create→toggle→delete dummy provider E2E; clear-field roundtrip; container stop/start; pi3 visible in ALL tab; action-on-pi3-from-pi5 works
- [ ] T010 Docs (README web-dashboard section) + commit/push + bump dev pin + open preview for user

Dependencies: T002 before T003/T004; T006 independent of T003; T007 last UI step consuming all APIs; T009 gates T010.
