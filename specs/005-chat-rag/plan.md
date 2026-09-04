# Plan: Chat Integration using RAG (005-chat-rag)

**Status**: Confirmed — all clarifications received 2026-09-04
**Branch**: `005-chat-rag`
**Repo**: `06-apps-aldo-f-github-io` + `~/dev/okf-home-lab` (RAG service)

---

## Goal (clear)

Floating chat widget on `aldo-f.github.io` connects to RAG endpoint at `rag.aldof.duckdns.org/search`. RAG service (`okf-home-lab`) provides data; docs site consumes.

---

## Confirmed Decisions

| # | Decision | Source / Note |
|---|----------|---------------|
| 1 | `RAG_API_KEY` | GitHub Secret `RAG_API_KEY` → env var → `chat.py` injects at build |
| 2 | Data source | ONLY `rag.aldof.duckdns.org/search`; no direct OKF `.specify/` query |
| 3 | Sources in UI | YES — show `data.sources` as citation links below AI message |
| 4 | Fallback (RAG down) | Show error message (current JS already does this) |
| 5 | Key storage | `.env` file in `okf-home-lab/`; `.env` NOT in git (`.gitignore`ed); `.env.example` with command; NO logging to docker/logs (security) |
| 6 | Auto-gen | `rag_api.py` creates `RAG_API_KEY='aido_rag_'+secrets.token_hex(16)` if `.env` missing; writes to `.env` only |
| 7 | Service architecture | `~/dev/okf-home-lab/` is native Python (not docker); stays at root; root cleaned to `docs/`, `rag/`, `scripts/`, `tests/`; docs/docs files moved to `docs/root/` |
| 8 | URL / routing | `rag.aldof.duckdns.org` served via Traefik (existing) |

---

## Implementation Order

1. Fix `hooks/chat.py`: `CSS_NAME` (`chat.js`→`chat.css`); inject `RAG_API_KEY` from env
2. Update `deploy.yml`: pass `RAG_API_KEY` secret to build
3. Set GitHub Secret `RAG_API_KEY` (manual, requires auth)
4. Add `rag_api.py` auto-gen snippet (`secrets.token_hex(16)`); `.env` creation
5. Clean `okf-home-lab/` root: move docs to `docs/root/`; add `.gitignore`; `.env.example`
6. Verify build passes; verify `assets/css/chat.css` 200; verify chat gets answer + sources

---

## Security Constraints (hard rules)

- `.env` never in git
- Key never in logs / docker output / console
- User gets key ONLY from `.env` file (manual read)
- Auto-gen writes to `.env`, never to stdout/stderr/log

---

## Verification (post-implementation)

- `curl -w "%{http_code}"` → 200 for chat.js and chat.css
- Live site: chat open → POST to RAG → answer + citations shown
- `.env` exists with `aido_rag_*`; `git status` shows `.env` ignored
