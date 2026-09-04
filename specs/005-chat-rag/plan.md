# Implementation Plan: Chat Widget (005-chat-rag)

**Branch**: `005-chat-rag` | **Date**: 2026-09-04 | **Spec**: [spec.md](./spec.md)

---

## Confirmed Decisions (from user clarification)

- `RAG_API_KEY` → GitHub Secret `RAG_API_KEY` → env var → `chat.py` injects at build
- Data source → ONLY `rag.aldof.duckdns.org/search` (no direct OKF `.specify/` query)
- Sources display → YES, show `data.sources` as citation links in chat UI
- Fallback when RAG down → show error: "Sorry, I encountered an error..."
- `~/dev/okf-home-lab/` stays as-is (no rename); it IS the RAG service

---

## Fix List (current bugs in hooks/chat.py)

| # | Bug | Fix | Line |
|---|-----|-----|------|
| 1 | `CSS_NAME = "assets/css/chat.js"` writes wrong filename | Change to `"assets/css/chat.css"` | 19 |
| 2 | `{{RAG_API_KEY}}` placeholder not replaced at build | Read `os.environ.get("RAG_API_KEY")`, replace in JS string before emit | 328 (JS) |
| 3 | `data.sources` only logged, not shown | Add citation links below AI message in chat widget | JS: after `addMessage()` |
| 4 | `deploy.yml` doesn't pass RAG_API_KEY | Add `env:` to build steps with `RAG_API_KEY: ${{ secrets.RAG_API_KEY }}` | deploy.yml |

---

## Verification Steps

1. `curl -s -w "%{http_code}" https://aldo-f.github.io/assets/css/chat.css` → 200
2. `curl -s -w "%{http_code}" https://aldo-f.github.io/assets/javascripts/chat.js` → 200 (already OK)
3. Live site: open chat, ask question → shows `data.answer` + sources links
4. Block RAG endpoint (simulate down) → chat shows error message
