# Passive Income Orchestrator (PINO)

One small reconciler that keeps passive-income provider containers running on a
Raspberry Pi 5, driven entirely by two config files. KISS + DRY by constitution
(see `.specify/memory/constitution.md`).

## Status

**Working and verified on the real Docker runtime of this host (2026-08-22).**
Providers ship **disabled with placeholder credentials** — nothing runs until
you configure it.

## What actually exists (complete file list)

| File | Purpose |
|---|---|
| `orchestrator.py` | 60s reconcile loop: registry × credentials → docker containers |
| `providers/provider.json` | **Single source of truth**: which providers exist, enabled?, image pin, required credential keys |
| `credentials.jsonc` | Placeholders only (git-safe). Real values live in `~/.config/pino/credentials.local.jsonc` on each host (mode 0600) |
| `compose.local.example.yml` | Template for mounting your real credentials via compose overlay |
| `Dockerfile` | `python:3.11-slim` + static docker-cli, zero pip packages |
| `docker-compose.yml` | One service: `pino-server` (container `pino_server`) on `:4747` |
| `tests/run_tests.py` | Static contract tests — plain `python3`, no venv/pip |
| `.specify/`, `specs/` | Spec-kit governance: constitution, feature spec, plan, tasks |

Supported providers today: **honeygain**, **traffmonetizer**
(`earnapp` was dropped — its upstream image vanished from Docker Hub; re-add
only with a verified image source).

## Quickstart

```bash
cd ~/dev/06-apps-passive-income
python3 tests/run_tests.py          # static contracts, expect exit 0
docker compose up -d --build        # start dashboard + orchestrator
curl http://127.0.0.1:4747/         # dashboard → HTTP 200 (whoami)
docker logs -f pino_orchestrator    # watch per-provider decisions
```

## Enabling a provider (the only two files you touch)

1. `providers/provider.json` → set `"enabled": true` for the provider.
   (Hot-reloaded every 60s tick; no rebuild needed.)
2. Real credentials → easiest via the web form on :4747 (writes the override
   file for you). CLI alternative: copy placeholders to
   `credentials.local.jsonc`, fill in real values, then:
   ```bash
   cp compose.local.example.yml compose.local.yml
   docker compose -f docker-compose.yml -f compose.local.yml up -d
   ```
   The server prefers the override automatically.

Decision matrix per tick:

| Registry says | Credentials say | Orchestrator does |
|---|---|---|
| disabled | anything | logs `disabled by registry`, no container |
| enabled | placeholder/missing | logs `not configured`, no container |
| enabled | real values | creates/reuses the container (idempotent) |

Adding a *new* provider = one registry entry + one handler function + one
line in `HANDLERS`. Nothing else changes.

## Web dashboard

Open `http://<pi-ip>:4747/` on the LAN:

- **Providers** table: registry enabled?, per-field credential state
  (`set` / `placeholder` / `missing` — never the values), container state
- **Credentials forms**: fill fields, Save → stored in
  `~/.config/pino/credentials.local.jsonc` on that host (mode 0600), used by
  the next tick; empty field = keep stored value; unknown fields rejected
- `/api/status` JSON for scripting, `/healthz` for probes

No auth: LAN-trust model — keep port 4747 off the internet.

## Operations

```bash
docker ps --filter label=managed-by=pino-orchestrator   # what we manage
docker compose down                                      # stop everything
```

Dashboard answers on port **4747 on all interfaces** — `http://<pi-ip>:4747/`
(e.g. http://192.168.0.5:4747/ on this network) plus localhost. Deliberately
not routed through Traefik: LAN-local by design, never exposed publicly.

## Deployment: parent-child (Pi5 → pi3)

- **Pi5 (`192.168.0.5`) is the MAIN**: the editor of itself and its children.
  All edits happen here (or on GitHub); never edit a child directly.
- **Children** (currently `pi3`, `aldo@pi3.local`) are deploy-only checkouts:
  `./deploy.sh` force-syncs them to pushed `master` and rebuilds.

```bash
./deploy.sh                      # update self + pi3
./deploy.sh aldo@other-host      # update self + another child
```

One-time child prerequisites: SSH key authorized for this host, GitHub SSH key
(`ssh -T git@github.com`), Docker + compose plugin.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Spec-driven: changes get a spec under
`specs/` first; tests must pass with plain `python3`; runtime behavior is
verified against real containers before merge.
