"""MkDocs hook: Mermaid diagram processor and lightbox integration.

This hook replaces the mermaid2 plugin which wasn't loading correctly.
It directly processes mermaid code blocks into inline SVG and adds zoom functionality.
"""

from __future__ import annotations

from pathlib import Path
import re

# Mermaid JS from CDN - load once per page
MERMAID_JS_URL = "https://cdn.jsdelivr.net/npm/mermaid@10.4.0/dist/mermaid.min.js"

_LIGHTBOX_ADDON_JS = """
(function() {
  'use strict';
  
  // Wait for mermaid to load, then render diagrams
  function initMermaid() {
    if (typeof mermaid === 'undefined') {
      setTimeout(initMermaid, 50);
      return;
    }
    
    mermaid.initialize({
      startOnLoad: false,
      theme: 'default',
      securityLevel: 'loose'
    });
    
    // Find all mermaid containers
    document.querySelectorAll('.mermaid-code').forEach(function(container) {
      // Decode HTML entities (e.g., &lt;br/&gt; -> <br/>)
      const text = container.textContent;
      const decoder = document.createElement('textarea');
      decoder.innerHTML = text;
      const code = decoder.value;
      const id = 'mermaid-' + Math.random().toString(36).substr(2, 9);
      
      mermaid.render(id, code).then(function(svgCode) {
        const wrapper = document.createElement('div');
        wrapper.className = 'mermaid-svg';
        wrapper.innerHTML = svgCode;
        container.parentNode.replaceChild(wrapper, container);
        
        // Add click handler for zoom
        wrapper.addEventListener('click', function(e) {
          if (e.target.closest('a') || e.target.closest('button')) return;
          e.preventDefault();
          openMermaidLightbox(svgCode);
        });
        wrapper.style.cursor = 'zoom-in';
      }).catch(function(err) {
        console.error('Mermaid render error:', err);
      });
    });
  }
  
  function openMermaidLightbox(svgCode) {
    var overlay = document.getElementById('mermaid-lightbox');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'mermaid-lightbox';
      overlay.className = 'mermaid-lightbox';
      overlay.innerHTML = '<button class="mermaid-close">&#10005;</button><div class="mermaid-content"></div>';
      document.body.appendChild(overlay);
      
      overlay.addEventListener('click', function(e) {
        if (e.target === overlay || e.target.closest('.mermaid-close')) {
          overlay.classList.remove('open');
        }
      });
      
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          var lb = document.getElementById('mermaid-lightbox');
          if (lb) lb.classList.remove('open');
        }
      });
    }
    
    overlay.querySelector('.mermaid-content').innerHTML = svgCode;
    overlay.classList.add('open');
  }
  
  // Start initialization
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMermaid);
  } else {
    initMermaid();
  }
})();
"""

_LIGHTBOX_CSS = """
.mermaid-svg {
  display: block;
  margin: 1rem auto;
  max-width: 100%;
  overflow: auto;
}

.mermaid-svg svg {
  max-width: 100%;
  height: auto;
}

.mermaid-lightbox {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.9);
  padding: 2rem;
  overflow: auto;
}

.mermaid-lightbox.open {
  display: flex;
  align-items: center;
  justify-content: center;
}

.mermaid-lightbox .mermaid-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 95vw;
  max-height: 90vh;
  overflow: auto;
}

.mermaid-lightbox .mermaid-content svg {
  max-width: 100%;
  height: auto;
}

.mermaid-close {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 10000;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  border-radius: 50%;
  width: 2.5rem;
  height: 2.5rem;
  font-size: 1.2rem;
  cursor: pointer;
}

.mermaid-close:hover {
  background: rgba(255, 255, 255, 0.3);
}
"""


def on_config(config, **kwargs):
    """Ensure mermaid JS is added to extra_javascript."""
    extra_js = list(config.get("extra_javascript") or [])
    if MERMAID_JS_URL not in extra_js:
        extra_js.append(MERMAID_JS_URL)
    config["extra_javascript"] = extra_js

    # Also add our addon script
    addon_js_name = "assets/javascripts/mermaid-lightbox-addon.js"
    if addon_js_name not in extra_js:
        extra_js.append(addon_js_name)
    config["extra_javascript"] = extra_js

    extra_css = list(config.get("extra_css") or [])
    lightbox_css = "assets/css/mermaid-lightbox.css"
    if lightbox_css not in extra_css:
        extra_css.append(lightbox_css)
    config["extra_css"] = extra_css
    return config


def on_post_build(config):
    """Write JS and CSS files."""
    site = Path(config.site_dir)

    # Write the addon JS
    js_path = site / "assets" / "javascripts" / "mermaid-lightbox-addon.js"
    js_path.parent.mkdir(parents=True, exist_ok=True)
    js_path.write_text(_LIGHTBOX_ADDON_JS, encoding="utf-8")

    # Write the CSS
    css_path = site / "assets" / "css" / "mermaid-lightbox.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(_LIGHTBOX_CSS, encoding="utf-8")

    print(f"mermaid-lightbox: wrote {js_path} + {css_path}")


def on_page_content(html, page, config, files):
    """Process mermaid code blocks and replace with containers."""
    if 'mermaid' not in html.lower():
        return html

    # Match both formats:
    # 1. <pre class="mermaid"><code>...</code></pre>
    # 2. <pre><code class="language-mermaid">...</code></pre>
    patterns = [
        (r'<pre class="mermaid"><code[^>]*>(.*?)</code></pre>', r'<div class="mermaid-code">\1</div>'),
        (r'<pre><code class="language-mermaid">(.*?)</code></pre>', r'<div class="mermaid-code">\1</div>'),
    ]

    for pattern, replacement in patterns:
        new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
        if new_html != html:
            print(f"[mermaid-lightbox] Applied pattern for page: {page.title if page else 'unknown'}")
        html = new_html

    return html
