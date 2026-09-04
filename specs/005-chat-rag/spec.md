# SDD Spec: Chat Widget (005-chat-rag)

**Status**: Draft — needs clarification before implementation
**Created**: 2026-09-04
**Branch**: `005-chat-rag`
**Author**: User (Aldo)

---

## Goal (clear / needs clarification)

Built-in floating chat widget in the MkDocs site (`aldo-f.github.io`) that connects to the RAG service (`rag.aldof.duckdns.org/search`).

### Known
- Widget is emitted by `hooks/chat.py` (JS embedded in build output)
- Uses `freeLLM/auto` model concept (from RAG endpoint docs?)
- Calls `https://rag.aldof.duckdns.org/search` with `X-API-Key: {{RAG_API_KEY}}`
- Returns `data.answer` displayed in chat UI
- CSS file (`assets/css/chat.css`) missing — hook writes `.js` filename for CSS output

### Unclear — needs user clarification (NEEDS_CLARIFICATION in spec)
- **FR-01 (NEEDS CLARIFICATION)**: Is `rag.aldof.duckdns.org/search` the ONLY data source, or should the chat also query OKF `.specify/` files (local spec docs) directly?
- **FR-02 (NEEDS CLARIFICATION)**: Where does `RAG_API_KEY` come from? (GitHub Secret `RAG_API_KEY`, `.env` file, build-time injection?)
- **FR-03 (NEEDS CLARIFICATION)**: Should the chat display `data.sources` in the UI? Currently only logs to console.
- **FR-04 (NEEDS CLARIFICATION)**: Should the chat support user authentication, or remain anonymous?

---

## User Scenarios & Testing

### User Story 1 - Visitor asks documentation question (P1)

**Why priority P1**: Main value of the feature.

**Independent Test**: Open any docs page, click chat button, type "What is the Blanky main docs?", receive response from RAG endpoint showing `data.answer`.

**Acceptance Scenarios**:
1. Given visitor on docs page, When clicking floating button (bottom-right), Then chat panel opens.
2. Given chat open, When user enters a question, Then `fetch` sends POST to `rag.aldof.duckdns.org/search` with correct `Content-Type` and `X-API-Key`.
3. Given successful response, When response contains `data.answer`, Then message appears in chat.
4. Given missing `data.answer`, Then error message shown.

---

## Requirements

### Functional Requirements (with clarification markers)

- **FR-001**: System MUST emit floating chat button and panel via MkDocs hook (`hooks/chat.py`). ✓ (implemented)
- **FR-002 (NEEDS CLARIFICATION)**: System MUST inject `RAG_API_KEY` at build time — source: [NEEDS CLARIFICATION: `.env`, GitHub Secret, or config file?]
- **FR-003**: System MUST send POST to `https://rag.aldof.duckdns.org/search` with `{question, k: 3}` payload. ✓ (implemented in hook JS)
- **FR-004 (NEEDS CLARIFICATION)**: System MUST display `data.sources` in UI? [NEEDS CLARIFICATION]
- **FR-005**: System MUST emit `assets/css/chat.css` file (currently named `.js` by error). ✓ (bug — fix needed)
- **FR-006 (NEEDS CLARIFICATION)**: System MUST handle RAG endpoint unreachable — fallback behavior: [NEEDS CLARIFICATION: show error message? redirect to docs?]

---

## Data Model

No persistent DB needed. Key data structures (from `chat.py` JS):

|| Field | Source | Notes |
||-------|--------|-------|
|| `messages` array | In-memory (JS) | Per-session, not persisted |
|| `message.textContent` | User input or `data.answer` | Plain text only (no markdown render) |
|| `data.sources` | RAG response | Currently logged, not shown |

---

## Contracts / API

### RAG Endpoint (external)
```
POST https://rag.aldof.duckdns.org/search
Headers: Content-Type: application/json, X-API-Key: <RAG_API_KEY>
Body: {question: string, k: int}
Response: {answer: string, sources?: Array}
```

### Chat Widget UI Contract
The widget is a DOM injection (no separate page). The user asks: should this remain a floating widget, or become an embedded chat section within docs?

---

## Tasks

- [ ] Confirm `RAG_API_KEY` injection method (user clarification)
- [ ] Fix `CSS_NAME` in `hooks/chat.py` (`chat.js` → `chat.css`)
- [ ] Confirm OKF `.specify/` query requirement (user clarification)
- [ ] Confirm `data.sources` display in UI (user clarification)
- [ ] Confirm fallback on RAG endpoint failure (user clarification)
- [ ] Update plan.md with confirmed clarifications
---

## Quickstart / Verification

1. Open any docs page with floating chat button visible.
2. Click button, enter a question.
3. Verify POST to `rag.aldof.duckdns.org/search` (check Network tab).
4. Verify `data.answer` appears.
5. Verify `assets/css/chat.css` loads (check Network tab — currently 404).
