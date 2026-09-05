"""MkDocs hook: decode HTML entities in mermaid code blocks."""

from __future__ import annotations

import re
import html as html_module


def on_page_content(html, page, config, files):
    """Decode HTML entities in mermaid code blocks."""
    if 'mermaid' not in html.lower():
        return html

    # Decode HTML entities in mermaid code blocks (e.g., <br/> -> <br/>)
    def decode_entities(match):
        code = match.group(1)
        decoded = html_module.unescape(code)
        return f'<pre class="mermaid"><code>{decoded}</code></pre>'

    html = re.sub(r'<pre class="mermaid"><code>(.*?)</code></pre>', decode_entities, html, flags=re.DOTALL)

    return html