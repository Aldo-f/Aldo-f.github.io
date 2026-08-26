# Contracts: Blog via Material Blog Plugin

Three contracts bind the feature: the URL space, the authoring format, and the
build configuration.

## C1 — Site URL contract (public)

| Route | Status | Must contain (stable markers) |
|-------|--------|-------------------------------|
| `/` | 200 | `Aldo Fieuw Documentation` (unchanged) |
| `/about/` | 200 | existing about content marker |
| `/projects/` | 200 | existing projects content marker |
| `/thuis/docs/` (imported index) | 200 | existing Thuis overview marker |
| `/blog/` | 200 | newest post title + older post title (in that DOM order) + excerpt text |
| `/blog/2026/08/23/welcome-to-the-blog/` | 200 | post `<h1>` + distinctive body token `xylophone-framework` + prev-link to the older post |
| `/blog/category/general/` | 200 | category label + published General posts' titles; NOT the draft title |

Draft route `/blog/2026/08/23/roadmap-notes-draft/` MUST NOT exist in
production output (404 / absent file).

Nav on every page includes a `Blog` entry linking to `/blog/`.

## C2 — Authoring contract (publishers)

```markdown
---
title: <post title>
date: YYYY-MM-DD          # required; strict build fails otherwise
categories:
  - General               # optional, repeatable
draft: true               # optional; excluded from production builds
---

First paragraph becomes the listing excerpt.
```

Publishing = adding exactly this one file. Nothing else may need editing
(FR-3).

## C3 — Build configuration contract

`mkdocs.yml` gains:

```yaml
plugins:
  - blog:
      blog_dir: blog
      post_date_format: yyyy-MM-dd
      archive: false
nav:
  ...
  - Blog: blog/index.md   # position: after About, before Projects
```

- `requirements.txt`: unchanged (plugin bundled in mkdocs-material).
- `.github/workflows/deploy.yml`: unchanged (`pip install -r requirements.txt`
  already provides the plugin; `mkdocs build` produces `site/`).
- Strict-build gate: `mkdocs build --strict` exits 0 with zero warnings.
