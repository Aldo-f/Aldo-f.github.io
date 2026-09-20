# Plan: Swagger UI docs + decoupled backend/frontend + Android backlog

## Goal
Add Swagger UI (`https://github.com/swagger-api/swagger-ui`) to the Express server to document `/api/*` endpoints, and document the backend/frontend split so each can deploy independently; backlog notes an Android-specific frontend.

## Current context / assumptions
- `package.json` has `express`; `server.ts` (line 1-90) is the Express entry point.
- No `swagger-ui-express` or `swagger-jsdoc` installed yet.
- `dist/` is the Vite production output (frontend static); backend serves from `server/services/` via `server.ts`; no separate deploy scripts exist.
- The user wants docs for developers, not end-users, so Swagger UI should mount at `/docs` (not root).
- Android frontend is backlog only (YAGNI — do not build); document the contract (REST JSON over `/api/*`) so an Android client can consume it.

## Architecture / proposed approach
Install `swagger-ui-express` + `swagger-jsdoc`; mount Swagger UI at `/docs`; keep `dist/` as standalone static frontend (any server can host it); document backend contract in `docs/API.md`. No Android code — only interface spec in backlog section.

## Step-by-step tasks

### Task 1 — Install Swagger dependencies (2 min)
File: `package.json` (edit via command, do not hand-edit JSON).
Run (expected: adds to dependencies, no errors):
```bash
bun add swagger-ui-express swagger-jsdoc
```
Verify: `grep -E "swagger-ui-express|swagger-jsdoc" package.json` returns both lines.
Commit: `git add package.json bun.lock; git commit -m "deps: add swagger-ui-express swagger-jsdoc"`

### Task 2 — Configure JSDoc annotations in `server.ts` (5 min)
File: `server.ts` (line 1-90, add after existing imports).
Copy-paste into `server.ts` after `import express` (line 2):
```typescript
import swaggerUi from 'swagger-ui-express';
import swaggerJSDoc from 'swagger-jsdoc';
const swaggerOptions = {
  definition: { openapi: '3.0.0', info: { title: 'UrbanFix API', version: '1.0.0', description: 'Road incident reporting API' } },
  apis: ['./server/services/*.ts'],
};
const specs = swaggerJSDoc(swaggerOptions);
```
Note: `swagger-jsdoc` may need `swagger-jsdoc` instead if types differ; if build fails, swap import to `import { swaggerJsdoc } from ...` per runtime error.

### Task 3 — Mount `/docs` endpoint (3 min)
File: `server.ts` — find the `app.use(...)` or `app.listen(...)` block; add before or after existing routes:
```typescript
app.use('/docs', swaggerUi.serve, swaggerUi.setup(specs));
```
If `server.ts` is only 90 lines with no routes defined here, add after `const app = express();` (assumed line ~5). Check with `grep -n "const app" server.ts`.

### Task 4 — Add JSDoc to first endpoint (`getReports` in `server/services/storage.ts`) (5 min)
File: `server/services/storage.ts`, insert above `export function getReports` (line 792):
```typescript
/**
 * @openapi
 * /api/reports:
 *   get:
 *     summary: List all reports
 *     responses:
 *       200:
 *         description: Array of ReportItem
 */
```
TDD cycle for this task: write failing test → implement → pass → commit.
Test file: `test/swagger-doc.test.ts`
Test content (copy-paste):
```typescript
import { describe, it, expect } from 'vitest';
describe('swagger docs', () => {
  it('exports swagger specs', () => {
    const { specs } = require('../server.ts');
    expect(specs).toBeDefined();
  });
});
```
Run failing: `bun run test swagger-doc.test.ts` (expect fail — specs not exported yet).
Implement: add `export { specs };` in `server.ts` after definition.
Run passing: `bun run test swagger-doc.test.ts` → expect 1 passed.
Commit.

### Task 5 — Verify Swagger UI loads (3 min)
Command (expected: HTTP 200 with HTML containing "swagger-ui"):
```bash
bun run build && bun start &
sleep 2
curl -s http://localhost:3000/docs | grep -o "swagger-ui" | head -1
kill %1 2>/dev/null
```
If `bun start` uses a different port (check `package.json` `start` script), adjust URL accordingly.

### Task 6 — Document backend/frontend split + Android backlog (2 min)
File: `docs/API.md` (create; if `docs/` missing, `mkdir -p docs`).
Content (copy-paste):
```markdown
# UrbanFix API Contract
- Base URL: `/api/*`
- Auth: none (public read; write via form / email sync)
- JSON responses: `{ success: boolean, data?: any, error?: string }`
- Frontend: `dist/` static build (React/Vite); can be deployed separately (e.g., Netlify/Vercel) pointing to any backend URL.
- Backend: `server.ts` (Express); serves `dist/` in production but can be split.
- Android backlog: Consume `/api/reports` (GET) and `/api/reports` (POST with JSON body matching `ReportItem` interface in `src/types.ts`). No Android code created (YAGNI).
```

## Tests / validation (TDD per task)
- Task 4 (docs): failing test `swagger-doc.test.ts` written first; after export added, passes.
- Task 5 (UI load): `curl` output verified with `grep`; if missing, check `server.ts` mount path.
- No tests for Task 1 (deps) or 3 (mount) — verified by build (`bun run build`) and curl.

## Risks, tradeoffs, open questions
- `swagger-jsdoc` can break TypeScript build if import types mismatch; open question: use `swagger-jsdoc` (JS) or `@types/swagger-jsdoc`?
- `server.ts` is only 90 lines — if routes are elsewhere, `/docs` mount must go in correct file; open question: locate all `express()` instances.
- Android backlog: no spec for mobile-specific endpoints; assume REST same as web.
- Tradeoff: Swagger UI at `/docs` requires server running; static docs (Markdown) could replace if server is down — keep both.
