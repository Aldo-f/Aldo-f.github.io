# UrbanFix Architecture Documentation

**Version:** 1.0.0
**Last Updated:** 2026-09-13
**Commit:** 04bf875

---

## 1. System Overview

UrbanFix is a full-stack web application for reporting and managing road defects/incidents in Flanders, Belgium. The system provides AI-powered analysis, email processing, and municipal integration for citizens and authorities.

### Core Value Proposition
- Citizens report road defects with photos and GPS location
- AI analyzes photos and generates detailed reports
- Email correspondence with municipalities is automatically processed
- Real-time status tracking through timeline events
- Integration with MeldpuntWegen.be and AWV systems

### Key Metrics
- **Total Files:** 181 (excluding node_modules, .git)
- **TypeScript Lines:** ~24,183
- **Frontend Components:** 17
- **Backend Services:** 9
- **AI Providers:** 5+ (configurable)

---

## 2. Technology Stack

### Frontend
| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Framework | React | 19.0.1 | UI library with hooks and concurrent rendering |
| Build Tool | Vite | 6.2.3 | Fast development server and production builds |
| Language | TypeScript | 5.8.2 | Type safety across the entire codebase |
| Styling | Tailwind CSS | 4.1.14 | Utility-first CSS framework |
| Maps | Leaflet | 1.9.4 | Interactive map visualization |
| Icons | Lucide React | 0.546.0 | Icon library |
| Animations | Motion | 12.23.24 | declarative animations |
| PWA | vite-plugin-pwa | 1.3.0 | Progressive Web App capabilities |

### Backend
| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Runtime | Node.js | 22+ | JavaScript runtime |
| Framework | Express | 4.21.2 | Web server framework |
| Bundler | esbuild | 0.25.0 | Production server bundling |
| Runner | tsx | 4.21.0 | TypeScript execution for dev |
| Logging | Pino | 10.3.1 | Structured logging |
| Email | Nodemailer | 9.0.6 | SMTP email sending |
| Email Parsing | mailparser | 3.9.17 | IMAP email processing |

### Database & Cloud
| Service | Technology | Purpose |
|---------|------------|---------|
| Primary Storage | Firebase Firestore | Reports, emails, settings persistence |
| Authentication | Firebase Auth | User authentication and authorization |
| AI Providers | Google Gemini, OpenAI, Anthropic, Groq, OpenRouter | Multi-provider AI waterfall |
| Hosting | Railway / Docker | Production deployment |

### Development & Testing
| Tool | Purpose |
|------|---------|
| Vitest | Unit testing framework |
| Playwright | End-to-end testing |
| ESLint | Code linting |
| Prettier | Code formatting |
| Husky | Git hooks |
| lint-staged | Pre-commit linting |

---

## 3. Architecture Patterns

### 3.1 Layered Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Pages/    │  │ Components/ │  │    Utils (UI helpers)   │ │
│  │  (Route     │  │  (Reusable  │  │    (deduplication,      │ │
│  │   specific) │  │   UI)       │  │     exif parsing)       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                          SERVICES LAYER                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Firestore  │  │     AI      │  │      Email Sync         │ │
│  │   Storage   │  │  Providers  │  │    (IMAP, processing)   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Meldpunt   │  │  Reminders  │  │      IMAP Service       │ │
│  │   Bot       │  │   Cron      │  │    (email polling)      │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                           API LAYER                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Express Routes (server.ts)                   │ │
│  │  • REST API endpoints (/api/*)                           │ │
│  │  • SSE endpoints (/api/sse)                              │ │
│  │  • Auth middleware (Firebase)                             │ │
│  │  • CSRF protection                                      │ │
│  └───────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                        INFRASTRUCTURE LAYER                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Firebase  │  │   Docker    │  │       CI/CD             │ │
│  │  (Firestore │  │  (Docker    │  │   (GitHub Actions)      │ │
│  │   , Auth)   │  │   Compose)  │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Data Flow Architecture

#### Report Creation Flow
```
User → NewReportWorkflow → AI Analysis → Report Save → Firestore
                                ↓
                         Photo Upload (base64)
                                ↓
                         GPS Extraction (EXIF)
                                ↓
                         Reverse Geocode (Nominatim proxy)
```

#### Email Processing Flow
```
IMAP Server → emailSync.ts → processIncomingEmail()
                    ↓
         Match to Report (fuzzy matching)
                    ↓
         Create Report if no match
                    ↓
         Update Timeline + Send Notifications
```

#### AI Waterfall Flow
```
Request → Provider 1 (FreeLLM) → Success? → Response
                  ↓ No
          Provider 2 (Google SDK) → Success? → Response
                      ↓ No
              Provider 3 (OpenRouter) → Success? → Response
                          ↓ No
                Provider 4 (OpenAI Direct) → Success? → Response
                            ↓ No
                  Provider 5 (Groq) → Success? → Response
                              ↓ No
                    Deterministic Fallback
```

### 3.3 Real-time Updates

The application uses **Server-Sent Events (SSE)** for real-time updates:

```
┌─────────┐     HTTP/SSE      ┌─────────┐
│ Browser │ ←───────────────→ │ Server  │
│  (React)│    EventSource    │(Express)│
└─────────┘                   └────┬────┘
                                   │
                          ┌────────┴────────┐
                          │  Firestore      │
                          │  Real-time      │
                          │  Listeners      │
                          └─────────────────┘
```

**SSE Events:**
- `init` - Initial data on connection
- `reports` - Report changes (create, update, delete)
- `emails` - Email changes

---

## 4. Component Architecture

### 4.1 Frontend Structure

```
src/
├── main.tsx                 # React entry point
├── App.tsx                  # Main app component (routing, state)
├── types.ts                 # Central TypeScript interfaces
├── firebase.ts              # Firebase initialization and helpers
├── components/              # Reusable UI components (17 total)
│   ├── AIWaterfallSettings.tsx    # AI provider configuration
│   ├── NewReportWorkflow.tsx      # Multi-step report creation
│   ├── MapView.tsx               # Leaflet map visualization
│   ├── TimelineView.tsx          # Status history display
│   ├── EmailInbox.tsx            # Email list view
│   ├── SettingsModal.tsx         # Application settings
│   ├── ReportCard.tsx            # Report summary card
│   ├── LocationPickerMap.tsx     # GPS location picker
│   └── ... (9 more components)
├── pages/                   # Route-specific pages (10 total)
│   ├── HomePage.tsx              # Dashboard (map + list)
│   ├── IncidentDetailPage.tsx    # Report detail view
│   ├── NewIncidentPage.tsx       # Report creation
│   ├── DocsPage.tsx              # API documentation
│   └── ... (6 more pages)
└── utils/                   # Utility functions (10 files)
    ├── aiModels.ts               # AI provider configuration
    ├── aiKeyEncoder.ts           # API key encryption
    ├── deduplication.ts          # Report deduplication
    ├── exifParser.ts             # Photo GPS extraction
    ├── geo.ts                    # Geolocation utilities
    └── ... (5 more utils)
```

### 4.2 Backend Structure

```
server/
├── server.ts                  # Main Express server (838 lines)
├── logger.ts                  # Logging configuration
├── swagger.ts                 # OpenAPI specification
├── middleware/
│   └── errorLogger.ts         # Error handling middleware
├── services/
│   ├── firestoreStorage.ts    # PRIMARY: Firestore storage layer
│   ├── storage.ts             # Legacy: JSON file storage
│   ├── ai.ts                  # AI service integration
│   ├── aiKeyEncoder.ts        # API key encryption
│   ├── emailSync.ts           # Email processing
│   ├── imapService.ts         # IMAP email polling
│   ├── meldpuntBot.ts         # MeldpuntWegen.be integration
│   ├── meldpuntBrowser.ts     # Browser automation for submission
│   ├── reminderCron.ts        # Scheduled reminders
│   ├── smtpSend.ts            # SMTP email sending
│   └── ... (more services)
└── utils/
    ├── id.ts                  # ID generation
    └── withAsyncError.ts      # Async error wrapper
```

---

## 5. Data Model

### 5.1 Core Entities

#### ReportItem (Primary Entity)
```typescript
interface ReportItem {
  id: string;                      // Unique identifier (rep-{timestamp})
  title: string;                   // Report title/summary
  rawDefectHint: string;           // Original user description
  fullReportText: string;          // AI-generated detailed report
  impactedGroups: ImpactedGroup[]; // Affected road users
  photos: PhotoItem[];             // Uploaded photos with GPS
  location: Location;              // GPS coordinates and address
  contactInfo: ContactInfo;        // Reporter contact details
  submissionStatus: SubmissionStatus;
  trackingCode?: string;           // Municipality reference
  submissionDate?: string;         // ISO timestamp
  lastUpdatedDate: string;         // ISO timestamp
  assignedAuthority?: string;      // Responsible department
  emails: EmailCorrespondence[];   // Linked email thread
  timeline: TimelineEvent[];       // Status history
  automationLogs: AutomationLog[]; // System automation records
}
```

#### EmailCorrespondence
```typescript
interface EmailCorrespondence {
  id: string;
  messageId?: string;
  date: string;
  from: string;
  to: string;
  subject: string;
  body: string;
  htmlBody?: string;
  attachments?: Attachment[];
  matchedReportId?: string;
  matchScore: number;              // 0.0 to 1.0
  isReply: boolean;
  statusUpdate?: SubmissionStatus;
  extractedTrackingCode?: string;
  senderAuthority?: string;
  read?: boolean;
}
```

#### TimelineEvent
```typescript
interface TimelineEvent {
  id: string;
  timestamp: string;
  title: string;
  description: string;
  authority: string;
  status?: SubmissionStatus;
  actorType: "authority" | "citizen" | "system" | "municipality";
  isOfficial?: boolean;
}
```

### 5.2 Firestore Collections

| Collection | Document ID | Purpose |
|------------|-------------|---------|
| `reports` | `{reportId}` | All incident reports |
| `emails` | `{emailId}` | Email correspondence |
| `settings` | `global_settings` | Application settings |
| `faq` | Auto-generated | FAQ entries |
| `partners` | Auto-generated | Municipality partners |
| `contact_messages` | `{messageId}` | Contact form submissions |

---

## 6. API Architecture

### 6.1 REST Endpoints

#### Reports (`/api/reports`)
```http
GET    /api/reports              # List all reports
GET    /api/reports/:id          # Get specific report
POST   /api/reports              # Create/update report
DELETE /api/reports/:id          # Delete report
POST   /api/reports/:id/timeline # Add timeline event
```

#### AI Features (`/api/ai`)
```http
POST /api/ai/analyze-defect      # Analyze photos for defects
POST /api/ai/generate-report     # Generate report text
POST /api/ai/generate-reply      # Generate email reply
POST /api/ai/generate-reminder   # Generate reminder email
POST /api/ai/test-provider       # Test AI provider connection
```

#### Emails (`/api/emails`)
```http
GET    /api/emails                         # List all emails
POST /api/emails/process-incoming         # Process incoming email
POST /api/emails/simulate-incoming        # Simulate email (testing)
POST /api/emails/:id/read                 # Mark email as read
POST /api/emails/send-reply               # Send AI reply via SMTP
POST /api/emails/send-reminder            # Send reminder email
POST /api/emails/:id/assign-report        # Link email to report
POST /api/emails/:id/create-report        # Create report from email
POST /api/emails/auto-link                # Auto-link all emails
POST /api/emails/poll-now                 # Trigger IMAP poll
POST /api/emails/seed-sample-thread       # Seed demo data
```

#### Meldpunt Integration (`/api/meldpunt`)
```http
POST /api/meldpunt/submit    # Submit to MeldpuntWegen.be
```

#### Settings (`/api/settings`)
```http
GET  /api/settings           # Get settings
POST /api/settings           # Update settings (admin only)
```

#### Utilities (`/api`)
```http
GET  /api/faq                # Get FAQ data
GET  /api/partners           # Get municipality partners
GET  /api/stats              # Get platform statistics
GET  /api/contact            # Get contact messages
POST /api/contact            # Submit contact message
GET  /api/geocode/reverse    # Reverse geocoding proxy
GET  /api/sse                # Server-Sent Events stream
GET  /api/health             # Health check
```

### 6.2 API Response Format

All API responses follow a consistent format:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Or for errors:
```json
{
  "success": false,
  "data": null,
  "error": "Error message"
}
```

---

## 7. Storage Architecture

### 7.1 Primary Storage: Firebase Firestore

**Why Firestore:**
- Real-time synchronization across clients
- Automatic scaling
- Offline support
- Integrated with Firebase Auth
- No server maintenance

**Firestore Security Rules:**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Reports: Admin can read/write, others read-only
    match /reports/{reportId} {
      allow read: if request.auth != null;
      allow write: if request.auth.token.admin == true;
    }
    
    // Emails: Admin can read/write
    match /emails/{emailId} {
      allow read, write: if request.auth.token.admin == true;
    }
    
    // Settings: Admin only
    match /settings/{docId} {
      allow read, write: if request.auth.token.admin == true;
    }
  }
}
```

### 7.2 Data Migration

**Migration Script:** `scripts/migrate-to-firestore.mjs`

Transfers data from:
- `data/reports.json` → Firestore `reports` collection
- `data/emails.json` → Firestore `emails` collection
- `data/settings.json` → Firestore `settings/global_settings` document

**Migration Process:**
1. Read JSON files from `data/` directory
2. Batch write to Firestore using `writeBatch()`
3. Verify migration completeness
4. Keep JSON files as backup (optional deletion after verification)

---

## 8. AI Architecture

### 8.1 Provider Waterfall

The AI system supports multiple providers with automatic fallback:

```
Priority 1: FreeLLM Proxy (gemini-3.7-flash)
Priority 2: Google SDK (gemini-3.7-flash)
Priority 3: OpenCode Custom (opencode-v1)
Priority 4: Google SDK (gemini-2.5-flash)
Priority 5: OpenRouter Free (google/gemini-2.0-flash-exp:free)
```

### 8.2 AI Services

| Service | Function | Purpose |
|---------|----------|---------|
| `analyzeDefect` | Analyze photos | Detect road defects from images |
| `generateFullReport` | Generate text | Create detailed report text |
| `generateEmailReply` | Generate reply | Draft email responses |
| `generateReminderEmail` | Generate reminder | Create follow-up emails |
| `testAIProvider` | Test connection | Verify provider connectivity |

### 8.3 AI Configuration

Users configure AI providers via the UI (`AIWaterfallSettings` component):
- Provider selection (Google, OpenAI, Anthropic, Groq, OpenRouter)
- Model selection per provider
- API key management (encrypted at rest)
- Temperature and verbosity settings
- Vision capability detection

---

## 9. Email Architecture

### 9.1 Email Processing Pipeline

```
IMAP Server → imapService.ts → emailSync.ts
                    ↓
         Parse email content
                    ↓
         Extract tracking codes
                    ↓
         Fuzzy match to reports
                    ↓
         Create/update report
                    ↓
         Generate timeline event
                    ↓
         Send notification
```

### 9.2 Fuzzy Matching Algorithm

The email-to-report matching uses:
1. Text normalization (remove line endings, punctuation, lowercase)
2. N-gram overlap ratio calculation
3. Tracking code extraction (regex: `MWV-\d+`, `Dossier: [A-Z0-9-]+`)
4. Score threshold (matchScore > 0.7 = high confidence)

### 9.3 Email Types

| Type | Description |
|------|-------------|
| `confirmation` | Automatic acknowledgment from AWV |
| `response` | Authority response to report |
| `reminder` | Follow-up reminder email |
| `simulation` | Test email for development |

---

## 10. Authentication & Authorization

### 10.1 Firebase Authentication

**Auth Providers:**
- Google Sign-In (popup)
- Email/Password
- Anonymous login (fallback)

**Role-Based Access Control:**
```typescript
type UserRole = "admin" | "authority" | "reporter";

const ADMIN_EMAILS = [
  "aldo.fieuw@gmail.com",
  "aldo@urbanfix.be"
];

const AUTHORITY_EMAIL_DOMAINS = [
  "vlaanderen.be",
  "awv.vlaanderen.be",
  "gemeente.be",
  "stad.be",
  "merelbeke-melle.be",
  "merelbeke.be"
];
```

**Role Permissions:**
| Role | Can View | Can Edit | Can Manage | Can Submit |
|------|----------|----------|------------|------------|
| admin | All | All | All | All |
| authority | All | Status only | Own reports | Yes |
| reporter | Own | Own | No | Yes |

### 10.2 API Authentication

All API endpoints (except health/docs) require Firebase ID token:
```http
Authorization: Bearer <firebase_id_token>
```

**Soft Auth Fallback:**
If Firebase Admin SDK is not configured, the API defaults to Aldo's admin user for development.

---

## 11. Deployment Architecture

### 11.1 Docker Deployment

**Production:**
```bash
docker compose up -d --build
```

**Development:**
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

**Services:**
| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| urbanfix | Custom (Node.js) | 3000 | Main application |

**Network:**
- Requires `traefik_net` network (from 01-core-infra)
- Traefik reverse proxy for routing
- SSL termination at proxy level

### 11.2 Production Build

```bash
npm run build      # Vite + esbuild
npm start          # Run from dist/
```

**Output:**
- `dist/` - Built frontend assets
- `dist/server.cjs` - Bundled Express server

---

## 12. Development Workflow

### 12.1 Local Development

```bash
# Install dependencies
bun install

# Copy environment
cp .env.example .env

# Start development server
npm run dev       #tsx server.ts (hot reload)
```

**Development Server:**
- Vite dev server: http://localhost:3000
- Express middleware: Same port
- HMR: Enabled by default

### 12.2 Code Quality

**Pre-commit Hooks:**
```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

**Linting:**
```bash
npm run lint      # ESLint with auto-fix
```

**Testing:**
```bash
npm run test      # Vitest unit tests
npm run test:e2e  # Playwright E2E tests
```

---

## 13. Key Files Reference

### Critical Files
| File | Purpose | Lines |
|------|---------|-------|
| `server.ts` | Main Express server, routes, middleware | 838 |
| `src/App.tsx` | Main React component, state management | 821 |
| `src/types.ts` | Central TypeScript interfaces | 350 |
| `src/firebase.ts` | Firebase initialization and helpers | 375 |
| `server/services/firestoreStorage.ts` | Primary data storage layer | 350+ |
| `server/services/ai.ts` | AI service integration | 723 |
| `src/components/AIWaterfallSettings.tsx` | AI configuration UI | 2187 |

### Configuration Files
| File | Purpose |
|------|---------|
| `package.json` | Dependencies and scripts |
| `vite.config.ts` | Vite build configuration |
| `tsconfig.json` | TypeScript configuration |
| `firebase-applet-config.json` | Firebase project config |
| `.env.example` | Environment variables template |
| `docker-compose.yml` | Docker production config |
| `docker-compose.dev.yml` | Docker development override |

---

## 14. Changing the Application

### Adding a New Page
1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Add navigation link in `src/components/Header.tsx`
4. Update `docs/FRONTEND_ROUTES.md`

### Adding a New API Endpoint
1. Add route handler in `server.ts`
2. Create service function in `server/services/`
3. Update OpenAPI spec in `server/swagger.ts`
4. Add tests in `test/`

### Adding a New AI Provider
1. Add provider config in `src/utils/aiModels.ts`
2. Update `DEFAULT_AI_ACCOUNTS` (if needed)
3. Add provider type in `src/types.ts`
4. Update `AIWaterfallSettings.tsx` UI

### Modifying Data Models
1. Update interface in `src/types.ts`
2. Update Firestore security rules
3. Update migration script if needed
4. Update API documentation

---

## 15. Security Considerations

### API Key Security
- All AI API keys are encrypted at rest using AES-256
- Encrypted keys stored in Firestore with `enc:` prefix
- Decryption happens only at runtime in server processes

### Input Validation
- All API inputs validated on arrival
- File uploads limited to 25MB (base64 encoded images)
- CSRF protection enabled for non-API routes
- Firebase Auth verification for all API endpoints

### Data Privacy
- Email content stored in Firestore (encrypted at rest by Firebase)
- GPS coordinates stored with reports
- No PII transmitted to AI providers except necessary context
- GDPR compliance for Belgian data protection

---

## 16. Performance Optimizations

### Current Optimizations
- Base64 image compression before storage
- N-gram fuzzy matching for email processing (optimized)
- Batch writes to Firestore for efficiency
- SSE for real-time updates (no polling)
- Lazy loading of route components

### Future Improvements
- Image CDN integration
- Firestore pagination for large datasets
- Redis caching for frequent queries
- WebRTC for real-time collaboration

---

## 17. Known Limitations

1. **Single Region:** Firestore database fixed to one region
2. **No Offline PWA:** PWA caching limited to static assets
3. **JSON Legacy:** Some services still reference JSON storage
4. **Manual Migration:** Data migration requires script execution
5. **Rate Limits:** AI providers have rate limits (handled by waterfall)

---

## 18. Future Roadmap

### Phase 1: Core Stability (Current)
- [x] Migrate to Firestore
- [x] Remove hardcoded defaults
- [x] Add comprehensive documentation
- [ ] Complete migration testing
- [ ] Remove legacy JSON storage

### Phase 2: Feature Enhancement
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Multi-language support expansion

### Phase 3: Scale & Integration
- [ ] Webhook integrations
- [ ] Advanced reporting
- [ ] Machine learning model training
- [ ] API marketplace for municipalities

---

**Document Version:** 1.0.0
**Next Review:** After Phase 1 completion
**Maintainers:** Aldo Fieuw, UrbanFix Team
