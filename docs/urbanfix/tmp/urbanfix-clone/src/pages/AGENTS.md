# Pages Knowledge Base

**Generated:** 2026-09-13 16:50:00 UTC

## OVERVIEW
Route-specific page components for the road defect reporting application. Each page handles a specific URL route and associated business logic.

## STRUCTURE
```
src/pages/
├── HomePage.tsx              # Dashboard with map + incident list
├── IncidentDetailPage.tsx    # Single report detail view
├── NewIncidentPage.tsx       # Report creation form
├── FaqPage.tsx               # FAQ display
├── AboutPage.tsx             # About information
├── ContactPage.tsx           # Contact form
├── PrivacyPage.tsx           # Privacy policy
├── TermsPage.tsx             # Terms of service
└── DocsPage.tsx              # API documentation (Swagger UI)
```

## ROUTE MAPPING
| Route | Component | Description |
|-------|-----------|-------------|
| `/` | HomePage | Main dashboard with map and report list |
| `/map` | HomePage | Map-only view |
| `/list` | HomePage | List-only view |
| `/new` | NewIncidentPage | Create new report |
| `/incident/:id` | IncidentDetailPage | View/edit specific report |
| `/faq` | FaqPage | Frequently asked questions |
| `/contact` | ContactPage | Contact/support form |
| `/docs` | DocsPage | API documentation |

## KEY PATTERNS
- **React Router**: Manual route state management in App.tsx (not react-router-dom)
- **Firebase Integration**: Pages subscribe to Firestore for real-time updates
- **Role-Based Access**: Different pages visible based on user role (admin, authority, citizen)
- **Data Fetching**: Pages receive data via props from App.tsx state

## NOTES
- HomePage is the most complex page (1184 lines) with both map and list views
- IncidentDetailPage handles timeline events and email correspondence
- Public pages (About, Contact, Privacy, Terms, FAQ) don't require authentication
- DocsPage embeds Swagger UI for API exploration