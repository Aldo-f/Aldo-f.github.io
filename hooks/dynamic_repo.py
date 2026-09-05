"""MkDocs hook: dynamic repo links based on current page path.

Injects JavaScript to fix repository links after page load.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Map path prefixes to their source repositories
REPO_MAP = {
    # Multirepo imports
    "thuis/": ("https://github.com/Aldo-f/thuis", "Aldo-f/thuis"),
    "thuis-v3/": ("https://github.com/Aldo-f/thuis", "Aldo-f/thuis"),
    "thuis-v4/": ("https://github.com/Aldo-f/thuis", "Aldo-f/thuis"),
    "thuis-v5/": ("https://github.com/Aldo-f/thuis", "Aldo-f/thuis"),
    "clock/": ("https://github.com/Aldo-f/clock", "Aldo-f/clock"),
    "blanky/": ("https://gitlab.com/Aldo-f/blanky", "Aldo-f/blanky"),
    "blanky-v1/": ("https://gitlab.com/Aldo-f/blanky", "Aldo-f/blanky"),
    "opencode-multi-model-fallback/": ("https://github.com/Aldo-f/opencode-multi-model-fallback", "Aldo-f/opencode-multi-model-fallback"),
}

DEFAULT_REPO_URL = "https://github.com/Aldo-f/Aldo-f.github.io"
DEFAULT_REPO_NAME = "Aldo-f/Aldo-f.github.io"


def _find_repo(page_path: str) -> tuple[str, str]:
    """Find the repository URL and name for a given page path."""
    # Normalize path
    path = page_path.replace("\\", "/").lower()
    
    for prefix, (repo_url, repo_name) in REPO_MAP.items():
        if prefix in path:
            return repo_url, repo_name
    
    return DEFAULT_REPO_URL, DEFAULT_REPO_NAME


JS_CODE = """
(function() {
  'use strict';
  var path = window.location.pathname;
  var map = %s;
  var defaultUrl = %s;
  var defaultName = %s;
  
  var repoUrl = defaultUrl;
  var repoName = defaultName;
  
  for (var prefix in map) {
    if (path.indexOf(prefix) === 0 || path.indexOf('/' + prefix) !== -1) {
      repoUrl = map[prefix].url;
      repoName = map[prefix].name;
      break;
    }
  }
  
  // Fix the repository link
  var source = document.querySelector('[data-md-component="source"]');
  if (source) {
    var link = source.querySelector('a');
    var repoDiv = source.querySelector('.md-source__repository');
    if (link) link.href = repoUrl;
    if (repoDiv) repoDiv.textContent = repoName;
  }
})();
"""


def on_config(config, **kwargs):
    """Register the JavaScript file."""
    extra_js = list(config.get("extra_javascript") or [])
    js_name = "assets/javascripts/dynamic-repo.js"
    if js_name not in extra_js:
        extra_js.append(js_name)
    config["extra_javascript"] = extra_js
    return config


def on_post_build(config, **kwargs):
    """Write the JavaScript file with repo mappings."""
    site = Path(config.site_dir)
    js_path = site / "assets" / "javascripts" / "dynamic-repo.js"
    js_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Build the mapping object
    mapping = {}
    for prefix, (repo_url, repo_name) in REPO_MAP.items():
        mapping[prefix] = {"url": repo_url, "name": repo_name}
    
    js_content = JS_CODE % (
        repr(mapping),
        repr(DEFAULT_REPO_URL),
        repr(DEFAULT_REPO_NAME),
    )
    
    js_path.write_text(js_content, encoding="utf-8")
    print(f"dynamic-repo: wrote {js_path}", file=sys.stderr)
