# Research: Blog via Material Blog Plugin

## R1 — Which blog capability? (resolves the "plugin" requirement)

**Decision**: Use the official **`blog` plugin bundled with Material for
MkDocs** (bundled since 9.2.0; installed version is 9.7.7).

**Rationale**: Constitution Principle III (upstream-first) mandates using the
platform's own extension points before new dependencies. The blog plugin ships
inside the already-installed `mkdocs-material` package, so `requirements.txt`
and the CI workflow stay untouched. It provides exactly the required surface:
post directory with front matter, newest-first listing, excerpts, pagination,
prev/next links, categories with views, draft exclusion, and search integration
(posts enter the standard `search` plugin index).

**Alternatives considered**:
- *mkdocs-blog-plugin (third-party)* — extra dependency, less maintained than
  the official one; rejected by Principle III.
- *Hand-maintained blog section* (markdown pages + manual listing) — violates
  the zero-friction publishing requirement (FR-3) and duplicates upstream
  functionality.
- *Separate blog engine (Hugo/Jekyll)* — second site, second deploy pipeline;
  massively over-scoped.

## R2 — Exact plugin configuration for mkdocs-material 9.7.7

**Decision**: Enable in `mkdocs.yml`:

```yaml
plugins:
  - blog:
      blog_dir: blog
      post_date_format: yyyy-MM-dd
      archive: false
```

with posts at `docs/blog/posts/*.md`. Keep `archive: false` (not required by
any FR; keeps URL-space and nav minimal). Categories stay enabled (default) for
FR-7. Drafts are supported natively via `draft: true` front matter and are
excluded from production (`drafts: false` is the default) while remaining
visible in `mkdocs serve`.

**Rationale**: Minimal config = every non-required knob left at default.
`blog_dir: blog` is also the default but pinned explicitly so the nav path
contract is stable.

**Alternatives considered**: enabling archive pages now (YAGNI — no FR asks
for them); custom `post_excerpt_format` (default "first paragraph" satisfies
FR-4).

## R3 — Explicit-nav interaction

**Decision**: Add `- Blog: blog/index.md` to the existing explicit `nav:` list.
The blog plugin auto-generates its internal pages (listing pagination, category
views, post pages) under `blog/`; they hang off the Blog nav item without extra
entries.

**Rationale**: The repo uses an explicit `nav:`; MkDocs errors on files not
reachable from nav during strict builds. `blog/index.md` is the single anchor
file that must appear; generated plugin pages are exempt as they are produced
by the plugin itself.

**Alternatives considered**: dropping the explicit `nav:` to let MkDocs infer —
rejected: it would reshuffle all existing docs ordering (regression risk
against SC-4).

## R4 — Verification strategy against the real runtime

**Decision**: A stdlib-only script `tests/verify_blog.py` that:
1. Runs `mkdocs build --strict` twice: once on a temp copy of the repo content
   WITHOUT a probe post and once WITH an added probe post — asserting exit 0,
   zero WARNING lines, and that the listing page contains the probe title only
   in the with-probe run (proves FR-3/SC-2 mechanically).
2. Serves the built `site/` with `http.server` on a loopback port and asserts
   HTTP 200 + body substrings for `/`, `/blog/`, a post route, and a category
   route (SC-3).
3. Asserts the draft post's expected output path does not exist in `site/`
   (SC-5).
4. Asserts regression routes (`/about/`, `/projects/`, imported docs index)
   still return 200 with unchanged marker strings (SC-4).
5. Asserts search index contains a distinctive word from a seed post (FR-9).

**Rationale**: House verification policy requires real end-to-end evidence
against the actual runtime, not venv-only or mocked checks. stdlib-only means
no test-runner dependency needs adding.

**Alternatives considered**: pytest suite (adds dev dependency for a
single-script job — unnecessary); eyeballing `mkdocs serve` (not reproducible,
not evidence).

## R5 — Seed content format

**Decision**: Three posts demonstrating every requirement:

| File | date | title | categories | draft |
|------|------|-------|-----------|-------|
| `welcome-to-the-blog.md` | 2026-08-23 | Welcome to the blog | General | no |
| `building-this-hub.md` | 2026-08-20 | How this documentation hub is built | Meta | no |
| `roadmap-notes-draft.md` | 2026-08-23 | Roadmap notes (draft) | General | **yes** |

Each post has one distinctive body token used by verification (e.g.
`xylophone-framework`) to prove full-content rendering and search indexing
without relying on titles alone.

**Rationale**: One draft proves FR-6/SC-5 continuously; two published posts
prove ordering (newest first) and prev/next linking (FR-5); two distinct
categories prove FR-7.
