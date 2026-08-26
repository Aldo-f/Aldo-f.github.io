---
title: Technology Stack
description: Radio Community technology stack and dependencies
---

# Technology Stack

## Backend

| Technology | Purpose |
|------------|---------|
| **Node.js** | Runtime environment |
| **Express** | Web framework and API server |
| **node-postgres (pg)** | PostgreSQL database driver |
| **axios** | HTTP client for external APIs |

## Database

| Technology | Purpose |
|------------|---------|
| **PostgreSQL** | Relational database for all data |
| **SQL Schema** | Table definitions in `init.postgres.sql` |

## Frontend

| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **TypeScript** | Type-safe JavaScript |
| **Tailwind CSS** | Utility-first CSS framework |
| **DaisyUI** | Component library built on Tailwind |
| **Vite** | Build tool and dev server |

## Streaming

| Technology | Purpose |
|------------|---------|
| **Icecast** | Icecast streaming server |
| **Liquidsoap** | Stream automation and playlist management |

## External Services

| Service | Purpose |
|---------|---------|
| **Joe.be API** | Belgian radio track data |
| **Deezer API** | Music catalog and downloads |
| **auth-service** | OAuth 2.0 authentication |

## Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Express   │────▶│ PostgreSQL  │
│  (React)    │     │   Server    │     │  Database   │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
         ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
         │ Joe.be  │ │ Deezer  │ │  Icecast │
         │   API   │ │   API   │ │ + Liquid │
         └─────────┘ └─────────┘ └─────────┘
```

## Code Style

### Backend (JavaScript)
- Language: JavaScript (ES6+) with CommonJS modules
- Indentation: 4 spaces
- Line Length: Soft limit 120 characters
- Functions: Prefer async/await with early returns

### Frontend (TypeScript/React)
- Language: TypeScript with React 18
- Styling: Tailwind CSS + DaisyUI
- Indentation: 2 spaces
- TypeScript: Strict mode, no `any` allowed
- Hooks: Follow react-hooks rules (exhaustive deps)