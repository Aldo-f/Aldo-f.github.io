# UrbanFix Pino Error Logging Plan

**Generated:** 2026-09-26 14:30 UTC
**Project:** `/home/aldo/dev/06-apps-urbanfix`

## Goal
Ensure every error condition in the UrbanFix backend (Express/Node.js) and frontend (React/TypeScript) is captured with structured pino logs, making failures observable and diagnosable.

## Current Context / Assumptions
- Backend runs on Express (Node.js) with a `server/logger.ts` file that exports a pino-based logger.
- Frontend uses a custom `src/utils/logger.ts` wrapper that mimics pino's API (`logger.error`, `logger.warn`, etc.) for browser-compatible logging.
- Errors can arise from: async route handlers, file system operations, database queries, authentication checks, failed network requests, state updates, component rendering exceptions.
- Existing code already imports `pino` in backend and uses the wrapper in frontend, but logging is not systematic.

## Architecture / Proposed Approach
1. Centralize error handling with an Express-level error middleware that logs all uncaught errors and routes them through the pino logger.
2. Wrap async route handlers with a reusable `withAsyncError` helper that catches exceptions, logs them with context (request ID, method, path), and forwards the error to the error middleware.
3. Instrument critical backend paths (file I/O in `storage.ts`, auth checks in `App.tsx`, API route handlers) with explicit `try/catch` blocks that invoke `logger.error` with descriptive messages and request context.
4. Frontend: wrap all `fetch`/`axios` calls and UI state updates with try/catch that call `logger.error` (via the wrapper) to surface client-side failures.

## Step-by-Step Tasks

### 1. Add a reusable async error-capture helper
- **File:** `server/utils/withAsyncError.ts`
- **Content:** Export a function `withAsyncError(fn: (req, res, next) => Promise<void>)`. It wraps an async route handler, catches any error, logs it with `logger.error` (including `req.id`, `req.method`, `req.path`), then calls `next(err)`.
- **Verification:** Run `node -e "require('./server/utils/withAsyncError').withAsyncError(() => Promise.reject(new Error('test')))"` and confirm a log line appears.

### 2. Create a global Express error-logging middleware
- **File:** `server/middleware/errorLogger.ts`
- **Action:** Add `app.use((err, req, res, next) => { logger.error({ message: err.message, stack: err.stack, requestId: req.id || 'unknown' }, err); res.status(500).json({ error: 'Internal Server Error' }); });`
- **Verification:** Trigger a 500 error (e.g., force a division by zero in a test route) and verify the log contains `message`, `stack`, and `requestId`.

### 3. Instrument `storage.ts` file-I/O operations
- **File:** `server/services/storage.ts`
- **Action:** Wrap each `fs.readFileSync`, `fs.writeFileSync`, and DB query call in a `try/catch`. On error, call `logger.error('File I/O error', { err: err.message, path: filePath })` before re-throwing or returning a fallback.
- **Verification:** Delete a required data file (e.g., `reports.json`) and restart the server; confirm a log entry reports "File I/O error" with the correct path.

### 4. Add error logging to authentication/guard logic in `App.tsx`
- **File:** `src/App.tsx` (lines ~622-663 where the `/settings` guard lives)
- **Action:** Surround the guard logic with a `try/catch` that logs `logger.error('Auth guard failed', { err: err.message, user: currentUser?.id })`. Ensure the guard still returns the correct boolean.
- **Verification:** Temporarily set `currentUserRole` to an invalid value and reload the page; verify a log entry appears.

### 5. Wrap all API route handlers (e.g., `/api/reports`, `/api/settings`)
- **Files:** `server/routes/*.js` (or wherever route handlers are defined)
- **Action:** For each handler, wrap the body with `withAsyncError` (from step 1). Ensure any thrown error is logged.
- **Verification:** Use `curl` to hit a deliberately broken endpoint (e.g., cause a `TypeError`), then check the server logs for the error entry.

### 6. Add frontend fetch-error logging in `src/components/*` (e.g., `SettingsModal.tsx`, any component that makes API calls)
- **Files:** Identify files with `fetch`/`axios` calls (search for `fetch(` or `axios.get(`).
- **Action:** Wrap each call in `try { ... } catch (err) { logger.error('API request failed', { url: url, err: err.message }) }`.
- **Verification:** Simulate a network failure (e.g., block the request with `curl --interface` or use Chrome devtools to offline) and confirm the log appears in the browser console.

### 7. Add a global unhandled-exception logger for the frontend
- **File:** `src/main.tsx` (or the entry point where the React app mounts)
- **Action:** Add `window.addEventListener('error', (e) => { logger.error('Uncaught frontend error', { message: e.message, stack: e.error?.stack }) });` and `window.addEventListener('unhandledrejection', (e) => { logger.error('Unhandled promise rejection', { reason: e.reason }) });`
- **Verification:** Force an uncaught error (e.g., call a non-existent function) and check the console/log for the entry.

### 8. Write a minimal end-to-end test to confirm logging works
- **File:** `tests/pino-error.test.ts` (or `.js` if TypeScript not available)
- **Content:**
  ```ts
  import { logger } from '../src/utils/logger';
  test('logger.error writes to console', () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    logger.error('test error', { context: 'unit-test' });
    expect(consoleSpy).toHaveBeenCalledWith('[error] test error context: unit-test');
    consoleSpy.mockRestore();
  });
  ```
- **Run:** `npm test` (or the project's test command) and ensure the test passes.

### 9. Validate logs in a running container
- **Steps:**
  1. `docker compose up -d --build` (ensure fresh build).
  2. `curl -i https://urbanfix.dev.aldof.duckdns.org/settings` → expect HTTP 200.
  3. Force an error (e.g., delete `settings.json` temporarily, restart container).
  4. Observe container logs (`docker logs <container-name>`) for pino entries containing "error" and the relevant context (file path, request path).

## Tests / Validation

- **Backend:** After each middleware or route modification, restart the container and use `curl` to provoke a known error; grep the container logs for `logger.error` entries with expected keywords (`File I/O`, `Auth guard`, `API request failed`).
- **Frontend:** Open the browser devtools console, trigger a network failure (e.g., disable network in devtools), verify a log line appears with `logger.error` and the request URL.
- **Unit test:** Run the Jest/Mocha test from step 8; it must pass without mock failures.

## Risks, Tradeoffs & Open Questions

- **Risk:** Over-logging may flood logs; we mitigate by logging only error-level events and using structured JSON for easy filtering.
- **Tradeoff:** Adding `try/catch` everywhere can slightly impact performance; the benefit of observability outweighs the negligible cost in a dev/test environment.
- **Open Question:** Are there any third-party libraries (e.g., database drivers) that already provide their own error logging? If so, we may need to adapt our wrapper to avoid duplicate logs.