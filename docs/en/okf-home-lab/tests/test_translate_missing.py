#!/usr/bin/env python3
"""RED tests for scripts/blog_translate.py (feature 003-blog-autotranslate).

Network-free: uses a FakeTranslator injected into the module's translate
functions. Run:  python3 tests/test_translate_missing.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import blog_translate as bt  # noqa: E402

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"PASS {name}")
    else:
        FAIL += 1
        print(f"FAIL {name}" + (f" — {detail}" if detail else ""))


class FakeTranslator:
    """Deterministic stand-in for the DeepL backend."""

    calls = 0

    def __call__(self, texts, source, target):
        type(self).calls += len(texts)
        out = []
        for t in texts:
            # simulate translation: prefix + swap obvious markers
            marker = "NL" if target == "EN" else "EN"
            out.append(f"[{marker}] {t.replace('zeester', 'star')}")
        return out


def write_post(dir_path: Path, slug: str, title: str, body: str,
               date="2026-01-01", cats=("General",), draft=False):
    cats_yaml = "".join(f"\n  - {c}" for c in cats)
    draft_line = "\ndraft: true" if draft else ""
    p = dir_path / f"{slug}.md"
    p.write_text(
        f"---\ntitle: {title}\ndate: {date}\ncategories:{cats_yaml}{draft_line}\n---\n\n{body}\n",
        encoding="utf-8",
    )
    return p


def fresh_env(en_posts: dict, nl_posts: dict) -> tuple:
    tmp = tempfile.mkdtemp(prefix="bt-test-")
    root = Path(tmp)
    en = root / "docs" / "en" / "blog" / "posts"
    nl = root / "docs" / "nl" / "blog" / "posts"
    en.mkdir(parents=True)
    nl.mkdir(parents=True)
    for slug, args in en_posts.items():
        write_post(en, slug, title=args[0], body=args[1])
    for slug, args in nl_posts.items():
        write_post(nl, slug, title=args[0], body=args[1])
    return root, en, nl


def main() -> int:
    tr = FakeTranslator()

    # 1. gap detection EN -> NL
    root, en, nl = fresh_env(
        {"hello": ("Hello", "Hello body zeester", "Hello body zeester")},
        {"hallo": ("Hallo", "Hallo body", "Hallo body")},
    )
    report = bt.fill_gaps(root, translator=tr, write=False)
    check("dry-run detects EN->NL gap",
          report.created == [("en", "nl", "hello"), ("nl", "en", "hallo")],
          f"got {report.created}")

    # 2. dry-run writes nothing
    check("dry-run creates no file", not (nl / "hello.md").exists())

    # 3. write mode creates translated file with preserved FM + provenance
    report = bt.fill_gaps(root, translator=tr, write=True)
    f = nl / "hello.md"
    check("write mode creates file", f.exists())
    text = f.read_text(encoding="utf-8")
    check("title translated", "[EN] Hello" in text)
    check("date preserved", "date: 2026-01-01" in text)
    check("categories preserved", "- General" in text)
    check("no draft flag added", "draft:" not in text)
    check("body translated", "[EN] Hello body star" in text)
    check("provenance marker present",
          "translated from `en/hello`" in text and "deepl" in text.lower())

    # 4. idempotence: second run is a no-op
    FakeTranslator.calls = 0
    report2 = bt.fill_gaps(root, translator=tr, write=True)
    check("re-run finds no gaps", report2.created == [])
    check("re-run makes zero API calls", FakeTranslator.calls == 0)

    # 5. drafts never propagate
    root2, en2, nl2 = fresh_env(
        {"secret": ("Secret", "body", "body")},
        {},
    )
    (en2 / "secret.md").write_text(
        (en2 / "secret.md").read_text().replace("---\n", "---\ndraft: true\n", 1)
        if not (en2 / "secret.md").read_text().startswith("---\ndraft")
        else (en2 / "secret.md").read_text()
    )
    # simpler: rewrite explicitly as draft
    (en2 / "secret.md").write_text(
        "---\ntitle: Secret\ndate: 2026-01-01\ncategories:\n  - General\ndraft: true\n---\n\nbody\n",
        encoding="utf-8")
    rep3 = bt.fill_gaps(root2, translator=tr, write=False)
    check("drafts skipped", rep3.created == [] and not (nl2 / "secret.md").exists(),
          f"got {rep3.created}")

    # 6. code fences pass through untranslated
    root3, en3, nl3 = fresh_env(
        {"codey": ("Codey", "```\nzeester code\n```\n\nAfter zeester.", "")},
        {},
    )
    bt.fill_gaps(root3, translator=tr, write=True)
    t3 = (nl3 / "codey.md").read_text(encoding="utf-8")
    check("code fence untouched", "```\nzeester code\n```" in t3 and "zeester code" in t3, t3)
    # FakeTranslator tags with the SOURCE lang + applies its word swap:
    # prose 'After zeester.' must become '[EN] After star.'
    check("prose around fence translated", "[EN] After star." in t3, t3)

    print(f"\n{PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
