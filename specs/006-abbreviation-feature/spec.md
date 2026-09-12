# Feature Specification: Abbreviation Cheatsheet

**Feature Branch**: `006-abbreviation-feature`
**Created**: 2026-09-12
**Status**: Ready for Review
**Input**: Add a searchable, filterable, alphabetically‑sorted abbreviation cheatsheet to the Aldo‑F documentation hub (Spec Kit SDD flow).

## User Scenarios & Testing

### User Story 1 — Visitor reads abbreviations (Priority: P1)
A visitor to https://aldo-f.github.io wants to quickly look up a technical abbreviation. They click **Abbreviations** in the top navigation and see a list of cards, each showing the abbreviation code. The list is alphabetically ordered. Clicking a card expands it to reveal one or more answer sections with a title, category tags, and definition. The visitor can type into the search box to find abbreviations by code, title, category, or definition.

**Why this priority**: The core purpose of the feature is to provide readable abbreviation information; if the UI cannot be used, the feature fails.

### User Story 2 — Contributor adds a new abbreviation (Priority: P1)
The site maintainer clicks the **Add Abbreviation** button on the page, which opens a pre‑filled GitHub new‑file form (`TEMPLATE.md`). They fill in the required front‑matter and at least one answer block, commit the changes, and open a PR. The CI runs a strict MkDocs build; on success the new abbreviation appears automatically on the live site.

**Why this priority**: The feature must be easy to extend without manual navigation edits.

### User Story 3 — Visitor filters by category (Priority: P2)
From the abbreviation page the visitor selects a category (e.g., *software‑engineering*) in the dropdown. All cards that do not contain at least one answer with that category are hidden. The UI updates instantly.

**Why this priority**: Filtering improves discoverability for large abbreviation sets.

#### Edge Cases
- A file missing the required `abbreviation:` front‑matter aborts the build with a clear error.
- Duplicate abbreviation codes abort the build.
- An answer block missing **Category** or **Definition** aborts the build.
- Draft flag is not used for abbreviations (all entries are public).
- If the abbreviation folder is empty the page renders an empty‑state message.

## Requirements

### Functional Requirements
- **FR‑1**: Abbreviation data lives as individual markdown files under `abbreviations/`.
- **FR‑2**: Each file must contain a YAML front‑matter with a unique `abbreviation:` key.
- **FR‑3**: Files may contain one or more answer sections, each starting with a level‑2 heading and accompanied by `**Category:**` and `**Definition:**` lines.
- **FR‑4**: The MkDocs hook parses the files, validates the contract, writes `site/assets/data/abbreviations.json`, and injects the same JSON into the page via `window.ABBREVIATIONS`.
- **FR‑5**: The UI renders cards alphabetically by abbreviation and answer titles.
- **FR‑6**: A category dropdown filters whole cards based on answer tags.
- **FR‑7**: A search box performs case‑insensitive substring matching across abbreviation code, answer titles, categories, and definitions.
- **FR‑8**: The page includes a **Add Abbreviation** button linking to `https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md`.
- **FR‑9**: The feature must pass a strict MkDocs build (`--strict`) for both English and Dutch configs.

### Non‑Goals (deferred)
- Internationalization of abbreviation content (Dutch version).
- Bulk import via CSV or other formats.
- REST endpoint exposing the JSON for external tools.
- Pagination for very large abbreviation sets.

## Constraints & Assumptions
- The repository already contains the `hooks/abbreviations.py` implementation.
- The documentation toolchain (MkDocs + Material) is installed in the project's virtualenv.
- Deployment target is GitHub Pages via the existing CI workflow.
- All existing site routes must remain unchanged (regression guard).
- Category strings are case‑insensitive and stored lower‑cased.

## Success Criteria
- **SC‑1**: Visiting `/abbreviations/` returns HTTP 200 and displays the UI with at least the seed entries (DRY, YAGNI, TDD, SDD).
- **SC‑2**: Adding a new abbreviation file and merging the PR increases the card count by exactly one on the live site.
- **SC‑3**: The search box finds a newly added abbreviation by any term in its title, category, or definition.
- **SC‑4**: Selecting a category hides all cards that lack that tag.
- **SC‑5**: A strict MkDocs build fails with a clear error message if any file violates the spec.
- **SC‑6**: All previously existing site pages continue to serve identical content after the change.

## Review & Acceptance Checklist
- [ ] FR‑1..FR‑9 are testable, unambiguous, and covered by automated CI.
- [ ] Edge cases are exercised in the test suite (duplicate, missing front‑matter, missing fields).
- [ ] Success criteria measurable via manual verification and CI logs.
- [ ] Scope bounded; non‑goals explicitly listed.
- [ ] Documentation updates (navigation link, spec page) are included in the same PR.

---
*Document version: 1.0 (2026‑09‑12)*