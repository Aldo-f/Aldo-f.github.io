# About this site

This is the central documentation hub for Aldo Fieuw's projects. It aggregates
documentation from several repositories at build time using
[`mkdocs-multirepo-plugin`](https://github.com/backstage/mkdocs-monorepo-plugin)
— each section below is pulled live from its source repo when this site builds.

## How the docs are organized

| Section | Source | Notes |
|---------|--------|-------|
| **Clock** | [`Aldo-f/clock`](https://github.com/Aldo-f/clock) (`main`) | Special clocks — features & development docs |
| **Hermes WebUI** | [`Aldo-f/hermes-webui`](https://github.com/Aldo-f/hermes-webui) (`master`) | Desktop app docs: onboarding, architecture, contracts |
| **Thuis main** | [`Aldo-f/thuis`](https://github.com/Aldo-f/thuis) (`main`) | Current MkDocs-based documentation (EN + NL) |
| **Thuis v5** | `thuis` branch `v5/main` | Docusaurus-era docs: getting started, API, architecture |
| **Thuis v4** | `thuis` tag `v4.1.0` | Docusaurus-era docs: installation, usage, credentials |
| **Thuis v3** | `thuis` tag `v3.0.0` | Legacy single-file Python version (MkDocs, EN + NL) |

## Adding a new repository

1. Make sure the repo is **public** and keeps markdown under a top-level `docs/`
   directory (or point `docs_dir` at another path in `mkdocs.yml`).
2. Add a `nav_repos` entry to `mkdocs.yml` with the repo URL and branch.
3. Add a matching item under `nav:` pointing at the imported `index.md`.
4. Push to `main` — GitHub Actions rebuilds and deploys automatically.

## Deployment

The site deploys via `.github/workflows/deploy.yml` on every push to `main`.
Build locally with:

```bash
source venv/bin/activate
mkdocs build --strict
```
