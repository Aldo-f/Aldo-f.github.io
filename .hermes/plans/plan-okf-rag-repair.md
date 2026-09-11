# OKF RAG Repair Plan

## Goal
Make `aldof.github.io` chat FAB connect to OKF RAG (`rag.aldof.duckdns.org`) with verified TDD steps.

## Current context / assumptions
- `02-ai-okf-home-lab` holds bundle + `.env` (key, hidden as `***`). `06-apps-aldo-f-github-io` holds MkDocs site + `hooks/chat.py`. `rag.aldof.duckdns.org` is live endpoint.
- `hooks/chat.py`: `on_config`/`on_post_build` re-enabled (key injection via `_load_api_key()` reading `.env`). `_load_api_key()` path: `/home/aldo/dev/02-ai-okf-home-lab/.env`.
- `tests/api/test_rag_api.py`: needs local server (`BUNDLE / "rag"`). `tests/test_watcher_map.py`: passes. `tests/e2e_chat_rag.py`: Playwright needs build.
- Secrets: `gh secret` controls `RAG_API_KEY`; build uses `secrets.RAG_API_KEY`.

## Approach
1. Verify `.env` key via `_load_api_key()` (hidden as `***`).
2. Verify `gh secret` exists; if missing set via `gh secret set`.
3. Per-fix loop (TDD): run failing test → fix → run again → commit.
4. End with build (`mkdocs build --strict`) and E2E verification.

## Steps (each verified before next)

### Step 1 — Secret verification
```
gh secret list --repo Aldo-f/06-apps-aldo-f-github-io | grep RAG_API_KEY
```
If empty: `gh secret set RAG_API_KEY --repo ... --body <.env value>`. Verify `echo $?` is 0.

### Step 2 — Hook key injection verified
```
cat /home/aldo/dev/02-ai-okf-home-lab/.env | grep RAG_API_KEY 2>/dev/null || echo "Key hidden"
python3 -c "from hooks.chat import _load_api_key; print('key=', _load_api_key()[:8]+'...')"
```
Expected: key present, non-empty. Commit if changed.

### Step 3 — Test: `tests/test_watcher_map.py` (always)
```
python -m pytest tests/test_watcher_map.py -v
```
Expected: 5 passed. Fix any failure before Step 4.

### Step 4 — `tests/api/test_rag_api.py`
Fix bundle reference first (`BUNDLE` points to `02-ai-okf-home-lab`, not `06-apps-aldo-f-github-io`). After fix:
```
python -m pytest tests/api/test_rag_api.py -v
```
Expected: pass (or clear error with server log). Fix loop until exit 0.

### Step 5 — Build gate
```
RAG_API_KEY=$(grep RAG_API_KEY ~/dev/02-ai-okf-home-lab/.env | cut -d= -f2) mkdocs build --strict -f mkdocs.en.yml -d site
```
Expected: exit 0, site emitted with `assets/javascripts/chat.js` containing real key (not `{{RAG_API_KEY}}`).

### Step 6 — Commit all
```
git add -A && git commit -m "fix(rag): hook + secret + bundle + tests verified" && git push
```

### Open questions / risks
- `.env` key rotation: if `rag.aldof.duckdns.org` changes key, `.env` must update and secret must resync.
- `mem0_store.py`: requires `MEM0_API_KEY`; test may skip. Not a blocker for FAB.
- Playwright (`e2e_chat_rag.py`): needs running site; run after build passes.