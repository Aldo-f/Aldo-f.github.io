"""
mkdocs-pivot-table — Interactive sortable/filterable comparison table plugin for MkDocs.

Usage in Markdown:
    [pivot-table]
    col1 | col2 | col3
    ---- | ---- | ----
    a    | b    | c
    d    | e    | f
    [/pivot-table]
"""

__version__ = "0.1.0"

import re
import os

from bs4 import BeautifulSoup
from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type as PluginType


# Match [pivot-table]...[/pivot-table] in markdown before HTML conversion
PIVOT_PATTERN = re.compile(
    r'\[pivot-table\]\s*\n(.*?)\n\s*\[/pivot-table\]',
    re.DOTALL
)

# ID column markers that should not be toggleable
LOCKED_ID_KEYS = {"id", "name", "tool", "row"}


def _parse_pivot_table(md_text):
    """Parse markdown pipe-table into (headers, rows)."""
    lines = [l.strip() for l in md_text.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return [], []
    headers = [c.strip() for c in lines[0].split('|') if c.strip()]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if cells:
            rows.append(cells)
    return headers, rows


def _generate_table_id(idx):
    return f"pivot-{idx:03d}"


def _escape_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def _build_table_html(headers, rows, table_id):
    """Generate the static HTML skeleton for an interactive table."""
    h = [f'<div class="pivot-table-wrap" data-pivot="{table_id}">']
    h.append(f'<div class="pivot-toolbar" data-for="{table_id}">')
    h.append(f'<button type="button" class="pivot-btn" data-action="swap" data-for="{table_id}">⇄ Swap R/Col</button>')
    h.append(f'<button type="button" class="pivot-btn" data-action="reset" data-for="{table_id}">↺ Reset</button>')
    h.append('<span class="pivot-hint">click headers to sort · drag to reorder · state saved in URL</span>')
    h.append('</div>')
    h.append(f'<table id="{table_id}" class="pivot-table" border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse;font-size:0.85rem;width:100%">')
    h.append('<thead><tr>')
    for i, col in enumerate(headers):
        h.append(f'<th draggable="true" data-col="{i}">{_escape_attr(col)}</th>')
    h.append('</tr></thead><tbody>')
    for ri, row in enumerate(rows):
        h.append('<tr>')
        for ci, cell in enumerate(row):
            h.append(f'<td data-col="{ci}">{_escape_attr(cell)}</td>')
        h.append('</tr>')
    h.append('</tbody></table></div>')
    return '\n'.join(h)


class PivotTablePlugin(BasePlugin):
    """MkDocs plugin for interactive comparison tables.

    Configure in mkdocs.yml:
        plugins:
          - mkdocs_pivot_table
    """

    config_scheme = (
        ('asset_url', PluginType(str, default="https://cdn.jsdelivr.net/npm/pivot-table-kit@0.1.0/dist/pivot-table.js")),
        ('asset_inline', PluginType(bool, default=False)),
    )

    def on_config(self, config):
        """Store config for later use."""
        self._global_counter = 0
        self._page_counters = {}
        self._has_table = False
        return config

    def _process_markdown(self, source, page):
        """Replace [pivot-table] blocks in raw markdown with HTML placeholders."""
        matches = list(PIVOT_PATTERN.finditer(source))
        if not matches:
            return source, []

        out_parts = []
        tables = []
        last = 0
        for idx, m in enumerate(matches, start=1):
            out_parts.append(source[last:m.start()])
            md = m.group(1)
            headers, rows = _parse_pivot_table(md)
            page_key = page.file.src_path if page else 'global'
            table_id = f"pivot-{page_key.replace('/', '-').replace('.', '-')}-{idx}"
            if headers and rows:
                out_parts.append(_build_table_html(headers, rows, table_id))
                tables.append({
                    'id': table_id,
                    'headers': headers,
                    'rows': rows,
                })
                self._has_table = True
            else:
                out_parts.append(m.group(0))  # leave as-is if malformed
            last = m.end()
        out_parts.append(source[last:])
        return ''.join(out_parts), tables

    def on_page_markdown(self, markdown, page, config, files):
        """Process raw markdown to substitute pivot blocks before HTML conversion."""
        return self._process_markdown(markdown, page)[0]

    def on_post_page(self, output_content, config, page, **kwargs):
        """No-op fallback (markdown handler already inserted HTML)."""
        return output_content

    def on_post_build(self, config):
        """Inject the pivot JS/CSS into the rendered site."""
        if not self._has_table:
            return

        asset = self.config['asset_url']
        css = PIVOT_CSS
        js = PIVOT_JS

        site_dir = config['site_dir']
        for root, _dirs, files in os.walk(site_dir):
            for fname in files:
                if not fname.endswith('.html'):
                    continue
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    html = f.read()
                if 'class="pivot-table"' not in html:
                    continue
                # Inject CSS
                if 'pivot-table-style' not in html:
                    style_tag = f'<style class="pivot-table-style">{css}</style>'
                    html = html.replace('</head>', f'{style_tag}\n</head>', 1)
                # Inject JS
                if 'pivot-table-script' not in html:
                    script_inline = f'<script class="pivot-table-script">\n{js}\n</script>'
                    if asset and not self.config['asset_inline']:
                        script_inline += f'\n<script class="pivot-table-script" src="{asset}"></script>'
                    html = html.replace('</body>', f'{script_inline}\n</body>', 1)
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(html)


PIVOT_CSS = """.pivot-table-wrap { margin: 1rem 0; }
.pivot-toolbar { margin: 0.5rem 0; display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
.pivot-btn { padding: 0.25rem 0.6rem; cursor: pointer; border: 1px solid var(--md-primary-fg-color, #3f51b5); background: var(--md-primary-fg-color, #3f51b5); color: white; border-radius: 4px; font-size: 0.8rem; }
.pivot-btn:hover { opacity: 0.85; }
.pivot-hint { font-size: 0.75rem; opacity: 0.6; }
.pivot-table th[draggable="true"] { cursor: grab; user-select: none; }
.pivot-table th[draggable="true"]:active { cursor: grabbing; }
.pivot-table th.sorted-asc::after { content: " ▲"; }
.pivot-table th.sorted-desc::after { content: " ▼"; }
.pivot-table th.drag-over { border-left: 3px solid var(--md-accent-fg-color, #ff4081); }"""


PIVOT_JS = r"""
(function(){
  if (window.__pivotTableInit) return;
  window.__pivotTableInit = true;

  function getState(tableId) {
    var u = new URLSearchParams(location.search);
    var raw = u.get('pivot') || '';
    var state = {sort: null, order: [], swapped: false};
    raw.split('&').forEach(function(part){
      if (!part) return;
      var kv = part.split(':');
      if (kv[0] === tableId) {
        kv.slice(1).forEach(function(tok){
          if (tok === 'swap') state.swapped = true;
          else if (tok.indexOf('=') > -1) {
            var s = tok.split('=');
            if (s[0] === 'sort') {
              var p = s[1].split('-');
              state.sort = {col: parseInt(p[0], 10), dir: p[1]};
            } else if (s[0] === 'order') {
              state.order = s[1].split(',').map(function(x){return parseInt(x,10);});
            }
          }
        });
      }
    });
    var saved = localStorage.getItem('pivot_table_' + tableId);
    if (saved) {
      try {
        var s2 = JSON.parse(saved);
        if (s2.sort) state.sort = s2.sort;
        if (s2.order && s2.order.length) state.order = s2.order;
        if (typeof s2.swapped === 'boolean') state.swapped = s2.swapped;
      } catch(e){}
    }
    return state;
  }

  function setState(tableId, state) {
    var u = new URLSearchParams(location.search);
    var parts = [];
    if (state.sort) parts.push('sort=' + state.sort.col + '-' + state.sort.dir);
    if (state.order && state.order.length) parts.push('order=' + state.order.join(','));
    if (state.swapped) parts.push('swap');
    var token = tableId + ':' + parts.join(':');
    var existing = u.get('pivot');
    var tokens = existing ? existing.split('|').filter(function(t){return t && t.indexOf(tableId+':') !== 0;}) : [];
    if (parts.length) tokens.push(token);
    if (tokens.length) u.set('pivot', tokens.join('|'));
    else u.delete('pivot');
    history.replaceState(null, '', location.pathname + (u.toString() ? '?' + u.toString() : ''));
    localStorage.setItem('pivot_table_' + tableId, JSON.stringify(state));
  }

  function applySort(table, col, dir) {
    var tbody = table.querySelector('tbody');
    var rows = Array.from(tbody.querySelectorAll('tr'));
    rows.sort(function(a,b){
      var av = a.children[col].textContent.trim();
      var bv = b.children[col].textContent.trim();
      var an = parseFloat(av), bn = parseFloat(bv);
      if (!isNaN(an) && !isNaN(bn)) { return dir==='asc' ? an-bn : bn-an; }
      return dir==='asc' ? av.localeCompare(bv) : bv.localeCompare(av);
    });
    rows.forEach(function(r){ tbody.appendChild(r); });
  }

  function applyOrder(table, order) {
    var thead = table.querySelector('thead tr');
    var headers = Array.from(thead.children);
    var sorted = order.map(function(i){ return headers[i]; }).filter(Boolean);
    sorted.forEach(function(h){ thead.appendChild(h); });
    Array.from(table.querySelectorAll('tbody tr')).forEach(function(row){
      var tds = Array.from(row.children);
      order.forEach(function(i){ if (tds[i]) row.appendChild(tds[i]); });
    });
  }

  function applySwap(table, swap) {
    if (!swap) return;
    var thead = table.querySelector('thead tr');
    var body = table.querySelector('tbody');
    var headerCells = Array.from(thead.children);
    var dataRows = Array.from(body.querySelectorAll('tr'));
    var firstHeader = headerCells[0].textContent.trim();
    // Build transposed: new header = [firstHeader, ...first cells of each row]
    thead.innerHTML = '';
    body.innerHTML = '';
    var labelTh = document.createElement('th');
    labelTh.textContent = firstHeader;
    thead.appendChild(labelTh);
    dataRows.forEach(function(row){
      var th = document.createElement('th');
      th.textContent = row.children[0].textContent.trim();
      thead.appendChild(th);
    });
    for (var c = 1; c < headerCells.length; c++) {
      var tr = document.createElement('tr');
      var lbl = document.createElement('td');
      lbl.textContent = headerCells[c].textContent.trim();
      tr.appendChild(lbl);
      dataRows.forEach(function(row){
        var td = document.createElement('td');
        td.textContent = row.children[c] ? row.children[c].textContent.trim() : '';
        tr.appendChild(td);
      });
      body.appendChild(tr);
    }
  }

  function unswap(table) {
    // rebuild from original - we need to re-read from data-* attributes
    var orig = table._original;
    if (!orig) return;
    var thead = table.querySelector('thead tr');
    var body = table.querySelector('tbody');
    thead.innerHTML = '';
    body.innerHTML = '';
    orig.headers.forEach(function(h){
      var th = document.createElement('th');
      th.setAttribute('draggable', 'true');
      th.setAttribute('data-col', orig.headers.indexOf(h));
      th.textContent = h;
      thead.appendChild(th);
    });
    orig.rows.forEach(function(r){
      var tr = document.createElement('tr');
      r.forEach(function(c, i){
        var td = document.createElement('td');
        td.setAttribute('data-col', i);
        td.textContent = c;
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
  }

  function init() {
    document.querySelectorAll('table.pivot-table').forEach(function(table){
      var id = table.id;
      if (!id) return;
      // Save original data
      var origHeaders = Array.from(table.querySelectorAll('thead th')).map(function(th){return th.textContent.trim();});
      var origRows = Array.from(table.querySelectorAll('tbody tr')).map(function(tr){return Array.from(tr.children).map(function(td){return td.textContent.trim();});});
      table._original = {headers: origHeaders, rows: origRows};

      var state = getState(id);
      if (state.swapped) applySwap(table, true);
      if (state.order && state.order.length) applyOrder(table, state.order);
      if (state.sort) {
        applySort(table, state.sort.col, state.sort.dir);
        var ths = table.querySelectorAll('thead th');
        if (ths[state.sort.col]) ths[state.sort.col].classList.add('sorted-' + state.sort.dir);
      }

      // Sort on header click
      table.querySelectorAll('thead th').forEach(function(th){
        th.addEventListener('click', function(e){
          if (th.dragged) { th.dragged = false; return; }
          var col = parseInt(th.getAttribute('data-col') || Array.prototype.indexOf.call(th.parentNode.children, th), 10);
          var st = getState(id);
          var dir = (st.sort && st.sort.col === col && st.sort.dir === 'asc') ? 'desc' : 'asc';
          st.sort = {col: col, dir: dir};
          setState(id, st);
          applySort(table, col, dir);
          table.querySelectorAll('thead th').forEach(function(x){x.classList.remove('sorted-asc','sorted-desc');});
          th.classList.add('sorted-' + dir);
        });
      });

      // Drag-to-reorder
      var dragSrc = null;
      table.querySelectorAll('thead th').forEach(function(th){
        th.addEventListener('dragstart', function(e){
          dragSrc = th;
          e.dataTransfer.effectAllowed = 'move';
        });
        th.addEventListener('dragover', function(e){ e.preventDefault(); th.classList.add('drag-over'); });
        th.addEventListener('dragleave', function(){ th.classList.remove('drag-over'); });
        th.addEventListener('drop', function(e){
          e.preventDefault();
          th.classList.remove('drag-over');
          if (!dragSrc || dragSrc === th) return;
          th.dragged = true;
          var headers = Array.from(table.querySelector('thead tr').children);
          var fromIdx = headers.indexOf(dragSrc);
          var toIdx = headers.indexOf(th);
          var order = headers.map(function(h){
            var i = parseInt(h.getAttribute('data-col'), 10);
            return isNaN(i) ? headers.indexOf(h) : i;
          });
          var moved = order.splice(fromIdx, 1)[0];
          order.splice(toIdx, 0, moved);
          var st = getState(id);
          st.order = order;
          setState(id, st);
          applyOrder(table, order);
        });
      });

      // Toolbar
      var toolbar = document.querySelector('.pivot-toolbar[data-for="' + id + '"]');
      if (toolbar) {
        toolbar.querySelectorAll('.pivot-btn').forEach(function(btn){
          btn.addEventListener('click', function(){
            var action = btn.getAttribute('data-action');
            var st = getState(id);
            if (action === 'swap') {
              st.swapped = !st.swapped;
              setState(id, st);
              if (st.swapped) applySwap(table, true);
              else unswap(table);
            } else if (action === 'reset') {
              st = {sort: null, order: [], swapped: false};
              setState(id, st);
              unswap(table);
              table._original = {headers: origHeaders, rows: origRows};
            }
          });
        });
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
"""
