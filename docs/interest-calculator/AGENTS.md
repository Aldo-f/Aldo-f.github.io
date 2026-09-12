# AGENTS.md — 06-apps-interest-calculator

Interest calculator for Belgian mortgage dossiers. Bundled single-page app (Bun/TS + Vite).

## Structure

```
06-apps-interest-calculator/
├── src/components/     # React components (DossierWorkflow, SharedView, Header, ReconciliationModal)
├── server.ts           # Bun server (serves SPA + API)
├── index.html          # Vite entry
├── vite.config.ts      # Vite config
├── tsconfig.json       # TypeScript config
├── .env.example        # Required env vars template
└── metadata.json       # AI Studio manifest
```

## Commands

```bash
bun install
bun run dev          # http://localhost:3000
bun run build        # → dist/
bun start            # production
```

## Conventions

- Bun runtime (not Node); use `bun.lock` not `package-lock.json`
- Single-server architecture: Bun serves both API and static assets
- Strict TypeScript — no `any`
- Environment variables from `.env` (gitignored); `.env.example` is tracked

## Anti-patterns

- ❌ Don't add dependencies without updating `bun.lock`
- ❌ Don't commit `.env` with real keys
- ❌ Don't use Node.js — this is a Bun project
- ❌ Don't add a database; uses `database.json` file storage
