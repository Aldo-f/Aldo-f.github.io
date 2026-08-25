#!/usr/bin/env python3
"""RED tests for hooks/slugmap.py (feature 004). Run: python3 tests/test_slugmap.py"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hooks"))
import slugmap as sm  # noqa: E402

PASS = FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"PASS {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


def post(dir_path: Path, slug: str, title: str, date="2026-01-01", draft=False):
    d = "\ndraft: true" if draft else ""
    (dir_path / f"{slug}.md").write_text(
        f"---\ntitle: {title}\ndate: {date}\ncategories:\n  - General{d}\n---\n\nbody\n",
        encoding="utf-8",
    )


def fresh(en=None, nl=None):
    tmp = Path(tempfile.mkdtemp(prefix="sm-test-"))
    for lang, items in (("en", en or {}), ("nl", nl or {})):
        d = tmp / "docs" / lang / "blog" / "posts"
        d.mkdir(parents=True)
        for slug, title in items.items():
            post(d, slug, title)
    return tmp


def main() -> int:
    # 1. parity with pymdownx default slugifier
    f = sm.slugifier()
    check("parity welkom", f("Welkom op de blog", "-") == "welkom-op-de-blog")
    check("parity scrum-week", f("Start van de Scrum-week", "-") == "start-van-de-scrum-week")
    check("parity 1 april", f("1 april", "-") == "1-april")

    # 2. mirrored pair -> both directions mapped (URLs use Y/M/D segments,
    #    matching the blog plugin's real route format). Mirrors share the
    #    FILENAME (translator's sync key); only titles/slugs differ.
    root = fresh(
        {"welcome-to-the-blog": ("Welcome to the blog",)},
        {"welcome-to-the-blog": ("Welkom op de blog",)},
    )
    m = sm.build_map(root)
    check("en->nl entry",
          m.get("/blog/2026/01/01/welcome-to-the-blog/") == "/nl/blog/2026/01/01/welkom-op-de-blog/",
          str(m))
    check("reverse entry",
          m.get("/nl/blog/2026/01/01/welkom-op-de-blog/") == "/blog/2026/01/01/welcome-to-the-blog/")

    # 3. unmirrored posts excluded; drafts excluded even if mirrored name exists
    root = fresh(
        {"only-en": ("Only EN",), "pair": ("Pair",)},
        {"solo-nl": ("Solo NL",), "pair": ("Paar",)},
    )
    post(root / "docs/en/blog/posts", "drafty", "Drafty", draft=True)
    post(root / "docs/nl/blog/posts", "drafty", "Concept", draft=True)
    m = sm.build_map(root)
    check("pair mapped", m.get("/blog/2026/01/01/pair/") == "/nl/blog/2026/01/01/paar/", str(m))
    check("unmirrored excluded", "/blog/2026/01/01/only-en/" not in m and "/nl/blog/2026/01/01/solo-nl/" not in m)
    check("drafts excluded from map", not any("drafty" in k for k in m))

    # 4. write_site emits valid JSON at given path and merges on second call
    out = root / "site" / "slugmap.json"
    sm.write_site(root, out)
    data = json.loads(out.read_text(encoding="utf-8"))
    check("json written + shape", isinstance(data, dict) and "/blog/2026/01/01/pair/" in data)

    print(f"\n{PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
