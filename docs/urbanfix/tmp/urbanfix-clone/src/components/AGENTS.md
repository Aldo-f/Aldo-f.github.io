# Components Knowledge Base

**Generated:** 2026-09-13 16:50:00 UTC

## OVERVIEW
Reusable React UI components for the road defect reporting application. Uses Tailwind CSS, TypeScript, and modern React hooks.

## STRUCTURE
```
src/components/
├── AIWaterfallSettings.tsx   # AI provider configuration (largest - 2187 lines)
├── NewReportWorkflow.tsx     # Multi-step report creation form
├── MapView.tsx               # Leaflet map with report markers
├── TimelineView.tsx          # Status history display
├── EmailInbox.tsx            # Email viewing interface
├── SettingsModal.tsx         # Application settings
└── ... (17 components total)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Complex state management | src/components/AIWaterfallSettings.tsx | Provider waterfall configuration |
| Report creation flow | src/components/NewReportWorkflow.tsx | Multi-step form with validation |
| Map integration | src/components/MapView.tsx, LocationPickerMap.tsx | Leaflet maps, GPS handling |
| Email display | src/components/EmailInbox.tsx, HighlightedEmailBody.tsx | Email threading and parsing |

## KEY PATTERNS
- **Functional Components**: All components use hooks (useState, useEffect, useMemo)
- **Tailwind CSS**: Utility-first styling, responsive design
- **TypeScript Props**: Strict interfaces for all component props
- **Path Aliases**: Use `@/components/...` for imports

## ANTI-PATTERNS (THIS DIRECTORY)
- No direct DOM manipulation (use React refs)
- No inline styles (use Tailwind classes)
- No hardcoded API URLs (use relative paths)
- No blocking synchronous operations

## NOTES
- Large components (>1000 lines) may need refactoring into smaller sub-components
- Map components use Leaflet with custom markers for report status
- Email components handle base64 attachments and HTML formatting