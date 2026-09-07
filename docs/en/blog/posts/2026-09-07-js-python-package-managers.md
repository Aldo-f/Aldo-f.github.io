---
title: "JS & Python Package Managers Compared: npm, pnpm, Bun, pip, uv"
date: 2026-09-07
tags: [tooling, javascript, python]
---

Choosing the right package manager isn't just about convenience—it's about disk space, install speed, and reproducible builds. The wrong choice can bloat your project with duplicate files, while the right one keeps your workspace lean and your CI pipelines humming.

## Quick comparison (interactive)

<p><small>Swap rows/columns • hide/show columns • state saved to URL + browser</small></p>

<table id="cmp-table" border="1" cellpadding="6" style="border-collapse:collapse;font-size:0.85rem;width:100%">
<thead><tr>
<th>Tool</th><th>Ecosystem</th><th>Store/cache</th><th>Linking</th><th>Fallback</th><th>Lockfile</th><th>Speed</th><th>Runtime?</th><th>Maturity</th>
</tr></thead><tbody>
<tr><td>npm</td><td>JS/TS</td><td>~/.npm</td><td>Copy</td><td>None</td><td>package-lock.json</td><td>Slow</td><td>No</td><td>High</td></tr>
<tr><td>pnpm</td><td>JS/TS</td><td>~/.pnpm-store</td><td>Hard link</td><td>Copy</td><td>pnpm-lock.yaml</td><td>Fast</td><td>No</td><td>High</td></tr>
<tr><td>Bun</td><td>JS/TS</td><td>~/.bun/bin/cache</td><td>Hard link</td><td>Copy</td><td>bun.lockb</td><td>Fastest</td><td>Yes</td><td>Medium</td></tr>
<tr><td>pip</td><td>Python</td><td>~/.cache/pip</td><td>Copy</td><td>None</td><td>requirements.txt</td><td>Slow</td><td>No</td><td>High</td></tr>
<tr><td>uv</td><td>Python</td><td>~/.uv/cache</td><td>Hard/reflink</td><td>Copy</td><td>uv.lock</td><td>Fast</td><td>No</td><td>Medium</td></tr>
</tbody></table>

<div style="margin:0.5rem 0">
  <button id="table-drawer-btn" onclick="toggleDrawer()" style="background:#f5f5f5;border:1px solid #ddd;border-radius:999px;padding:2px 10px;font-size:0.75rem;cursor:pointer;color:#555;font-family:inherit">&#9881; Customize table</button>
</div>

<div id="table-drawer" style="display:none;border:1px solid #e0e0e0;border-radius:8px;padding:12px;margin-bottom:0.5rem;background:#fafafa">
  <p style="font-size:0.7rem;color:#888;margin:0 0 8px 0">Click pills to hide/show columns • Strike-through = hidden</p>

  <div style="margin-bottom:8px">
    <span style="font-size:0.7rem;color:#666;margin-right:6px">Columns:</span>
    <button onclick="toggleCol('eco')"     id="pilleco"     style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">Ecosystem</button>
    <button onclick="toggleCol('store')"  id="pillstore"   style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">Store</button>
    <button onclick="toggleCol('link')"   id="pilllink"    style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">Linking</button>
    <button onclick="toggleCol('fallback')" id="pillfallback" style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">Fallback</button>
    <button onclick="toggleCol('lock')"   id="pilllock"    style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">Lockfile</button>
    <button onclick="toggleCol('speed')"  id="pillspeed"   style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">Speed</button>
    <button onclick="toggleCol('runtime')"id="pillruntime" style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">Runtime?</button>
    <button onclick="toggleCol('mature')"id="pillmature"  style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">Maturity</button>
  </div>

  <div style="margin-bottom:8px">
    <span style="font-size:0.7rem;color:#666;margin-right:6px">Rows:</span>
    <button onclick="toggleRow('npm')"  id="rownpm"  style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">npm</button>
    <button onclick="toggleRow('pnpm')" id="rownpmpm"style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">pnpm</button>
    <button onclick="toggleRow('bun')"  id="rownbun" style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">Bun</button>
    <button onclick="toggleRow('pip')"  id="rowpip"  style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">pip</button>
    <button onclick="toggleRow('uv')"   id="rowuv"   style="background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit">uv</button>
  </div>

  <div>
    <button onclick="swapRC()" style="background:#6366f1;color:#fff;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);font-family:inherit">Swap rows/cols</button>
    <button onclick="resetTable()" style="background:#e53935;color:#fff;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);font-family:inherit">Reset</button>
  </div>
</div>

<script>
(function(){
  const table = document.getElementById('cmp-table');
  const theadRow = table.querySelector('thead tr');
  const tbody = table.querySelector('tbody');
  const origHeaders = Array.from(theadRow.querySelectorAll('th')).map(h=>h.textContent.trim());
  const origRows = Array.from(tbody.querySelectorAll('tr')).map(tr=>Array.from(tr.querySelectorAll('td')));
  const colKeys = ['eco','store','link','fallback','lock','speed','runtime','mature'];
  const STORAGE_KEY = 'cmp_table_state';
  const ALL_ROWS   = ['npm','pnpm','bun','pip','uv'];
  const COL_IDS    = {eco:'pilleco',store:'pillstore',link:'pilllink',fallback:'pillfallback',lock:'pilllock',speed:'pillspeed',runtime:'pillruntime',mature:'pillmature'};
  const ROW_IDS    = {npm:'rownpm',pnpm:'rownpnpm',bun:'rownbun',pip:'rowpip',uv:'rowuv'};

  function getState(){
    const u = new URLSearchParams(location.search);
    let hidden = u.get('hide') ? u.get('hide').split(',').filter(Boolean) : [];
    let hiddenRows = u.get('hiderows') ? u.get('hiderows').split(',').filter(Boolean) : [];
    let swapped = u.get('swap') === '1';
    const saved = localStorage.getItem(STORAGE_KEY);
    if(saved){
      try{
        const s = JSON.parse(saved);
        if(Array.isArray(s.hidden)) hidden = s.hidden;
        if(Array.isArray(s.hiddenRows)) hiddenRows = s.hiddenRows;
        if(typeof s.swapped === 'boolean') swapped = s.swapped;
      }catch(e){}
    }
    return {hidden: new Set(hidden), hiddenRows: new Set(hiddenRows), swapped};
  }

  function saveState(hiddenSet, hiddenRowsSet, swapped){
    const hiddenArr = Array.from(hiddenSet);
    const hiddenRowsArr = Array.from(hiddenRowsSet);
    const params = new URLSearchParams();
    if(hiddenArr.length) params.set('hide', hiddenArr.join(','));
    if(hiddenRowsArr.length) params.set('hiderows', hiddenRowsArr.join(','));
    if(swapped) params.set('swap','1');
    history.replaceState(null,'',location.pathname+(params.toString()?'?'+params.toString():''));
    localStorage.setItem(STORAGE_KEY, JSON.stringify({hidden:hiddenArr, hiddenRows:hiddenRowsArr, swapped}));
  }

  function updateAllPillStyles(){
    const {hidden, hiddenRows} = getState();
    colKeys.forEach(k => {
      const el = document.getElementById(COL_IDS[k]);
      if(el) el.style.cssText = hidden.has(k) ? 'background:#bbb;color:#666;text-decoration:line-through;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit' : 'background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit';
    });
    ALL_ROWS.forEach(k => {
      const el = document.getElementById(ROW_IDS[k]);
      if(el) el.style.cssText = hiddenRows.has(k) ? 'background:#bbb;color:#666;text-decoration:line-through;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit' : 'background:#e8e8e8;color:#333;border:none;border-radius:999px;padding:1px 7px;font-size:0.7rem;cursor:pointer;box-shadow:0 1px 2px rgba(0,0,0,0.12);transition:all 0.15s;font-family:inherit';
    });
  }

  function render(){
    const {hidden, hiddenRows, swapped} = getState();
    theadRow.innerHTML = '';
    tbody.innerHTML = '';

    if(swapped){
      // Columns = tools, rows = attributes
      const th0 = document.createElement('th'); th0.textContent = 'Attribute'; theadRow.appendChild(th0);
      const visibleTools = origRows.filter(r => !hiddenRows.has(r[0].textContent.trim()));
      visibleTools.forEach(row => {
        const th = document.createElement('th'); th.textContent = row[0].textContent.trim(); theadRow.appendChild(th);
      });
      const labels = origHeaders.slice(1);
      colKeys.filter(k => !hidden.has(k)).forEach((k, ci) => {
        const tr = document.createElement('tr');
        const td0 = document.createElement('td'); td0.textContent = labels[ci]; tr.appendChild(td0);
        visibleTools.forEach(row => {
          const td = document.createElement('td'); td.textContent = row[ci+1].textContent.trim(); tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    } else {
      // Columns = attributes, rows = tools
      origHeaders.forEach((h, i) => {
        if(i === 0){ const th = document.createElement('th'); th.textContent = h; theadRow.appendChild(th); }
        else if(!hidden.has(colKeys[i-1])){ const th = document.createElement('th'); th.textContent = h; theadRow.appendChild(th); }
      });
      const visibleRows = origRows.filter(r => !hiddenRows.has(r[0].textContent.trim()));
      visibleRows.forEach(row => {
        const tr = document.createElement('tr');
        const td0 = document.createElement('td'); td0.textContent = row[0].textContent.trim(); tr.appendChild(td0);
        row.slice(1).forEach((td, ci) => {
          if(!hidden.has(colKeys[ci])){
            const tdc = document.createElement('td'); tdc.textContent = td.textContent.trim(); tr.appendChild(tdc);
          }
        });
        tbody.appendChild(tr);
      });
    }
    updateAllPillStyles();
  }

  window.toggleDrawer = function(){
    const d = document.getElementById('table-drawer');
    const b = document.getElementById('table-drawer-btn');
    if(!d) return;
    const open = d.style.display !== 'none';
    d.style.display = open ? 'none' : 'block';
    b.textContent = open ? '\u2699\ufe0f Customize table' : '\u2715\ufe0f Close';
  };

  window.toggleCol = function(key){
    const {hidden, hiddenRows, swapped} = getState();
    if(hidden.has(key)) hidden.delete(key); else hidden.add(key);
    saveState(hidden, hiddenRows, swapped);
    render();
  };

  window.toggleRow = function(key){
    const {hidden, hiddenRows, swapped} = getState();
    if(hiddenRows.has(key)) hiddenRows.delete(key); else hiddenRows.add(key);
    saveState(hidden, hiddenRows, swapped);
    render();
  };

  window.swapRC = function(){
    const {hidden, hiddenRows, swapped} = getState();
    saveState(hidden, hiddenRows, !swapped);
    render();
  };

  window.resetTable = function(){
    localStorage.removeItem(STORAGE_KEY);
    history.replaceState(null,'',location.pathname);
    render();
  };

  render();
})();
</script>

## Install flow diagrams

### npm install flow
```mermaid
flowchart TD
    A[registry] --> B[download]
    B --> C[node_modules]
    C -.-> D[(project copy)]
    D --> C
```

### pnpm install flow
```mermaid
flowchart TD
    A[global store] --> B[hard link]
    B --> C[.pnpm virtual store]
    C --> D[symlink]
    D --> E[node_modules]
    E --> F[(project link)]
```

### Bun install flow
```mermaid
flowchart TD
    A[global cache] --> B[hard link]
    B -.-> C[(copy fallback)]
    C --> D[node_modules]
```

### pip install flow
```mermaid
flowchart TD
    A[PyPI] --> B[download]
    B --> C[venv site-packages]
    C -.-> D[(project copy)]
```

### uv install flow
```mermaid
flowchart TD
    A[global cache] --> B[hard link or reflink]
    B -.-> C[(copy fallback)]
    C --> D[venv site-packages]
```

## Which one avoids duplicate files on disk?

npm and pip copy packages per project, so installing the same library across multiple projects stores it multiple times on disk. pnpm, Bun, and uv all link from a shared global store/cache, giving you automatic deduplication.

## The bottom line

When you install the same package version across 10 projects, pnpm/Bun/uv only store it once on disk, while npm/pip store it 10 times. That means you save disk space and reduce CI build times—simple as that.
