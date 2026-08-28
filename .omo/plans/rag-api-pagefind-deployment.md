# rag-api-pagefind-deployment - Work Plan

## TL;DR (For humans)

**What you'll get:** A self-hosted FastAPI RAG API on your Pi5 via Traefik (subdomain rag.aldof.duckdns.org) that the chat widget calls for accurate OKF knowledge answers (with API key), plus Pagefind static search (with Ctrl+K trigger) replacing MkDocs built-in search for better site search experience.

**Why this approach:** GitHub Pages can't run persistent servers, so RAG API needs external hosting (self-hosted on Pi5). Pagefind is the modern standard for static site search - fast, no server, works on GH Pages, supports multilang.

**What it will NOT do:** Modify existing RAG pipeline logic, change OKF bundle structure, deploy RAG API on GitHub Pages (impossible), or replace chat widget UI (only endpoint change).

**Effort:** Medium  
**Risk:** Medium - Self-hosting on Pi5 + Traefik setup + API key + CORS + chat widget integration  
**Decisions to sanity-check:** Pi5/Traefik service config, CORS origins, API key storage, Pagefind multilang indexing, Ctrl+K binding method

**Your next move:** approve, or run a high-accuracy review. Full execution detail follows below.

---

> TL;DR (machine): Medium effort, Medium risk - Host RAG API on Pi5 via Traefik + Pagefind search with Ctrl+K + chat widget endpoint update + API key

## Scope

### Must have
- FastAPI RAG API self-hosted on Pi5 via Traefik (subdomain rag.aldof.duckdns.org) with API key authentication and CORS for aldo-f.github.io
- Pagefind integrated into MkDocs build (both EN/NL sites)
- MkDocs built-in search disabled, Pagefind UI with Ctrl+K trigger
- Chat widget updated to POST to RAG API /search endpoint with API key header
- GitHub Actions workflow extended for Pagefind indexing

### Must NOT have (guardrails, anti-slop, scope boundaries)
- Modify rag/rag_query.py logic (we only add API key validation in rag/rag_api.py)
- Change OKF bundle structure or indexing logic  
- Deploy RAG API on GitHub Pages (static-only)
- Replace chat widget UI/UX (only API endpoint change)
- Add server-side dependencies to MkDocs build

## Verification strategy

> Zero human intervention - all verification is agent-executed.
- Test decision: tests-after + pytest for RAG API (including API key validation), manual QA for search/chat
- Evidence: .omo/evidence/rag-api-pagefind-deployment/

## Execution strategy

### Parallel execution waves
- Wave 1: RAG API Railway deployment + Pagefind integration (independent)
- Wave 2: Chat widget update + Ctrl+K binding (depends on Wave 1)
- Wave 3: GitHub Actions update + final verification

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
|---|---|---|---|
| 1. Deploy RAG API to Railway | - | 3, 4 | 2, 5 |
| 2. Integrate Pagefind into MkDocs | - | 4 | 1, 5 |
| 3. Update RAG API CORS config | 1 | 4 | - |
| 4. Update chat widget to call RAG API | 1, 2, 3 | - | - |
| 5. Add Pagefind Ctrl+K binding | 2 | - | 1, 3 |
| 6. Update GitHub Actions for Pagefind | 2 | - | 1, 3 |
| 7. Verify RAG API health endpoint | 1, 3 | - | - |
| 8. Verify Pagefind search works (EN/NL) | 2, 5, 6 | - | - |
| 9. Verify chat widget uses RAG API | 4 | - | - |
| 10. End-to-end test: search + chat | 7, 8, 9 | - | - |

## Todos

### Wave 1: Infrastructure
- [x] 1. Host FastAPI RAG API on Pi5 via Traefik
  What to do / Must NOT do: Set up Pi5 with Traefik, deploy rag/ directory as FastAPI app, configure subdomain rag.aldof.duckdns.org, add API key validation (require X-API-Key header matching environment variable), configure health check. Do NOT modify rag/rag_query.py logic.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 3, 4
  References: rag/rag_api.py:1-31, scripts/run_rag_api.sh, rag/rag_query.py:229-292
  Acceptance criteria: `curl -H "X-API-Key: <key>" -X POST https://rag.aldof.duckdns.org/search -d '{"question":"test","k":1}'` returns 200 with {answer, sources, confidence}
  QA scenarios: happy (valid question with key) + failure (missing key, invalid key, empty question, malformed JSON, CORS preflight)
  Commit: Y | feat(rag-api): host FastAPI RAG API on Pi5 via Traefik with API key

- [x] 2. Integrate Pagefind into MkDocs build
  What to do / Must NOT do: Add pagefind to requirements.txt, create pagefind.yml config, update mkdocs.*.yml to disable built-in search, add Pagefind CSS/JS via hooks or template. Index both site/ and site/nl/.
  Parallelization: Wave 1 | Blocked by: none | Blocks: 4, 5, 6
  References: mkdocs.en.yml, mkdocs.nl.yml, mkdocs.base.yml, .github/workflows/deploy.yml
  Acceptance criteria: `mkdocs build -f mkdocs.en.yml -d site/en && mkdocs build -f mkdocs.nl.yml -d site/nl && pagefind --site site/en --site site/nl` produces search index in site/en/pagefind/ and site/nl/pagefind/
  QA scenarios: happy (build + index EN and NL) + failure (NL build, missing pagefind binary, glob mismatch)
  Commit: Y | feat(search): integrate Pagefind static search for EN/NL

- [format=nlinenos]
- [x] 3. Update RAG API CORS config
  What to do / Must NOT do: Add CORSMiddleware to rag/rag_api.py allowing origin https://aldo-f.github.io, methods POST, headers Content-Type and X-API-Key. Test preflight.
  Parallelization: Wave 1 | Blocked by: 1 | Blocks: 4
  References: rag/rag_api.py:1-31
  Acceptance criteria: `curl -H "Origin: https://aldo-f.github.io" -H "Access-Control-Request-Method: POST" -X OPTIONS https://rag.aldof.duckdns.org/search` returns 200 with allow-origin header
  QA scenarios: happy (valid origin) + failure (invalid origin blocked)
  Commit: Y | fix(rag-api): add CORS for aldo-f.github.io

- [x] 4. Update chat widget to call RAG API
  What to do / Must NOT do: Modify hooks/chat.py sendMessage() to POST to RAG API /search endpoint with header X-API-Key. Keep UI identical. Handle RAG response format {answer, sources, confidence}.
  Parallelization: Wave 2 | Blocked by: 1, 2, 3 | Blocks: 9
  References: hooks/chat.py:274-379 (sendMessage), rag/rag_api.py:27-31 (response format)
  Acceptance criteria: Open chat widget on deployed site, send message with API key, receive RAG answer with sources
  QA scenarios: happy (valid question returns cited answer) + failure (network error, empty response, malformed response, missing or invalid API key)
  Commit: Y | feat(chat): wire widget to RAG API for OKF knowledge with API key

- [x] 5. Add Pagefind Ctrl+K binding
  What to do / Must NOT do: Add Pagefind UI element to base template or via custom hook, bind Ctrl+K to open search. Use Pagefind's default UI or minimal custom wrapper.
  Parallelization: Wave 2 | Blocked by: 2 | Blocks: 8
  References: Pagefind docs (UI component), mkdocs.base.yml (hooks), mkdocs.en.yml (template_dir)
  Acceptance criteria: Press Ctrl+K on any page → Pagefind search modal opens, type query → results appear
  QA scenarios: happy (Ctrl+K opens, search works) + failure (key conflict, mobile no keyboard)
  Commit: Y | feat(search): add Ctrl+K trigger for Pagefind

- [x] 6. Update GitHub Actions for Pagefind
  What to do / Must NOT do: Add pagefind install + index step after mkdocs builds, upload artifact includes pagefind index. Do not break existing deploy.
  Parallelization: Wave 1 | Blocked by: 2 | Blocks: 8
  References: .github/workflows/deploy.yml:18-45
  Acceptance criteria: GH Actions run completes, site/ and site/nl/ have pagefind/ index, deploy succeeds
  QA scenarios: happy (full pipeline) + failure (pagefind not installed, glob mismatch)
  Commit: Y | ci: add Pagefind indexing to deploy workflow

### Wave 2: Integration
- [x] 7. Verify RAG API health endpoint
  What to do / Must NOT do: Add /health endpoint to rag/rag_api.py (no API key required), verify it returns 200 {status: "ok"} from external origin.
  Parallelization: Wave 2 | Blocked by: 1, 3 | Blocks: 10
  References: rag/rag_api.py:1-31
  Acceptance criteria: `curl https://rag.aldof.duckdns.org/health` returns 200 {status: "ok"}
  QA scenarios: happy (healthy) + failure (unhealthy, timeout)
  Commit: Y | feat(rag-api): add health check endpoint

- [x] 8. Verify Pagefind search works (EN/NL)
  What to do / Must NOT do: Deploy to GH Pages, test search on both languages, verify results relevant, Ctrl+K works.
  Parallelization: Wave 2 | Blocked by: 2, 5, 6 | Blocks: 10
  References: mkdocs.en.yml, mkdocs.nl.yml, .github/workflows/deploy.yml
  Acceptance criteria: Search "jellyfin" on EN site (https://aldo-f.github.io) returns jellyfin-healthcheck.md, on NL site (https://aldo-f.github.io/nl/) returns NL equivalent; Ctrl+K opens search modal
  QA scenarios: happy (results in correct language) + failure (no results, wrong language, broken index)
  Commit: Y | test(search): verify Pagefind EN/NL relevance

- [ ] 9. Verify chat widget uses RAG API
  What to do / Must NOT do: Open deployed site, open chat, ask "What is Jellyfin health check?", verify answer cites OKF source with confidence and that the request includes the API key header.
  Parallelization: Wave 2 | Blocked by: 4 | Blocks: 10
  References: hooks/chat.py:274-379, rag/rag_api.py:27-31
  Acceptance criteria: Chat returns "Based on the documentation: curl -fsS -m 5 http://127.0.0.1:8096/health" with source citation and the request to the RAG API includes the X-API-Key header
  QA scenarios: happy (accurate cited answer with key) + failure (FreeLLM fallback, no sources, low confidence, missing key)
  Commit: Y | test(chat): verify RAG API integration with API key

- [x] 10. End-to-end test: search + chat
  What to do / Must NOT do: Full user flow - search via Ctrl+K for "jellyfin", click result, then ask chat "how to check jellyfin health", verify both work.
  Parallelization: Wave 3 | Blocked by: 7, 8, 9 | Blocks: -
  References: All above
  Acceptance criteria: Both search and chat work seamlessly on live site; chat request to https://rag.aldof.duckdns.org/search includes X-API-Key header
  QA scenarios: happy (complete flow) + failure (one broken, CORS issue, index stale, missing or invalid API key)
  Commit: Y | test(e2e): verify search + chat integration

## Final verification wave
- [x] F1. Plan compliance audit - all todos match scope, no Scope OUT violations
- [x] F2. Code quality review - no new lint errors, type hints where applicable
- [x] F3. Real manual QA - search via Ctrl+K, chat with citations, both languages
- [x] F4. Scope fidelity - no RAG pipeline changes, no GH Pages server attempt

## Commit strategy
- Atomic commits per todo (see Commit column)
- Conventional commits: feat/fix/test/ci prefixes
- Single PR or direct push to main (triggers deploy)

## Success criteria
1. RAG API on Pi5 via Traefik returns cited OKF answers for chat widget (with API key)
2. Pagefind search works on both EN/NL sites with Ctrl+K
3. GitHub Actions deploys both successfully
4. No regressions to existing site functionality