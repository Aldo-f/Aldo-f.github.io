# PROJECT KNOWLEDGE BASE

**Generated:** 2026-09-13 16:50:00 UTC
**Commit:** 511114d
**Branch:** main

## OVERVIEW
Backend service layer containing business logic for report storage, AI processing, email handling, and municipal integrations.

## STRUCTURE
```
server/services/
├── storage.ts          # Report persistence (JSON file-based)
├── ai.ts               # AI service integration (defect analysis, report generation)
├── aiKeyEncoder.ts     # AES-256 encryption for API keys
├── emailSync.ts        # Email processing and synchronization
├── imapService.ts      # IMAP email polling
├── meldpuntBot.ts      # Integration with MeldpuntWegen.be system
└── reminderCron.ts     # Scheduled email reminders
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Report Storage | storage.ts | getReports, saveReports, ID generation |
| AI Features | ai.ts | analyzeDefect, generateFullReport, generateEmailReply |
| Email Handling | emailSync.ts, imapService.ts | processIncomingEmail, simulateIncomingEmail |
| Municipal API | meldpuntBot.ts | executeMeldpuntSubmission to Belgian road authority |
| Security | aiKeyEncoder.ts | Encrypt/decrypt API keys before storage |

## CONVENTIONS
- **Service Pattern**: Each file exports functions for a specific concern
- **Error Handling**: Try/catch with standardized error responses
- **Data Flow**: Functions accept plain objects, return processed results
- **Async/Await**: All I/O operations use async/await
- **Configuration**: Settings loaded from AppSettings interface (user-defined)
- **Base64 Images**: Photos stored as base64 dataUrls in ReportItem
- **Encrypted Keys**: AI API keys encrypted at rest using aiKeyEncoder

## ANTI-PATTERNS (THIS PROJECT)
- No direct file system access outside storage.ts
- No hardcoded AI provider keys (use AppSettings from UI configuration)
- No blocking synchronous operations
- No console.log in production code
- No tight coupling between services (loose interface-based)
- No default accounts or models in source (user-configured only)

## UNIQUE STYLES
- **AI Waterfall**: Multiple AI providers with fallback mechanism (configured via UI)
- **Email-First Processing**: Supports email-triggered report creation
- **Timeline Automation**: Automatic timeline events for status changes
- **Municipal Abstraction**: Pluggable architecture for different city integrations
- **Encrypted Storage**: API keys stored encrypted using AES-256
- **Firestore Primary**: All data now stored in Firebase Firestore (see firestoreStorage.ts)