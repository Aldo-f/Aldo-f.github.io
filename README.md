# aldo-f.github.io

Personal documentation hub for Aldo Fieuw's projects and home-lab services.

[![GitHub Pages Deploy](https://github.com/Aldo-f/Aldo-f.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/Aldo-f/Aldo-f.github.io/actions/workflows/deploy.yml)
[![GitHub Pages Status](https://img.shields.io/github/actions/workflow/status/Aldo-f/Aldo-f.github.io/deploy.yml?branch=main&label=pages%20deploy)](https://aldo-f.github.io)
[![MkDocs Material](https://img.shields.io/badge/mkdocs-material-9.5.31-blue)](https://squidfunk.github.io/mkdocs-material/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Last Updated](https://img.shields.io/github/last-commit/Aldo-f/Aldo-f.github.io/main)](https://github.com/Aldo-f/Aldo-f.github.io/commits/main)

## What's here

Documentation collected from multiple repositories and served via [GitHub Pages](https://aldo-f.github.io):

| Project | Description |
|---------|-------------|
| **[Thuis](https://aldo-f.github.io/thuis-v5/website/docs/intro/)** | VRT MAX video downloader (v3–v5) |
| **[Clock](https://aldo-f.github.io/clock/docs/)** | React clock studio |
| **[Blanky](https://aldo-f.github.io/blanky/docs/)** | External link opener library |
| **[Radio Community](https://aldo-f.github.io/radio-community/)** | Democratic internet radio |
| **[Home-lab](https://aldo-f.github.io/home-lab-docs/)** | Home infrastructure docs |

## Structure

```
06-apps-aldo-f-github-io/
├── docs/en/          # English documentation
├── docs/nl/          # Dutch documentation
├── .github/workflows/
│   ├── deploy.yml    # GitHub Pages deployment
│   └── rag-tests.yml # RAG tests
├── hooks/            # MkDocs hooks (mermaid, dynamic-repo, slugmap)
├── mkdocs.base.yml   # Shared configuration
├── mkdocs.en.yml     # English build config
└── mkdocs.nl.yml     # Dutch build config
```

## Local development

```bash
# Install dependencies
pip install -r requirements.txt

# Start dev server (English)
mkdocs serve -f mkdocs.en.yml

# Start dev server (Dutch)
mkdocs serve -f mkdocs.nl.yml

# Build both sites
mkdocs build --strict -f mkdocs.en.yml
mkdocs build --strict -f mkdocs.nl.yml
```

## Deployment

Pushes to `main` trigger automatic GitHub Pages deployment via the [deploy.yml](.github/workflows/deploy.yml) workflow.

- English site → `https://aldo-f.github.io/`
- Dutch site → `https://aldo-f.github.io/nl/`
