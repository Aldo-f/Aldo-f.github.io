# MkDocs hook URL reconstruction — pitfall from related_posts.py

When a MkDocs hook injects links by computing URLs from raw file paths (e.g. `docs/nl/blog/posts/foo.md` → `/nl/blog/2019/04/08/foo/`), the file path does NOT contain the blog plugin's date slug, language prefix, or slug transformation. The hook must either use MkDocs' own page/url objects (if available in hook context) or document that file-path math will 404.

## Rules

1. **Never claim a hook URL fix is verified without site verification**: Read the built `site/` HTML — file-path arithmetic is not enough to determine correct URLs.

2. **Translation labels in hooks**: Use `config.docs_dir.lower()` to detect language and show "See also" (EN) vs "Lees ook" (NL) — never hardcode.

3. **INHERIT replaces, not merges**: When using `INHERIT: mkdocs.base.yml`, plugin lists are replaced entirely. NL and EN configs must declare `blog:` with `blog_dir` explicitly if needed.

## Pitfall: relative_to() path math

```python
blog_base = Path('docs/nl/blog/posts')
rel_url = '/' + path.relative_to(blog_base.parent.parent).as_posix()
# Results in /blog/posts/foo.md — missing language prefix and date slug!
```

## Better approach

Hooks have access to `page.url` in `on_page_markdown()` — use it directly instead of computing from file paths.
