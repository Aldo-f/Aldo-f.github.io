# RAG Endpoint Detail (okf-home-lab)

## Service (verified 2026-09-11)

- Systemd unit: `app-okf-rag.service`
- WorkingDirectory / AppDir / EnvFile: `/home/aldo/dev/02-ai-okf-home-lab` (RENAMED)
- Interpreter: `~/dev/02-ai-okf-home-lab/venv_rag/bin/python`
- Bind: `0.0.0.0:8000` (exposed via Traefik at `https://rag.aldof.duckdns.org`)
- Log: `~/logs/okf-rag.log`
- Restart: `systemctl restart app-okf-rag` (NOT `run_rag_api.sh` — it uses wrong interpreter)

## RAG API (`rag_api.py`)

- Auth: `X-API-Key` header; validates against `RAG_API_KEY` env + `.env`
- CORS: `allow_origins=["https://aldo-f.github.io"]`
- Test-mode bypass: when `RAG_API_KEY` is unset or starts with `***`, auth is skipped (for CI).
- Endpoint: `POST /search` → `{question, k}` → `{answer, sources, confidence}`

## Key management

- `.env` path: `~/dev/02-ai-okf-home-lab/.env` (contains `aido_rag_...`)
- Secret: `gh secret set RAG_API_KEY` on `Aldo-f/Aldo-f.github.io` (repo name verified; NOT the site-repo `Aldo-f/Aldo-f.github.io` must match remote)
- `.env` value is masked (`***`) — never log; load into variable (`grep RAG_API_KEY .env | cut -d= -f2-`) for curl/build.

## Build-time injection (`hooks/chat.py`)

- `on_config`: reads `.env`, injects key into `_CHAT_JS_TEMPLATE`, writes assets.
- `on_post_build`: reads `.env` (or env var) and writes `site/assets/javascripts/chat.js`.
- Verify: `grep -c "aido_rag_" site/assets/javascripts/chat.js` must be 2 (two header lines). Zero `{{RAG_API_KEY}}` allowed.
- Build: `RAG_API_KEY=... mkdocs build --strict -f mkdocs.en.yml -d site` for EN and NL.
