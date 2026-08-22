# AGENTS.md — 06-apps-aldo-f-github-io

## Overview
Personal documentation hub (MkDocs + Material theme) deployed to https://aldo-f.github.io via GitHub Pages.
Aggregates documentation from other repos at build time using `mkdocs-multirepo-plugin`.

## Structure
```
06-apps-aldo-f-github-io/
├── docs/                     # This site's own content (home page)
├── download/                 # Static downloads served via docs (CV, etc.)
├── .github/workflows/deploy.yml  # CI: build + deploy on push to main
├── mkdocs.yml                # Site config: theme, plugins, nav, multirepo imports
├── requirements.txt          # Python deps: mkdocs, mkdocs-material, mkdocs-multirepo-plugin
└── AGENTS.md                 # This file
```

## HOW THE MULTIREPO DOCS WORK
- `mkdocs.yml` → `plugins.multirepo.nav_repos` lists remote repos/branches.
- At `mkdocs build` time the plugin clones each repo and copies its `docs/` folder in.
- Nav entries reference imported paths, e.g. `thuis/docs/index.md`.
- To add a repo's docs: add a `nav_repos` entry (name + `import_url?branch=`) AND a matching nav item.

## WHERE TO LOOK
| File | Purpose |
|------|---------|
| `mkdocs.yml` | Site configuration (site_name, theme, plugins, nav, multirepo imports) |
| `docs/` | Local markdown content (home page lives here as `index.md`) |
| `.github/workflows/deploy.yml` | Deployment pipeline (trigger branch must match working branch — currently `main`) |
| `requirements.txt` | Python dependencies for build |

## CONVENTIONS
- MkDocs markdown with Material extensions; TOC permalinks enabled in `mkdocs.yml`
- Remote repos must keep their documentation under a top-level `docs/` folder to be importable
- Versioned docs = extra `nav_repos` entry pinned to a tag/branch (see `thuis-v3.0.0` example)
- Deploy only happens on pushes to `main` (GitHub Actions, `build_type: workflow`)
- Build locally with `mkdocs serve`; output goes to `site/` (not committed)

## ANTI-PATTERNS
- ❌ Editing files in `site/` directory directly — regenerated on each build
- ❌ Committing `site/`, `venv/`, or imported repo caches to git
- ❌ Adding multirepo entries without a matching `nav:` item — they won't appear
- ❌ Renaming/moving this repo's default branch without updating `deploy.yml` trigger
- ❌ Using Jekyll/Hugo concepts here (legacy leftovers have been removed) — this is MkDocs
