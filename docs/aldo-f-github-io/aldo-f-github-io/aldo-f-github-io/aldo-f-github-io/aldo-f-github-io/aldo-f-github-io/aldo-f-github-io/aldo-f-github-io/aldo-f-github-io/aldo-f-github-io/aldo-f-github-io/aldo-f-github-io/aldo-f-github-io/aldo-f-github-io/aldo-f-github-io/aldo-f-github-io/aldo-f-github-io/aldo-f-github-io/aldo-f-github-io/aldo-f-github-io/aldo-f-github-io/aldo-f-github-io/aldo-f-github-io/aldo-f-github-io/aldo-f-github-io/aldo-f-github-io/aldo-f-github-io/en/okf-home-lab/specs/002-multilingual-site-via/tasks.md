# Tasks: Multilingual Site via Multi-Build Recipe

**Input**: spec.md / plan.md / research.md of this feature. Tests explicitly
requested (house policy): harness-first, RED before restructure.

## Phase 1: Setup

- [ ] T001 Write `mkdocs.base.yml` (shared theme/plugins/extensions/social;
      plugins WITHOUT multirepo) and `mkdocs.en.yml` (INHERIT; docs_dir
      `docs/en`; current nav with `en/` prefixes; alternate EN/NL; multirepo)
      and `mkdocs.nl.yml` (INHERIT; docs_dir `docs/nl`; site_url …/nl/;
      `theme.language: nl`; Dutch nav; no multirepo); delete root `mkdocs.yml`

## Phase 2: RED gate

- [ ] T002 Update `tests/verify_blog.py` to v2 (bilingual staging, merged-site
      assertions per plan Design Decisions §5) and capture failing output as
      pre-restructure evidence (old layout lacks `docs/en`, `docs/nl`,
      language configs)

## Phase 3: Structure & content

- [ ] T003 `git mv docs docs_en_tmp && mkdir docs/en && git mv docs_en_tmp/. docs/en/`
      (preserves history; leaves no `docs/` ambiguity)
- [ ] T004 [P] Create `docs/nl/index.md`, `docs/nl/about.md`,
      `docs/nl/blog/index.md`
- [ ] T005 [P] Create Dutch posts under `docs/nl/blog/posts/` (1-april,
      start-scrumweek, einde-scrum) from the recovered originals
- [ ] T006 Extend `scripts/gen_category_index.py` to iterate language roots
      (`docs/en`, `docs/nl`) and regenerate both overviews; verify EN output
      byte-equals the previously committed file; commit NL overview

## Phase 4: GREEN gate + CI

- [ ] T007 Harness GREEN: 100% checks ×2 interpreters (venv + python3);
      archive evidence in implementation-notes.md
- [ ] T008 `.github/workflows/deploy.yml`: replace single build with the two
      strict `-f` builds per plan R4

## Phase 5: Ship & verify live

- [ ] T009 Commit feature branch, merge to main, push; CI green
- [ ] T010 Live verification: legacy routes 200 unchanged; `/nl/`,
      `/nl/about/`, `/nl/blog/`, one NL post, `/nl/blog/category/` 200 with
      Dutch content; selector present; record evidence

## Dependencies

T001 → T002 (harness needs new config names) → T003..T006 → T007 → T008 →
T009 → T010. T004 ∥ T005 ∥ T006.
