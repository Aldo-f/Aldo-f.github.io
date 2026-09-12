# AGENTS.md — Passive Income Orchestrator (PINO)

One reconciler that keeps passive-income provider containers running on a Raspberry Pi 5. Driven by two config files: `providers/provider.json` (registry) + `credentials.local.jsonc` (secrets). KISS + DRY by constitution (see `.specify/memory/constitution.md`).

## Structure

```
06-apps-passive-income/
├── orchestrator.py           # 60s reconcile loop: registry × credentials → docker containers
├── providers/provider.json   # Single source of truth: which providers exist, enabled?, image pin
├── credentials.jsonc         # Placeholders only (git-safe)
├── compose.local.example.yml # Overlay template for real credentials
├── Dockerfile                # python:3.11-slim + static docker-cli, zero pip packages
├── docker-compose.yml        # One service: pino-server on :4747
├── tests/run_tests.py        # Static contract tests (plain python3, no venv)
├── .specify/                 # Spec-kit governance
└── specs/                    # Feature specs
```

Supported providers: **honeygain**, **traffmonetizer** (`earnapp` dropped — upstream image vanished).

## Commands

```bash
python3 tests/run_tests.py          # static contracts, expect exit 0
docker compose up -d --build        # start dashboard + orchestrator
curl http://127.0.0.1:4747/         # dashboard → HTTP 200
docker logs -f pino_orchestrator    # watch per-provider decisions
```

## Agent Rules

- **Never modify configs directly** — use the web form on :4747 or `credentials.local.jsonc`
- **Real secrets live in** `~/.config/pino/credentials.local.jsonc` (mode 0600), never in git
- **Adding a provider** = one registry entry + one handler function + one line in `HANDLERS`
- **Port 4747 is LAN-only** — deliberately not routed through Traefik
- **Parent-child deploy**: Pi5 is the editor; children (pi3) are deploy-only checkouts via `./deploy.sh`

## Verification

After any change:
1. `python3 tests/run_tests.py` — exit 0
2. `docker ps --filter "name=pino_"` — containers running
3. `curl -s http://localhost:4747/health` — HTTP 200
4. Real container verification against live runtime