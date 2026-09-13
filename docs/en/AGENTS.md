# PROJECT KNOWLEDGE BASE – docs/en

**Generated:** 2026-09-13
**Commit:** {{short_sha}}
**Branch:** {{branch}}

## OVERVIEW
English-language documentation source for the Aldo-f docs hub.

## STRUCTURE
```
docs/en/
├── index.md                 # Home page
├── about.md                 # About page
├── projects.md              # Projects listing
├── abbreviations.md         # Abbreviation cheatsheet
├── 404.md                   # 404 page content
├── blog/
│   ├── index.md
│   ├── posts/               # Blog posts (YYYY-MM-DD-slug.md)
│   ├── category/            # Category index pages
│   └── archive/             # Blog archive
├── radio-community/         # Radio Community project docs
└── ...
```

## WHERE TO LOOK
| File | Purpose |
|------|---------|
| `index.md` | Site home page |
| `blog/posts/` | Blog content (sorted by date in filename) |
| `radio-community/` | Radio Community documentation |
| `abbreviations.md` | DRY, YAGNI, TDD, SDD cheatsheet |

## CONVENTIONS
- Blog posts: `YYYY-MM-DD-title-slug.md` naming.
- Front-matter required: `title:` (mandatory), `date:` (optional for posts).
- Use `draft: true` to preview without publishing.
- Mirrored posts in `docs/nl/` use same filename.

## ANTI‑PATTERNS
- Do not commit generated `site/` content.
- Do not use Markdown links to `site/` paths.
- Do not add posts without running `gen_category_index.py`.

## COMMANDS
```bash
# Preview English site
mkdocs serve -f mkdocs.en.yml

# Build English site
mkdocs build -f mkdocs.en.yml --strict
```
