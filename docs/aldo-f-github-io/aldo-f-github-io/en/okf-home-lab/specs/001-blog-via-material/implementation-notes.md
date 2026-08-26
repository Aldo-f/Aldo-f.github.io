# Implementation Notes: Blog via Material Blog Plugin

**Feature**: 001-blog-via-material | **Completed**: 2026-08-23

## Evidence trail

### RED (before implementation)

`./venv/bin/python tests/verify_blog.py` → exit **1**, 8/10 checks failing
(archived at `/tmp/verify_red.log`):

```
FAIL publish mechanics — FileNotFoundError ... site/blog/index.html
FAIL listing shows newest-first + excerpts (FR-4) — /blog/ returned HTTP 404
FAIL ordering newest-first (FR-4)
FAIL post page renders w/ prev-next (FR-5) — post page HTTP 404
FAIL draft excluded from production (FR-6, SC-5)
FAIL category views exist (FR-7) — /blog/category/meta/ HTTP 404
FAIL existing routes intact + Blog nav everywhere — nav Blog link missing on /
FAIL search indexes blog posts (FR-9) — published post not indexed
2/10 checks passed · SOME CHECKS FAILED · EXIT_CODE=1
```

### GREEN (after implementation)

`./venv/bin/python tests/verify_blog.py` → exit **0**
(`/tmp/verify_green5.log`) and plain `python3` rerun (`/tmp/verify_plainpy.log`)
— both `10/10 checks passed · ALL CHECKS PASSED`:

```
PASS strict build baseline (exit 0, zero warnings)
PASS publish mechanics: single file add/remove (FR-3, SC-2)
PASS full strict build — rc=0, warnings=0
PASS listing shows newest-first + excerpts (FR-4)
PASS ordering newest-first (FR-4) — newer post listed above older post
PASS post page renders w/ prev-next (FR-5) — body token + visible prev-link
PASS draft excluded from production (FR-6, SC-5) — absent from routes,
     listing, category and disk
PASS category views exist (FR-7) — meta category view lists its post
PASS existing routes intact + Blog nav everywhere (SC-4, FR-1) — home/about/
     projects/thuis all 200 + Blog nav present
PASS search indexes blog posts (FR-9) — published post indexed; draft excluded
10/10 checks passed · ALL CHECKS PASSED · EXIT_CODE=0
```

## Deviations / decisions made during implementation

1. **`navigation.footer` feature added** to `theme.features`. The blog plugin
   only emits machine-readable `<link rel="prev">` without it; the visible
   footer prev/next cards required by FR-5 come from this theme feature. This
   also adds footer prev/next to regular docs pages, which is standard
   Material behavior.
2. **Harness hardening** during RED: banner-warning filter (mkdocs2 +
   Material team banners are not build warnings), per-check staging dirs,
   ephemeral server port (fixed-port reruns collided with TIME_WAIT).
3. **Assertion correction**: initial "newest-first" check compared indices in
   the wrong direction; verified real DOM order first, then fixed the check —
   the site was already correct.
4. **No dependency changes**: `requirements.txt` untouched; the blog plugin
   ships inside mkdocs-material 9.7.7 (constitution Principle III).

## Final task state

T001–T014 complete. T015 (commit/merge/push + live CI confirmation) tracked
separately — see git history and the GitHub Actions run for main.
