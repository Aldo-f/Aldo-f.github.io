# Implementation Notes: Blog Auto-Translation (003)

**Completed**: 2026-08-23

## Evidence trail

- **RED**: `python3 tests/test_translate_missing.py` → ModuleNotFoundError
  (module absent), then after first implementation 11/14 → fixed test-helper
  unpacking bug, two wrong expectations (bidirectional gap report includes
  both directions; provenance cites slug without `.md`), and one real bug
  (blank-line edges of prose chunks carried into translated output) fixed in
  `split_blocks`. Final: **14/14 PASS**.
- **DeepL probes** (free tier): `tag_handling=markdown` → HTTP 400 unsupported;
  plain mode preserves `**bold**` and `[links](url)` verbatim → design uses
  plain mode with code-fence passthrough instead.
- **Real run**: dry-run reported exactly `building-this-hub`,
  `welcome-to-the-blog` (EN→NL) + draft skip; `--write` consumed **1,251**
  chars. Sample quality: "Welkom op de blog" … natural Dutch, links/bold
  intact, front matter preserved, provenance comment appended.
- **Harness**: after regeneration 13→14/15; the single remaining FAIL is the
  freshness guard correctly flagging that the new NL overview was not yet
  committed (by design it compares HEAD vs working tree).
- Harness invariant updated for 003: mirrored posts are now EXPECTED in both
  search indexes (`xylophone-framework` must appear in NL index too); draft
  exclusion remains the isolation guarantee.

## Operational notes

- Key lives in `~/.config/deepl/api_key` (0600) or `DEEPL_API_KEY`; never in
  git. `:fx` suffix auto-selects the free endpoint.
- Workflow: write/publish post in one language →
  `python3 scripts/blog_translate.py` (review plan) → `--write` → review diff
  → `scripts/gen_category_index.py` → commit. Re-running is a no-op; to
  retranslate delete the target file first.
- Quota: ~1.3k chars for two posts → 1M/month free tier is ample.
