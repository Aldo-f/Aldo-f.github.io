# SDD Spec: Chat Widget (005-chat-rag)

**Status**: Draft → Implementation Ready (clarifications received 2026-09-04)
**Created**: 2026-09-04
**Branch**: `005-chat-rag`
**Author**: User (Aldo)

---

## Goal

Floating chat widget on `aldo-f.github.io` (MkDocs docs site) that connects to the RAG service at `rag.aldof.duckdns.org`. The RAG service is `~/dev/okf-home-lab/` (FastAPI, stays as-is — no rename).

---

## Clarifications Confirmed

| Item | Decision | Source |
|------|----------|--------|
| `RAG_API_KEY` injection | GitHub Secret `RAG_API_KEY` → env var → injected at build time in `chat.py` | User confirmed |
| Data source | `rag.aldof.duckdns.org` only — no direct OKF `.specify/` query | User confirmed |
| Sources in UI | YES — show `data.sources` inline in chat as citations | User deferred to agent recommendation |
| Fallback | Show error message when RAG endpoint unreachable | User confirmed |
| RAG service location | `~/dev/okf-home-lab/` — no rename needed | User to decide |

---

## User Scenarios & Testing

### User Story 1 - Visitor asks documentation question (P1)

**Why priority P1**: Main value of the feature.

**Independent Test**: Open any docs page, click chat button, type "What is the Blanky main docs?", receive response from RAG showing `data.answer` and `data.sources` citations.

**Acceptance Scenarios**:
1. Given visitor on docs page, When clicking floating button (bottom-right), Then chat panel opens.
2. Given chat open, When user enters a question, Then `fetch` sends POST to `rag.aldof.duckdns.org/search` with correct `Content-Type` and `X-API-Key` (from GitHub Secret).
3. Given successful response, When response contains `data.answer`, Then message appears in chat with sources below.
4. Given missing `data.answer`, Then error message shown ("Sorry, I encountered an error...").
5. Given RAG endpoint unreachable, When user sends message, Then error message shown (current JS already handles this).
6. Given response with `data.sources`, When displaying answer, Then sources rendered as clickable citation links below the message.

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST emit floating chat button and panel via MkDocs hook (`hooks/chat.py`). ✓ (implemented)
- **FR-002**: System MUST inject `RAG_API_KEY` at build time from GitHub Secret `RAG_API_KEY`. Build env var passed via `mkdocs build` environment.
- **FR-003**: System MUST send POST to `https://rag.aldof.duckdns.org/search` with `{question, k: 3}` payload. ✓ (implemented in hook JS — URL confirmed)
- **FR-004**: System MUST display `data.sources` in UI as clickable citation links below the answer message.
- **FR-005**: System MUST emit `assets/css/chat.css` file (currently named `.js` by error — bug fix needed).
- **FR-006**: System MUST show error message when RAG endpoint unreachable. ✓ (already implemented in JS)
- **FR-007**: RAG service (`~/dev/okf-home-lab/rag_api.py`) MUST remain available at `rag.aldof.duckdns.org` (existing FastAPI service).

### Non-Functional Requirements

- **NFR-001**: Chat widget MUST NOT block page load (JS deferred via `DOMContentLoaded`).
- **NFR-002**: API key MUST NOT appear in client-side source code — must be injected server-side in the emitted JS during MkDocs build.

---

## Data Model

No persistent DB needed.

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `messages` | array | In-memory JS | Per-session, not persisted |
| `message.text` | string | User input or `data.answer` | Plain text (no markdown render in v1) |
| `data.answer` | string | RAG response | Displayed as AI message |
| `data.sources` | array | RAG response | Rendered as citation links below answer |

---

## Contracts / API

### RAG Endpoint (existing FastAPI service in `~/dev/okf-home-lab/`)

```
POST https://rag.aldof.duckdns.org/search
Headers: Content-Type: application/json, X-API-Key: <RAG_API_KEY>
Body: {question: string, k: int}
Response: {answer: string, sources?: Array<{title: string, url: string}>}
```

### GitHub Actions Injection

```yaml
# In deploy.yml — pass secret as env var to mkdocs build
- name: Build EN site
  env:
    RAG_API_KEY: ${{ secrets.RAG_API_KEY }}
  run: RAG_API_KEY=$RAG_API_KEY mkdocs build --strict -f mkdocs.en.yml -d site
```

### `chat.py` Build-Time Injection

```python
# In on_config(): replace {{RAG_API_KEY}} placeholder with real key from env
_RAG_API_KEY = os.environ.get("RAG_API_KEY", "UNCONFIGURED")
_CHAT_JS = _CHAT_JS.replace("{{RAG_API_KEY}}", _RAG_API_KEY)
```

---

## Tasks

- [ ] T1: Fix `CSS_NAME` in `hooks/chat.py` — change `chat.js` to `chat.css`
- [ ] T2: Add `RAG_API_KEY` env var injection in `hooks/chat.py` (replace `{{RAG_API_KEY}}` placeholder)
- [ ] T3: Pass `RAG_API_KEY` from GitHub Secret in `deploy.yml` to mkdocs build env
- [ ] T4: Add GitHub Secret `RAG_API_KEY` to repo settings (user action — not scriptable)
- [ ] T5: Render `data.sources` as citation links in chat UI (below AI message)
- [ ] T6: Verify `assets/css/chat.css` loads (HTTP 200 after fix)
- [ ] T7: End-to-end test: open chat, ask question, verify answer + sources appear
- [ ] T8: Verify RAG down → error message shown

---

## Quickstart / Verification

```bash
# 1. Verify chat.css 404 → 200
curl -s -o /dev/null -w "%{http_code}" https://aldo-f.github.io/assets/css/chat.css
# Expected: 200

# 2. Verify chat.js loads
curl -s -o /dev/null -w "%{http_code}" https://aldo-f.github.io/assets/javascripts/chat.js
# Expected: 200

# 3. Open site, click chat, send question, verify:
#    - Network tab: POST to rag.aldof.duckdns.org/search
#    - Chat shows answer + sources
#    - Console: no "UNCONFIGURED" RAG_API_KEY visible

# 4. Verify RAG down error
#    (block rag.aldof.duckdns.org or set fake key)
#    → chat shows: "Sorry, I encountered an error. Please try again."
```
