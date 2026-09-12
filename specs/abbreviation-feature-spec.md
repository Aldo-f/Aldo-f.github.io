---
title: Abbreviation Feature Specification
---

# Specification – Abbreviation Cheatsheet Feature

## 1. Goal
Provide a searchable, filterable, alphabetically‑sorted cheat‑sheet of technical abbreviations (e.g. **DRY**, **YAGNI**, **TDD**, **SDD**) that lives in the Aldo‑F documentation site (`https://aldo-f.github.io`). The feature must be **Spec‑Driven**: the documentation spec is the single source of truth, and the implementation is derived from it.

## 2. Scope
- Data stored as one markdown file per abbreviation under `abbreviations/`.
- MkDocs hook parses files, validates structure, generates JSON, and injects it into the page.
- UI displays abbreviation cards with answer sections, category filter, and a text search.
- Contribution flow uses a pre‑filled GitHub "Add Abbreviation" link.
- CI runs a strict MkDocs build for English (and Dutch) on every push.

## 3. Data Model (Markdown file format)
```
---
abbreviation: <CODE>
---

## <Answer Title>

**Category:** <comma‑separated list of tags>
**Definition:** <free‑form description>
```
- The front‑matter `abbreviation:` is mandatory and must be unique across the folder.
- One file may contain multiple answer sections (repeat `## <Title>` blocks). Each section must contain **both** `**Category:**` and `**Definition:**` lines.
- Files must be UTF‑8 and placed directly under `abbreviations/` (no sub‑folders).
- Example (`DRY.md`):
  ```markdown
  ---
abbreviation: DRY
---

## Don't Repeat Yourself

**Category:** software‑engineering, best‑practices
**Definition:** A principle encouraging reduction of duplicate knowledge or logic.
  ```

## 4. Hook – `hooks/abbreviations.py`
- **Entry point**: module‑level `on_page_markdown` (MkDocs calls it for each page) and `on_post_build` for final JSON write.
- **Parsing**: iterate over `abbreviations/*.md`, using a regular expression to extract front‑matter and answer blocks.
- **Validation**:
  - Abort if `abbreviation:` missing or duplicate.
  - Abort if any answer block lacks `Category` or `Definition`.
  - Normalize categories to lower case, strip whitespace.
- **Output**:
  - JSON array written to `site/assets/data/abbreviations.json`.
  - Same JSON injected into the page via a `<script>` that defines `window.ABBREVIATIONS`.
- **Error handling**: raise `MkDocsException` with a clear message; the strict build will fail.

## 5. UI – `docs/en/abbreviations.md`
- On page load, the injected `window.ABBREVIATIONS` is read.
- **Rendering**:
  1. Sort cards alphabetically by `abbreviation`.
  2. For each card, render the abbreviation as a header.
  3. Sort answer sections alphabetically by their title.
  4. Show `Category` tags as clickable filter chips.
- **Filter**: a dropdown listing all distinct categories; selecting a category hides cards that do not contain at least one answer with that tag.
- **Search**: text input performs a case‑insensitive substring match against abbreviation code, answer titles, categories, and definitions.
- **Add button**: links to `https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md`.
- No external JS libraries; vanilla JavaScript and Material‑theme CSS.

## 6. Contribution Workflow
1. User clicks **Add Abbreviation** on the page.
2. GitHub opens a new‑file form with `TEMPLATE.md` pre‑populated.
3. Contributor fills in the required fields and submits a PR.
4. CI runs a strict MkDocs build.
   - If the hook validation fails, the build fails and the PR cannot be merged.
   - On success, the site is redeployed automatically; the new abbreviation appears.

## 7. CI / Verification
- **Local verification** command:
  ```bash
  DISABLE_MKDOCS_2_WARNING=true ./venv/bin/mkdocs build -f mkdocs.en.yml --strict
  ```
  Checks:
  - JSON file exists (`site/assets/data/abbreviations.json`).
  - Page contains `window.ABBREVIATIONS` with the full dataset.
  - Hook reports no validation errors.
- **GitHub Actions** (`.github/workflows/deploy.yml`): runs the same strict build for both `mkdocs.en.yml` and `mkdocs.nl.yml`. A failing step blocks the push.
- Optional sanity‑check script (Python) can be added to load the generated JSON and assert:
  - number of entries > 0
  - alphabetical order of abbreviations and answer titles
  - each entry has at least one category.

## 8. Edge Cases & Pitfalls
- **Duplicate abbreviation** – the hook raises an error.
- **Category spelling** – normalised to lower case; avoid accidental duplicates (`_Performance` vs `performance`).
- **Large data set** – client‑side O(N) search may become sluggish beyond ~200 entries; consider pagination if the list grows.
- **Dutch build** – feature is English‑only; the Dutch navigation currently points to the English page via an absolute link (`/abbreviations/`).
- **Missing front‑matter** – will abort the build; always start with the template.

## 9. Future Improvements (Road‑Map)
- **Bulk import**: CSV → markdown conversion script for bulk addition.
- **REST endpoint**: expose the generated JSON via a lightweight API for external tools.
- **Localization**: separate JSON per language and a language selector.
- **Unit tests** for the hook (pytest) to enforce schema invariants automatically.
- **Pagination** in the UI for very large abbreviation sets.

---
*Document version: 1.0 (2026‑09‑12)*