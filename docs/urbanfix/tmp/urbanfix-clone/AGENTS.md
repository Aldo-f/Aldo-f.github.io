# PROJECT KNOWLEDGE BASE

**Generated:** 2026-09-13 16:49:38 UTC
**Commit:** 511114d
**Branch:** main

## OVERVIEW
Meldpunt Wegen & Verkeer Automator - A full-stack application for reporting and managing road defects/incidents with AI-powered analysis, built with React/Vite frontend and Express/Node.js backend. Supports spec-driven development with comprehensive documentation.

## STRUCTURE
```
.
├── src/               # Frontend React application (components, pages, types, utils)
│   ├── components/    # Reusable UI components (AIWaterfallSettings, MapView, Timeline, etc.)
│   ├── pages/         # Route-specific page components (HomePage, IncidentDetail, etc.)
│   ├── utils/         # Helper functions (AI models, geo, logging, etc.)
│   └── types.ts       # Central TypeScript interfaces (ReportItem, SubmissionStatus, etc.)
├── server/            # Backend Express server
│   ├── services/      # Business logic services (storage, ai, email, meldpunt bot)
│   └── middleware/    # Express middleware (error handling, CSRF)
├── specs/             # Spec-driven development specifications
│   ├── 001-gmail-report-import/
│   ├── 002-incident-creation-workflow/
│   ├── 003-email-sync-tracking/
│   └── 004-reminders-automation/
├── docs/              # Project documentation (API specs, architecture, etc.)
├── data/              # JSON storage for reports, emails, settings
├── graphify-out/      # Knowledge graph outputs (graph.json, graph.html, GRAPH_REPORT.md)
├── server.ts          # Main Express/Vite server entry point
├── vite.config.ts     # Vite build configuration with React and Tailwind plugins
└── package.json       # Scripts: dev, build, lint, test, clean
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| UI Components | src/components/ | Reusable React components with Tailwind CSS |
| Page Components | src/pages/ | Route-specific pages (HomePage, IncidentDetailPage, etc.) |
| Shared Types | src/types.ts | Central TypeScript interfaces - core data models |
| Utility Functions | src/utils/ | Geo calculations, EXIF parsing, AI model config |
| API Endpoints | server.ts | Express route handlers for all /api/* endpoints |
| Business Logic | server/services/ | Storage, AI, email sync, Meldpunt integration |
| Configuration | tsconfig.json, vite.config.ts | Build and TypeScript configuration |
| Specs | specs/*/ | Spec-driven development workflows |
| OpenAPI | specs/openapi.yaml | Machine-readable API specification |
| Knowledge Graph | graphify-out/ | Interactive graph (graph.html), report (GRAPH_REPORT.md), raw data (graph.json) |

## CODE MAP
| Symbol | Type | Location | Refs | Role |
|--------|------|----------|------|------|
| ReportItem | Interface | src/types.ts | High | Core data model for defect reports |
| SubmissionStatus | Type Alias | src/types.ts | High | Report status tracking (concept, verzenden, etc.) |
| TimelineEvent | Interface | src/types.ts | Medium | History of report status changes |
| EmailCorrespondence | Interface | src/types.ts | Medium | Email tracking and matching |
| ImpactedGroup | Type Alias | src/types.ts | Low | Categories of affected road users |
| getReports | Function | server/services/storage.ts | High | Retrieve stored reports |
| saveReports | Function | server/services/storage.ts | High | Persist report data |
| analyzeDefect | Function | server/services/ai.ts | Medium | AI-powered defect analysis from images |
| generateFullReport | Function | server/services/ai.ts | Medium | Create comprehensive report text |
| startServer | Function | server.ts | High | Main server initialization and Express setup |
| app | Object | server.ts | High | Express application instance |
| DEFAULT_AI_ACCOUNTS | Constant | src/utils/aiModels.ts | Medium | User-defined AI provider accounts |
| PRESET_MODEL_CATALOG | Constant | src/utils/aiModels.ts | Medium | Available AI models (empty - user configured) |

## CONVENTIONS
- **Path Aliases**: `@/*` maps to project root (configured in tsconfig.json and vite.config.ts)
- **API Response Format**: Consistent `{ success: boolean, data?: any, error?: string }` structure
- **Error Handling**: Try/catch blocks in API routes with 500 status and JSON error responses
- **File Organization**: Feature-based grouping in src/ (components, pages, utils) and service-based in server/services/
- **TypeScript**: Strict typing with interfaces for all complex objects and API payloads
- **Image Handling**: Base64 encoding for photo storage and transmission (25MB limit)
- **Timestamp Format**: ISO 8601 strings for all date/time values
- **AI Configuration**: All AI providers and models defined via UI settings (no hardcoded defaults)
- **Spec-Driven Dev**: Specifications in `specs/` directory guide implementation

## ANTI-PATTERNS (THIS PROJECT)
- No direct DOM manipulation in React components (use refs and effects appropriately)
- No hardcoded API endpoints (relative paths used in frontend, Express handles routing)
- No blocking synchronous operations in Express route handlers (async/await used)
- No console.log in production code (remove debug statements before commits)
- No magic strings/numbers (use constants from types.ts or configuration)
- No hardcoded AI provider configurations (use user-defined settings)
- No default model catalogs (all configurations stored in database/settings)

## UNIQUE STYLES
- **AI-First Design**: Core functionality built around AI analysis (defect detection, report generation, email replies)
- **AI Waterfall**: Multiple AI providers with configurable fallback mechanism (via UI settings)
- **Multi-Channel Input**: Accepts reports via web form, email processing, and simulated inputs
- **Timeline Tracking**: Every status change recorded as timeline event with actor type and authority
- **Municipal Integration**: Service-layer abstraction for different municipality APIs (live API, email sync, planned)
- **Automated Reminders**: Configurable email reminders based on submission dates and thresholds
- **Reverse Geocoding Proxy**: Express middleware to avoid CORS issues with Nominatim API
- **SSE Updates**: Real-time updates via Server-Sent Events (`/api/sse`)
- **Firebase Auth**: Role-based access control with admin/authority/user roles
- **Encrypted Keys**: AI API keys stored encrypted at rest (aiKeyEncoder.ts)
- **Firestore Storage**: Primary data storage is Firebase Firestore (migrate with `scripts/migrate-to-firestore.mjs`)

## COMMANDS
```bash
# Development
npm run dev          # Start Vite dev server with Express middleware
npm run build        # Build frontend (vite build) and bundle server (esbuild)
npm start            # Start production server from dist/
npm run lint         # TypeScript type checking (tsc --noEmit)
npm run clean        # Remove dist/ and server.js artifacts
npm run test         # Run Vitest unit tests
npm run test:e2e     # Run Playwright E2E tests

# Environment
cp .env.example .env # Copy example environment file
```

## NOTES
- AI service configuration is modular - supports multiple providers (Google Gemini, OpenAI, OpenRouter, Groq, Custom) with fallback waterfall
- Photo uploads handled with 25MB payload limit to accommodate base64-encoded images
- Email synchronization includes both IMAP-style polling and simulated incoming emails for testing
- MeldpuntWegen.be integration enables automatic submission to Belgian road authority system
- All API endpoints prefixed with /api/ for clear separation from static assets
- Frontend uses React 19 with modern hooks and concurrent rendering capabilities
- Tailwind CSS v4 integrated via Vite plugin for utility-first styling
- Server serves frontend static assets in production mode from dist/ directory
- All AI provider credentials are user-configured via UI settings (no hardcoded defaults)
- AI API keys are encrypted at rest using AES-256 encryption
- Spec-driven development workflow: specs/ directory contains implementation specifications
- OpenAPI spec auto-generated at startup and available at /docs
- Knowledge graph available in `graphify-out/` - use `/graphify query "question"` to explore architecture, or open `graph.html` in browser for interactive visualization