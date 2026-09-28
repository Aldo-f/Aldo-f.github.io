"""MkDocs hook: inject 'Related blog posts' sidebar into project pages.

Scans blog posts for those with matching 'projects:' frontmatter,
and injects a styled HTML block into project pages at build time.
"""

from __future__ import annotations

import sys
import re
from pathlib import Path
from collections import defaultdict


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract frontmatter dict and body from markdown content."""
    if not content.startswith("---"):
        return {}, content
    match = re.match(r"^---\n(.*?)\n---\n?(.*)", content, re.DOTALL)
    if not match:
        return {}, content
    fm_text, body = match.groups()

    fm: dict = {}
    current_key = None
    current_list: list[str] = []

    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            if current_key:
                current_list.append(line[2:].strip().strip('"').strip("'"))
        elif ":" in line:
            if current_key and current_list:
                fm[current_key] = current_list
                current_list = []
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_key = key
            if value:
                fm[key] = value
                current_key = None

    if current_key and current_list:
        fm[current_key] = current_list

    return fm, body


def _find_blog_posts(docs_dir: Path) -> list[Path]:
    """Find all blog post files."""
    posts_dir = docs_dir / "blog" / "posts"
    if not posts_dir.exists():
        return []
    return sorted(posts_dir.glob("*.md"))


def _build_project_index(posts: list[Path]) -> dict[str, list[tuple[Path, dict]]]:
    """Build index mapping project names to blog posts."""
    project_index: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    for post_path in posts:
        content = post_path.read_text(encoding="utf-8")
        fm, _ = _parse_frontmatter(content)
        # Skip draft posts
        if fm.get("draft", "").lower() == "true":
            continue
        post_projects = [p.lower() for p in fm.get("projects", [])]
        for proj in post_projects:
            project_index[proj].append((post_path, fm))
    return dict(project_index)


def _get_blog_links(
    current_path: Path,
    project_index: dict,
    blog_base: Path,
) -> list[tuple[str, str]]:
    """Find blog posts related to current page's project."""
    # Extract project slug from path (e.g., "nocturna" from "nocturna/docs/index.md")
    parts = current_path.parts
    project_slug = None
    for i, part in enumerate(parts):
        if part in project_index and i > 0:
            project_slug = part
            break
    
    if not project_slug:
        return []
    
    results = []
    for post_path, fm in project_index.get(project_slug, []):
        if post_path.resolve() == current_path.resolve():
            continue
        title = fm.get("title", post_path.stem)
        # Generate published URL from frontmatter date and title slug
        # Source: docs/{lang}/blog/posts/YYYY-MM-DD-title.md
        # Published: /{lang}/blog/YYYY/MM/DD/slugified-title/
        date_str = fm.get("date", "")
        if date_str:
            date_match = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(date_str))
            if date_match:
                year, month, day = date_match.groups()
                slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
                # Detect language from path
                lang = "en"
                if "/nl/" in str(post_path) or "\\nl\\" in str(post_path):
                    lang = "nl"
                rel_url = f"/{lang}/blog/{year}/{int(month):02d}/{int(day):02d}/{slug}/"
            else:
                try:
                    rel_url = "/" + post_path.relative_to(blog_base.parent.parent).as_posix()
                except ValueError:
                    rel_url = "/" + post_path.name
        else:
            try:
                rel_url = "/" + post_path.relative_to(blog_base.parent.parent).as_posix()
            except ValueError:
                rel_url = "/" + post_path.name
        results.append((title, rel_url))
    
    return results[:5]  # Max 5 related posts


def on_config(config, **kwargs):
    """Pre-build the blog post index for reuse."""
    docs_dir = Path(config.docs_dir)
    blog_posts = _find_blog_posts(docs_dir)
    if blog_posts:
        project_index = _build_project_index(blog_posts)
        config._project_blog_index = project_index
        print(f"[PROJECT-BLOG] Found {len(blog_posts)} blog posts, indexed {len(project_index)} projects", file=sys.stderr)
    return config


def on_page_markdown(markdown: str, page, config, **kwargs):
    """Inject related blog posts into project pages."""
    src_path = getattr(getattr(page, "file", None), "src_path", None)
    abs_src_path = getattr(getattr(page, "file", None), "abs_src_path", None)

    # Only process project pages (projects.md or imported project docs)
    if not src_path or not abs_src_path:
        return markdown
    
    # Check if this is a project page
    is_project_page = (
        src_path == "projects.md" or 
        any(part in src_path for part in ["nocturna/docs/", "thuis/docs/", "clock/docs/", "blanky/docs/"])
    )
    
    if not is_project_page:
        return markdown
    
    project_index = getattr(config, "_project_blog_index", {})
    if not project_index:
        return markdown
    
    current_path = Path(abs_src_path).resolve()
    blog_base = Path(config.docs_dir) / "blog" / "posts"
    
    related = _get_blog_links(current_path, project_index, blog_base)
    
    if not related:
        return markdown
    
    # Determine language for label
    docs_dir_str = str(config.docs_dir).lower()
    section_label = "Related blog posts" if "/en/" in docs_dir_str else "Gerelateerde blogberichten"
    
    sections = []
    for title, url in related:
        sections.append(f'<a href="{url}">{title}</a>')
    
    related_html = f"""
<div class="project-blog-sidebar md-typeset">
<h2 id="related-blog-posts">{section_label}</h2>
<ul class="related-blog-list">
{" ".join(f'<li>{s}</li>' for s in sections)}
</ul>
</div>
"""
    
    # Insert after first H2 or at beginning
    if "<h1" in markdown:
        markdown = markdown.replace("<h1", related_html + "\n<h1", 1)
    else:
        markdown = related_html + "\n" + markdown
    
    print(
        f"[PROJECT-BLOG] Injected {len(related)} related blog posts into {src_path}",
        file=sys.stderr,
    )
    return markdown


def on_post_page(output: str, page, config, **kwargs):
    """Add CSS for project blog sidebar."""
    src_path = getattr(getattr(page, "file", None), "src_path", None)
    if not src_path:
        return output
    
    is_project_page = (
        src_path == "projects.md" or
        any(part in src_path for part in ["nocturna/docs/", "thuis/docs/", "clock/docs/", "blanky/docs/"])
    )
    
    if not is_project_page:
        return output
    
    css = """
<style>
.project-blog-sidebar {
  margin: 2rem 0;
  padding: 1.5rem;
  background: var(--md-default-fg-color--lightest);
  border-radius: 4px;
  border-left: 4px solid var(--md-accent-fg-color);
}
.project-blog-sidebar h2 {
  margin-top: 0;
  font-size: 1.1rem;
  text-transform: uppercase;
  color: var(--md-default-fg-color--medium);
}
.related-blog-list {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}
.related-blog-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--md-default-fg-color--light);
}
.related-blog-list li:last-child {
  border-bottom: none;
}
.related-blog-list a {
  color: var(--md-default-fg-color);
  text-decoration: none;
}
.related-blog-list a:hover {
  color: var(--md-accent-fg-color);
  text-decoration: underline;
}
</style>
"""
    return output + css
