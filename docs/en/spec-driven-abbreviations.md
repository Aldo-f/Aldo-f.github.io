---
title: Spec‑Driven Development – Abbreviation Cheatsheet
---

## What is Spec‑Driven Development?
Spec‑Driven Development (SDD) is a lightweight approach where **specs act as the authoritative source** for a feature’s behavior, data model, and validation rules. Rather than writing code first and then documenting, you write a concise specification and let the implementation be driven by that spec.

## SDD applied to the Abbreviation Cheatsheet
- **Specification location** – The feature’s spec lives in this file (`docs/en/spec-driven‑abbreviations.md`). It describes the expected data shape, UI behavior, and build‑time integration.
- **Data contract** – Each abbreviation file must contain:
  ```yaml
  abbreviation: <CODE>
  ```
  followed by one or more answer sections (`## Title` headings) that each provide a **Category** and a **Definition** line. The hook validates this contract and emits `site/assets/data/abbreviations.json`.
- **UI contract** – The generated JSON is injected as `window.ABBREVIATIONS` and the client‑side script guarantees:
  1. Cards are ordered alphabetically by abbreviation.
  2. Answers inside a card are sorted alphabetically by their heading.
  3. Category filters hide/show whole cards.
  4. The search box matches abbreviation, title, category and definition.
- **Verification** – After each change the workflow runs:
  - `mkdocs build --strict` for English (and Dutch) to ensure the spec matches the generated site.
  - A quick Python sanity‑check that the JSON file contains the expected number of entries and that the search logic works on the raw data.
- **Contribution flow** – The spec lists the GitHub *Add Abbreviation* link:
  `https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md` – contributors paste a new file that conforms to the spec, then the CI rebuilds the site automatically.

## Why use SDD here?
- Guarantees **consistent data** across all abbreviation files.
- Prevents **broken UI** – the hook aborts the build if a file is malformed.
- Makes the feature **self‑documenting** – future contributors see the spec before they add or edit entries.
- Aligns with the repo’s overall **Spec‑Driven Development** culture used for other features (e.g., SDD for REST endpoints, UI components, etc.).

---

*This page is linked from the navigation under **Spec‑Driven Development** for quick reference.*