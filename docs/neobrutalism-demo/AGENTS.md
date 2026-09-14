# AGENTS.md — Neobrutalism Demo

React + TypeScript + Vite demo showcasing neobrutalist UI components. Dual nature: standalone demo app plus a reusable component library.

## OVERVIEW

This project demonstrates neobrutalist design — bold borders, hard shadows, high contrast. It has two layers:

- **Demo app** (`src/`) — Vite + React 19, shows components in context
- **Component library** (`neobrutalism-components/`) — Next.js app serving as both the published component source and a live docs site

## STRUCTURE
```
.
├── src/                    # Demo app (Vite)
│   ├── components/         # Demo layout + chrome (navbar, sidebar, etc.)
│   ├── components/ui/      # shadcn/ui-style components used by the demo
│   └── app/page.tsx        # Demo entry point
├── neobrutalism-components/  # Component library (Next.js)
│   ├── src/components/     # Each component is a single file
│   ├── src/app/            # Docs site pages (Next.js)
│   ├── src/data/           # Theme, colors, registry JSON
│   └── src/scripts/        # Codegen (stars, charts, registry)
├── tailwind.config.js      # Tailwind v4 config
├── vite.config.ts          # Vite config with @ alias
└── package.json            # Root scripts (no workspaces)
```

## WHERE TO LOOK
| Task | Location |
|------|----------|
| Add or modify a component | `neobrutalism-components/src/components/` |
| Update the demo app | `src/` |
| Change global theme / colors | `neobrutalism-components/src/data/theme.json` |
| Tailwind styles | `tailwind.config.js` + `src/index.css` |
| Build configuration | `vite.config.ts` |
| Lint rules | `.oxlintrc.json` |

## CONVENTIONS
- React 19 with TypeScript, strict mode
- Tailwind CSS v4 via `@vitejs/plugin-react` + PostCSS
- Oxlint for linting (not ESLint). Config in `.oxlintrc.json`
- shadcn/ui-style: each component is a standalone `.tsx` file, imported by path, no monolithic barrel
- Lucide icons throughout
- `class-variance-authority` + `clsx` + `tailwind-merge` for component styling
- No build frameworks beyond Vite in the demo; the component library itself is a Next.js app

## ANTI-PATTERNS
- Don't add React frameworks to the demo (Next.js, Remix) — it's Vite-only
- Don't use ESLint — use Oxlint as configured
- Don't import heavy UI libraries (MUI, AntD) — neobrutalism is custom-styled
- Don't commit `node_modules/` or build output (`dist/`)

## COMMANDS
```bash
npm install                          # bootstrap dependencies
npm run dev                          # Vite dev server (demo app)
npm run build                        # production build
npm run preview                      # preview production build locally
npm run lint                         # oxlint check

# In neobrutalism-components/:
cd neobrutalism-components && npm run dev    # Next.js dev for component library + docs
cd neobrutalism-components && npm run build  # build the component library docs site
```
