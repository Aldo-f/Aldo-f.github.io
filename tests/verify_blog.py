#!/usr/bin/env python3
"""End-to-end verification harness for the blog feature.

Spec: specs/001-blog-via-material/spec.md
Contracts: specs/001-blog-via-material/contracts/site-contract.md

stdlib-only. Runs against the REAL toolchain:
  1. strict builds (baseline, probe-added) asserting exit 0 + zero warnings
  2. a real HTTP server serving the built site with route/body assertions
  3. draft-exclusion, search-index and regression checks

Exit 0 = ALL CHECKS PASSED. Any failing check prints FAIL and exits 1.
"""

from __future__ import annotations

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
DOCS = REPO / "docs"
POSTS = DOCS / "blog" / "posts"
MKDOCS = shutil.which("mkdocs")
VENV_BIN = REPO / "venv" / "bin"
if MKDOCS is None:
    candidate = VENV_BIN / "mkdocs"
    if candidate.is_file():
        MKDOCS = str(candidate)

RESULTS: list[tuple[str, bool, str]] = []


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


def run_build(workdir: Path) -> tuple[int, str]:
    """Run mkdocs build --strict inside workdir; return (rc, combined_output)."""
    assert MKDOCS is not None, "mkdocs executable not resolved"
    env = dict(os.environ)
    env.setdefault("DISABLE_MKDOCS_2_WARNING", "true")  # upstream banner noise
    proc = subprocess.run(
        [MKDOCS, "build", "--strict", "--site-dir", "site"],
        cwd=workdir,
        capture_output=True,
        text=True,
        env=env,
        timeout=900,
    )
    return proc.returncode, (proc.stdout + proc.stderr)


# --------------------------------------------------------------------------
# Build-tree helpers
# --------------------------------------------------------------------------

PROBE_TITLE = "ZZProbe Post Alpha"
PROBE_TOKEN = "zzprobe-alpha-unique-token"
DRAFT_SLUG = "roadmap-notes-draft"


def stage_repo(tmp: Path, *, include_draft: bool = False, tag: str = "work") -> Path:
    """Copy tracked content + config into tmp for isolated strict builds."""
    work = tmp / f"work-{tag}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    shutil.copytree(DOCS, work / "docs")
    # multirepo caches live outside docs/, so imported nav entries are absent
    # in staged builds; prune those entries so the staged build is valid.
    cfg = (REPO / "mkdocs.yml").read_text(encoding="utf-8")
    cfg = _prune_multirepo(cfg)
    (work / "mkdocs.yml").write_text(cfg, encoding="utf-8")
    if not include_draft:
        draft = work / "docs" / "blog" / "posts" / f"{DRAFT_SLUG}.md"
        if draft.exists():
            draft.unlink()
    return work


def _prune_multirepo(cfg: str) -> str:
    """Remove the multirepo plugin + its nav_repos block and the nav entries
    that reference imported paths, so an isolated build without the cloned
    repos still validates."""
    lines = cfg.splitlines(keepends=True)
    out: list[str] = []
    skipping_block = False
    depth = 0
    in_nav = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("multirepo:"):
            skipping_block = True
            depth = len(line) - len(line.lstrip())
            continue
        if skipping_block:
            ind = len(line) - len(line.lstrip())
            if line.strip() and ind <= depth:
                skipping_block = False
            else:
                continue
        if stripped == "nav:":
            in_nav = True
            out.append(line)
            continue
        if in_nav:
            ind = len(line) - len(line.lstrip())
            if line.strip() and ind == 0:
                in_nav = False
            elif "- clock/" in line or "- thuis" in line:
                # drop any list item under Projects referencing imported paths
                continue
        out.append(line)
    text = "".join(out)
    text = text.replace("  - section-index\n", "")
    return text


def serve_site(site_dir: Path):
    """Serve site_dir over loopback HTTP; returns (httpd, thread, base_url).

    Binds an ephemeral port (0) so concurrent/rapid reruns never collide.
    """

    class Server(socketserver.TCPServer):
        allow_reuse_address = True

    class Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            # SimpleHTTPRequestHandler serves relative to cwd; pin to site_dir.
            path = path.split("?", 1)[0].split("#", 1)[0]
            return str(site_dir / path.lstrip("/"))

        def log_message(self, format, *args):  # noqa: A002 - stdlib signature
            pass

    httpd = Server(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    port = httpd.server_address[1]
    return httpd, thread, f"http://127.0.0.1:{port}"


def fetch(url: str) -> tuple[int, str]:
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.status, body
    except urllib.error.HTTPError as err:  # type: ignore[attr-defined]
        return err.code, ""


import urllib.error  # noqa: E402  (after function defs is fine at module scope)


def assert_route(base: str, route: str, must_contain: list[str], not_contain: list[str] | None = None):
    status, body = fetch(base + route)
    assert status == 200, f"{route} returned HTTP {status}"
    for marker in must_contain:
        assert marker in body, f"{route} missing marker {marker!r}"
    for marker in not_contain or []:
        assert marker not in body, f"{route} unexpectedly contains {marker!r}"


# --------------------------------------------------------------------------
# Check implementations (run in order inside main)
# --------------------------------------------------------------------------

_BANNER_PAT = re.compile(
    r"warning from the material for mkdocs team|"
    r"mkdocs may break support|this warning was initiated",
    re.IGNORECASE,
)


def _real_warnings(output: str) -> list[str]:
    """True build warnings only — excludes the mkdocs2 banner chatter."""
    return [
        ln
        for ln in output.splitlines()
        if "WARNING" in ln.upper() and not _BANNER_PAT.search(ln)
    ]


def check_strict_build_baseline(tmp: Path) -> str:
    work = stage_repo(tmp)
    rc, output = run_build(work)
    warnings = _real_warnings(output)
    assert rc == 0, f"strict build failed rc={rc}\n{output[-2000:]}"
    assert not warnings, "strict build emitted warnings:\n" + "\n".join(warnings[:10])
    return "exit 0, zero warnings (staged content)"


def make_probe_post(work: Path) -> Path:
    posts = work / "docs" / "blog" / "posts"
    probe = posts / "zz-probe-alpha.md"
    probe.write_text(
        "---\n"
        f"title: {PROBE_TITLE}\n"
        "date: 2026-08-25\n"
        "categories:\n"
        "  - General\n"
        "---\n\n"
        f"Probe body mentioning {PROBE_TOKEN} for verification.\n",
        encoding="utf-8",
    )
    return probe


def check_probe_publish(tmp: Path) -> str:
    """FR-2/FR-3/SC-2: adding ONE file publishes a post; removing unpublishes."""
    work = stage_repo(tmp, tag="probe")
    baseline_listing = work / "site" / "blog" / "index.html"

    # Build WITHOUT probe first (draft included here; irrelevant to this check)
    rc, output = run_build(work)
    assert rc == 0, f"pre-probe strict build failed rc={rc}\n{output[-1500:]}"
    before = baseline_listing.read_text(encoding="utf-8") if baseline_listing.exists() else ""
    assert PROBE_TITLE not in before, "probe title present before probe added?!"

    probe = make_probe_post(work)
    rc, output = run_build(work)
    assert rc == 0, f"post-probe strict build failed rc={rc}\n{output[-1500:]}"
    after = baseline_listing.read_text(encoding="utf-8")
    assert PROBE_TITLE in after, "adding one file did not publish the post (FR-3)"
    assert PROBE_TOKEN in after or PROBE_TITLE in after, "excerpt/listing did not update"

    probe.unlink()
    rc, output = run_build(work)
    assert rc == 0, f"cleanup strict build failed rc={rc}\n{output[-1500:]}"
    restored = baseline_listing.read_text(encoding="utf-8")
    assert PROBE_TITLE not in restored, "removing the file did not unpublish it"
    return "add-file → published; remove-file → unpublished (strict builds green throughout)"


def main() -> int:
    if MKDOCS is None:
        print("FATAL: mkdocs executable not found", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="verify-blog-") as td:
        tmp = Path(td)

        # ---- Phase A: strict-build checks on staged copies -----------------
        check("strict build baseline (exit 0, zero warnings)", lambda: check_strict_build_baseline(tmp))
        check("publish mechanics: single file add/remove (FR-3, SC-2)", lambda: check_probe_publish(tmp))

        # ---- Phase B: full-repo build into repo site/ -----------------------
        # This is the REAL build (multirepo imports included).
        rc, output = run_build(REPO)
        full_ok = rc == 0
        full_warnings = _real_warnings(output)
        RESULTS.append(("full strict build (real repo, multirepo included)", full_ok,
                        f"rc={rc}, warnings={len(full_warnings)}"))
        print(f"{'PASS' if full_ok else 'FAIL'} full strict build — rc={rc}, "
              f"warnings={len(full_warnings)}")
        if not full_ok:
            print(output[-3000:])
            return _summary()

        httpd, _thread, base = serve_site(REPO / "site")
        try:
            # ---- US1: reading the blog -------------------------------------
            check("listing shows newest-first + excerpts (FR-4)",
                  lambda: assert_route(base, "/blog/", [
                      "Welcome to the blog",
                      "How this documentation hub is built",
                  ], ["Roadmap notes"]))
            order = fetch(base + "/blog/")[1]
            i_new = order.find("Welcome to the blog")
            i_old = order.find("How this documentation hub is built")

            def ordering():
                assert 0 <= i_new < i_old, (
                    f"listing not newest-first (newer@{i_new}, older@{i_old})"
                )
                return "newer post listed above older post"

            check("ordering newest-first (FR-4)", ordering)

            def post_page():
                status, body = fetch(base + "/blog/2026/08/23/welcome-to-the-blog/")
                assert status == 200, f"post page HTTP {status}"
                assert "xylophone-framework" in body, "post body token missing"
                assert 'rel="prev"' in body and \
                    "how-this-documentation-hub-is-built" in body, \
                    "prev link to older post missing (FR-5)"
                assert "md-post__nav" in body or "md-footer__link" in body, \
                    "no VISIBLE prev/next navigation rendered (FR-5)"
                return "body token + visible prev-link present"

            check("post page renders w/ prev-next (FR-5)", post_page)

            # ---- US2: drafts + categories ----------------------------------
            def draft_absent():
                status, _ = fetch(base + f"/blog/2026/08/23/{DRAFT_SLUG}/")
                assert status != 200, "draft post is publicly served! (FR-6)"
                listing_status, listing_body = fetch(base + "/blog/")
                assert listing_status == 200
                assert "Roadmap notes" not in listing_body, "draft appears in listing"
                cat_status, cat_body = fetch(base + "/blog/category/general/")
                assert cat_status == 200, f"category page HTTP {cat_status}"
                assert "Welcome to the blog" in cat_body, "category missing published post"
                assert "Roadmap notes" not in cat_body, "draft leaks via category page"
                site_dir = REPO / "site"
                assert not (site_dir / "blog" / "2026" / "08" / "23" / DRAFT_SLUG).exists(), \
                    "draft directory exists in built output"
                return "absent from routes, listing, category and disk"

            check("draft excluded from production (FR-6, SC-5)", draft_absent)

            def category_meta():
                status, body = fetch(base + "/blog/category/meta/")
                assert status == 200, f"/blog/category/meta/ HTTP {status}"
                assert "How this documentation hub is built" in body
                return "meta category view lists its post"

            check("category views exist (FR-7)", category_meta)

            # ---- US4: categories overview (/blog/category/) -----------------
            def run_generator():
                import subprocess as _sp

                proc = _sp.run(
                    [sys.executable, str(REPO / "scripts" / "gen_category_index.py")],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                assert proc.returncode == 0, (
                    "gen_category_index.py failed:\n" + proc.stderr[-500:]
                )
                return proc.stdout.strip()

            check("category-index generator runs", run_generator)

            def index_fresh():
                head = subprocess.run(
                    ["git", "-C", str(REPO), "show", "HEAD:docs/blog/category/index.md"],
                    capture_output=True,
                    text=True,
                )
                current = (REPO / "docs" / "blog" / "category" / "index.md").read_text(
                    encoding="utf-8"
                )
                if head.returncode != 0:
                    return "new file (not yet committed)"
                assert head.stdout == current, (
                    "docs/blog/category/index.md is STALE vs regenerated content — "
                    "run scripts/gen_category_index.py and commit the result"
                )
                return "committed copy matches regenerated content"

            check("committed category index is fresh", index_fresh)

            def categories_overview():
                status, body = fetch(base + "/blog/category/")
                assert status == 200, f"/blog/category/ HTTP {status}"
                # Published posts only (drafts excluded) as of this writing:
                expected = {
                    "General": 1,      # welcome-to-the-blog (roadmap draft excluded)
                    "Jekyll update": 1,
                    "Meta": 1,
                    "Scrum": 2,
                    "VDAB": 2,
                }
                # count cells carry an alignment style -> allow attributes
                rows = re.findall(r"<td[^>]*>(.*?)</td>", body, re.DOTALL)
                names = [re.sub(r"<[^>]+>", "", cell).strip() for cell in rows[::2]]
                counts = [re.sub(r"\s+", "", cell) for cell in rows[1::2]]
                assert names == sorted(expected, key=str.lower), (
                    f"overview categories wrong: {names}"
                )
                for name, count in zip(names, counts):
                    assert count == str(expected[name]), (
                        f"{name}: got {count!r}, want {expected[name]}"
                    )
                    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
                    assert f'href="{slug}/"' in body, f"link {slug}/ missing"
                assert "Roadmap notes" not in body, "draft leaked into overview"
                return f"{len(names)} categories with live counts"

            check("categories overview w/ counts (US4)", categories_overview)

            # ---- US3: discovery --------------------------------------------
            def nav_everywhere():
                for route, marker in (
                    ("/", "Aldo Fieuw Documentation"),
                    ("/about/", "central documentation hub"),
                    ("/projects/", "quick index of the projects"),
                    ("/thuis/docs/", "Overview - Aldo Fieuw Documentation"),
                ):
                    status, body = fetch(base + route)
                    assert status == 200, f"regression: {route} HTTP {status}"
                    assert marker in body, f"regression: {route} lost marker"
                    # MkDocs emits depth-relative nav hrefs: "blog/",
                    # "../blog/", "../../blog/", ...
                    import re as _re

                    assert _re.search(r'href="(?:\.\./)*blog/"', body), \
                        f"nav Blog link missing on {route}"
                return "home/about/projects/thuis all 200 + Blog nav present"

            check("existing routes intact + Blog nav everywhere (SC-4, FR-1)", nav_everywhere)

            def search_index():
                status, body = fetch(base + "/search/search_index.json")
                assert status == 200, f"search index HTTP {status}"
                assert "xylophone-framework" in body, "published post not indexed"
                assert DRAFT_SLUG not in body, "draft leaked into search index"
                return "published post indexed; draft excluded"

            check("search indexes blog posts (FR-9)", search_index)
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
