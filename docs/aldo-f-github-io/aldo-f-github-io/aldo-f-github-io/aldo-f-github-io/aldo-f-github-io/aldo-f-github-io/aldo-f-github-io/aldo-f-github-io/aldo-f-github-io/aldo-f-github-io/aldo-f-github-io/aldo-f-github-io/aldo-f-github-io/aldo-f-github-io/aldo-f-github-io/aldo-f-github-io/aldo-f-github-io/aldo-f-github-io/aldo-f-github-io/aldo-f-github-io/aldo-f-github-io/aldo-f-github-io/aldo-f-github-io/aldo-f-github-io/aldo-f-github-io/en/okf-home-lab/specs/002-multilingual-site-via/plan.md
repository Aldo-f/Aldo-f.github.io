# Implementation Plan: Multilingual Site via Multi-Build Recipe

**Branch**: `002-multilingual-site-via` | **Date**: 2026-08-23 | **Spec**: [spec.md](spec.md)

## Summary

Split the hub into two per-language builds using Material's official INHERIT
recipe (validated end-to-end in the 2026-08-23 spike): shared
`mkdocs.base.yml` (theme, blog plugin, extensions) + `mkdocs.en.yml` (current
content, builds to site root, keeps multirepo imports) + `mkdocs.nl.yml`
(`docs/nl/`, Dutch UI, builds into `site/nl/`, no multirepo). Deploy pipeline
runs both strict builds; language selector wired via `extra.alternate`.

## Technical Context

**Language/Version**: Python 3.x repo venv; mkdocs 1.6.1 + material 9.7.7
(INHERIT + `extra.alternate` + blog plugin bundled — no dependency changes)

**Testing**: extended stdlib harness `tests/verify_blog.py` (bilingual staged
strict builds + served-route assertions on merged `site/`)

**Target Platform**: GitHub Pages, single artifact: EN at `/`, NL at `/nl/`

**Research**: [research.md](research.md) — spike head-to-head
(static-i18n INVALIDATED: silently drops all blog-plugin posts, upstream #4863
"not fixable"; multi-build VALIDATED: both builds green, selector + hreflang +
`lang="nl"` confirmed)

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Build Purity | PASS | FR-6/SC-1: both builds strict zero-warning |
| II. Nav-Explicitness | PASS | Each language build has its own explicit `nav:` |
| III. Upstream-First | PASS | Uses Material's official multi-build recipe (#2346); no new deps; rejected third-party i18n plugin |
| IV. Output Hygiene | PASS | Only tracked sources added; `site/` stays ignored |
| V. Verified Before Deployed | PASS | RED captured before restructure; GREEN = harness 100% ×2 interpreters; CI + live curl checks |

## Design Decisions

1. **Config split**: `mkdocs.base.yml` (shared) ← INHERIT ←
   `mkdocs.en.yml` (docs_dir `docs/en`, site_url `/`, alternate, current nav
   with `en/` prefixes, multirepo) and `mkdocs.nl.yml` (docs_dir `docs/nl`,
   site_url `/nl/`, `theme.language: nl`, Dutch nav, plugins WITHOUT multirepo
   — avoids a second clone round in CI; project docs stay EN-side).
   Root `mkdocs.yml` disappears; every build names its config (`-f`).
2. **Content ownership (least surprise)**: EN build keeps ALL current posts
   (incl. the Dutch 2019 ones → existing URLs like `/blog/2019/04/17/einde-scrum/`
   stay valid, current category table unchanged). NL build owns Dutch copies
   of the three 2019 posts + its own home/about/blog-index.
3. **Generator v2**: `scripts/gen_category_index.py` iterates existing language
   roots (`docs/en`, `docs/nl`) and writes each `<root>/blog/category/index.md`.
   Byte-stable per language; EN output must equal the currently committed file.
4. **CI**: two steps — `mkdocs build --strict -f mkdocs.en.yml -d site` then
   `... -f mkdocs.nl.yml -d site/nl`; upload `site/`.
5. **Harness v2**: stages each language separately (copies the three configs +
   that language's `docs/`), probes publishing on EN, serves merged `site/`
   and asserts EN regressions + NL routes + selector/hreflang/lang attributes
   + NL category table {General:1, Scrum:2, VDAB:2}, draft absence in both.

## Project Structure

```text
mkdocs.base.yml            # NEW shared config (theme/plugins/extensions/social)
mkdocs.en.yml              # NEW EN config (INHERIT base)  [replaces mkdocs.yml]
mkdocs.nl.yml              # NEW NL config (INHERIT base)
docs/en/…                  # MOVED from docs/ (unchanged content)
docs/nl/
├── index.md               # NEW Dutch home
├── about.md               # NEW "Over"
└── blog/
    ├── index.md           # NEW
    ├── category/index.md  # GENERATED for nl
    └── posts/{1-april,start-scrumweek,einde-scrum}.md   # Dutch copies
scripts/gen_category_index.py   # v2: per-language generation
tests/verify_blog.py            # v2: bilingual E2E
.github/workflows/deploy.yml    # two-stage build
```

## Complexity Tracking

Empty — no constitution violations.
