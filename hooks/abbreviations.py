"""MkDocs hook for the abbreviations cheatsheet.

The hook reads ``abbreviations/*.md``, validates entries, writes
``site/assets/data/abbreviations.json``, and injects the same data into the
``Abbreviations Cheatsheet`` page so the client-side UI can filter and search.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ABBREVIATIONS_DIR = Path("abbreviations")
OUTPUT_FILE = "assets/data/abbreviations.json"
PAGE_TITLE = "Abbreviations Cheatsheet"

_abbreviations: list[dict[str, Any]] = []


def _parse_abbreviation(path: Path) -> dict[str, Any] | None:
    """Parse one abbreviation file; return ``None`` for the unfilled template."""
    text = path.read_text(encoding="utf-8")
    match = re.match(
        r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$",
        text,
        re.DOTALL,
    )
    if not match:
        print(f"⚠️  {path.name}: Missing or malformed front-matter")
        return None

    front_matter, body = match.groups()
    abbreviation_match = re.search(
        r"^abbreviation:\s*(\S+)\s*$", front_matter, re.MULTILINE | re.I
    )
    if not abbreviation_match:
        print(f"⚠️  {path.name}: Missing 'abbreviation:' in front-matter")
        return None

    abbreviation = abbreviation_match.group(1).upper()
    if abbreviation == "NEW_ABBREVIATION":
        return None

    answers: list[dict[str, Any]] = []
    for section in re.split(r"(?m)^##\s+", body):
        section = section.strip()
        if not section:
            continue

        title_match = re.match(r"(.+?)\s*\n", section)
        title = title_match.group(1).strip() if title_match else section
        category_match = re.search(
            r"\*\*Category:\*\*\s*(.+?)(?:\r?\n|$)",
            section,
            re.I | re.DOTALL,
        )
        definition_match = re.search(
            r"\*\*Definition:\*\*\s*(.+?)(?:\r?\n\r?\n|\Z)",
            section,
            re.I | re.DOTALL,
        )
        if not title:
            print(f"⚠️  {path.name}: Section missing title")
            continue
        if not category_match:
            print(f"⚠️  {path.name}: Section '{title}' missing 'Category:'")
            continue
        if not definition_match:
            print(f"⚠️  {path.name}: Section '{title}' missing 'Definition:'")
            continue

        categories = [
            category.strip()
            for category in category_match.group(1).split(",")
            if category.strip()
        ]
        answers.append(
            {
                "title": title,
                "categories": categories,
                "definition": definition_match.group(1).strip(),
            }
        )

    if not answers:
        print(f"⚠️  {path.name}: No valid answers found")
        return None
    return {"abbreviation": abbreviation, "answers": answers}


def _load_abbreviations() -> list[dict[str, Any]]:
    """Load and validate all abbreviation files from the repository root."""
    entries: list[dict[str, Any]] = []
    for source in sorted(ABBREVIATIONS_DIR.glob("*.md")):
        entry = _parse_abbreviation(source)
        if entry is not None:
            entries.append(entry)
    entries.sort(key=lambda entry: entry["abbreviation"].casefold())
    return entries


def on_config(config: Any) -> Any:
    """Load entries before pages are rendered."""
    global _abbreviations
    _abbreviations = _load_abbreviations()
    print(f"📚 Loaded {len(_abbreviations)} abbreviation(s)")
    return config


def on_page_markdown(markdown: str, page: Any, config: Any, files: Any) -> str:
    """Inject the build-time data into the cheatsheet page."""
    if page.meta.get("title") == PAGE_TITLE:
        data = json.dumps(_abbreviations, ensure_ascii=False)
        assets = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:ital,wght@0,400;0,500;1,400&family=Roboto:wght@300;400;500;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<link rel="stylesheet" href="/assets/css/abbreviations.css">
<script src="/assets/javascripts/abbreviations.js"></script>
"""
        return f"<script>window.ABBREVIATIONS = {data};</script>\n{assets}{markdown}"
    return markdown


def on_post_build(*, config: Any, **kwargs: Any) -> None:
    """Write the generated JSON into the MkDocs output directory."""
    site_dir = Path(config.site_dir)
    output_path = site_dir / OUTPUT_FILE
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(_abbreviations, indent=2), encoding="utf-8")
    print(f"✅ Wrote {len(_abbreviations)} abbreviations to {OUTPUT_FILE}")
    # Copy client-side assets so the page renders
    for src, dst_name in [
        ("assets/js/abbreviations.js", "assets/javascripts/abbreviations.js"),
        ("assets/css/abbreviations.css", "assets/css/abbreviations.css"),
    ]:
        src_path = Path(src)
        if src_path.exists():
            dst_path = site_dir / dst_name
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            dst_path.write_text(src_path.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"✅ Copied {src} -> {dst_path}")
