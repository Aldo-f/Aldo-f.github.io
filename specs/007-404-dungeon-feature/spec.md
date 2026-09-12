# Feature Specification: 404 Dungeon Game Feature

**Feature Branch**: `007-404-dungeon-feature`
**Created**: 2026-09-12
**Status**: Ready for Review
**Input**: Add an interactive, multilingual "404 Dungeon" experience to the Aldo‑F documentation hub, delivered as a Material‑Design 3 themed page (Spec Kit SDD flow).

## User Scenarios & Testing

### User Story 1 — Visitor lands on a missing page (P1)
A visitor navigates to an unknown URL such as `https://aldo-f.github.io/nl/404-pagina/` or `https://aldo-f.github.io/404-pagina/`. Instead of a bland 404 page they see a small, styled adventure game (the "404 Dungeon"). The page displays a title, a brief narrative, HP/Confusion stats, and a set of choice buttons that drive a 5‑node state machine.

**Why this priority**: The core purpose of the feature is to replace the default 404 with an engaging experience. If the visitor never sees the game, the feature fails.

### User Story 2 — Visitor interacts with the game (P1)
From the start node the visitor can:
- Take a torch → the torch node.
- Walk forward → the corridor node.
- Choose actions that increase or decrease the confusion stat.
- Finally reach an "escape" node which shows a "Back to Homepage" button.
All interactions happen client‑side without page reloads.

### User Story 3 — Dutch and English visitors see the same game (P2)
The game UI, layout, and state‑machine logic are identical for both languages. Only the narrative text is translated (EN/NL). The language is selected automatically via Material’s `autotranslate` plugin (`page.meta.lang`).

### Edge Cases
- If the JSON data file is missing the page shows a clear error message and falls back to a plain 404.
- The HP/Confusion stats never go below 0 or above the maximum (3).
- When a node has no choices the "Back to Homepage" button appears automatically.
- The page is never linked from the navigation; it is reachable only via a 404 error (the "lost realm").

## Requirements

### Functional Requirements
- **FR‑1**: The site generates a static HTML page at `/404.html` (EN) and `/nl/404/index.html` (NL) that contains the fully rendered dungeon (no Jinja tags remain).
- **FR‑2**: The page extends `base.html` to inherit the header, footer, theme variables, and navigation.
- **FR‑3**: All static assets (CSS, JS, images) are referenced with absolute URLs (`/assets/...`). The `hooks/slugmap.py` rewrites any language‑prefixed paths during build.
- **FR‑4**: Game data lives in `data/404_dungeon.json` with bilingual `text` fields. The JSON is copied to `site/assets/data/` for both builds.
- **FR‑5**: The page loads the JSON via `fetch('assets/data/404_dungeon.json')` and renders the current node, HP/Confusion chips, and choice buttons.
- **FR‑6**: UI components use Material Design 3 tokens (`--md-sys-color-primary`, `--md-sys-color-surface`, etc.) and follow the design guidelines.
- **FR‑7**: The page respects `prefers-reduced-motion` – animations are disabled for users who request it.
- **FR‑8**: The 404 page is **not** present in any `nav:` section of the MkDocs configuration.
- **FR‑9**: Playwright E2E test (`tests/e2e/test_404_dungeon_multilingual.py`) verifies that:
  - The page loads at both language URLs.
  - `#dungeon-scene` is visible.
  - Absolute asset URLs are present.
  - The title contains "The 404 Dungeon".
  - At least one state transition works (click a choice and see new text).
- **FR‑10**: The site builds strictly (`mkdocs build --strict`) with zero warnings for both EN and NL configs.

### Non‑Goals (deferred)
- Persisting player progress across sessions.
- Adding sound effects or animation beyond the minimal fade/scale.
- Multi‑language support beyond EN/NL.
- Server‑side rendering of the game (the game is purely client‑side).
- Exposing the JSON via an API endpoint.

## Constraints & Assumptions
- All Python dependencies are installed with **`uv pip`** (no regular `pip`).
- The documentation toolchain already includes MkDocs, Material, `autotranslate`, and the custom `hooks/slugmap.py`.
- Deployment target is GitHub Pages (`https://aldo-f.github.io`).
- The game must not impact existing site routes or performance; the additional JSON (~1 KB) is negligible.
- The 404 page will be served as a static file; no backend is involved.
- The site already serves assets from `/assets/`; the hook guarantees absolute paths.

## Success Criteria
- **SC‑1**: A visitor accessing a missing URL receives HTTP 200 with the rendered dungeon (EN and NL).
- **SC‑2**: Adding a new node or translation to `data/404_dungeon.json` increases the game flow without rebuilding other parts of the site.
- **SC‑3**: The Playwright test passes on a local server (`python -m http.server 8000 --directory site`).
- **SC‑4**: All strict builds (`mkdocs build -f mkdocs.en.yml` and `-f mkdocs.nl.yml`) exit with code 0 and produce no warnings.
- **SC‑5**: No existing navigation entry points to the 404 page; `grep -R "404" mkdocs.*.yml` shows only the promotion hook.
- **SC‑6**: Asset URLs in the generated HTML all start with `/assets/` (verified by `tests/test_asset_paths.py`).
- **SC‑7**: The HP/Confusion chips never exceed the range 0‑3 during any player interaction.

## Review & Acceptance Checklist
- **Gate G‑**
  - [ ] FR‑1 … FR‑10 are testable and unambiguous.
  - [ ] Success criteria are measurable and technology‑agnostic where possible.
  - [ ] Edge cases (missing JSON, out‑of‑range stats) are covered.
  - [ ] Scope is bounded; non‑goals are explicit.
  - [ ] Documentation (this spec) lives under `specs/007-404-dungeon-feature/`.
  - [ ] CI pipeline runs the Playwright test and the strict MkDocs builds.

---

*Document version: 1.0 (2026‑09‑12)*