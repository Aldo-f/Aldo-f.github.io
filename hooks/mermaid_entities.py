"""MkDocs hook: decode HTML entities in mermaid code blocks and initialize rendering."""

from __future__ import annotations

import re
import html as html_module

MERMAID_INIT_JS = """
(function() {
  'use strict';
  
  function initMermaid() {
    if (typeof mermaid === 'undefined') {
      setTimeout(initMermaid, 50);
      return;
    }
    
    mermaid.initialize({
      startOnLoad: true,
      theme: 'default',
      securityLevel: 'loose'
    });
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMermaid);
  } else {
    initMermaid();
  }
})();
"""

MERMAID_JS_URL = "https://cdn.jsdelivr.net/npm/mermaid@10.4.0/dist/mermaid.min.js"


def on_page_content(html, page, config, files):
    """Decode HTML entities in mermaid code blocks and inject mermaid scripts."""
    if 'mermaid' not in html.lower():
        return html

    # Decode HTML entities in mermaid code blocks (e.g., <br/> -> <br/>)
    def decode_entities(match):
        code = match.group(1)
        decoded = html_module.unescape(code)
        return f'<pre class="mermaid">{decoded}</pre>'

    html = re.sub(r'<pre class="mermaid"><code>(.*?)</code></pre>', decode_entities, html, flags=re.DOTALL)
    
    # Also handle the newer format with <code> tags
    html = re.sub(r'<pre class="mermaid">\s*(.*?)\s*</pre>', 
                  lambda m: f'<pre class="mermaid">{html_module.unescape(m.group(1))}</pre>', 
                  html, flags=re.DOTALL)

    # Add mermaid JS and initialization if not present
    if MERMAID_JS_URL not in html:
        html = html.replace('</body>', 
                           f'<script src="{MERMAID_JS_URL}"></script>\n{MERMAID_INIT_JS}\n  </body>')
    elif 'mermaid.initialize' not in html:
        html = html.replace('</body>', 
                           f'{MERMAID_INIT_JS}\n  </body>')

    return html


def on_config(config, **kwargs):
    """Ensure mermaid CSS is included if needed."""
    extra_css = list(config.get("extra_css") or [])
    # Mermaid2 plugin handles its own CSS, so we don't need to add anything here
    config["extra_css"] = extra_css
    return config


def on_post_build(config):
    """Log completion."""
    print("mermaid hook: processed all pages")
