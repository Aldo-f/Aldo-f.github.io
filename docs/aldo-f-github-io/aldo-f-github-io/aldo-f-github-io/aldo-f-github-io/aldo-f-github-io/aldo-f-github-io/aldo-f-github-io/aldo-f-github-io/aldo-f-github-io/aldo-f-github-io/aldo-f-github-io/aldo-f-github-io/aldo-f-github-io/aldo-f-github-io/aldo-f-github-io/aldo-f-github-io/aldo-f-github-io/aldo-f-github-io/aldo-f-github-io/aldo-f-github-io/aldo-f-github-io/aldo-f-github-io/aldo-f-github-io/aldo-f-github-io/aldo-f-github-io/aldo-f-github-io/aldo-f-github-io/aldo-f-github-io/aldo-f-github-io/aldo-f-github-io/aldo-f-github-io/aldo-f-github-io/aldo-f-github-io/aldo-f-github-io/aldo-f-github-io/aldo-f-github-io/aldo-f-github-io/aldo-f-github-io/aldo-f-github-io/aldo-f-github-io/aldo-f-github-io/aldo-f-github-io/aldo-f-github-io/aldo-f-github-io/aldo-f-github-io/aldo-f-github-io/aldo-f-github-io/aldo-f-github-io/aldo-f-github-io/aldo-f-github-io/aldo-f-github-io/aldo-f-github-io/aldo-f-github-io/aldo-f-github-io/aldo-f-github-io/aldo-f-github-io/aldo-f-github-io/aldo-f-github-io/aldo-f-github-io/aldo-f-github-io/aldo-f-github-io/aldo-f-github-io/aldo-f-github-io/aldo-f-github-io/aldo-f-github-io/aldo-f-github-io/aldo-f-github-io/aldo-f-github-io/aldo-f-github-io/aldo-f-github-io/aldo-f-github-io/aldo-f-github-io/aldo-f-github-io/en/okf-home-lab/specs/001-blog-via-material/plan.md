# Implementation Plan: Blog via Material Blog Plugin

**Branch**: `001-blog-via-material` | **Date**: 2026-08-23 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-blog-via-material/spec.md`

## Summary

Add a blog to the Aldo Fieuw documentation hub delivered through the official,
bundled **Material for MkDocs blog plugin** — zero new dependencies. Posts live
under `docs/blog/posts/*.md` with `date`+`title` front matter; the hub gains a
"Blog" nav entry pointing at `/blog/` with newest-first listing, excerpts,
prev/next links, category views, draft exclusion, and search integration. All
existing routes and the strict-build guarantee are regression-guarded by a
stdlib-only verification script executed RED→GREEN against the real runtime.

## Technical Context

**Language/Version**: Python 3.x (repo venv, pinned by `venv/`; CI uses 3.x)

**Primary Dependencies**: mkdocs 1.6.1, mkdocs-material 9.7.7 (bundles the
`blog` plugin since 9.2.0), mkdocs-multirepo-plugin 0.8.3,
mkdocs-section-index 0.3.12 — **no dependency changes required**

**Storage**: N/A (static site generator; content is markdown files in git)

**Testing**: stdlib-only verification script (`tests/verify_blog.py`) driving
real `mkdocs build --strict` runs + HTTP checks against a served build;
executed with the repo venv interpreter (plain `python3` fallback verified too)

**Target Platform**: GitHub Pages (https://aldo-f.github.io) via existing
GitHub Actions workflow on push to `main`

**Project Type**: static documentation site (single project)

**Performance Goals**: strict build completes without material runtime increase
vs current baseline (multirepo clones dominate); blog adds <2s locally

**Constraints**: zero-warning strict build (constitution Principle I);
explicit-nav completeness (Principle II); no manual deploy steps (Principle V)

**Scale/Scope**: ~3 seed posts (incl. 1 draft), 1 category, single author;
designed to stay healthy to dozens of posts via pagination defaults

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Build Purity | PASS | Verification script asserts `mkdocs build --strict` exit 0 + zero WARNING lines |
| II. Nav-Explicitness | PASS | Plan adds `- Blog: blog/index.md` to explicit `nav:`; generated category/archive/pagination pages attach under the Blog section automatically |
| III. Upstream-First | PASS | Uses the bundled Material `blog` plugin; `requirements.txt` unchanged; no custom code re-implementing blog features |
| IV. Generated-Output Hygiene | PASS | Only tracked-file changes: `mkdocs.yml`, `docs/blog/**`, `tests/verify_blog.py`, specs; `site/` remains gitignored |
| V. Verified Before Deployed | PASS | RED observed before implementation; GREEN includes served-site HTTP checks; deployment only via existing CI workflow |

No violations → Complexity Tracking table stays empty.

## Project Structure

### Documentation (this feature)

```text
specs/001-blog-via-material/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── site-contract.md # Phase 1 output (URL + front-matter + config contracts)
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
mkdocs.yml                      # MODIFIED: enable blog plugin + nav entry
docs/
└── blog/
    ├── index.md                # NEW: blog landing page (listing)
    └── posts/
        ├── welcome-to-the-blog.md      # NEW: seed post (published)
        ├── building-this-hub.md        # NEW: seed post (published)
        └── roadmap-notes-draft.md      # NEW: seed post (draft: true)
tests/
└── verify_blog.py              # NEW: stdlib verification harness (RED→GREEN)
.github/workflows/deploy.yml   # UNCHANGED (already installs requirements + builds)
requirements.txt               # UNCHANGED (plugin ships inside mkdocs-material)
```

**Structure Decision**: Single-project static site; no src/tests split beyond a
new `tests/` directory because the repo currently has none. The verification
script is intentionally dependency-free so it runs identically locally (repo
venv or system `python3`) and can later be adopted by CI.

## Complexity Tracking

> Empty — no constitution violations to justify.
