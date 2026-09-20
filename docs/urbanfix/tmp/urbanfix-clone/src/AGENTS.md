# PROJECT KNOWLEDGE BASE

**Generated:** 2026-09-13 16:50:00 UTC
**Commit:** 511114d
**Branch:** main

## OVERVIEW
Frontend React application containing UI components, page components, shared types, and utility functions. See subdirectory AGENTS.md for specific guidance.

## STRUCTURE
```
src/
├── components/   # Reusable UI components (see components/AGENTS.md)
├── pages/        # Route-specific page components (see pages/AGENTS.md)
├── types.ts      # Shared TypeScript interfaces
├── utils/        # Specialized helper functions (see utils/AGENTS.md)
├── main.tsx      # React entry point
└── App.tsx       # Main application component with routing
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Reusable UI | src/components/ | Header, Footer, Modals, Form controls, etc. |
| Page Views | src/pages/ | Home, Incident overview, Incident detail, etc. |
| Shared Types | src/types.ts | ReportItem, SubmissionStatus, TimelineEvent, etc. |
| Utilities | src/utils/ | Geo calculations, EXIF parsing, formatters |
| Sub-dir Docs | */AGENTS.md | Component-specific conventions in subdirectory docs |

## CONVENTIONS
- **Component Structure**: Functional components with React hooks
- **Styling**: Tailwind CSS utility classes
- **Type Safety**: Strict TypeScript interfaces for all props and state
- **File Naming**: PascalCase for components (.tsx), camelCase for utilities (.ts)
- **State Management**: React hooks (useState, useEffect) for local state
- **Routing**: Manual route state in App.tsx (not react-router-dom)
- **Path Aliases**: Use `@/components/...`, `@/pages/...`, `@/utils/...`

## ANTI-PATTERNS (THIS PROJECT)
- No direct DOM manipulation (use refs and effects)
- No hardcoded API URLs (use relative paths)
- No blocking operations in render
- No console.log in production builds
- No any types (strict TypeScript mode)
- No default AI accounts/models (user-configured via UI only)

## UNIQUE STYLES
- **AI-Integrated UI**: Components designed to display AI-generated analysis results
- **Multi-step Workflow**: NewReportWorkflow guides users through incident reporting
- **Real-time Updates**: Timeline components show live status changes
- **Map Integration**: Leaflet maps for location selection and visualization
- **Role-Based Views**: Different UI based on user role (admin, authority, citizen)

## SUBDIRECTORY DOCUMENTATION
- [src/components/AGENTS.md](components/AGENTS.md) - Component patterns and conventions
- [src/pages/AGENTS.md](pages/AGENTS.md) - Page routing and structure
- [src/utils/AGENTS.md](utils/AGENTS.md) - Utility functions and security