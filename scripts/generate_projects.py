#!/usr/bin/env python3
"""Generate Projects pages from mkdocs.en.yml nav_repos — single source of truth."""

from __future__ import annotations
import re
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MKDOCS_EN = REPO_ROOT / "mkdocs.en.yml"
INDEX_MD = REPO_ROOT / "docs" / "en" / "index.md"
PROJECTS_MD = REPO_ROOT / "docs" / "en" / "projects.md"


def parse_nav_repos() -> list[dict]:
    """Extract nav_repos entries from mkdocs.en.yml (SOT)."""
    content = MKDOCS_EN.read_text(encoding="utf-8")
    data = yaml.safe_load(content)

    nav_repos = []
    for plugin in data.get("plugins", []):
        if isinstance(plugin, dict) and "multirepo" in plugin:
            for entry in plugin["multirepo"].get("nav_repos", []):
                name = entry.get("name", "")
                import_url = entry.get("import_url", "")
                if name and import_url:
                    nav_repos.append({"name": name, "import_url": import_url})
    return nav_repos


def repo_to_doc_link(name: str, import_url: str) -> str:
    """Convert repo name and import_url to a doc link path."""
    # Special cases for versioned docs
    if name == "thuis":
        return "thuis/docs/index.md"
    elif name == "thuis-v3":
        return "thuis-v3/docs/index.md"
    elif name == "thuis-v4":
        return "thuis-v4/website/docs/intro.md"
    elif name == "thuis-v5":
        return "thuis-v5/website/docs/intro.md"
    elif name == "clock":
        return "clock/docs/index.md"
    elif name == "blanky":
        return "blanky/docs/index.md"
    elif name == "blanky-v1":
        return "blanky-v1/docs/index.md"
    elif name == "radio-community":
        return "radio-community/index.md"
    elif name == "opencode-multi-model-fallback":
        return "opencode-multi-model-fallback/docs/index.md"
    elif name == "vaultwarden-backup":
        return "vaultwarden-backup/docs/index.md"
    elif name == "neo-brutalist-home":
        return ""  # No separate docs, part of hub
    else:
        # Default: {name}/docs/index.md
        return f"{name}/docs/index.md"


def repo_to_display_name(name: str) -> str:
    """Convert repo name to display name."""
    mappings = {
        "thuis": "Thuis",
        "thuis-v3": "Thuis v3",
        "thuis-v4": "Thuis v4",
        "thuis-v5": "Thuis v5",
        "clock": "Clock",
        "blanky": "Blanky",
        "blanky-v1": "Blanky v1",
        "radio-community": "Radio Community",
        "opencode-multi-model-fallback": "OpenCode Multi-Model Fallback",
        "vaultwarden-backup": "Vaultwarden Backup",
        "neo-brutalist-home": "Neo-Brutalist Home",
    }
    return mappings.get(name, name.replace("-", " ").title())


def repo_to_source_url(import_url: str) -> str:
    """Extract source URL from import_url."""
    # Remove branch/docs_dir params
    base = import_url.split("?")[0]
    if base.endswith(".git"):
        base = base[:-4]
    return base


def generate_index_table(nav_repos: list[dict]) -> str:
    """Generate the Projects table for index.md (SOT: nav_repos)."""
    lines = [
        "## Projects\n",
        "| Project | What it is | Docs |",
        "|---------|------------|------|",
    ]

    for entry in nav_repos:
        name = entry["name"]
        import_url = entry["import_url"]
        display = repo_to_display_name(name)
        doc_link = repo_to_doc_link(name, import_url)
        source_url = repo_to_source_url(import_url)

        if name == "clock":
            desc = "A React clock studio: 13 hand-built clocks plus an AI customizer"
        elif name == "thuis":
            desc = "VRT MAX video downloader with automatic authentication (v3 → v5)"
        elif name == "radio-community":
            desc = "Democratic internet radio with voting-based playlists"
        elif name == "neo-brutalist-home":
            desc = "Dashboard design exploration"
        elif name == "opencode-multi-model-fallback":
            desc = "OpenCode plugin that automatically switches through a hierarchy of fallback models when rate limits are hit"
        elif name == "blanky":
            desc = "External link opener library"
        elif name == "blanky-v1":
            desc = "Legacy version of Blanky"
        elif name == "vaultwarden-backup":
            desc = "Automated Vaultwarden backup to cloud storage"
        else:
            desc = ""

        # Versioned entries (thuis-v3/v4/v5, blanky-v1) are sub-items, not top-level rows
        if name.startswith("thuis-v"):
            continue

        if doc_link:
            docs_md = f"[Docs]({doc_link})"
        else:
            docs_md = ""

        if name == "thuis":
            docs_md = f"[Latest]({doc_link}) · [All versions](projects.md)"
        elif name == "neo-brutalist-home":
            docs_md = f"[GitHub]({source_url})"

        lines.append(f"| **{display}** | {desc} | {docs_md} |")

    return "\n".join(lines) + "\n"


def generate_projects_md(nav_repos: list[dict]) -> str:
    """Generate the full projects.md content."""
    lines = [
        "# Projects\n",
        "A quick index of everything documented on this hub.\n",
    ]

    for entry in nav_repos:
        name = entry["name"]
        import_url = entry["import_url"]
        display = repo_to_display_name(name)
        doc_link = repo_to_doc_link(name, import_url)
        source_url = repo_to_source_url(import_url)

        if name == "clock":
            lines.extend(
                [
                    "## Clock — *Clocky*\n",
                    "A React clock studio with 13 hand-built clocks (marble run, nixie tubes,\n"
                    "split-flap, game of life, …) and an AI customizer backed by a configurable\n"
                    "provider waterfall.\n",
                    f"- Docs: [Clock]({doc_link})",
                    f"- Source: [{source_url}]({source_url})\n",
                ]
            )
        elif name == "thuis":
            lines.extend(
                [
                    "## Thuis\n",
                    "VRT MAX video downloader with automatic authentication. The hub tracks its\n"
                    "documentation across major versions:\n",
                    "",
                    "| Version | Docs | Source ref |",
                    "|---------|------|------------|",
                ]
            )
            # Thuis versions
            thuis_versions = [
                ("main", "Thuis main", "thuis/docs/index.md", "`main` branch"),
                (
                    "v5",
                    "Thuis v5",
                    "thuis-v5/website/docs/intro.md",
                    "`v5/main` branch",
                ),
                ("v4", "Thuis v4", "thuis-v4/website/docs/intro.md", "tag `v4.1.0`"),
                ("v3", "Thuis v3", "thuis-v3/docs/index.md", "tag `v3.0.0`"),
            ]
            for ver_name, ver_display, ver_doc, ver_ref in thuis_versions:
                lines.append(f"| {ver_name} | [{ver_display}]({ver_doc}) | {ver_ref} |")
            lines.extend(["", f"Source: [{source_url}]({source_url})\n"])
        elif name == "radio-community":
            lines.extend(
                [
                    "## Radio Community\n",
                    "Democratic internet radio: communities vote on the playlist, streams are\n"
                    "served through Icecast/Liquidsoap. Documentation covers the architecture,\n"
                    "API and streaming setup.\n",
                    f"- Docs: [Radio Community]({doc_link})\n",
                ]
            )
        elif name == "neo-brutalist-home":
            lines.extend(
                [
                    "## Neo-Brutalist Home\n",
                    "A dashboard design exploration in neo-brutalist style.\n",
                    f"- Source: part of [this hub's repos]({source_url})\n",
                ]
            )
        elif name == "opencode-multi-model-fallback":
            lines.extend(
                [
                    "## OpenCode Multi-Model Fallback\n",
                    "OpenCode plugin that automatically switches through a hierarchy of fallback models when rate limits are hit.\n",
                    f"- Docs: [opencode-multi-model-fallback]({doc_link})",
                    f"- Source: [{source_url}]({source_url})",
                    "- Install: `npm install @aldo-f/opencode-multi-model-fallback`\n",
                ]
            )
        elif name == "blanky":
            lines.extend(
                [
                    "## Blanky\n",
                    "External link opener library.\n",
                    f"- Docs: [Blanky]({doc_link})",
                    f"- Source: [{source_url}]({source_url})\n",
                ]
            )
        elif name == "blanky-v1":
            lines.extend(
                [
                    "## Blanky v1\n",
                    "Legacy version of Blanky.\n",
                    f"- Docs: [Blanky v1]({doc_link})",
                    f"- Source: [{source_url}]({source_url})\n",
                ]
            )
        elif name == "vaultwarden-backup":
            lines.extend(
                [
                    "## Vaultwarden Backup\n",
                    "Automated Vaultwarden backup to cloud storage.\n",
                    f"- Docs: [Vaultwarden Backup]({doc_link})",
                    f"- Source: [{source_url}]({source_url})\n",
                ]
            )
        elif name == "thuis-v3":
            pass  # Handled under Thuis
        elif name == "thuis-v4":
            pass  # Handled under Thuis
        elif name == "thuis-v5":
            pass  # Handled under Thuis
        else:
            lines.extend(
                [
                    f"## {display}\n",
                    f"- Docs: [{display}]({doc_link})",
                    f"- Source: [{source_url}]({source_url})\n",
                ]
            )

    lines.append("## Home lab\n")
    lines.append(
        "The infrastructure behind all of this — two Raspberry Pis, Ansible-managed\n"
    )
    lines.append("services, Traefik reverse proxy — is described in\n")
    lines.append("[Home-lab documentation](home-lab-docs.md).\n")

    return "\n".join(lines)


def update_file(
    path: Path, marker_start: str, marker_end: str, new_content: str
) -> bool:
    """Replace content between markers in a file. Returns True if changed."""
    content = path.read_text(encoding="utf-8")

    # Find markers
    start_idx = content.find(marker_start)
    end_idx = content.find(marker_end)

    if start_idx == -1 or end_idx == -1:
        print(f"❌ Markers not found in {path}")
        return False

    start_idx += len(marker_start)
    new_content_full = content[:start_idx] + "\n" + new_content + content[end_idx:]

    if new_content_full != content:
        path.write_text(new_content_full, encoding="utf-8")
        print(f"✅ Updated {path}")
        return True
    else:
        print(f"⏭️  No changes to {path}")
        return False


def main():
    nav_repos = parse_nav_repos()
    print(f"Found {len(nav_repos)} nav_repos entries")

    # Generate content
    index_table = generate_index_table(nav_repos)
    projects_content = generate_projects_md(nav_repos)

    # Update index.md - replace the Projects table section
    # We'll use a more targeted approach: replace from "## Projects" to next "## "
    index_content = INDEX_MD.read_text(encoding="utf-8")
    # Find the Projects section and replace it
    projects_start = index_content.find("## Projects\n")
    if projects_start == -1:
        print("❌ Could not find '## Projects' in index.md")
        return 1

    # Find next section after Projects
    next_section = index_content.find("\n## ", projects_start + 1)
    if next_section == -1:
        next_section = len(index_content)

    new_index = (
        index_content[:projects_start] + index_table + index_content[next_section:]
    )
    if new_index != index_content:
        INDEX_MD.write_text(new_index, encoding="utf-8")
        print("✅ Updated docs/en/index.md")
    else:
        print("⏭️  No changes to docs/en/index.md")

    # Update projects.md entirely (it's generated from nav_repos)
    PROJECTS_MD.write_text(projects_content, encoding="utf-8")
    print("✅ Updated docs/en/projects.md")

    print("\nDone! Rebuild with: mkdocs build -f mkdocs.en.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
