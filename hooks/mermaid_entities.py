"""MkDocs hook: decode HTML entities in mermaid code blocks and initialize rendering."""

from __future__ import annotations

import re
import html as html_module

MERMAID_INIT_JS = """
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.4.0/dist/mermaid.esm.min.mjs';

mermaid.initialize({
  startOnLoad: true,
  theme: 'default',
  securityLevel: 'loose'
});
</script>
"""

MERMAID_JS_URL = "https://cdn.jsdelivr.net/npm/mermaid@10.4.0/dist/mermaid.min.js"


def on_page_content(html, page, config, files):
    """Decode HTML entities in mermaid code blocks."""
    if 'mermaid' not in html.lower():
        return html

    # Decode HTML entities in mermaid code blocks (e.g., <br/> -> <br/>)
    def decode_entities(match):
        code = match.group(1)
        decoded = html_module.unescape(code)
        # Convert <br/> to proper HTML for mermaid
        decoded = decoded.replace('<br/>', '<br>').replace('&lt;br/&gt;', '<br>')
        return f'<pre class="mermaid">{decoded}</pre>'

    # Handle multiple formats
    html = re.sub(r'<pre class="mermaid"><code>(.*?)</code></pre>', decode_entities, html, flags=re.DOTALL)
    html = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', decode_entities, html, flags=re.DOTALL)
    html = re.sub(r'<pre class="mermaid">\s*(.*?)\s*</pre>', 
                  lambda m: f'<pre class="mermaid">{html_module.unescape(m.group(1))}</pre>', 
                  html, flags=re.DOTALL)

    return html


def on_post_page(output, page, config, files=None):
    """Add mermaid JS after template rendering."""
    if 'mermaid' not in output.lower():
        return output

    # Decode any remaining HTML entities in mermaid blocks
    def decode_entities(match):
        code = match.group(1)
        decoded = html_module.unescape(code)
        decoded = decoded.replace('<br/>', '<br>').replace('&lt;br/&gt;', '<br>')
        return f'<pre class="mermaid">{decoded}</pre>'
    
    output = re.sub(r'<pre class="mermaid">(.*?)</pre>', decode_entities, output, flags=re.DOTALL)

    # Add mermaid ES module JS if not present
    if 'mermaid.esm.min.mjs' not in output:
        output = output.replace('</head>', 
                               f'{MERMAID_INIT_JS}\n  </head>')
    
    return output


def on_post_build(config):
    """Log completion."""
    print("mermaid hook: complete")
