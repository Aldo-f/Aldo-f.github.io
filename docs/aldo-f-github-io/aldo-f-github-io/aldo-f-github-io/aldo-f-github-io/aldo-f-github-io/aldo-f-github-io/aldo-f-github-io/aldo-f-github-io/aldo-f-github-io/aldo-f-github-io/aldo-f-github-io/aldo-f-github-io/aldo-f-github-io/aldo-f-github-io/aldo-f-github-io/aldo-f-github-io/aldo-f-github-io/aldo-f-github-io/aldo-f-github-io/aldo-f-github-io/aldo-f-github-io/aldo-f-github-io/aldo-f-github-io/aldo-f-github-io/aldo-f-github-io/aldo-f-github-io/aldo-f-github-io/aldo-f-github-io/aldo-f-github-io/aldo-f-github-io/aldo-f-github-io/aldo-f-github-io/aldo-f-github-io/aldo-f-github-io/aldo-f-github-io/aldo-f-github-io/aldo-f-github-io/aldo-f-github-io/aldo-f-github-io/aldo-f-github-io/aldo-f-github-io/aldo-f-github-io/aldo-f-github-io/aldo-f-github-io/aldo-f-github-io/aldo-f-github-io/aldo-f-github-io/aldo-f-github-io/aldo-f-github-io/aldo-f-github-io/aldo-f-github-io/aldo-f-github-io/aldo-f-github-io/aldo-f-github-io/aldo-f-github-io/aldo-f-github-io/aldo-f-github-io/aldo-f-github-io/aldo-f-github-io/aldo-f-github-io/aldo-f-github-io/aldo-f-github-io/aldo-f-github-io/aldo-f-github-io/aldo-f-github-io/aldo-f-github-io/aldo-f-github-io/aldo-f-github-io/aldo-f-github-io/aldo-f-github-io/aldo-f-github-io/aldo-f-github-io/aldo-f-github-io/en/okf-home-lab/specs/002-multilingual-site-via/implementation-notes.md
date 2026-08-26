# Implementation Notes: Multilingual Site via Multi-Build Recipe

**Feature**: 002-multilingual-site-via | **Completed**: 2026-08-23

## Evidence trail

### RED (before restructure)

Harness v2 run against the old single-language layout
(`/tmp/verify_i18n_1.log` predecessor: staged builds failed with
`docs/en missing — language tree not created yet`; full EN build rc=1 config
error) — exit 1, 10/15.

### Mid-implementation catch (kept as regression guard)

After the split, the first GREEN attempt failed 5 EN-side checks. Root cause,
proven empirically: **`INHERIT` REPLACES list values — it does not merge**.
`mkdocs.en.yml` declared only `plugins: [multirepo]`, silently dropping the
blog plugin (posts built as plain pages, no listing). Fixed by declaring each
language's full plugin list explicitly. The harness caught this before any
push — exactly its job.

### GREEN (final)

`./venv/bin/python tests/verify_blog.py` → **15/15 ALL CHECKS PASSED**
(`/tmp/verify_i18n_2.log`), plain `python3` rerun identical
(`/tmp/verify_i18n_plain.log`). Coverage: staged strict builds both languages;
single-file publish mechanics; real repo builds (EN incl. multirepo); legacy
EN routes; EN listing/prev-next; selector both directions; `/nl/`, `/nl/about/`,
`/nl/blog/` Dutch + newest-first; NL post; drafts absent in BOTH languages;
generator v2; freshness guard; per-language category tables; per-language
search indexes (NL index excludes EN-only content).

## Key facts for future work

- Configs: `mkdocs.base.yml` (shared) ← INHERIT ← `mkdocs.en.yml`
  (`docs/en`, site root, multirepo) / `mkdocs.nl.yml` (`docs/nl`,
  `theme.language: nl`, site root + `/nl/`). Root `mkdocs.yml` is GONE — every
  build must name its config via `-f`.
- INHERIT replaces lists (plugins/nav/theme.features): keep each language
  config self-complete for those keys.
- Content ownership: EN keeps ALL posts (incl. Dutch 2019 ones → URLs stable);
  NL owns copies of the three Dutch posts. Category overviews are per-language.
- Generator v2 auto-discovers `docs/*/blog/posts`; adding a language = create
  the tree + rerun `scripts/gen_category_index.py`.
- CI builds twice (`-f mkdocs.en.yml -d site`, `-f mkdocs.nl.yml -d site/nl`)
  and uploads the merged `site/`.

T001–T010 executed; T009/T010 evidence added after push (see git log and this
file's addendum).
