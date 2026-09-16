# AGENTS.md — 06-apps-neo-brutalist-home

React + Vite neobrutalist component library for the neo-brutalist homepage. Deployed via `01-core-infra/roles/neo-brutalist-home` as a static site.

## OVERVIEW

React + Vite neobrutalist component library and homepage for the home lab dashboard.

## STRUCTURE

```
06-apps-neo-brutalist-home/
├── config/              # Deployment config (nginx, TLS)
├── docker/              # Dockerfile for static build
├── specs/               # Spec-kit feature specifications
├── docker-compose.yml   # Local dev compose
├── package.json         # Vite + React 18, TypeScript
└── package-lock.json
```

## WHERE TO LOOK

| Task | Location |
|------|----------|
| Component development | `specs/` + Vite dev server |
| Build for deployment | `docker/` (multi-stage) |
| Deploy to Pi | `01-core-infra/roles/neo-brutalist-home` |

## CONVENTIONS

- **pnpm forbidden** — uses npm (package-lock.json present)
- **Static export** — Vite builds to `dist/`, served by nginx in container
- **Neobrutalist styling** — raw CSS, no Tailwind, no component library
- **Spec-driven** — features spec'd in `specs/<nn>-<name>/` before implementation

## ANTI-PATTERNS

- ❌ Don't add Tailwind or CSS frameworks — raw CSS only
- ❌ Don't use `npm install` — use `npm ci` for reproducible builds
- ❌ Don't edit deployed static files — edit source and rebuild via Docker