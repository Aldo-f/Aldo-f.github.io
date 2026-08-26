# Feature Specification: Blog via Material Blog Plugin

**Feature Branch**: `001-blog-via-material`
**Created**: 2026-08-23
**Status**: Draft
**Input**: Add a blog to the Aldo Fieuw documentation hub, delivered as a plugin (Spec Kit SDD flow).

## User Scenarios & Testing

### User Story 1 — Visitor reads the blog (Priority: P1)

A visitor to https://aldo-f.github.io wants to read posts. They open "Blog" in
the main navigation and see a reverse-chronological list of posts with titles,
dates and excerpts. Clicking a post shows the full post with standard Material
styling (TOC, back-to-top, theme-aware palette), plus prev/next navigation.

**Why this priority**: A blog that cannot be read is not a blog; this is the
core user-visible outcome of the whole feature.

### User Story 2 — Author publishes a post (Priority: P1)

The site owner adds a markdown file with front matter (`date`, `title`,
optionally `categories`, `draft`) into a dedicated content directory and it
appears on the blog automatically on next build/deploy — no manual list
editing, no touching nav for each post.

**Why this priority**: Zero-friction publishing is the reason to use a plugin
instead of hand-maintained pages; without it the feature fails its purpose.

### User Story 3 — Visitor discovers the blog (Priority: P2)

From any existing docs page, the visitor can reach the blog through a visible
"Blog" entry in the site navigation. The blog does not disturb existing docs
nav structure or URLs.

**Why this priority**: Discoverability matters but only once reading and
publishing work.

### Edge Cases

- A post with `draft: true` must NOT appear anywhere in a production build.
- A post missing the required `date` front matter must fail the strict build
  with a clear warning/error rather than silently dropping.
- The blog listing when zero published posts exist must render an empty-state
  page without breaking the build.
- Existing pages' URLs and content MUST be unchanged (no regressions).

## Requirements

### Functional Requirements

- **FR-1**: The hub exposes a blog section at URL `/blog/` reachable from the
  top-level site navigation.
- **FR-2**: Posts live in a dedicated directory inside the site's own content,
  separate from regular docs pages.
- **FR-3**: Publishing a post requires only adding one markdown file with
  `date` + `title` front matter (categories optional); no other file edits.
- **FR-4**: Post listing is ordered newest-first and shows title, date, and
  excerpt (first paragraph) per post.
- **FR-5**: Each post page offers previous/next post links.
- **FR-6**: Posts can be marked as drafts and are excluded from production
  builds.
- **FR-7**: Categories group posts; category views exist under `/blog/category/`.
- **FR-8**: The full existing site continues to build strictly and serve all
  previously working routes after the change (regression guard).
- **FR-9**: The blog integrates with the site's search so published posts are
  findable via the existing search box.

## Intent / Non-goals (deferred)

The following are explicitly OUT OF SCOPE for this first iteration:

- RSS/Atom feed generation (can be added later by enabling feed support).
- Comments, social sharing buttons, view counters, analytics.
- Multi-author metadata or author pages.
- Backdating/importing historical content beyond seed posts.
- Any change to multirepo-imported project docs.

## Constraints & Assumptions

- Deployment target is GitHub Pages at https://aldo-f.github.io via CI;
  verification may use a locally served build.
- The installed documentation toolchain already bundles the required blog
  capability as an official plugin; no new dependency is expected.
- Seed content consists of a small number of placeholder-quality posts written
  by the owner; they establish the format and prove every requirement.

## Assumptions

- Blog lives at path `/blog/` with default pagination (posts-per-page default
  is acceptable until volume makes it otherwise).
- One primary author (the site owner); no author pages needed.
- Dutch/English: posts follow the existing site language (English UI labels);
  individual posts may be in either language.
- Draft workflow = front-matter flag, excluded from production builds.

## Success Criteria

- **SC-1**: A visitor navigating from the home page reaches `/blog/` within one
  click and sees the listing with all published seed posts.
- **SC-2**: Adding a new post file increases the listing count by exactly one
  on rebuild without any other file changes.
- **SC-3**: All functional requirements hold in a strict build AND against the
  actually-served built site (HTTP 200 + expected body content on key routes:
  `/`, `/blog/`, one post route, `/blog/category/<x>/`).
- **SC-4**: Every previously working route still serves identical status and
  content shape after the change.
- **SC-5**: A draft post is verifiably absent from the production build output.
- **SC-6**: Search finds published posts by a distinctive word in their body.

## Review & Acceptance Checklist

*Gate phase: G - -*

- [ ] FR-1..FR-9 testable and unambiguous
- [ ] Success criteria measurable and technology-agnostic where possible
- [ ] Edge cases covered (drafts, missing date, empty listing, regressions)
- [ ] Scope bounded; non-goals explicit
