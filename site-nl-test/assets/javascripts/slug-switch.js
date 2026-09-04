(function () {
  'use strict';
  var map = null;
  fetch('/slugmap.json', { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (j) { map = j; })
    .catch(function () { map = null; });

  function currentPath() {
    var p = location.pathname;
    p = p.replace(/index\.html$/, '');
    if (p.length > 1 && !p.endsWith('/')) p += '/';
    return p;
  }

  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[hreflang]');
    if (!a || !map) return;
    var target = map[currentPath()];
    if (target && target !== currentPath()) {
      ev.preventDefault();
      location.assign(target);
    }
  }, true);
})();
