# Implementation Plan: Blog Auto-Translation (003)

**Branch**: `003-blog-autotranslate` | **Date**: 2026-08-23 | **Spec**: [spec.md](spec.md)

## Summary

Repo-native translator `scripts/blog_translate.py`: compares blog-post slug
sets across `docs/en` ↔ `docs/nl`, fills gaps bidirectionally via DeepL free
API (plain text mode — probe confirmed markdown survives: bold/links intact),
preserving front matter (title translated; date/categories verbatim), passing
code fences through untouched, appending a provenance marker. Dry-run default,
`--write` to persist, mock-injectable backend for network-free tests.

## Key decisions

| Decision | Rationale |
|----------|-----------|
| Script tool, not build-time MkDocs plugin | CI deploys must not spend API quota or publish unreviewed machine translation; output is committed after human review |
| Plain DeepL mode, block-wise batching | `tag_handling=markdown` unsupported on free tier (HTTP 400 verified); blank-line block splitting keeps requests small and diffs clean |
| Categories kept verbatim | Shared taxonomy across languages; NL table currently already uses neutral names |
| Slugs identical across languages | 1:1 mapping enables gap detection and stable URLs (`/nl/blog/<same-path>`) |
| Key from `DEEPL_API_KEY` or `~/.config/deepl/api_key` | Never in repo/git; file chmod 600 |

## Constitution check

I PASS (strict gate untouched) · II PASS (generated posts enter nav via blog
plugin) · III PASS (no new pip deps — stdlib urllib only) · IV PASS (key
outside repo) · V PASS (mock RED→GREEN + real-run evidence + live checks)

## Tasks

- [ ] T001 RED: `tests/test_translate_missing.py` with FakeTranslator covering
      SC-1 matrix; observe failures (module absent)
- [ ] T002 Implement `scripts/blog_translate.py`; GREEN on unit checks
- [ ] T003 Real run: dry-run report → `--write` → inspect diffs; regenerate
      category indexes
- [ ] T004 Harness GREEN 15/15 ×2 interpreters; strict builds clean
- [ ] T005 Commit (code + generated NL posts + specs), push, CI green, live
      `/nl/blog/<new>/` 200 with translated content; record usage delta
