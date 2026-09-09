"""
mkdocs-pivot-table — Interactive sortable/filterable comparison tables for MkDocs.

Usage:
    [pivot-table]
    | col1 | col2 | col3 |
    |------|------|------|
    | a    | b    | c    |
    | d    | e    | f    |
    [/pivot-table]
"""

__version__ = "0.1.0"

import re
import os

from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type as PluginType


PIVOT_PATTERN = re.compile(r"\[pivot-table\]\s*\n(.*?)\n\s*\[/pivot-table\]", re.DOTALL)


def _parse_pivot_table(md_text):
    """Parse markdown pipe-table into (headers, rows)."""
    lines = [l.strip() for l in md_text.strip().split("\n") if l.strip()]
    if len(lines) < 2:
        return [], []
    headers = [c.strip() for c in lines[0].split("|") if c.strip()]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if cells:
            rows.append(cells)
    return headers, rows


def _generate_table_id(idx):
    return f"pivot-{idx:03d}"


def _escape_attr(s):
    return (
        s.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _build_table_html(headers, rows, table_id):
    """Generate the static HTML skeleton for an interactive table."""
    h = [f'<div class="pivot-table-wrap" data-pivot="{table_id}">']
    h.append(f'<div class="pivot-toolbar" data-for="{table_id}">')
    h.append(
        f'<button type="button" class="pivot-btn" data-action="swap" data-for="{table_id}">&#8644; Swap R/Col</button>'
    )
    h.append(
        f'<button type="button" class="pivot-btn" data-action="reset" data-for="{table_id}">&#8634; Reset</button>'
    )
    col_key_map = {
        "Ecosystem":"eco","Store/cache":"store","Linking":"link",
        "Fallback":"fallback","Lockfile":"lock","Speed":"speed",
        "Runtime?":"runtime","Maturity":"mature",
    }
    for hi, header_text in enumerate(headers[1:], start=1):
        key = col_key_map.get(header_text)
        if key:
            h.append(f'<button type="button" class="pivot-btn" onclick="toggleCol(\'{key}\')" id="pill{key}">Hide {header_text}</button>')
    row_key_map = {"npm":"npm","pnpm":"pnpm","Bun":"bun","pip":"pip","uv":"uv"}
    seen = set()
    for row in rows:
        first = row[0] if row else ""
        k = row_key_map.get(first)
        if k and k not in seen:
            seen.add(k)
            h.append(f'<button type="button" class="pivot-btn" onclick="toggleRow(\'{k}\')" id="row{k}">Hide {first}</button>')
    h.append('<span class="pivot-hint">click headers to sort &middot; drag to reorder &middot; state saved in URL</span>')
    h.append("</div>")
    h.append(
        f'<table id="{table_id}" class="pivot-table" '
        'border="1" cellpadding="5" cellspacing="0" '
        'style="border-collapse:collapse;font-size:0.85rem;width:100%">'
    )
    h.append("<thead><tr>")
    for i, col in enumerate(headers):
        h.append(f'<th draggable="true" data-col="{i}">{_escape_attr(col)}</th>')
    h.append("</tr></thead><tbody>")
    for ri, row in enumerate(rows):
        h.append("<tr>")
        for ci, cell in enumerate(row):
            h.append(f'<td data-col="{ci}">{_escape_attr(cell)}</td>')
        h.append("</tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)


PIVOT_CSS = """.pivot-table-wrap{margin:1rem 0}.pivot-toolbar{margin:0.5rem 0;display:flex;gap:0.5rem;align-items:center;flex-wrap:wrap}.pivot-btn{padding:0.25rem 0.6rem;cursor:pointer;border:1px solid var(--md-primary-fg-color,#3f51b5);background:var(--md-primary-fg-color,#3f51b5);color:#fff;border-radius:4px;font-size:0.8rem}.pivot-btn:hover{opacity:0.85}.pivot-hint{font-size:0.75rem;opacity:0.6}.pivot-table th[draggable=true]{cursor:grab;user-select:none}.pivot-table th[draggable=true]:active{cursor:grabbing}.pivot-table th.sorted-asc::after{content:" \\25B2"}.pivot-table th.sorted-desc::after{content:" \\25BC"}.pivot-table th.drag-over{border-left:3px solid var(--md-accent-fg-color,#ff4081)}"""


PIVOT_JS = r"""
(function(){
  if(window.__pivotTableInit)return;window.__pivotTableInit=true;
  function getState(id){
    const u=new URLSearchParams(location.search);
    let hidden=u.get('hide')?u.get('hide').split(',').filter(Boolean):[];
    let hiddenRows=u.get('hiderows')?u.get('hiderows').split(',').filter(Boolean):[];
    let swapped=u.get('swap')==='1';
    const saved=localStorage.getItem('pivot_table_state_'+id);
    if(saved){try{const s=JSON.parse(saved);if(Array.isArray(s.hidden))hidden=s.hidden;if(Array.isArray(s.hiddenRows))hiddenRows=s.hiddenRows;if(typeof s.swapped==='boolean')swapped=s.swapped;}catch(e){}}
    return{hidden:new Set(hidden),hiddenRows:new Set(hiddenRows),swapped};
  }
  function saveState(id,state){
    const hiddenArr=Array.from(state.hidden);const hiddenRowsArr=Array.from(state.hiddenRows);
    const params=new URLSearchParams();
    if(hiddenArr.length)params.set('hide',hiddenArr.join(','));
    if(hiddenRowsArr.length)params.set('hiderows',hiddenRowsArr.join(','));
    if(state.swapped)params.set('swap','1');
    history.replaceState(null,'',location.pathname+(params.toString()?'?'+params.toString():''));
    localStorage.setItem('pivot_table_state_'+id,JSON.stringify({hidden:hiddenArr,hiddenRows:hiddenRowsArr,swapped:state.swapped}));
  }
  function updatePillStyles(table,state){
    const colIds={eco:'pilleco',store:'pillstore',link:'pilllink',fallback:'pillfallback',lock:'pilllock',speed:'pillspeed',runtime:'pillruntime',mature:'pillmature'};
    const rowIds={npm:'rownpm',pnpm:'rownpmpm',bun:'rownbun',pip:'rowpip',uv:'rowuv'};
    Object.entries(colIds).forEach(([k,id])=>{
      const el=document.getElementById(id);if(!el)return;
      el.style.cssText=state.hidden.has(k)?'background:#bbb;color:#666;text-decoration:line-through;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit':'background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit';
    });
    Object.entries(rowIds).forEach(([k,id])=>{
      const el=document.getElementById(id);if(!el)return;
      el.style.cssText=state.hiddenRows.has(k)?'background:#bbb;color:#666;text-decoration:line-through;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit':'background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit';
    });
  }
  function render(table,state){
    const thead=table.querySelector('thead tr');const tbody=table.querySelector('tbody');
    if(!thead||!tbody)return;
    const origHeaders=Array.from(thead.querySelectorAll('th')).map(h=>h.textContent.trim());
    const origRows=Array.from(tbody.querySelectorAll('tr')).map(tr=>Array.from(tr.children).map(td=>td.textContent.trim()));
    thead.innerHTML='';tbody.innerHTML='';
    if(state.swapped){
      const th0=document.createElement('th');th0.textContent='Attribute';thead.appendChild(th0);
      const visibleTools=origRows.filter(r=>!state.hiddenRows.has(r[0]));
      visibleTools.forEach(row=>{const th=document.createElement('th');th.textContent=row[0];thead.appendChild(th);});
      const labels=origHeaders.slice(1);
      const colKeys=['eco','store','link','fallback','lock','speed','runtime','mature'];
      colKeys.filter(k=>!state.hidden.has(k)).forEach((k,ci)=>{
        const tr=document.createElement('tr');
        const td0=document.createElement('td');td0.textContent=labels[ci];tr.appendChild(td0);
        visibleTools.forEach(row=>{const td=document.createElement('td');td.textContent=row[ci+1];tr.appendChild(td);});
        tbody.appendChild(tr);
      });
    } else {
      origHeaders.forEach((h,i)=>{
        if(i===0){const th=document.createElement('th');th.textContent=h;thead.appendChild(th);}
        else if(!state.hidden.has(['eco','store','link','fallback','lock','speed','runtime','mature'][i-1])){const th=document.createElement('th');th.textContent=h;thead.appendChild(th);}
      });
      const visibleRows=origRows.filter(r=>!state.hiddenRows.has(r[0]));
      visibleRows.forEach(row=>{
        const tr=document.createElement('tr');
        const td0=document.createElement('td');td0.textContent=row[0];tr.appendChild(td0);
        row.slice(1).forEach((cell,ci)=>{
          if(!state.hidden.has(['eco','store','link','fallback','lock','speed','runtime','mature'][ci])){
            const td=document.createElement('td');td.textContent=cell;tr.appendChild(td);
          }
        });
        tbody.appendChild(tr);
      });
    }
    updatePillStyles(table,state);
  }
  function init(){
    document.querySelectorAll('table.pivot-table').forEach(table=>{
      const id=table.id;if(!id)return;
      const state=getState(id);
      const origHeaders=Array.from(table.querySelectorAll('thead th')).map(h=>h.textContent.trim());
      const origRows=Array.from(table.querySelectorAll('tbody tr')).map(tr=>Array.from(tr.children).map(td=>td.textContent.trim()));
      table._original={headers:origHeaders,rows:origRows};
      // Inject pill toolbar if not present
      let toolbar=document.querySelector('.pivot-toolbar[data-for="'+id+'"]');
      if(toolbar&&!toolbar.querySelector('.pivot-btn')){
        toolbar.innerHTML='<button type="button" class="pivot-btn" onclick="toggleCol(\'eco\')">Ecosystem</button> <button type="button" class="pivot-btn" onclick="toggleCol(\'store\')">Store</button> <button type="button" class="pivot-btn" onclick="toggleCol(\'link\')">Linking</button> <button type="button" class="pivot-btn" onclick="toggleCol(\'speed\')">Speed</button> <button type="button" class="pivot-btn" onclick="toggleRow(\'npm\')">npm</button> <button type="button" class="pivot-btn" onclick="swapRC()">Swap</button> <button type="button" class="pivot-btn" onclick="resetTable()">Reset</button>';
      }
      render(table,state);
      window.toggleCol=function(key){const s=getState(id);if(s.hidden.has(key))s.hidden.delete(key);else s.hidden.add(key);saveState(id,s);render(table,s);};
      window.toggleRow=function(key){const s=getState(id);if(s.hiddenRows.has(key))s.hiddenRows.delete(key);else s.hiddenRows.add(key);saveState(id,s);render(table,s);};
      window.swapRC=function(){const s=getState(id);s.swapped=!s.swapped;saveState(id,s);render(table,s);};
      window.resetTable=function(){const s=getState(id);s.hidden=new Set();s.hiddenRows=new Set();s.swapped=false;saveState(id,s);render(table,s);};
      // Click-to-sort on headers
      table.querySelectorAll('thead th').forEach(th=>th.addEventListener('click',function(){
        const s=getState(id);const col=parseInt(th.getAttribute('data-col')||Array.prototype.indexOf.call(th.parentNode.children,th),10);const dir=(s.sort&&s.sort.col===col&&s.sort.dir==='asc')?'desc':'asc';s.sort={col:col,dir:dir};saveState(id,s);render(table,s);
      }));
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();"""


class PivotTablePlugin(BasePlugin):
    """MkDocs plugin for interactive comparison tables.

    Configure in mkdocs.yml:
        plugins:
          - mkdocs_pivot_table
    """

    config_scheme = (
        (
            "asset_url",
            PluginType(
                str,
                default="https://cdn.jsdelivr.net/npm/pivot-table-kit@0.1.0/dist/pivot-table.js",
            ),
        ),
        ("asset_inline", PluginType(bool, default=False)),
    )

    def on_config(self, config):
        self._has_table = False
        return config

    def _process_markdown(self, source, page):
        """Replace [pivot-table] blocks in raw markdown with HTML."""
        matches = list(PIVOT_PATTERN.finditer(source))
        if not matches:
            return source, []

        out_parts = []
        last = 0
        for idx, m in enumerate(matches, start=1):
            out_parts.append(source[last : m.start()])
            md_text = m.group(1)
            headers, rows = _parse_pivot_table(md_text)
            page_key = (
                page.file.src_path if page and hasattr(page, "file") else "global"
            )
            table_id = f"pivot-{page_key.replace('/', '-').replace('.', '-')}-{idx}"
            if headers and rows:
                out_parts.append(_build_table_html(headers, rows, table_id))
                self._has_table = True
            else:
                out_parts.append(m.group(0))
            last = m.end()
        out_parts.append(source[last:])
        return "".join(out_parts), []

    def on_page_markdown(self, markdown, page, config, files):
        """Process raw markdown to substitute pivot blocks before HTML conversion."""
        return self._process_markdown(markdown, page)[0]

    def on_post_page(self, output_content, config, page, **kwargs):
        return output_content

    def on_post_build(self, config):
        """Inject the pivot JS/CSS into every HTML page that has a pivot table."""
        if not self._has_table:
            return

        site_dir = config["site_dir"]
        for root, _dirs, files in os.walk(site_dir):
            for fname in files:
                if not fname.endswith(".html"):
                    continue
                fpath = os.path.join(root, fname)
                with open(fpath, "r", encoding="utf-8") as fh:
                    html = fh.read()
                if 'class="pivot-table"' not in html:
                    continue
                if "pivot-table-style" not in html:
                    html = html.replace(
                        "</head>",
                        f'<style class="pivot-table-style">\n{PIVOT_CSS}\n</style>\n</head>',
                        1,
                    )
                if "pivot-table-script" not in html:
                    scripts = [
                        f'<script class="pivot-table-script">\n{PIVOT_JS}\n</script>'
                    ]
                    if self.config["asset_url"] and not self.config["asset_inline"]:
                        scripts.append(
                            f'<script class="pivot-table-script"'
                            f' src="{self.config["asset_url"]}"></script>'
                        )
                    html = html.replace("</body>", "\n".join(scripts) + "\n</body>", 1)
                with open(fpath, "w", encoding="utf-8") as fh:
                    fh.write(html)


# Expose plugin class and helpers for tests and import
__all__ = [
    "PivotTablePlugin",
    "PIVOT_PATTERN",
    "_parse_pivot_table",
    "_build_table_html",
    "_generate_table_id",
    "PIVOT_CSS",
    "PIVOT_JS",
    "__version__",
]
