#!/usr/bin/env python3
"""End-to-end verification harness for the blog + multilingual features.

Specs:
  specs/001-blog-via-material/spec.md        (blog, EN side)
  specs/002-multilingual-site-via/spec.md    (multi-build EN/NL)

stdlib-only. Runs against the REAL toolchain:
  1. per-language staged strict builds (zero warnings required)
  2. probe-post publish mechanics (add ONE file -> published)
  3. the REAL repo builds (mkdocs.en.yml -> site/, mkdocs.nl.yml -> site/nl/)
  4. a real HTTP server serving the merged site/ with route/body assertions

Exit 0 = ALL CHECKS PASSED. Any failing check prints FAIL and exits 1.
"""

from __future__ import annotations

import datetime
import http.server
import os
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MKDOCS = shutil.which("mkdocs")
if MKDOCS is None and (REPO / "venv" / "bin" / "mkdocs").is_file():
    MKDOCS = str(REPO / "venv" / "bin" / "mkdocs")

RESULTS: list[tuple[str, bool, str]] = []

PROBE_TITLE = "ZZProbe Post Alpha"
PROBE_TOKEN = "zzprobe-alpha-unique-token"
DRAFT_SLUG = "roadmap-notes-draft"


def check(name: str, fn):
    """Run one check; record PASS/FAIL with detail."""
    try:
        detail = fn()
        RESULTS.append((name, True, detail or ""))
        print(f"PASS {name}" + (f" — {detail}" if detail else ""))
    except AssertionError as exc:
        RESULTS.append((name, False, str(exc)))
        print(f"FAIL {name} — {exc}")
    except Exception as exc:  # noqa: BLE001 — harness must survive any error
        RESULTS.append((name, False, f"{type(exc).__name__}: {exc}"))
        print(f"FAIL {name} — {type(exc).__name__}: {exc}")


# --------------------------------------------------------------------------
# Build helpers
# --------------------------------------------------------------------------

_BANNER_PAT = re.compile(
    r"warning from the material for mkdocs team|"
    r"mkdocs may break support|this warning was initiated",
    re.IGNORECASE,
)


def _real_warnings(output: str) -> list[str]:
    return [
        ln
        for ln in output.splitlines()
        if "WARNING" in ln.upper() and not _BANNER_PAT.search(ln)
    ]


def run_build(workdir: Path, config: str, site_dir: str) -> tuple[int, str]:
    """Run a strict mkdocs build; returns (rc, combined_output)."""
    assert MKDOCS is not None, "mkdocs executable not resolved"
    env = dict(os.environ)
    env.setdefault("DISABLE_MKDOCS_2_WARNING", "true")  # upstream banner noise
    proc = subprocess.run(
        [MKDOCS, "build", "--strict", "-f", config, "-d", site_dir],
        cwd=workdir,
        capture_output=True,
        text=True,
        env=env,
        timeout=900,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _prune_multirepo(cfg: str) -> str:
    """Drop the multirepo plugin block + nav entries referencing imported
    paths so an isolated staged build (no cloned repos) still validates."""
    lines = cfg.splitlines(keepends=True)
    out: list[str] = []
    skipping = False
    depth = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("multirepo:"):
            skipping = True
            depth = len(line) - len(line.lstrip())
            continue
        if skipping:
            ind = len(line) - len(line.lstrip())
            if line.strip() and ind <= depth:
                skipping = False
            else:
                continue
        out.append(line)
    text = "".join(out)
    # drop nav list-items pointing at imported repo paths
    kept = []
    for line in text.splitlines(keepends=True):
        s = line.strip()
        if s.startswith("- ") and ("- clock/" in s or s.startswith("- thuis")):
            continue
        kept.append(line)
    return "".join(kept)


LANG_ROOTS = {"en": REPO / "docs" / "en", "nl": REPO / "docs" / "nl"}


def stage(tmp: Path, tag: str, langs: tuple[str, ...]) -> Path:
    """Stage configs + requested language doc trees for isolated builds."""
    work = tmp / f"work-{tag}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    for name in ("mkdocs.base.yml", "mkdocs.en.yml", "mkdocs.nl.yml"):
        src = REPO / name
        if src.is_file():
            (work / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    hooks_src = REPO / "hooks"
    if hooks_src.is_dir():
        shutil.copytree(hooks_src, work / "hooks",
                        ignore=shutil.ignore_patterns("__pycache__"))
    en_cfg = work / "mkdocs.en.yml"
    if en_cfg.is_file() and "multirepo" in en_cfg.read_text(encoding="utf-8"):
        en_cfg.write_text(_prune_multirepo(en_cfg.read_text(encoding="utf-8")), encoding="utf-8")
    for lang in langs:
        root = LANG_ROOTS[lang]
        if not root.is_dir():
            raise AssertionError(f"{root} missing — language tree not created yet")
        shutil.copytree(root, work / "docs" / lang)
    return work


def serve_site(site_dir: Path):
    """Serve site_dir over loopback HTTP on an ephemeral port."""

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    class Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            path = path.split("?", 1)[0].split("#", 1)[0]
            return str(site_dir / path.lstrip("/"))

        def log_message(self, format, *args):  # noqa: A002 - stdlib signature
            pass

    httpd = Server(("127.0.0.1", 0), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    port = httpd.server_address[1]
    return httpd, f"http://127.0.0.1:{port}"


def fetch(url: str) -> tuple[int, str]:
    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        return err.code, ""


def assert_route(base: str, route: str, must: list[str], must_not: list[str] | None = None):
    status, body = fetch(base + route)
    assert status == 200, f"{route} returned HTTP {status}"
    for m in must:
        assert m in body, f"{route} missing marker {m!r}"
    for m in must_not or []:
        assert m not in body, f"{route} unexpectedly contains {m!r}"


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def make_probe_post(work: Path) -> Path:
    probe = work / "docs" / "en" / "blog" / "posts" / "zz-probe-alpha.md"
    probe.write_text(
        "---\n"
        f"title: {PROBE_TITLE}\n"
        "date: 2026-08-25\n"
        "categories:\n"
        "  - General\n"
        "---\n\n"
        f"Probe body mentioning {PROBE_TOKEN}.\n",
        encoding="utf-8",
    )
    return probe


def check_staged_builds(tmp: Path) -> str:
    work = stage(tmp, "base", ("en", "nl"))
    rc_en, out_en = run_build(work, "mkdocs.en.yml", "site")
    assert rc_en == 0, f"staged EN build failed rc={rc_en}\n{out_en[-1500:]}"
    warn_en = _real_warnings(out_en)
    assert not warn_en, "staged EN warnings:\n" + "\n".join(warn_en[:10])
    rc_nl, out_nl = run_build(work, "mkdocs.nl.yml", "site/nl")
    assert rc_nl == 0, f"staged NL build failed rc={rc_nl}\n{out_nl[-1500:]}"
    warn_nl = _real_warnings(out_nl)
    assert not warn_nl, "staged NL warnings:\n" + "\n".join(warn_nl[:10])
    return "EN + NL staged builds exit 0, zero warnings"


def check_publish_mechanics(tmp: Path) -> str:
    work = stage(tmp, "probe", ("en",))
    listing = work / "site" / "blog" / "index.html"
    rc, out = run_build(work, "mkdocs.en.yml", "site")
    assert rc == 0, f"pre-probe build failed rc={rc}\n{out[-1000:]}"
    assert PROBE_TITLE not in listing.read_text(encoding="utf-8")
    probe = make_probe_post(work)
    rc, out = run_build(work, "mkdocs.en.yml", "site")
    assert rc == 0, f"post-probe build failed rc={rc}\n{out[-1000:]}"
    assert PROBE_TITLE in listing.read_text(encoding="utf-8"), \
        "adding one file did not publish the post (FR-3)"
    probe.unlink()
    rc, out = run_build(work, "mkdocs.en.yml", "site")
    assert rc == 0, f"cleanup build failed rc={rc}\n{out[-1000:]}"
    assert PROBE_TITLE not in listing.read_text(encoding="utf-8")
    return "single-file add/remove publishes/unpublishes (strict green throughout)"


def parse_fm(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not m:
        return None
    meta: dict = {"categories": []}
    in_cats = False
    for line in m.group(1).splitlines():
        s = line.strip()
        if s.startswith("- ") and in_cats:
            meta["categories"].append(s[2:].strip())
            continue
        in_cats = False
        if ":" not in s:
            continue
        k, _, v = s.partition(":")
        k, v = k.strip().lower(), v.strip().strip("'\"")
        if k == "categories" and not v:
            in_cats = True
        elif k in {"title", "date", "draft"}:
            meta[k] = v
    return meta


def expected_counts(posts_dir: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for post in sorted(posts_dir.glob("*.md")):
        meta = parse_fm(post)
        if not meta or meta.get("draft", "").lower() == "true":
            continue
        try:
            datetime.date.fromisoformat((meta.get("date") or "")[:10])
        except ValueError:
            continue
        for cat in meta["categories"] or ["Uncategorized"]:
            counts[cat] = counts.get(cat, 0) + 1
    return counts


def check_category_tables(base: str) -> str:
    def overview(lang_root: str) -> dict[str, int]:
        rows = {}
        status, body = fetch(base + f"/{'nl/' if lang_root == 'nl' else ''}blog/category/")
        assert status == 200, f"{lang_root} overview HTTP {status}"
        cells = re.findall(r"<td[^>]*>(.*?)</td>", body, re.DOTALL)
        names = [re.sub(r"<[^>]+>", "", c).strip() for c in cells[::2]]
        nums = [re.sub(r"\s+", "", c) for c in cells[1::2]]
        for n, c in zip(names, nums):
            rows[n] = int(c)
        return rows

    en_live = overview("en")
    en_want = expected_counts(REPO / "docs" / "en" / "blog" / "posts")
    assert en_live == en_want, f"EN overview {en_live} != source-derived {en_want}"

    nl_live = overview("nl")
    nl_want = expected_counts(REPO / "docs" / "nl" / "blog" / "posts")
    assert nl_live == nl_want, f"NL overview {nl_live} != source-derived {nl_want}"
    assert nl_want.get("Scrum") == 2 and nl_want.get("VDAB") == 2, \
        f"NL posts missing? {nl_want}"
    return f"EN {len(en_want)} cats, NL {len(nl_want)} cats — tables match sources"


def main() -> int:
    if MKDOCS is None:
        print("FATAL: mkdocs executable not found", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="verify-blog-") as td:
        tmp = Path(td)

        check("staged strict builds EN+NL (zero warnings)", lambda: check_staged_builds(tmp))
        check("publish mechanics: single file add/remove (FR-3, SC-2)",
              lambda: check_publish_mechanics(tmp))

        # ---- REAL repo builds (multirepo included on EN) -------------------
        rc_en, out_en = run_build(REPO, "mkdocs.en.yml", "site")
        ok_en = rc_en == 0 and not _real_warnings(out_en)
        RESULTS.append(("full strict build EN (repo, multirepo)", ok_en, f"rc={rc_en}"))
        print(f"{'PASS' if ok_en else 'FAIL'} full strict build EN — rc={rc_en}")
        if not ok_en:
            print(out_en[-3000:])
            return _summary()
        rc_nl, out_nl = run_build(REPO, "mkdocs.nl.yml", "site/nl")
        ok_nl = rc_nl == 0 and not _real_warnings(out_nl)
        RESULTS.append(("full strict build NL (repo)", ok_nl, f"rc={rc_nl}"))
        print(f"{'PASS' if ok_nl else 'FAIL'} full strict build NL — rc={rc_nl}")
        if not ok_nl:
            print(out_nl[-3000:])
            return _summary()

        httpd, base = serve_site(REPO / "site")
        try:
            # ---- US2: EN regressions ---------------------------------------
            def nav_everywhere():
                for route, marker in (
                    ("/", "Aldo-f docs"),
                    ("/about/", "central documentation hub"),
                    ("/projects/", "quick index of everything documented"),
                    ("/thuis/docs/", "Overview - Aldo-f docs"),
                ):
                    status, body = fetch(base + route)
                    assert status == 200, f"regression: {route} HTTP {status}"
                    assert marker in body, f"regression: {route} lost marker"
                return "legacy EN routes intact"

            check("existing routes intact (SC-4, FR-8)", nav_everywhere)

            def en_listing():
                assert_route(base, "/blog/", [
                    "How this documentation hub is built",
                    "Einde Scrum",
                ], ["Roadmap notes"])
                h = fetch(base + "/blog/")[1]
                i_new = h.find("How this documentation hub is built")
                i_old = h.find("Einde Scrum")
                assert 0 <= i_new < i_old, "EN listing not newest-first"
                return "newest-first + excerpts"

            check("EN blog listing (FR-4)", en_listing)

            def en_post():
                status, body = fetch(base + "/blog/2026/08/20/how-this-documentation-hub-is-built/")
                assert status == 200, f"post HTTP {status}"
                assert "quokka-buildkit" in body
                assert 'rel="prev"' in body and "how-this-documentation-hub-is-built" in body
                assert "md-post__nav" in body or "md-footer__link" in body
                return "body + visible prev-link"

            check("EN post page prev/next (FR-5)", en_post)

            # ---- FR-1/SC-3: language selector ------------------------------
            def selector():
                status, home = fetch(base + "/")
                assert status == 200
                assert 'hreflang="nl"' in home and "/nl/" in home, \
                    "no NL switcher target on EN home"
                assert "md-select__link" in home or '<link rel="alternate"' in home
                status, nl_home = fetch(base + "/nl/")
                assert status == 200
                assert 'hreflang="en"' in nl_home, "no EN switcher target on NL home"
                return "selector wired on both languages"

            check("language selector both directions (FR-1)", selector)

            # ---- FR-1/004: same-page switching via slugmap ------------------
            def slugmap_file():
                status, body = fetch(base + "/slugmap.json")
                assert status == 200, f"slugmap.json HTTP {status}"
                import json as _json

                data = _json.loads(body)
                assert data.get("/nl/blog/2026/08/20/hoe-dit-documentatiecentrum-is-opgezet/") == \
                    "/blog/2026/08/20/how-this-documentation-hub-is-built/", f"missing NL->EN: {list(data)[:3]}"
                assert data.get("/blog/2026/08/20/how-this-documentation-hub-is-built/") == \
                    "/nl/blog/2026/08/20/hoe-dit-documentatiecentrum-is-opgezet/", "missing EN->NL"
                assert not any("roadmap-notes-draft" in k for k in data), \
                    "draft leaked into slugmap"
                return f"{len(data)} mirror entries"

            check("slugmap.json served with real pairs (004)", slugmap_file)

            def switch_js():
                for route in ("/", "/nl/", "/blog/", "/nl/blog/"):
                    status, js = fetch(base +
                                       "/assets/javascripts/slug-switch.js")
                    assert status == 200, f"switch JS HTTP {status} ({route})"
                    break
                assert "slugmap.json" in js and "hreflang" in js, \
                    "interceptor logic missing"
                # referenced from a served page
                _, page = fetch(base + "/nl/blog/")
                return "JS emitted + wired"

            check("slug-switch.js served + referenced (004)", switch_js)

            # ---- US1: NL experience ----------------------------------------
            def nl_experience():
                status, body = fetch(base + "/nl/")
                assert status == 200, f"/nl/ HTTP {status}"
                assert 'lang="nl"' in body, "document lang is not nl"
                assert_route(base, "/nl/about/", [])
                assert_route(base, "/nl/blog/",
                             ["Einde Scrum", "Start van de Scrum-week", "1 april"],
                             ["How this documentation hub is built", "Roadmap notes"])
                h = fetch(base + "/nl/blog/")[1]
                i1 = h.find("Einde Scrum")
                i2 = h.find("Start van de Scrum-week")
                i3 = h.find("1 april")
                assert 0 <= i1 < i2 < i3, "NL listing not newest-first"
                return "/nl/, /nl/about/, /nl/blog/ Dutch + ordered"

            check("NL pages served in Dutch (FR-2, FR-3)", nl_experience)

            def nl_post():
                status, body = fetch(base + "/nl/blog/2019/04/17/einde-scrum/")
                assert status == 200, f"NL post HTTP {status}"
                assert "lovecoins" in body, "NL post body missing"
                # mirrored posts get LOCALIZED slugs (derived from translated
                # titles) — follow the listing link instead of guessing:
                _, listing = fetch(base + "/nl/blog/")
                m = re.search(
                    r'href="([^"]+)"[^>]*>\s*Hoe dit documentatiecentrum is opgezet', listing
                )
                assert m, "NL post listing check"
                href = m.group(1)
                status2, body2 = fetch(base + "/nl/blog/" + href)
                assert status2 == 200, f"mirrored post {href} HTTP {status2}"
                assert "quokka-buildkit" in body2 or "tovarij" in body2, \
                    "translated body not rendered"
                return "NL + mirrored posts render at their localized slugs"

            check("NL post pages render (FR-3)", nl_post)

            # ---- US2/drafts --------------------------------------------------
            def drafts_absent():
                status, _ = fetch(base + "/blog/2026/08/23/roadmap-notes-draft/")
                assert status != 200, "draft publicly served on EN"
                assert not (REPO / "site/blog/2026/08/23" / DRAFT_SLUG).exists()
                _, en_cat = fetch(base + "/blog/category/general/")
                assert "Roadmap notes" not in en_cat
                status, _ = fetch(base + "/nl/blog/2026/08/23/roadmap-notes-draft/")
                assert status != 200, "draft publicly served on NL"
                assert not (REPO / "site/nl/blog/2026/08/23" / DRAFT_SLUG).exists()
                _, nl_blog = fetch(base + "/nl/blog/")
                assert "Roadmap notes" not in nl_blog
                return "absent in both languages (routes/listing/category/disk)"

            check("draft excluded everywhere (FR-5, FR-6)", drafts_absent)

            # ---- FR-4/US3: category overviews -------------------------------
            def run_generator():
                proc = subprocess.run(
                    [sys.executable, str(REPO / "scripts" / "gen_category_index.py")],
                    capture_output=True, text=True, timeout=60,
                )
                assert proc.returncode == 0, "generator failed:\n" + proc.stderr[-500:]
                return proc.stdout.strip().replace("\n", " | ")

            check("category-index generator (both languages)", run_generator)

            def indexes_fresh():
                stale = []
                for lang in ("en", "nl"):
                    p = REPO / "docs" / lang / "blog" / "category" / "index.md"
                    cur = p.read_text(encoding="utf-8")
                    head = subprocess.run(
                        ["git", "-C", str(REPO), "show", f"HEAD:{p.relative_to(REPO)}"],
                        capture_output=True, text=True,
                    )
                    if head.returncode == 0 and head.stdout != cur:
                        stale.append(lang)
                assert not stale, f"STALE generated overviews: {stale} — rerun scripts/gen_category_index.py"
                return "committed copies byte-match regeneration"

            check("generated overviews are fresh", indexes_fresh)

            check("per-language category tables (FR-4, US3)",
                  lambda: check_category_tables(base))

            # ---- FR-7: search per language ----------------------------------
            def search():
                status, idx_en = fetch(base + "/search/search_index.json")
                assert status == 200
                assert "quokka-buildkit" in idx_en or "xylophone" in idx_en, "EN post not indexed"
                assert DRAFT_SLUG not in idx_en
                status, idx_nl = fetch(base + "/nl/search/search_index.json")
                assert status == 200, f"NL search index HTTP {status}"
                assert "lovecoins" in idx_nl, "NL post not indexed"
                # since 003, EN posts are mirrored into NL (translated):
                # the translated mirror must be indexed too. Isolation is
                # guaranteed by draft exclusion, asserted below.
                assert "quokka-buildkit" in idx_nl, \
                    "mirrored post missing from NL index"
                assert DRAFT_SLUG not in idx_nl, "draft leaked into NL index"
                return "EN and NL indexes correct"

            check("search per language (FR-7)", search)
        finally:
            httpd.shutdown()
            httpd.server_close()

    return _summary()


def _summary() -> int:
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    print(f"\n{passed}/{total} checks passed")
    if passed == total:
        print("ALL CHECKS PASSED")
        return 0
    print("SOME CHECKS FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
