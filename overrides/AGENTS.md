# PROJECT KNOWLEDGE BASE – overrides

**Generated:** 2026-09-13
**Commit:** {{short_sha}}
**Branch:** {{branch}}

## OVERVIEW
MkDocs Material template overrides for custom HTML rendering.

## STRUCTURE
```
overrides/
├── 404.html                   # 404 dungeon game page
├── 404_dungeon.md             # 404 dungeon content (JSON data)
├── main.html                  # Base template layout
├── partials/
│   ├── blog_post.html         # Blog post rendering
│   ├── comments.html          # Disqus/comments integration
│   ├── copyright.html         # Footer copyright
│   └── source.html            # Source file link
└── ...
```

## WHERE TO LOOK
| File | Purpose |
|------|---------|
| `404.html` | 404 error page with interactive dungeon game |
| `main.html` | Root template extending Material base |
| `partials/blog_post.html` | Custom blog post card layout |
| `partials/source.html` | Edit this page link |

## CONVENTIONS
- Templates use Jinja2 syntax.
- Override Material templates by matching the same file structure.
- JavaScript/CSS in templates is inline — no external assets unless needed.
- 404 dungeon data lives in `data/404_dungeon.json`.

## ANTI‑PATTERNS
- Do not edit generated `site/` output — only modify source templates.
- Do not add heavy JavaScript libraries — keep it lightweight.
- Do not duplicate content from parent templates.

## COMMANDS
```bash
# Build site with overrides
mkdocs build -f mkdocs.en.yml --strict

# Preview locally
mkdocs serve -f mkdocs.en.yml
```
