"""MkDocs hook: dynamic repo links based on current page path.

Fetches and displays star/fork counts from GitHub/GitLab API.
"""

from __future__ import annotations

import sys
import json
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


def _get_js() -> str:
    """Generate the JavaScript code for dynamic repo links."""
    # Build mapping as JSON
    mapping = {}
    for prefix, (repo_url, repo_name) in REPO_MAP.items():
        mapping[prefix] = {"url": repo_url, "name": repo_name}
    
    js = """(function() {
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
  
  function updateRepoSource() {
    var sources = document.querySelectorAll('[data-md-component="source"]');
    sources.forEach(function(source) {
      var link = source.querySelector('a');
      var repoDiv = source.querySelector('.md-source__repository');
      if (link) link.href = repoUrl;
      if (repoDiv) {
        repoDiv.textContent = repoName;
        // Fetch and append stats
        fetchRepoStats(repoUrl, repoDiv);
      }
    });
  }
  
  function fetchRepoStats(url, element) {
    var api_url;
    var is_gitlab = url.includes('gitlab.com');
    var is_github = url.includes('github.com');
    
    if (is_github) {
      var match = url.match(/github\\.com\\/(.+)\\/(.+)/);
      if (match) {
        api_url = 'https://api.github.com/repos/' + match[1] + '/' + match[2];
        fetch(api_url)
          .then(function(r) { return r.json(); })
          .then(function(data) {
            var stats = [];
            if (data.stargazers_count) stats.push('⭐ ' + formatNumber(data.stargazers_count));
            if (data.forks_count) stats.push('🍴 ' + formatNumber(data.forks_count));
            if (stats.length > 0) {
              element.innerHTML = repoName + ' <span class="repo-stats">' + stats.join(' ') + '</span>';
            }
          })
          .catch(function() {});
      }
    } else if (is_gitlab) {
      var match = url.match(/gitlab\\.com\\/(.+)\\/(.+)/);
      if (match) {
        api_url = 'https://gitlab.com/api/v4/projects/' + match[1] + '%2F' + match[2];
        fetch(api_url)
          .then(function(r) { return r.json(); })
          .then(function(data) {
            var stats = [];
            if (data.star_count) stats.push('⭐ ' + formatNumber(data.star_count));
            if (data.forks_count) stats.push('🍴 ' + formatNumber(data.forks_count));
            if (stats.length > 0) {
              element.innerHTML = repoName + ' <span class="repo-stats">' + stats.join(' ') + '</span>';
            }
          })
          .catch(function() {});
      }
    }
  }
  
  function formatNumber(n) {
    if (n >= 1000) {
      return (n / 1000).toFixed(1) + 'k';
    }
    return n.toString();
  }
  
  // Run immediately and also on DOMContentLoaded for safety
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateRepoSource);
  } else {
    updateRepoSource();
  }
})();
""" % (json.dumps(mapping), json.dumps(DEFAULT_REPO_URL), json.dumps(DEFAULT_REPO_NAME))
    return js


def on_config(config, **kwargs):
    """Register the JavaScript file."""
    extra_js = list(config.get("extra_javascript") or [])
    js_name = "assets/javascripts/dynamic-repo.js"
    if js_name not in extra_js:
        extra_js.append(js_name)
    config["extra_javascript"] = extra_js
    return config


def on_post_build(config, **kwargs):
    """Write the JavaScript file."""
    site = Path(config.site_dir)
    js_path = site / "assets" / "javascripts" / "dynamic-repo.js"
    js_path.parent.mkdir(parents=True, exist_ok=True)
    js_content = _get_js()
    js_path.write_text(js_content, encoding="utf-8")
    print(f"dynamic-repo: wrote {js_path}", file=sys.stderr)
