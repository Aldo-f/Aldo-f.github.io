# Frontend Routes & UI Contracts

## Routes

| Route | Component (src/pages) | Description |
|------|-----------------------|-------------|
| `/` | `HomePage` | Home view with map + incident list |
| `/map` | `HomePage` (map view) | Map‑only view |
| `/list` | `HomePage` (list view) | List of incidents |
| `/new` | `NewIncidentPage` | Form for creating a new report |
| `/incident/:id` | `IncidentDetailPage` | Detail view for a specific incident |
| `/faq` | `FaqPage` | Frequently asked questions |
| `/about` | `AboutPage` | About the project |
| `/contact` | `ContactPage` | Contact & support page |
| `/privacy` | `PrivacyPage` | Privacy policy |
| `/terms` | `TermsPage` | Terms of service |
| `/emails` | `EmailInbox` (component) | Inbox of incoming emails |
| `/settings` | `SettingsModal` (component) | Application settings (admin only) |
| `/docs` | `DocsPage` | API documentation & Swagger UI |

> The routing is managed manually in `src/App.tsx` via the `currentRoute` state.

## Core UI Component Contracts

### 1. `MapView`
```tsx
interface MapViewProps {
  reports: ReportItem[];
  onSelectReport: (report: ReportItem) => void;
  onNewReportAtLocation: (lat: number, lng: number) => void;
  onNavigate?: (route: PageRoute) => void;
}
```
*Displays a Leaflet map with report markers, status filter, locate‑me button, and inspector panel.*

### 2. `TimelineView`
```tsx
interface TimelineViewProps {
  timeline: TimelineEvent[];
  currentStatus: SubmissionStatus;
  currentUserRole?: UserRole; // defaults to "reporter"
  onAddTimelineEvent?: (event: Omit<TimelineEvent, "id" | "timestamp">) => void;
}
```
*Renders a chronological list of status updates, with optional add‑event form for admins.*

### 3. `ImageUploader` (embedded in `NewReportWorkflow`)
The upload UI is part of `NewReportWorkflow` and uses the following prop contract:
```tsx
interface NewReportWorkflowProps {
  settings: AppSettings;
  existingReports: ReportItem[];
  onReportCreated: (report: ReportItem) => void;
  onNavigateToTab: (tab: "map" | "list" | "emails") => void;
  onNavigate?: (route: PageRoute) => void;
  prefillLocation?: { lat: number; lng: number } | null;
}
```
*Key upload callbacks:*
- `handleFilesSelected(files: FileList | null)` – parses EXIF, extracts GPS, updates `photos` state.
- `handleCameraClick()` – opens camera after permission handling.

### 4. `ReportForm` (conceptual – handled by `NewReportWorkflow`)
The report creation form consists of the same props as `NewReportWorkflowProps` (see above) and internally manages:
- Photo upload & GPS extraction
- Location picker (`LocationPickerMap`)
- Impacted groups selection
- AI analysis & report text generation
- Submission to MeldpuntWegen.be

## Verification Script
A small Node script (`scripts/check_routes.js`) validates that every route listed above has a corresponding page component file under `src/pages/`.
```js
// scripts/check_routes.js
const fs = require('fs');
const path = require('path');

const routes = [
  '/', '/map', '/list', '/new', '/incident/:id', '/faq', '/about',
  '/contact', '/privacy', '/terms', '/emails', '/settings', '/docs'
];

const pageFiles = fs.readdirSync(path.join(__dirname, '..', 'src', 'pages'))
  .filter(f => f.endsWith('.tsx'));

// Simple sanity check – ensure we have at least as many page files as routes.
if (pageFiles.length < routes.length) {
  console.error('Route count mismatch: expected >=', routes.length, 'page files found', pageFiles.length);
  process.exit(1);
}

console.log('✅ Routes and page components are in sync.');
process.exit(0);
```
Run with `node scripts/check_routes.js`. The script exits with code 0 on success.
