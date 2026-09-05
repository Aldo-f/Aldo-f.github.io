"""MkDocs hook: writes a build timestamp file injected into the site footer.

Produces site/build-info.js exposing BUILD_TIME as a UTC ISO string (rounded
to the minute so the value is stable across reruns without CI cache invalidation).

Wired via `hooks:` in mkdocs.base.yml; runs on both EN and NL builds.
"""

from __future__ import annotations

import datetime
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
JS_NAME = "assets/javascripts/build-info.js"

_FOOTER_INJECT_JS = """\
(function () {
  'use strict';
  var raw = typeof BUILD_TIME !== 'undefined' ? BUILD_TIME : null;
  if (!raw) return;
  var d = new Date(raw);
  var formatted = d.toLocaleString(undefined, {
    year: 'numeric', month: 'short', day: '2-digit',
    hour: '2-digit', minute: '2-digit', timeZoneName: 'short'
  });
  var el = document.createElement('div');
  el.id = 'build-footer';
  el.style.cssText = 'font-size:0.75rem;color:#999;margin-top:4px;text-align:right;';
  el.textContent = 'Build: ' + formatted;
  var copyright = document.querySelector('.md-copyright');
  if (copyright) copyright.appendChild(el);
})();
"""


def on_post_build(*, config, **kwargs):
    site_dir = Path(config.site_dir)
    js_path = site_dir / JS_NAME
    js_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).replace(second=0, microsecond=0)
    js_path.write_text(
        f"BUILD_TIME = {now.isoformat(timespec='seconds')!r};",
        encoding="utf-8",
    )
    print(f"build-info: wrote {js_path.relative_to(site_dir)} = {now.isoformat()}")


def on_config(config, **kwargs):
    extra_js = list(config.get("extra_javascript") or [])
    if JS_NAME not in extra_js:
        extra_js.append(JS_NAME)
    config["extra_javascript"] = extra_js
    # Inject footer script here so it runs immediately (not deferred) and
    # stamps the footer before the browser paints the page.
    extra_js.append(_FOOTER_INJECT_JS)
    config["extra_javascript"] = extra_js
    return config
