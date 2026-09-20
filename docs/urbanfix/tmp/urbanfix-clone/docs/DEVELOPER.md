# Developer Documentation

## API Overview
The backend exposes a REST API under the `/api/*` namespace. The full OpenAPI specification is generated automatically via **swagger-jsdoc** and served at:

- **Swagger UI**: `http://localhost:<port>/docs`

The spec includes all current endpoints (reports, incident codes, emails, AI services, etc.):
- `GET /api/reports`: List all reports (supports filtering)
- `POST /api/reports`: Create a new road defect report
- `GET /api/reports/codes`: Get list of all distinct incident tracking codes
- `POST /api/reports/:id/codes`: Update incident codes for a report
- `POST /api/reports/:id/emails`: Add email correspondence to report

## IMAP Email Ingestion
The application includes an IMAP-based email polling and import service for AWV (Agentschap Wegen en Verkeer) and municipal notifications:
- **Service**: `server/services/imapService.ts` parses incoming emails, detects incident codes (e.g. `KM-2025-29314`), associates correspondence with existing reports or creates new reports, and triggers AI analysis.
- **Batch Import**: `server/services/realImport2.ts` provides batch import capabilities for historical inbox processing.

## Backend / Frontend Separation
- **Backend** (`server.ts` and `server/services/*`): Handles data persistence, email sync, AI integrations, and exposes the API.
- **Frontend** (`src/` + Vite build output in `dist/`): A React app that consumes the API. In production the backend statically serves the SPA, but you can also host the frontend separately (e.g., Netlify) and point it at any backend URL via environment variable `VITE_API_BASE`.

### Deploying Independently
1. **Backend only**: `bun run start` launches the Express server. The `/docs` UI is available for API consumers.
2. **Frontend only**: `bun run dev` serves the React dev server (Vite). Set `VITE_API_BASE` to the backend URL.
3. **Production bundle**: `bun run build` creates `dist/` containing both the SPA and the compiled `server.cjs`. Hosting `dist/` with any static file server works, but you can also copy only the static files to a CDN and keep the API on a separate domain.

## Testing
- API contract tests live in `test/api-contract.test.ts`.
- Swagger export test lives in `test/swagger-doc.test.ts`.

Run all tests with `bun test`.
