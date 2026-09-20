# UrbanFix & Meldpunt Wegen Automator — API Reference

Official API documentation for the **UrbanFix** / **Meldpunt Wegen & Verkeer Automator** platform.

- **Base URL:** `/api`
- **Interactive Swagger UI:** Available at [`/docs`](/docs)
- **Live OpenAPI 3.0 JSON Spec:** Available at [`/docs.json`](/docs.json) and [`/api/openapi.json`](/api/openapi.json)
- **Static Schema File:** Located in [`docs/openapi.json`](./openapi.json)
- **Content-Type:** `application/json` (unless streaming with `text/event-stream`)
- **Standard Response Format:**
  ```json
  {
    "success": true,
    "data": { ... }
  }
  ```
- **Standard Error Format:**
  ```json
  {
    "error": "Beschrijving van de fout"
  }
  ```

---

## Table of Contents

1. [Architecture & Synchronization Guarantee](#architecture--synchronization-guarantee)
2. [Authentication & Authorization](#authentication--authorization)
3. [System & Real-Time Endpoints](#system--real-time-endpoints)
4. [Incident Reports (`/api/reports`)](#incident-reports)
5. [Email Synchronization & Assignment (`/api/emails`)](#email-synchronization--assignment)
6. [AI Services (`/api/ai`)](#ai-services)
7. [MeldpuntWegen.be Bot (`/api/meldpunt`)](#meldpuntwegenbe-bot)
8. [Public Information & Statistics](#public-information--statistics)
9. [Citizen Contact & Onboarding (`/api/contact`)](#citizen-contact--onboarding)
10. [Application Settings (`/api/settings`)](#application-settings)
11. [Geocoding Proxies (`/api/geocode`)](#geocoding-proxies)
12. [Core Data Models](#core-data-models)

---

## Architecture & Synchronization Guarantee

To ensure that the API documentation **always reflects the exact state of the codebase**:

1. **Single Source of Truth (`server/swagger.ts`)**: Every endpoint, parameter, request payload, response status code, and data model is defined in the centralized OpenAPI 3.0 specification module.
2. **Automated Server Boot Sync**: Every time the backend server starts, `writeOpenApiSpecFile()` automatically regenerates and writes `/docs/openapi.json`.
3. **Live Endpoints**: The Express server exposes `/docs` (interactive Swagger UI), `/docs.json`, and `/api/openapi.json`.
4. **Continuous Contract Tests (`test/swagger-doc.test.ts`)**: Vitest automated tests verify that all Express routes have corresponding OpenAPI path definitions and valid schemas.

---

## Authentication & Authorization

UrbanFix operates on a role-aware public service model:
- **Public access:** Citizens can view reports, inspect stats, consult FAQs, submit incident dossiers, and send contact inquiries without authentication tokens.
- **Admin & Authority functions:** Internal administrative functions (IMAP polling, email assignments, settings changes) are accessible within the admin dashboard or via direct API calls.
- **Payload Limits:** The server accepts JSON payloads up to **25 MB** to accommodate base64-encoded high-resolution inspection photos.

---

## System & Real-Time Endpoints

### 1. Health Check
`GET /api/health`

Verifies that the backend service is running and returns the system timestamp.

**Response `200 OK`**:
```json
{
  "status": "ok",
  "service": "Meldpunt Wegen & Verkeer Automator",
  "timestamp": "2026-09-12T14:00:00.000Z"
}
```

**Example Curl**:
```bash
curl -s http://localhost:3000/api/health
```

---

### 2. Server-Sent Events (SSE) Stream
`GET /api/sse`

Provides a persistent real-time event stream. Clients receive initial data on connection and live broadcasts whenever reports, timeline updates, or incoming emails are modified.

**Headers**:
- `Accept: text/event-stream`
- `Cache-Control: no-cache`
- `Connection: keep-alive`

**Event Types**:
- `event: init` — Emits `{ reports: ReportItem[], emails: EmailCorrespondence[] }` on first connection.
- `event: reports` — Emits `{ reports: ReportItem[] }` whenever a report is created, updated, or deleted.
- `event: emails` — Emits `{ emails: EmailCorrespondence[] }` whenever emails are polled, linked, or updated.

---

## Incident Reports

### 1. List All Reports
`GET /api/reports`

Retrieves all road defect reports, including linked correspondence, timeline events, and automation logs.

**Response `200 OK`**: Array of [`ReportItem`](#reportitem).

**Example Curl**:
```bash
curl -s http://localhost:3000/api/reports
```

---

### 2. Get Single Report
`GET /api/reports/:id`

Retrieves a single report by its internal `id` (e.g. `rep-1788712095034`) or by its official Flemish reference code (e.g. `KM-2026-08317` or `MWV-2026-12345`).

**Responses**:
- `200 OK`: Returns the matched [`ReportItem`](#reportitem).
- `404 Not Found`: `{ "error": "Melding niet gevonden" }`

**Example Curl**:
```bash
curl -s http://localhost:3000/api/reports/rep-1788712095034
```

---

### 3. Create or Update Report
`POST /api/reports`

Creates a new road defect dossier or updates an existing one (matching by `id`). Automatically triggers an SSE broadcast to all active clients.

**Request Body**: [`ReportItem`](#reportitem)
```json
{
  "title": "Diepe put in fietspad Bergbosstraat",
  "rawDefectHint": "Wegverzakking en scherpe asfaltkanten",
  "fullReportText": "Op het fietspad ter hoogte van huisnummer 45 bevindt zich een gevaarlijke verzakking...",
  "impactedGroups": ["fietsers", "voetgangers"],
  "location": {
    "latitude": 50.9882,
    "longitude": 3.7719,
    "address": "Bergbosstraat 45, 9820 Merelbeke",
    "street": "Bergbosstraat",
    "municipality": "Merelbeke",
    "postalCode": "9820",
    "hasGps": true
  },
  "contactInfo": {
    "firstName": "Aldo",
    "lastName": "Fieuw",
    "email": "aldo.fieuw@gmail.com",
    "wantsResponse": true
  },
  "submissionStatus": "concept",
  "photos": []
}
```

**Response `200 OK`**:
```json
{
  "success": true,
  "report": { ... }
}
```

---

### 4. Delete Report
`DELETE /api/reports/:id`

Deletes the specified report permanently and broadcasts the updated collection via SSE.

**Response `200 OK`**:
```json
{
  "success": true
}
```

---

### 5. Add Timeline Event
`POST /api/reports/:id/timeline`

Appends a new official progress event to the report's timeline history and optionally updates its `submissionStatus`.

**Request Body**:
```json
{
  "title": "Inspectie Ter Plaatse Uitgevoerd",
  "description": "Technisch controleur heeft de verzakking opgemeten.",
  "authority": "AWV District Gent",
  "status": "in_behandeling",
  "actorType": "authority",
  "isOfficial": true
}
```

**Response `200 OK`**:
```json
{
  "success": true,
  "timelineEvent": { ... },
  "report": { ... }
}
```

---

## Email Synchronization & Assignment

### 1. List Synchronized Emails
`GET /api/emails`

Returns all incoming, processed, and simulated email correspondence.

**Response `200 OK`**: Array of [`EmailCorrespondence`](#emailcorrespondence).

---

### 2. Process Incoming Email
`POST /api/emails/process-incoming`

Ingests a raw email message, extracts incident reference codes (`MWV-`, `KM-`, `MB-`), assigns match scores against active dossiers, and records status transitions.

**Request Body**:
```json
{
  "from": "meldpuntwegen@wegenenverkeer.vlaanderen.be",
  "to": "aldo.fieuw@gmail.com",
  "subject": "Melding MWV-2026-84920 in behandeling",
  "body": "Uw melding is overgemaakt aan de lokale wegendienst Merelbeke.",
  "messageId": "<notif-84920@wegenenverkeer.be>"
}
```

**Response `200 OK`**: `{ "success": true, "email": { ... } }`

---

### 3. Simulate Incoming Authority Notification
`POST /api/emails/simulate-incoming`

Generates realistic mock correspondence for testing and demonstration purposes.

**Request Body**:
```json
{
  "reportId": "rep-1788712095034",
  "type": "district_update"
}
```
*Valid `type` values:* `"confirmation"`, `"district_update"`, `"forwarded_municipality"`, `"resolved"`

---

### 4. Assign or Unlink Email to/from Report
`POST /api/emails/:id/assign-report`

Connects an incoming email to a specific incident report or disconnects it (`targetReportId: null`). Automatically syncs the dossier's `emails` array and records an official timeline event.

**Request Body**:
```json
{
  "targetReportId": "rep-1788712095034"
}
```

**Response `200 OK`**:
```json
{
  "success": true,
  "email": { ... },
  "updatedReport": { ... }
}
```

---

### 5. Create Dossier from Unlinked Email
`POST /api/emails/:id/create-report`

Converts an orphaned or newly arrived email directly into a full incident dossier. Automatically transfers subjects, descriptions, extracted reference codes, and photo attachments.

**Response `200 OK`**:
```json
{
  "success": true,
  "report": { ... },
  "email": { ... }
}
```

---

### 6. Auto-Link Unlinked Emails
`POST /api/emails/auto-link`

Scans all unlinked emails in the database against registered dossiers and incident codes, linking matches automatically.

**Response `200 OK`**:
```json
{
  "success": true,
  "linkedCount": 2,
  "totalUnlinked": 0,
  "updatedReportsCount": 1
}
```

---

### 7. Trigger Immediate IMAP Polling
`POST /api/emails/poll-now`

Establishes a live connection to the configured IMAP mail server, searches the inbox for correspondence related to road defects, downloads full RFC822 messages and image attachments, and persists new messages.

**Response `200 OK`**:
```json
{
  "success": true,
  "count": 3
}
```

---

### 8. Mark Email as Read
`POST /api/emails/:id/read`

Marks the specified email as read (`read: true`).

---

### 9. Send Email Reply via SMTP
`POST /api/emails/send-reply`

Sends an AI-drafted reply to an authority or user via configured SMTP credentials. If SMTP is unconfigured, records a simulated delivery.

**Request Body**:
```json
{
  "reportId": "rep-1788712095034",
  "reply": "Geachte heer/mevrouw, dank voor de toelichting...",
  "toEmail": "meldpuntwegen@wegenenverkeer.vlaanderen.be"
}
```

---

### 10. Send Dossier Reminder via SMTP
`POST /api/emails/send-reminder`

Sends an automated inquiry letter for an unresolved dossier.

---

### 11. Seed Sample Email Thread
`POST /api/emails/seed-sample-thread`

Seeds a multi-code correspondence thread with SVG terrain inspection attachments for testing.

---

## AI Services

### 1. Vision AI Defect Analysis
`POST /api/ai/analyze-defect`

Analyzes photos of road damage using Gemini Vision AI models, returning defect classifications, affected road user groups, traffic signs, and severity levels.

**Request Body**: [`AIAnalysisRequest`](#aianalysisrequest)
```json
{
  "images": [
    {
      "filename": "fietspad.jpg",
      "base64Data": "/9j/4AAQSkZJRg...",
      "mimeType": "image/jpeg"
    }
  ],
  "userHint": "Diepe put in asfalt",
  "locationContext": "Merelbeke, Bergbosstraat"
}
```

**Response `200 OK`**:
```json
{
  "defectHypotheses": ["Verzakking in asfaltverharding", "Gevaarlijke put voor fietsers"],
  "suggestedCategories": ["fietsers"],
  "detectedSigns": ["Verkeersbord D7 (Verplicht fietspad)"],
  "severity": "hoog"
}
```

---

### 2. Generate Full Report Text
`POST /api/ai/generate-report`

Generates an objective, legally sound, highly descriptive road defect report formatted according to Flemish municipal standards.

**Request Body**: [`AIGenerateReportRequest`](#aigeneratereportrequest)

**Response `200 OK`**:
```json
{
  "fullReportText": "Hierbij meld ik een ernstige beschadiging aan het openbaar domein...",
  "suggestedTitle": "Ernstige verzakking in fietspad Bergbosstraat ter hoogte van nr. 45"
}
```

---

### 3. Generate AI Reply to Authority Email
`POST /api/ai/generate-reply`

Drafts a context-aware response based on previous emails and user intent.

---

### 4. Generate Reminder Text
`POST /api/ai/generate-reminder`

Drafts a polite reminder asking for an update on a pending dossier.

---

### 5. Test AI Provider Connectivity
`POST /api/ai/test-provider`

Pings an AI provider endpoint (Google Gemini, OpenAI, OpenRouter, DuckDNS Proxy) to verify credentials and report network latency.

---

## MeldpuntWegen.be Bot

### Submit Report to MeldpuntWegen.be
`POST /api/meldpunt/submit`

Dispatches an automated headless submission of the dossier to the official Flemish road defect portal (`meldpuntwegen.vlaanderen.be`).

**Request Body**:
```json
{
  "reportId": "rep-1788712095034"
}
```

**Response `200 OK`**:
```json
{
  "success": true,
  "trackingCode": "MWV-2026-94821",
  "automationLogs": [
    {
      "stepNumber": 1,
      "stepName": "Locatie valideren",
      "status": "success",
      "timestamp": "2026-09-12T14:15:00.000Z"
    }
  ]
}
```

---

## Public Information & Statistics

### 1. Frequently Asked Questions
`GET /api/faq`

Returns categorized FAQs (procedures, jurisdictions, privacy, technical).

### 2. Partner Municipalities & Road Authorities
`GET /api/partners`

Returns connected Flemish cities, municipalities, and AWV districts.

### 3. Platform Statistics
`GET /api/stats`

Returns aggregated statistics:
```json
{
  "totalReports": 284,
  "resolvedReports": 198,
  "inProgressReports": 64,
  "activeMunicipalities": 38,
  "avgResolutionDays": 9.4,
  "aiAccuracyPercent": 96.2
}
```

---

## Citizen Contact & Onboarding

### 1. Submit Contact Message
`POST /api/contact`

Allows citizens, municipal officials, and partners to send messages.

**Request Body**:
```json
{
  "name": "Jan Peeters",
  "email": "jan.peeters@merelbeke.be",
  "phone": "+32 9 210 32 11",
  "organization": "Gemeente Merelbeke - Technische Dienst",
  "subject": "aansluiten",
  "message": "Wij willen graag onze meldingsstroom koppelen aan UrbanFix."
}
```

### 2. List Contact Messages (Admin)
`GET /api/contact`

---

## Application Settings

### 1. Get Settings
`GET /api/settings`

Returns active user role (`reporter`, `authority`, `admin`), contact presets, AI waterfall configuration, and email sync parameters.

### 2. Update Settings
`POST /api/settings`

Updates and persists application configuration.

---

## Geocoding Proxies

### 1. Reverse Geocoding
`GET /api/geocode/reverse?lat=50.9882&lng=3.7719`

Converts coordinates to street, municipality, and postal code via OpenStreetMap Nominatim with caching and CORS proxying.

### 2. Forward Geocoding Search
`GET /api/geocode/search?q=Bergbosstraat+Merelbeke`

Searches Belgian addresses matching the query.

---

## Core Data Models

### `ReportItem`
| Field | Type | Description |
|---|---|---|
| `id` | `string` | Unique identifier (e.g. `rep-1788712095034`) |
| `title` | `string` | Human-readable title of the road defect |
| `rawDefectHint` | `string` | Citizen's original input or voice transcript |
| `fullReportText` | `string` | Formal, detailed report text |
| `impactedGroups` | `ImpactedGroup[]` | `["voetgangers" \| "fietsers" \| "openbaar_vervoer" \| "gemotoriseerd"]` |
| `location` | `object` | Latitude, longitude, address, street, municipality, postalCode |
| `photos` | `PhotoItem[]` | Base64 photos with EXIF GPS metadata |
| `contactInfo` | `object` | First name, last name, email, wantsResponse |
| `submissionStatus` | `SubmissionStatus` | `"concept" \| "verzenden" \| "ingediend" \| "bevestigd" \| "in_behandeling" \| "doorgestuurd" \| "opgelost" \| "afgewezen"` |
| `trackingCode` | `string?` | Official dossier reference (e.g. `MWV-2026-84920` or `KM-2026-08317`) |
| `incidentCodes` | `string[]?` | All associated tracking references |
| `timeline` | `TimelineEvent[]` | Historical chronological status events |
| `emails` | `EmailCorrespondence[]` | Linked incoming and outgoing messages |
| `automationLogs` | `AutomationLogStep[]` | Execution logs of automated actions |

### `EmailCorrespondence`
| Field | Type | Description |
|---|---|---|
| `id` | `string` | Unique email ID |
| `messageId` | `string` | RFC822 Message-ID header |
| `date` | `string` (ISO 8601) | Date email was received or sent |
| `from` | `string` | Sender name and email address |
| `to` | `string` | Recipient address |
| `subject` | `string` | Subject line |
| `body` | `string` | Plain text content |
| `htmlBody` | `string?` | Renderable HTML content |
| `attachments` | `EmailAttachment[]?` | Attached inspection photos or documents |
| `matchedReportId` | `string?` | Linked report dossier ID |
| `matchScore` | `number` | Confidence score (0.0 to 1.0) |
| `extractedTrackingCode` | `string?` | Primary incident code detected |
| `extractedCodes` | `string[]?` | All incident references found in thread |
| `read` | `boolean?` | Read status |

---

## Interactive Explorer

To explore the endpoints interactively and execute live test requests against the backend:
- Navigate to **[Swagger UI (`/docs`)](/docs)** in your browser.
- Or download the complete machine-readable specification from **[`/docs.json`](/docs.json)**.
