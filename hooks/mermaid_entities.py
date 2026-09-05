"""MkDocs hook: decode HTML entities in mermaid code blocks and initialize rendering."""

from __future__ import annotations

import re
import html as html_module

MERMAID_INIT_JS = """
<script>
(function() {
  'use strict';
  
  // Initialize mermaid once it's loaded
  function initMermaid() {
    if (typeof mermaid === 'undefined') {
      setTimeout(initMermaid, 100);
      return;
    }
    
    mermaid.initialize({
      startOnLoad: false,
      theme: 'default',
      securityLevel: 'loose'
    });
    
    // Render all mermaid diagrams
    const mermaidElements = document.querySelectorAll('.mermaid');
    mermaidElements.forEach(function(element) {
      const id = 'mermaid-' + Math.random().toString(36).substr(2, 9);
      mermaid.render(id, element.textContent).then(function(svgCode) {
        const wrapper = document.createElement('div');
        wrapper.className = 'mermaid-svg';
        wrapper.innerHTML = svgCode;
        element.parentNode.replaceChild(wrapper, element);
      }).catch(function(err) {
        console.error('Mermaid render error:', err);
      });
    });
  }
  
  // Wait for DOM and mermaid to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMermaid);
  } else {
    initMermaid();
  }
})();
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
        return f'<pre class="mermaid">{decoded}</pre>'
    
    output = re.sub(r'<pre class="mermaid">(.*?)</pre>', decode_entities, output, flags=re.DOTALL)

    # Add mermaid JS and init script if not present
    if MERMAID_JS_URL not in output:
        output = output.replace('</body>', 
                               f'<script src="{MERMAID_JS_URL}"></script>\n{MERMAID_INIT_JS}\n  </body>')
    
    return output


def on_post_build(config):
    """Log completion."""
    print("mermaid hook: complete")
