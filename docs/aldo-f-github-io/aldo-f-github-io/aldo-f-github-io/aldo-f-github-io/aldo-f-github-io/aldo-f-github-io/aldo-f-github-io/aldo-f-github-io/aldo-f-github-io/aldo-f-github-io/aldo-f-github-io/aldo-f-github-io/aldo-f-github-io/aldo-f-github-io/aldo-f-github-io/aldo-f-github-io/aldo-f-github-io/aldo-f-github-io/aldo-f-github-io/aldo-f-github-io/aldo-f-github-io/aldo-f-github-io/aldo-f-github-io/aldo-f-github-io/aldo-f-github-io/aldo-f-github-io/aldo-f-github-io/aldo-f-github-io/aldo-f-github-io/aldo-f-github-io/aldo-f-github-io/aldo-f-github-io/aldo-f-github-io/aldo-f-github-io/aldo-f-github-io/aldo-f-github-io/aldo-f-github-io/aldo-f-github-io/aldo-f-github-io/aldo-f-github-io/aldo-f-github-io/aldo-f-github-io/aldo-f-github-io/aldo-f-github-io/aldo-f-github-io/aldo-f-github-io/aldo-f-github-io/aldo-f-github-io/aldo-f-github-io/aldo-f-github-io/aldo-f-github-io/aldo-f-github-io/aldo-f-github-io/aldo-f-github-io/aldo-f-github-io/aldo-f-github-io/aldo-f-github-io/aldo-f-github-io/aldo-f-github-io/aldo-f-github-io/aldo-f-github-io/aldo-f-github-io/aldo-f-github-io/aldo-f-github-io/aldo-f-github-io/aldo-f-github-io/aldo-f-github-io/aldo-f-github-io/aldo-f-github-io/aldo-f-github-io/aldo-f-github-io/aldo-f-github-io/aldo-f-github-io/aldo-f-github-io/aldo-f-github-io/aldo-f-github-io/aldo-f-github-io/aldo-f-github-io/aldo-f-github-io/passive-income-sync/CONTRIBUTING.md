# Contributing to PINO

Thanks for keeping this small. The constitution (`.specify/memory/
constitution.md`) is the law; this file is the how-to.

## Ground rules

1. **KISS** — if a change adds a dependency, an abstraction, or a config knob,
   it must justify itself against the simplest alternative.
2. **DRY** — provider facts live only in `providers/provider.json`; secrets
   only in `credentials.local.jsonc`. Duplicated facts are defects.
3. **Secrets never enter git.** Ever. Not in env blocks, not in logs, not in
   tests fixtures.

## Workflow (spec-driven)

```bash
# 1. Spec first — scaffold a feature:
bash .specify/scripts/bash/create-new-feature.sh "<description>"
# then fill specs/<NNN>-<name>/spec.md before writing code

# 2. Tests first where possible: extend tests/run_tests.py, see it FAIL,
#    implement until GREEN:
python3 tests/run_tests.py        # plain python3 — no venv, no pip

# 3. Runtime proof (non-negotiable): exercise the change on real containers
#    and capture the evidence (docker ps / logs / curl output).

# 4. Commit with a message that says what + why.
```

## Adding a provider

1. Pin its image: `docker pull <image> && docker image inspect <image> --format '{{json .RepoDigests}}'`
   → put the `@sha256:...` form in `providers/provider.json`.
2. Add `required_credentials` keys matching what the provider needs.
3. Write one handler function in `orchestrator.py` returning
   `manage_container(name, image, cmd=...)`.
4. Register it in the `HANDLERS` dict. One line.
5. Extend `tests/run_tests.py` expectations; run GREEN; verify at runtime by
   enabling it locally with dummy-but-real-shaped values, observe the created
   container, then disable again.

## Test commands

```bash
python3 tests/run_tests.py                 # static contracts (exit 0 = pass)
python3 -m py_compile orchestrator.py      # syntax
docker compose up -d --build               # runtime
curl -o /dev/null -w '%{http_code}\n' http://127.0.0.1:4747/   # expect 200
```

Negative test (once, after changes): temporarily set any image to `:latest`
and confirm `run_tests.py` exits 1. Revert.

## Credential rotation procedure (if a secret leaks)

1. **Rotate at the source first** — Honeygain: change password in account
   settings; Traffmonetizer: reset the application token in the dashboard.
   Rotation beats cleanup.
2. Purge the secret from git history if it was ever committed:
   `git filter-repo --replace-text <(echo 'SECRET==>[REDACTED]')`
   then force-push and re-clone all working copies.
3. Update `credentials.local.jsonc` on this host with the new value and
   `docker compose -f docker-compose.yml -f compose.local.yml up -d`.
4. Check `docker logs pino_orchestrator` for successful ticks with new creds;
   confirm no container restart loop.
5. If the repo was public at any point, consider every key/password in it
   compromised even if deleted — rotate everything, not just the leaked one.

## Release / deploy

Single-host flow: merge to `master`, push, then on the Pi:

```bash
cd ~/dev/06-apps-passive-income && git pull && docker compose up -d --build
```

The parent monorepo (`~/dev`) pins this repo as a submodule; bump the pin
there after pushing (`git add 06-apps-passive-income && git commit`).
