# Tasks: Blog via Material Blog Plugin

**Input**: Design documents from `/specs/001-blog-via-material/`

**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅,
contracts/site-contract.md ✅, quickstart.md ✅

**Tests**: Explicitly requested by the user ("be sure to test it") and mandated
by constitution Principle V — verification tasks are first-class, executed
RED before implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1 read, US2 publish,
  US3 discover)

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create content directory `docs/blog/posts/` for posts
- [ ] T002 Create verification harness `tests/verify_blog.py` per
      contracts/site-contract.md C1 + research R4: stdlib-only; builds strict,
      asserts zero warnings, probe-post mechanics (FR-2/FR-3/SC-2), serves
      `site/` over loopback HTTP asserting routes `/`, `/about/`, `/projects/`,
      `/thuis/docs/`, `/blog/`, seed post route, category route with stable
      markers (SC-3), regression markers (SC-4), draft absence (SC-5),
      search-index token (FR-9). Script must FAIL when the feature is absent.

---

## Phase 2: User Story 1 — Visitor reads the blog (P1) 🎯 MVP

**Goal**: `/blog/` exists in nav, lists published posts newest-first with
excerpts; post pages render fully with prev/next links.

**Independent Test**: run `tests/verify_blog.py` after Phase 3 — all US1
checks pass against served build.

### Tests for User Story 1 ⚠️

> Written FIRST in T001/T002 harness; observed RED before any config change.

- [ ] T003 [US1] RED gate: run `./venv/bin/python tests/verify_blog.py`;
      capture failing output (blog routes 404 / no listing) as pre-change
      evidence

### Implementation for User Story 1

- [ ] T004 [US1] Enable blog plugin block in `mkdocs.yml` per contract C3
      (`blog_dir: blog`, `post_date_format: yyyy-MM-dd`, `archive: false`)
- [ ] T005 [P] [US1] Add `- Blog: blog/index.md` to explicit `nav:` in
      `mkdocs.yml` between About and Projects
- [ ] T006 [P] [US1] Write seed post `docs/blog/posts/welcome-to-the-blog.md`
      per data-model (date 2026-08-23, category General, body token
      `xylophone-framework`)
- [ ] T007 [P] [US1] Write seed post `docs/blog/posts/building-this-hub.md`
      (date 2026-08-20, category Meta, older than T006 post to prove ordering;
      body token `quokka-buildkit`)
- [ ] T008 [US1] GREEN gate: re-run verifier; blog listing + post page +
      prev/next checks pass; capture output as evidence

**Checkpoint**: A visitor can read the blog end-to-end; MVP achieved.

---

## Phase 3: User Story 2 — Author publishes a post (P1)

**Goal**: Publishing = adding one markdown file; drafts excluded from
production; categories work.

**Independent Test**: probe-post sub-check inside the harness (adds a temp
post, rebuilds, asserts count+1 and removal restores baseline).

### Implementation for User Story 2

- [ ] T009 [US2] Write draft seed post
      `docs/blog/posts/roadmap-notes-draft.md` (`draft: true`, category
      General, title "Roadmap notes"); verify harness draft-absence check now
      has a real target
- [ ] T010 [US2] GREEN gate: verifier confirms draft absent from production
      build while both published posts remain listed (FR-6, SC-5) and
      probe-publish mechanics pass (FR-3, SC-2)

**Checkpoint**: Author workflow proven mechanically by the probe test.

---

## Phase 4: User Story 3 — Visitor discovers the blog (P2)

**Goal**: Blog reachable from site chrome everywhere; search indexes posts.

**Independent Test**: nav-link assertion on multiple served pages + search
index token check in harness output.

### Implementation for User Story 3

- [ ] T011 [US3] Verify nav `Blog` link present in served HTML of `/`,
      `/about/`, and a post page (harness assertions already cover these —
      confirm PASS lines)
- [ ] T012 [US3] Confirm search index contains `xylophone-framework` from the
      published post body (FR-9; harness check)

**Checkpoint**: All three user stories independently verified.

---

## Phase 5: Polish & Cross-Cutting

- [ ] T013 Update repo `AGENTS.md` conventions section with one line: blog
      posts live in `docs/blog/posts/` and publishing = adding one file
- [ ] T014 Run full quickstart.md validation sequence one final time from a
      clean build; archive evidence (exit codes + key PASS lines) into
      specs/001-blog-via-material/implementation-notes.md
- [ ] T015 Commit feature branch content and merge to `main`; push; confirm
      GitHub Actions deploy run is green and live site serves `/blog/` (SC
      final acceptance at https://aldo-f.github.io/blog/)

---

## Dependencies & Execution Order

- T001 → T002 (posts dir must exist before harness fixtures reference it)
- T002 → T003 (RED needs the harness)
- T003 → T004–T007 (implementation only after RED evidence captured)
- T008 depends on T004–T007 (GREEN of US1)
- T009–T010 depend on T008 (draft target added onto working blog)
- T011–T012 depend on T010 (discovery checks run against full feature)
- T013–T015 last (polish, evidence, ship)

## Parallel Opportunities

- T006 ∥ T007 ∥ T005 (independent files once plugin block lands)
- Verification reruns are single-threaded by design (shared `site/` output)

## Implementation Strategy

- MVP = through T008 (US1 complete, readable blog live in local build)
- Each subsequent phase adds an independently verifiable increment
- Ship only after T015's live-site confirmation
