# Implementation Plan: Same-Page Language Switching (004)

**Branch**: `004-slugmap-language-switch` | **Date**: 2026-08-23 | **Spec**: [spec.md](spec.md)

## Summary

An MkDocs `hooks` module (`hooks/slugmap.py`, supported natively by MkDocs —
no plugin packaging needed) runs `on_post_build` per language build: it reads
both docs trees' blog posts, pairs them by filename, slugifies titles with
Material's own default slugifier, writes `slugmap.json` into the site root,
and injects a tiny JS interceptor via each build's config so the language
selector prefers the mapped twin URL.

## Design decisions

| Decision | Rationale |
|----------|-----------|
| MkDocs hooks (native) instead of packaged plugin | zero packaging/pip overhead; hooks are first-class in mkdocs 1.6 |
| Map written by BOTH builds to the same merged file | EN build writes EN→NL entries; NL build merges its own view; deterministic union keyed by URL path |
| JS injected via `extra_javascript` + file emitted by the hook | survives strict builds; no theme overrides dir to maintain |
| Lookup by normalized pathname | tolerant of trailing-slash/index.html variants |

## Tasks

- [ ] T001 RED: `tests/test_slugmap.py` (parity with pymdownx slugify, pairing
      logic, missing-mirror exclusion, JSON shape)
- [ ] T002 Implement `hooks/slugmap.py` (+ embedded slug-switch.js emission);
      wire `hooks:` + `extra_javascript:` into base config of both builds
- [ ] T003 Unit GREEN; full harness GREEN ×2 interpreters
- [ ] T004 Ship: commit, push, CI green; live `slugmap.json` + JS + behavior
      verified with curl (URL present in map; JS served on post pages)
