# Quickstart: Verify the Passive Income Orchestrator End-to-End

Prerequisites: Docker + compose v2 on this Pi 5, this repo cloned.

```bash
cd ~/dev/06-apps-passive-income

# 1. Static contract tests (plain python3, no venv)
python3 tests/run_tests.py            # expect: all PASS, exit 0

# 2. Build & start
docker compose up -d --build          # expect: 2 containers created

# 3. Runtime evidence
docker ps --filter name=pino_ --filter name=passive-income-dashboard
#   expect both Up
curl -s http://localhost:4747/health  # hmm — whoami has no /health!
```

> NOTE: whoami answers every path with headers echoing the request; there is
> no dedicated health endpoint. Our verification therefore checks:
> `curl -s http://localhost:4747/` returns 200 + whoami headers/body.

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4747/   # expect 200

# 4. Orchestrator behavior evidence (placeholder creds → safe idle)
docker logs pino_orchestrator 2>&1 | tail -10
#   expect lines like:
#   [INFO] honeygain: disabled by registry
#   [INFO] earnapp: not configured (placeholder)
#   ...and NO crash/restart loop (docker ps restart count stays 0)

# 5. Idempotency check
docker compose up -d                  # again → expect "Running"/"up-to-date", no recreate
```

Tear down / leave clean:

```bash
docker compose down                   # removes containers, keeps images cached
```

Expected total time: < 2 min after first build.
