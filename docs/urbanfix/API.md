# UrbanFix API Contract

- Base URL: `/api/*`
- Auth: none (public read; write via form / email sync)
- JSON responses: `{ success: boolean, data?: any, error?: string }`
- Frontend: `dist/` static build (React/Vite); can be deployed separately (e.g., Netlify/Vercel) pointing to any backend URL.
- Backend: `server.ts` (Express); serves `dist/` in production but can be split.
- Android backlog: Consume `/api/reports` (GET) and `/api/reports` (POST with JSON body matching `ReportItem` interface in `src/types.ts`). No Android code created (YAGNI).

## Endpoints

### Health & Info
- `GET /api/health` — Service health check
- `GET /api/faq` — Frequently asked questions
- `GET /api/partners` — Partner organizations
- `GET /api/stats` — Platform statistics

### Reports
- `GET /api/reports` — List all reports
- `GET /api/reports/:id` — Get single report by ID or trackingCode
- `POST /api/reports` — Create or update a report
- `DELETE /api/reports/:id` — Delete a report
- `POST /api/reports/:id/timeline` — Add timeline event to report

### AI Services
- `POST /api/ai/analyze-defect` — Analyze defect from image
- `POST /api/ai/generate-report` — Generate full report text
- `POST /api/ai/generate-reply` — Generate email reply
- `POST /api/ai/generate-reminder` — Generate reminder email
- `POST /api/ai/test-provider` — Test AI provider connectivity

### MeldpuntWegen.be Integration
- `POST /api/meldpunt/submit` — Submit report to MeldpuntWegen.be

### Emails & Synchronization
- `GET /api/emails` — List all emails
- `POST /api/emails/process-incoming` — Process incoming email
- `POST /api/emails/simulate-incoming` — Simulate incoming email for report
- `POST /api/emails/:id/read` — Mark email as read
- `POST /api/emails/send-reply` — Send AI-generated reply via SMTP
- `POST /api/emails/send-reminder` — Send reminder via SMTP
- `POST /api/emails/poll-now` — Trigger manual IMAP poll

### Contact
- `POST /api/contact` — Submit contact message
- `GET /api/contact` — List contact messages

### Real-time
- `GET /api/sse` — Server-Sent Events stream for real-time updates

## Swagger UI
- Available at `/docs` (interactive API documentation)

## Data Models

### ReportItem
See `src/types.ts` for full interface. Key fields:
- `id: string`
- `trackingCode?: string`
- `incidentCodes?: string[]`
- `title: string`
- `description: string`
- `location: { lat: number, lng: number, address?: string }`
- `photos: string[]` (base64 data URLs)
- `submissionStatus: SubmissionStatus`
- `timeline: TimelineEvent[]`
- `emails: EmailCorrespondence[]`

### TimelineEvent
- `id: string`
- `timestamp: string` (ISO 8601)
- `title: string`
- `description: string`
- `authority: string`
- `status: SubmissionStatus`
- `actorType: 'citizen' | 'authority' | 'system'`
- `isOfficial: boolean`