---
title: Project Structure
description: Radio Community project structure and file organization
---

# Project Structure

```
radio-community/
├── server.js              # Main Express server (2608 lines, 80+ routes)
├── package.json           # Node.js dependencies
├── docker-compose.yml     # Service orchestration
├── Dockerfile             # Container image (www-data user for file ownership)
├── .env                   # Environment variables (secrets)
│
├── db/
│   └── init.postgres.sql  # PostgreSQL database schema
│
├── utils/
│   ├── auth.js            # Permission system (ROLES, PERMISSIONS, isAdmin)
│   ├── slugify.js         # URL slug generation
│   └── fileUtils.js       # File operations (setOwnership)
│
├── streams/
│   ├── deezerDownloader.js  # Deezer API integration + track download
│   ├── joeBeDownloader.js   # Joe.be API integration
│   └── streamManager.js     # Liquidsoap stream management
│
├── frontend/
│   ├── src/
│   │   ├── components/    # 17 React components
│   │   ├── pages/         # 6 route pages
│   │   ├── types/         # Shared TypeScript interfaces
│   │   └── lib/           # Context providers, auth
│   └── dist/              # Built frontend (served by Express)
│
└── tests/
    ├── e2e/               # Playwright E2E tests
    └── unit/              # Jest unit tests
```

## Key Directories

### `/server.js`
Main Express server handling:
- API routes (80+ endpoints)
- Frontend static file serving
- Authentication middleware
- Database operations

### `/utils/`
- `auth.js` - Permission system with ROLES, PERMISSIONS, and helper functions
- `slugify.js` - URL-safe slug generation for community names
- `fileUtils.js` - File operations including ownership management

### `/streams/`
- `streamManager.js` - Liquidsoap container lifecycle management
- `joeBeDownloader.js` - Joe.be API integration and track fetching
- `deezerDownloader.js` - Deezer API integration and track downloads

### `/frontend/src/`
- 17 React components for UI
- 6 route pages (Home, Community, Create, Manage, etc.)
- Shared TypeScript types for consistency

### `/db/`
- `init.postgres.sql` - Complete database schema and seed data