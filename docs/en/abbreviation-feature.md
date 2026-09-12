---
title: Full Abbreviation Feature Overview
---

# Abbreviation Cheatsheet Feature – Full Overview

## Purpose
The abbreviation feature provides a searchable, filterable, alphabetically‑sorted cheatsheet of technical abbreviations (e.g. **DRY**, **YAGNI**, **TDD**, **SDD**). It is intended for the documentation hub (https://aldo-f.github.io) and serves as a self‑service knowledge base for developers and maintainers.

## Data Model
Each abbreviation lives in its own markdown file under `abbreviations/` with the following structure:

```markdown
---
abbreviation: DRY
---

## Don't Repeat Yourself

**Category:** software‑engineering, best‑practices
**Definition:** A principle that encourages reducing duplication of knowledge or logic.
```

- The **front‑matter** (`abbreviation:`) is mandatory – it becomes the key shown on the card.
- One or more **answer sections** are allowed. Every section starts with a level‑2 heading (`## …`). Inside each section:
  - `**Category:**` – a comma‑separated list of tags used for the filter UI.
  - `**Definition:**` – free‑form description of the abbreviation.
- Files must be UTF‑8 encoded and placed directly under `abbreviations/` (no sub‑folders).

## Hook (`hooks/abbreviations.py`)
A MkDocs **module‑level** hook performs all heavy lifting:
1. **Parse** every `abbreviations/*.md` file, validating the contract.
2. **Build** a JSON array of objects:
   ```json
   [{
     "abbreviation": "DRY",
     "answers": [{"title":"Don't Repeat Yourself","category":["software‑engineering","best‑practices"],"definition":"…"}],
   }, ...]
   ```
3. **Write** the JSON to `site/assets/data/abbreviations.json` (generated during the build).
4. **Inject** the same JSON into the page via a `<script>` that defines `window.ABBREVIATIONS = …` – the client‑side UI consumes this variable.
5. **Abort** the build with a clear error if any file violates the spec (missing front‑matter, malformed category line, etc.).

## UI (`docs/en/abbreviations.md`)
The page loads the data script, then renders each abbreviation as a **card**:
- Cards are ordered alphabetically by the abbreviation string.
- Inside a card, answer headings are sorted alphabetically.
- A **category filter** dropdown shows all distinct categories; selecting a category hides all cards that do not contain at least one answer with that tag.
- A **search box** performs a case‑insensitive substring match against:
  - abbreviation code
  - answer title
  - category tags
  - definition text
- The UI is built with vanilla JavaScript and Material‑theme CSS, no external dependencies.

## Contribution Workflow
1. Click the **“Add Abbreviation”** button on the page – it points to the GitHub URL: `https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md`.
2. Fill in the template with the required front‑matter and at least one answer block.
3. Submit the PR. The CI runs a **strict MkDocs build**; the hook validates the file. If the build succeeds the new abbreviation appears automatically after the next deployment.
4. If the PR fails, the build logs pinpoint the validation error (e.g., missing `abbreviation:` key).

## Verification & CI
- **Local verification**: `DISABLE_MKDOCS_2_WARNING=true ./venv/bin/mkdocs build -f mkdocs.en.yml --strict`. The command checks:
  - JSON file exists (`site/assets/data/abbreviations.json`).
  - The page contains `window.ABBREVIATIONS` with the full data set.
  - No validation errors reported by the hook.
- **GitHub Actions**: The repository’s workflow (`.github/workflows/deploy.yml`) runs the same strict build for both English and Dutch. A failing build blocks the merge.
- **Runtime sanity‑check** (optional): a small Python script loads the generated JSON and runs a few assertions (entry count, alphabetical order, at least one category).

## Deployment
The site is deployed via GitHub Pages on push to `main`. Because the hook writes into the **site** directory, the JSON file is version‑controlled only in the build artifact – it never appears in the repository source.

## Edge Cases & Pitfalls
- **Duplicate abbreviations** – the hook will raise an error if two files declare the same `abbreviation:` value.
- **Category spelling** – categories are case‑insensitive, but the hook normalises them to lower case to avoid duplicate filter entries.
- **Large number of answers** – client‑side performance is O(N) for search; with > 200 entries the UI may become sluggish – consider pagination if the list grows substantially.
- **Dutch build** – the feature is English‑only; the Dutch navigation currently links to the English page (the link is absolute `/abbreviations/`).

## Future Improvements (road‑map)
- Add **bulk import** support (e.g., CSV → markdown) for large teams.
- Expose a **REST endpoint** serving the JSON for external tools.
- Implement **localisation** – separate JSON per language and a language selector.
- Add **unit tests** for the hook (pytest) to enforce schema invariants.

---

*For a concise spec‑driven reference see the page **Spec‑Driven Development – Abbreviation Cheatsheet** linked from the navigation.*