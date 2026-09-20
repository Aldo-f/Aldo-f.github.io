# PROJECT KNOWLEDGE BASE – docs/nl

**Generated:** 2026-09-20

## OVERVIEW
Dutch-language documentation source for the Aldo-f docs hub. Mirrors English structure.

## STRUCTURE
```
docs/nl/
├── index.md                 # NL home page
├── about.md                 # NL about page
├── projects.md              # NL projects listing
├── 404.md                   # NL 404 page
├── blog/
│   ├── index.md
│   └── posts/               # NL blog posts (mirrored from en)
└── ...
```

## WHERE TO LOOK
| File | Purpose |
|------|---------|
| `index.md` | NL site home page |
| `blog/posts/` | Dutch blog posts |

## CONVENTIONS
- Mirrored posts share filename with English version.
- Auto-translation via `mkdocs-autotranslate` plugin.
- Fill gaps manually after translation.
- Serve at `/nl/` path.

## ANTI‑PATTERNS
- Do not manually edit translated content — use autotranslate tool.
- Do not remove `draft: true` from untranslated pages.

## COMMANDS
```bash
# Preview Dutch site
mkdocs serve -f mkdocs.nl.yml

# Build Dutch site
mkdocs build -f mkdocs.nl.yml --strict

# Generate translations (dry-run)
autotranslate --docs-dir docs --paths . --exclude 'blog/category/*'
```
