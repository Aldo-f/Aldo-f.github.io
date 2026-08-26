# Feature Specification: Bidirectional Blog Auto-Translation

**Feature Branch**: `003-blog-autotranslate` | **Created**: 2026-08-23
**Status**: Draft
**Input**: Own translation tooling ("our own plugin") using DeepL; a post existing only in NL gets an EN counterpart and vice versa.

## User Story (P1)

After writing/publishing a post in one language, the author runs
`scripts/blog_translate.py` (dry-run first, `--write` to apply). Every post
missing in the other language tree is created there — front matter preserved,
title + body translated via DeepL, code blocks untouched, provenance marker
appended. The author reviews the git diff before committing.

## Functional Requirements

- **FR-1**: Bidirectional gap-fill between `docs/en/blog/posts/` and
  `docs/nl/blog/posts/` (slug-set comparison, both directions).
- **FR-2**: Never overwrite existing files (idempotent; re-run = no-op).
- **FR-3**: Drafts (`draft: true`) are never propagated.
- **FR-4**: Front matter preserved structurally: `title` translated, `date`
  and `categories` kept verbatim (shared taxonomy), `draft` never added.
- **FR-5**: Fenced code blocks pass through untranslated.
- **FR-6**: Prose translated via DeepL free API (`api-free.deepl.com`,
  `DEEPL_API_KEY` env or `~/.config/deepl/api_key`, mode 0600).
- **FR-7**: Provenance HTML comment appended: source slug, direction, date.
- **FR-8**: Default is dry-run (report only); `--write` persists; clear summary.
- **FR-9**: Testability: translator backend injectable (mock for tests);
  harness never touches the network.

## Non-goals

- Translating docs pages / imported repos (blog only, v1)
- Re-translating or updating existing translations (delete + re-run manually)
- Category name localization (shared taxonomy by design)
- Running translation during CI deploys (explicitly rejected: API burn,
  unreviewed output)

## Success Criteria

- **SC-1**: With a mock translator, unit checks prove: gap detection both ways,
  front-matter shape, code-fence passthrough, idempotence, draft skip,
  provenance marker, dry-run default.
- **SC-2**: Real run fills the current real gap: `welcome-to-the-blog` +
  `building-this-hub` appear under `docs/nl/blog/posts/` (en→nl); nothing is
  overwritten.
- **SC-3**: After regeneration + harness: 15/15 bilingual checks still PASS;
  strict builds zero warnings; live site shows the translated NL posts after
  push; DeepL usage delta reasonable (<20k chars).
