# Feature Specification: Same-Page Language Switching

**Feature Branch**: `004-slugmap-language-switch` | **Created**: 2026-08-23
**Status**: Draft
**Input**: Switching language from a post must land on the twin post in the other language, not the other language's home.

## User Story (P1)

A visitor on `/nl/blog/2026/08/23/welkom-op-de-blog/` clicks "English" and
lands on `/blog/2026/08/23/welcome-to-the-blog/`. On pages without a mirror,
the switcher falls back to the other language's home (current behavior).

## Functional Requirements

- **FR-1**: Both builds generate a slug map (`slugmap.json`) at site root
  containing mirror URLs for every blog post that exists in both languages:
  `{"/blog/<date>/<en-slug>/": "/nl/blog/<date>/<nl-slug>/", …}`.
- **FR-2**: Slugs are computed with Material's own default slugifier
  (`pymdownx.slugs.slugify(case='lower')`, separator `-`) applied to each
  post's title → byte-parity with real built URLs.
- **FR-3**: The switcher is intercepted client-side (~30 lines vanilla JS,
  injected into both builds): on click, look up the current URL in the map;
  if found redirect to the twin page; otherwise fall back to the configured
  alternate link (home).
- **FR-4**: No changes to existing switcher markup/CSS; graceful no-JS
  fallback (plain links still work).
- **FR-5**: Non-blog pages (home, about, category overviews) may also be
  mapped when a mirror exists; otherwise home fallback applies.
- **FR-6**: Zero new pip dependencies; stdlib + already-bundled pymdownx only.

## Non-goals

- Server-side redirects (GitHub Pages has none); auto-redirect by browser
  language; translating non-mirrored content.

## Success Criteria

- **SC-1**: Unit checks prove slug parity against `pymdownx` defaults and
  correct mirror mapping both directions; missing-mirror posts excluded.
- **SC-2**: Built `site/slugmap.json` contains the welkom↔welcome pair and
  serves 200 on the live site.
- **SC-3**: Harness GREEN including new switcher-map checks; CI green;
  JS present on served NL and EN post pages.
