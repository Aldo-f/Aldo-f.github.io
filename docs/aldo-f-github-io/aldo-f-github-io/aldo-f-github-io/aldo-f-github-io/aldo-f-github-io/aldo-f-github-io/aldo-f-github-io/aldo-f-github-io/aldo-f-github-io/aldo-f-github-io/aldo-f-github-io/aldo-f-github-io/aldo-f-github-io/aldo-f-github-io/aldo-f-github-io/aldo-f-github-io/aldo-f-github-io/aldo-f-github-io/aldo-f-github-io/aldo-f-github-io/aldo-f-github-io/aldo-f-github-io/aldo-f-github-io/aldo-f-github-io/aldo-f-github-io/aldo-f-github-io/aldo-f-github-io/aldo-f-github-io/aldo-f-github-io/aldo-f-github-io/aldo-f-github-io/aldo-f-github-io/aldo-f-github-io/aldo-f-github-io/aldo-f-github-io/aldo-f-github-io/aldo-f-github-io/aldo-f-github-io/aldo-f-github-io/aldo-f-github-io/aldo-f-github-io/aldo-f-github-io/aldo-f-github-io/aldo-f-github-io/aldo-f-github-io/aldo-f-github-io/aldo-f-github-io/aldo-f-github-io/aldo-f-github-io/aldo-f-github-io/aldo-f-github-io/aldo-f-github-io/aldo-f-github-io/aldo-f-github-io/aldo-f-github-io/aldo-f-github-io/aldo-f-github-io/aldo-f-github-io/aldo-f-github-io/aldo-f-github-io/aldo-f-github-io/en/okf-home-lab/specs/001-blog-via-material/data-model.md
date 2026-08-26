# Data Model: Blog via Material Blog Plugin

## Entities

### Post

A markdown file under `docs/blog/posts/<slug>.md`.

| Field | Source | Required | Rules |
|-------|--------|----------|-------|
| `title` | front matter | yes | string; becomes `<h1>` and listing entry text |
| `date` | front matter | yes | ISO date `YYYY-MM-DD`; drives ordering + display |
| `categories` | front matter | no | list of strings; each creates/joins a category view |
| `draft` | front matter | no | boolean, default false; true ⇒ excluded from production build output entirely |
| slug | filename | yes | `[a-z0-9-]+`; becomes URL segment `/blog/<year>/<month>/<day>/<slug>/` |
| body | markdown below front matter | yes | first paragraph doubles as excerpt |

Validation rules (enforced by strict build):
- missing/invalid `date` → build error (fail closed, per spec edge case)
- duplicate slug+date combination → build error

State transitions: none (static). Draft ⇄ published is a front-matter edit +
rebuild.

### Category view

Generated page at `/blog/category/<name>/` aggregating posts sharing a
category value (case-normalized, slugified). Exists only when ≥1 published
post declares it.

### Listing (blog index)

`/blog/` renders newest-first published posts (title, formatted date, excerpt)
paginated by the plugin default. Anchored in nav via `blog/index.md`.

## Relationships

- Post 0..* → 0..* Category (via `categories` front matter)
- Listing aggregates all published Posts ordered by `date` desc
- Search index includes body of every published Post; drafts excluded
