# UrbanFix

Het intelligente burgerplatform voor verkeersveiligheid, defecte signalisatie en wegeninfrastructuur met AI-multimodel analyse.

A full-stack application for reporting and managing road defects/incidents with AI-powered analysis.

## Tech Stack

- **Frontend**: React 19, Vite, Tailwind CSS v4, Leaflet, TypeScript
- **Backend**: Express.js, Node.js, TypeScript
- **AI**: Google Gemini (multi-provider waterfall support)
- **Build**: esbuild (server), Vite (frontend)

## Installation

```bash
npm install
cp .env.example .env
# Configure your API keys in .env
```

## Development

```bash
npm run dev
# Start dev server on http://localhost:3000
```

## Build

```bash
npm run build
npm start
```

## Docker

### Production

```bash
docker compose up -d --build      # build and start
docker compose logs -f urbanfix   # view logs
docker compose down               # stop
```

### Development (with live reload)

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

The dev override uses the builder stage as the runtime, mounts source code for live reload, and exposes the Vite HMR port.

Requires `traefik_net` network (from 01-core-infra). Route pre-configured in `04-network-traefik/routes.yml`.

## API Endpoints

### Swagger UI
- Swagger UI is available at `http://localhost:<port>/docs`.
- OpenAPI JSON spec is at `http://localhost:<port>/api-docs.json`.
- The UI documents all `/api/*` endpoints.



### Reports
- `GET /api/reports` - List all reports
- `GET /api/reports/:id` - Get single report
- `POST /api/reports` - Create/update report
- `DELETE /api/reports/:id` - Delete report
- `POST /api/reports/:id/timeline` - Add timeline event

### AI Features
- `POST /api/ai/analyze-defect` - Analyze photos for defects
- `POST /api/ai/generate-report` - Generate report text
- `POST /api/ai/generate-reply` - Generate email reply
- `POST /api/ai/generate-reminder` - Generate reminder email
- `POST /api/ai/test-provider` - Test AI provider connection

### Emails
- `GET /api/emails` - List emails
- `POST /api/emails/process-incoming` - Process incoming email
- `POST /api/emails/simulate-incoming` - Simulate email for testing

### Settings
- `GET /api/settings` - Get settings
- `POST /api/settings` - Update settings

### Utilities
- `GET /api/geocode/reverse` - Reverse geocoding proxy
- `GET /api/faq` - Get FAQ data
- `GET /api/partners` - Get municipality partners
- `GET /api/stats` - Get platform statistics

### Meldpunt Integration
- `POST /api/meldpunt/submit` - Submit to MeldpuntWegen.be

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key for AI features |
| `APP_URL` | Application base URL |
| `MELDPUNT_MODE` | Set to `real` to use real browser automation (default: mock) |
| `BUSTER_EXTENSION_PATH` | Path to Buster extension (default: `.bundler/buster-extension`) |
| `BUSTER_WHISPER_MODEL` | Whisper model for audio challenge (default: `tiny`) |

See `.env.example` for full list.

## Buster Extension Setup

To use real browser automation for submitting to AWV, you need the Buster extension for reCAPTCHA solving.

```bash
# Download and extract the Buster extension
npm run setup:buster
```

This will download Buster v3.4.0 from GitHub and extract it to `.bundler/buster-extension/`.

### Using Real Mode

```bash
# Set environment variables
export MELDPUNT_MODE=real
# BUSTER_EXTENSION_PATH defaults to .bundler/buster-extension

# Start the server
npm run dev
```

### Dry-Run Testing

Test the submission flow without actually sending to AWV:

```bash
# Test with mock (no browser required)
curl -X POST http://localhost:3000/api/meldpunt/submit \
  -H "Content-Type: application/json" \
  -d '{"reportId": "rep-001", "dryRun": true}'

# Test with real browser (requires Buster extension)
curl -X POST http://localhost:3000/api/meldpunt/submit \
  -H "Content-Type: application/json" \
  -d '{"reportId": "rep-001", "dryRun": true}' \
  -H "X-Meldpunt-Mode: real"
```

The response includes screenshots at each step for visual verification.

## Project Structure

```
.
├── src/          # Frontend React application
│   ├── components/   # Reusable UI components
│   ├── pages/      # Route-specific pages
│   ├── types.ts    # Shared TypeScript types
│   └── utils/      # Helper functions
├── server/       # Backend Express server
│   └── services/ # Business logic services
├── dev/          # Development documentation
├── assets/       # Static assets
├── graphify-out/ # Knowledge graph (graph.html, graph.json, GRAPH_REPORT.md)
├── server.ts     # Main server entry point
└── vite.config.ts # Vite build configuration
```

## Key Features

- **AI-Powered Analysis**: Automatic defect detection and report generation from photos
- **Multi-Channel Input**: Web form, email processing, and simulated inputs
- **Timeline Tracking**: Full status history with authority and citizen updates
- **Municipal Integration**: Pluggable architecture for different city APIs
- **Automated Reminders**: Configurable email reminders based on thresholds
- **Reverse Geocoding**: Nominatim proxy for location lookup

## License

Private project.

## Origin

Built for Belgian road safety reporting, integrates with [MeldpuntWegen.be](https://meldpuntwegen.be) and Flemish waterways & traffic authority (AWV).

## Documentation

See `docs/` for project specifications:
- `ORIGINAL_PROMPT.md` - Original project prompt
- `GOAL.md` - Project goals & objectives
- `PLAN.md` - Architecture & implementation plan
- `SDD_SPEC.md` - Technical specifications
- `TDD_TESTS.md` - Test specifications

## Knowledge Graph

The project includes a knowledge graph in `graphify-out/` for exploring codebase architecture:

- **Interactive Graph**: Open `graphify-out/graph.html` in a browser
- **Audit Report**: Read `graphify-out/GRAPH_REPORT.md` for God Nodes, Surprising Connections, and Suggested Questions
- **Raw Data**: `graphify-out/graph.json` for programmatic access
- **Query CLI**: Run `/graphify query "your question"` to traverse the graph

Example queries:
```bash
/graphify query "How does AI defect analysis connect to the report creation workflow?"
/graphify query "What connects the Meldpunt browser automation to the settings persistence bug?"
/graphify path "startServer" "analyzeDefect"
/graphify explain "MeldpuntBrowserAgent"
```