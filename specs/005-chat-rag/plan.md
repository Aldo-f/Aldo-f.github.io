# Implementation Plan: Chat Widget (005-chat-rag)

**Branch**: `005-chat-rag`
**Date**: 2026-09-04
**Spec**: [spec.md](./spec.md)

## Summary

Fix the broken chat widget in `hooks/chat.py` and make it fully functional with RAG API integration. Current state: widget JS emits but `assets/css/chat.css` is missing (hook naming bug), `RAG_API_KEY` not injected, sources not shown in UI.

## Technical Context

| | |
|---|---|
| **Language** | Python 3 (MkDocs hook) + Vanilla JS (widget) |
| **Primary Deps** | MkDocs, mkdocs-material, RAG service |
| **Storage** | In-memory (no persistence) |
| **Testing** | Manual via browser + `curl` |
| **Target** | `aldo-f.github.io` (GitHub Pages) |
| **Project Type** | MkDocs hook + JS widget |
| **Scale** | Single site, no auth |
| **Performance** | RTT to RAG endpoint + render latency |

## Known Gaps (from spec.md)

1. `CSS_NAME` bug — writes `.js` filename, not `.css`
2. `RAG_API_KEY` — placeholder `{{RAG_API_KEY}}` not injected at build time
3. `data.sources` — logged to console, not shown in UI
4. RAG endpoint failure — no fallback behavior defined
5. OKF `.specify/` files — unclear if queried directly or via RAG

## Constitution Check

Not applicable (no external constraints detected — MkDocs build is standard Python tooling).

## Project Structure

```text
06-apps-aldo-f-github-io/
├── hooks/
│   └── chat.py           # FIX: CSS_NAME + RAG_API_KEY injection
├── specs/
│   └── 005-chat-rag/
│       ├── spec.md        # This spec
│       └── plan.md        # This plan
└── site/                  # Generated output (gitignored)
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | — | — |
