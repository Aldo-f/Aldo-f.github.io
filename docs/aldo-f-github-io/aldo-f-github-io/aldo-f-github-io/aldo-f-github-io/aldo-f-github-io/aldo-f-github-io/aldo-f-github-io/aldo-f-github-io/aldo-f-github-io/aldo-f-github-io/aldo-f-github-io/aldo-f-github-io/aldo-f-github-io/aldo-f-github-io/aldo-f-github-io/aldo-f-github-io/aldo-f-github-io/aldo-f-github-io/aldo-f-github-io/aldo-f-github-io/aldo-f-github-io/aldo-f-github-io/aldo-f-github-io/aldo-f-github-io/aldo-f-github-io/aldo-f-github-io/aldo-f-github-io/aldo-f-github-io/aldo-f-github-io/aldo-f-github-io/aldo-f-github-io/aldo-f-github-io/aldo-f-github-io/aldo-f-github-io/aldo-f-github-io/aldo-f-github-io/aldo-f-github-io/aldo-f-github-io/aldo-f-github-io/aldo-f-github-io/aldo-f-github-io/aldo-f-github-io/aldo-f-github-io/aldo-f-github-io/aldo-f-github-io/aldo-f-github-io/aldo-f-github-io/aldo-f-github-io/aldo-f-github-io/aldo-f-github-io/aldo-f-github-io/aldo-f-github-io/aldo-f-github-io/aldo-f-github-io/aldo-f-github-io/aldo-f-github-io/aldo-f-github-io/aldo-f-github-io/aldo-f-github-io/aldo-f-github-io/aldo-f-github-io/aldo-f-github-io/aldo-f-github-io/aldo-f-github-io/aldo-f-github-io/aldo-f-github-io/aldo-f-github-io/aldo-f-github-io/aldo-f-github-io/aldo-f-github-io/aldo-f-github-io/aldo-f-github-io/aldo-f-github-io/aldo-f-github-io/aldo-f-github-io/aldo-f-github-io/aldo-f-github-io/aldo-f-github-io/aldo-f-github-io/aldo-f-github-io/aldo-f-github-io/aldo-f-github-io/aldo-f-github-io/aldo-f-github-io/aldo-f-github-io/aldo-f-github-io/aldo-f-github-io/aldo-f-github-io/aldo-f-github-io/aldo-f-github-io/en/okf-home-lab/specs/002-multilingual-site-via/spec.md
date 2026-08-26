# Feature Specification: Multilingual Site via Multi-Build Recipe

**Feature Branch**: `002-multilingual-site-via`
**Created**: 2026-08-23
**Status**: Draft
**Input**: Make the repository really multilingual, using the Material multi-build recipe (validated in spike /tmp/spike-i18n, see research.md).

## User Scenarios & Testing

### User Story 1 — Dutch visitor reads in Dutch (P1)

A Dutch-speaking visitor opens the site, picks "Nederlands" in the language
selector, and gets Dutch chrome (UI labels, `lang="nl"`), a Dutch home page,
about page and blog section with the Dutch posts. URLs live under `/nl/`.

### User Story 2 — English visitor unaffected (P1)

Everything that works today keeps working at the same URLs: `/`, `/about/`,
`/projects/`, imported docs, `/blog/…` including the `/blog/category/`
overview with identical counts. The EN listing keeps carrying the Dutch
historical posts (status quo).

### User Story 3 — Author publishes per language (P2)

Adding a post to `docs/en/blog/posts/` or `docs/nl/blog/posts/` publishes it
in that language's blog only; the per-language category overview regenerates
via the existing script pattern (one invocation covers both languages).

## Requirements

- **FR-1**: Language selector (Material `extra.alternate`) on every page of
  both languages, linking `/` (EN) and `/nl/` (NL).
- **FR-2**: NL build served under `/nl/` with `lang="nl"` document attributes
  and Dutch UI labels (`theme.language: nl`).
- **FR-3**: NL content: home, about ("Over"), blog index, and the three Dutch
  posts (1 april, Start van de Scrum-week, Einde Scrum).
- **FR-4**: Per-language category overview tables (EN: current five-category
  table byte-stable; NL: General/Scrum/VDAB from NL posts only).
- **FR-5**: Drafts excluded in both languages.
- **FR-6**: Both languages build with `--strict`, zero warnings.
- **FR-7**: Search works per language build.
- **FR-8**: Multirepo imports keep working in the EN build.

## Non-goals (deferred)

- Same-page language switching (upstream: not possible across separate builds)
- Translating imported project docs or the EN posts into Dutch
- RSS feeds, additional languages beyond EN/NL

## Constraints & Assumptions

- Approach fixed by spike verdict: multi-build INHERIT configs; NO
  mkdocs-static-i18n (drops blog posts, upstream #4863 "not fixable").
- Accepted trade-off: switching language lands on the other language's home.
- Root `mkdocs.yml` is replaced by `mkdocs.en.yml`; all builds name their
  config explicitly (`-f`).

## Success Criteria

- **SC-1**: Both strict builds exit 0, zero warnings, locally and in CI.
- **SC-2**: Served merged output: all pre-existing routes return 200 with
  unchanged markers; `/nl/`, `/nl/about/`, `/nl/blog/`, NL post route,
  `/nl/blog/category/` return 200 with expected content.
- **SC-3**: Switcher renders on both languages' pages (hreflang links + menu).
- **SC-4**: NL pages emit `lang="nl"`; EN pages unchanged.
- **SC-5**: Harness passes 100% under repo venv AND plain python3; CI green;
  live site verified with curl.
