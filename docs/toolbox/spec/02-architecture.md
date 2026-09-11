# Architecture Overview

```
┌─────────────────────┐      ┌─────────────────────┐
│   Frontend (React)  │      │   Backend (Node)    │
│  - Vite dev server  │◀────▶│  - Express API      │
│  - ToolPage component│     │  - Tool CRUD routes │
│  - Dynamic Form lib │      │  - Execution engine│
│                     │      │  - Storage (JSON)   │
└─────────────────────┘      └─────────────────────┘
        ▲                               ▲
        │                               │
        ▼                               ▼
   Browser (user)                Docker container
        │                               │
        ▼                               ▼
   HTTP/HTTPS (Traefik)  ←→  /api/v1/* endpoints
```

## Layers
1. **Presentation** – React components generated from the UI spec (`ui‑design.md`).
2. **Application** – Express routes defined in `API‑spec.md`. All business logic lives in the **Execution Engine**.
3. **Persistence** – Simple JSON file (`data/tools.json`) or SQLite table; abstracted by the **Storage Layer**.
4. **Infrastructure** – Existing Docker‑Compose, Traefik, env‑vars remain untouched.

## Non‑functional
- **Stateless** – Execution engine does not keep session state; all required data travels in the request body.
- **Error‑first** – All responses follow `{ ok: boolean, data?: …, error?: string }`.
- **Extensible** – New tool types added by updating `tool‑schema.json` and UI components; no code change required.