#!/usr/bin/env python3
"""Generate Projects pages from mkdocs.en.yml nav_repos — ONE big SOT object."""
# Add a new repo: just add one line to PROJECTS (name, display, desc, doc_link, source_type)
# All rendering logic is generic; no if/elif per repo.

from __future__ import annotations
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MKDOCS_EN = REPO_ROOT / "mkdocs.en.yml"
INDEX_MD = REPO_ROOT / "docs" / "en" / "index.md"
PROJECTS_MD = REPO_ROOT / "docs" / "en" / "projects.md"

# DEFAULT PROJECT ORDER — consistent across all locations (menu, homepage, projects-page)
# Edit this list to change the canonical order; entries not listed appear at the end in nav_repos order.
PROJECT_ORDER = [
    "thuis",
    "clock",
    "blanky",
    "blanky-v1",
    "opencode-multi-model-fallback",
    "vaultwarden-backup",
    "radio-community",
    "neo-brutalist-home",
]

# SINGLE SOT OBJECT — edit HERE to add/update any repo
PROJECTS = {
    "thuis": {
        "display": "Thuis",
        "desc": "VRT MAX video downloader with automatic auth (v3→v5)",
        "doc": "thuis/docs/index.md",
        "docs_md": "[Latest](thuis/docs/index.md) · [All versions](projects.md)",
        "project_md": "full",
        "versions": [
            ("main", "Thuis main", "thuis/docs/index.md", "`main` branch"),
            ("v5", "Thuis v5", "thuis-v5/website/docs/intro.md", "`v5/main`"),
            ("v4", "Thuis v4", "thuis-v4/website/docs/intro.md", "tag `v4.1.0`"),
            ("v3", "Thuis v3", "thuis-v3/docs/index.md", "tag `v3.0.0`"),
        ],
        "source_url": None,
    },
    "clock": {
        "display": "Clock",
        "desc": "React clock studio (13 clocks + AI customizer)",
        "doc": "clock/docs/index.md",
        "docs_md": "[Docs](clock/docs/index.md)",
        "project_md": "full",
        "source_url": "https://github.com/Aldo-f/clock",
    },
    "blanky": {
        "display": "Blanky",
        "desc": "External link opener library",
        "doc": "blanky/docs/index.md",
        "docs_md": "[Docs](blanky/docs/index.md)",
        "project_md": "full",
        "source_url": "https://gitlab.com/Aldo-f/blanky",
    },
    "blanky-v1": {
        "display": "Blanky v1",
        "desc": "Legacy Blanky version",
        "doc": "blanky-v1/docs/index.md",
        "docs_md": "[Docs](blanky-v1/docs/index.md)",
        "project_md": "full",
        "source_url": "https://gitlab.com/Aldo-f/blanky",
    },
    "opencode-multi-model-fallback": {
        "display": "OpenCode Multi-Model Fallback",
        "desc": "Auto-switches fallback models on rate limits",
        "doc": "opencode-multi-model-fallback/docs/index.md",
        "docs_md": "[Docs](opencode-multi-model-fallback/docs/index.md)",
        "project_md": "full",
        "install_note": "npm install @aldo-f/opencode-multi-model-fallback",
        "source_url": "https://github.com/Aldo-f/opencode-multi-model-fallback",
    },
    "vaultwarden-backup": {
        "display": "Vaultwarden Backup",
        "desc": "Automated cloud backup",
        "doc": "vaultwarden-backup/docs/index.md",
        "docs_md": "[Docs](vaultwarden-backup/docs/index.md)",
        "project_md": "full",
        "source_url": "https://github.com/Aldo-f/07-security-vaultwarden-backup",
    },
    "radio-community": {
        "display": "Radio Community",
        "desc": "Democratic radio with voting playlists",
        "doc": "radio-community/index.md",
        "docs_md": "[Docs](radio-community/index.md)",
        "project_md": "full",
        "source_url": "https://github.com/Aldo-f/radio-community",
    },
    "neo-brutalist-home": {
        "display": "Neo-Brutalist Home",
        "desc": "Dashboard design exploration",
        "doc": "",
        "docs_md": "[GitHub](https://github.com/Aldo-f/Aldo-f.github.io)",
        "project_md": "short",
        "source_url": "https://github.com/Aldo-f/Aldo-f.github.io",
    },
}

# Skip sub-items (thuis-v3/v4/v5) in index table — handled under Thuis
SKIP_INDEX = {"thuis-v3", "thuis-v4", "thuis-v5"}


def parse_nav_repos() -> list[str]:
    content = MKDOCS_EN.read_text(encoding="utf-8")
    data = yaml.safe_load(content)
    from_nav = []
    for p in data.get("plugins") or []:
        if isinstance(p, dict) and "multirepo" in p:
            for e in p["multirepo"].get("nav_repos", []):
                n = e.get("name", "")
                if n and n not in SKIP_INDEX:
                    from_nav.append(n)
    # Default order first (new items to top — prepend if needed), then nav order
    ordered = [r for r in PROJECT_ORDER if r in from_nav]
    for r in from_nav:
        if r not in ordered:
            ordered.append(r)
    return ordered


def make_index_table(repos: list[str]) -> str:
    lines = [
        "## Projects\n",
        "| Project | What it is | Docs |",
        "|---------|------------|------|",
    ]
    for r in repos:
        info = PROJECTS.get(r)
        if not info:
            lines.append(f"| **{r}** |  |  |")
            continue
        docs = info.get("docs_md", "")
        lines.append(f"| **{info['display']}** | {info['desc']} | {docs} |")
    return "\n".join(lines) + "\n"


def make_projects_md(repos: list[str]) -> str:
    lines = ["# Projects\n", "A quick index of everything documented on this hub.\n"]
    for r in repos:
        info = PROJECTS.get(r)
        if not info:
            lines.append(f"\n## {r}\n\n- Source: [repo]({r})\n")
            continue
        if info.get("project_md") == "full":
            lines.append(f"\n## {info['display']}\n\n{info['desc']}.\n")
            doc = info.get("doc")
            if doc:
                lines.append(f"- Docs: [{info['display']}]({doc})")
            src = info.get("source_url")
            if src:
                lines.append(f"- Source: [{src}]({src})")
            if info.get("install_note"):
                lines.append(f"- Install: `{info['install_note']}`")
            if r == "thuis":
                lines.append("\n| Version | Docs | Source ref |")
                lines.append("|---------|------|------------|")
                for ver, disp, ld, ref in info.get("versions", []):
                    lines.append(f"| {ver} | [{disp}]({ld}) | {ref} |")
                if src:  # Only show Source for Thuis if URL exists
                    lines.append(f"\nSource: [{src}]({src})\n")
            lines.append("")
        elif info.get("project_md") == "short":
            lines.append(f"\n## {info['display']}\n\n{info['desc']}.\n")
            src = info.get("source_url")
            if src:
                lines.append(f"- Source: part of [this hub's repos]({src})")
    lines.append("\n## Home lab\n")
    lines.append(
        "The infrastructure behind all of this — two Raspberry Pis, Ansible-managed\n"
    )
    lines.append("services, Traefik reverse proxy — is described in\n")
    lines.append("[Home-lab documentation](home-lab-docs.md).\n")
    return "\n".join(lines)


def main() -> int:
    repos = parse_nav_repos()
    print(f"SOT: {len(repos)} repos from nav_repos")

    # Generate content
    index_table = make_index_table(repos)
    projects_content = make_projects_md(repos)

    # Update index.md - replace the Projects table section
    content = INDEX_MD.read_text(encoding="utf-8")

    # Find the Projects section and replace it
    start = content.find("## Projects\n")
    if start == -1:
        print("❌ Could not find '## Projects' in index.md")
        return 1

    # Find next major section after Projects (## heading or end of file)
    # Look for next heading at same level
    after_projects = content[start + len("## Projects\n") :]
    next_heading = after_projects.find("\n## ")
    if next_heading != -1:
        end = start + len("## Projects\n") + next_heading
    else:
        end = len(content)

    # Replace the section
    new_content = content[:start] + index_table + content[end:]
    INDEX_MD.write_text(new_content, encoding="utf-8")
    print("✅ Updated docs/en/index.md")

    PROJECTS_MD.write_text(projects_content, encoding="utf-8")
    print("✅ Updated docs/en/projects.md")
    print("\nDone! Rebuild with: mkdocs build -f mkdocs.en.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
