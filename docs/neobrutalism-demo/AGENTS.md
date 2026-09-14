# AGENTS.md — Neobrutalism Demo

React + TypeScript + Vite project demonstrating neobrutalist UI components. Dual nature: demo app + reusable component library (shadcn/ui-style). ~470 source files.

## STRUCTURE
```
.
├── src/                  # Demo app
│   ├── components/       # Demo-specific components
│   └── pages/            # Route pages
├── neobrutalism-components/  # Reusable component library
│   └── src/              # Individual component sources
├── public/               # Static assets
├── tailwind.config.js    # Tailwind CSS v4 config
├── vite.config.ts        # Vite build config
└── package.json          # Workspaces: demo + components
```

## WHERE TO LOOK
| Task | Location |
|------|----------|
| Component library | neobrutalism-components/src/ — each component is a file |
| Demo app | src/ — shows components in context |
| Styling | tailwind.config.js + any global CSS |
| Build config | vite.config.ts |

## CONVENTIONS
- React 19 with TypeScript, strict mode
- Tailwind CSS v4 via Vite plugin
- Oxlint for linting (not ESLint) — config in .oxlintrc.json
- shadcn/ui-style: each component is a standalone file, imported by path
- Vite HMR for dev; `npm run build` produces static output
- Native JS/TS — no build frameworks beyond Vite

## ANTI-PATTERNS
- Don't add React framework abstractions (Next.js, Remix) — this is Vite-only
- Don't use ESLint — use Oxlint as configured
- Don't add heavy UI libraries (MUI, AntD) — neobrutalism is custom-styled
- Don't commit node_modules or dist/

## COMMANDS
```bash
npm install                              # bootstrap
npm run dev                              # Vite dev server + HMR
npm run build                            # production build
npm run lint                             # oxlint check
```
