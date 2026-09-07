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
<button onclick="toggleCol('eco')">Ecosystem</button>
<button onclick="toggleCol('store')">Store</button>
<button onclick="toggleCol('link')">Linking</button>
<button onclick="toggleCol('fallback')">Fallback</button>
<button onclick="toggleCol('lock')">Lockfile</button>
<button onclick="toggleCol('speed')">Speed</button>
<button onclick="toggleCol('runtime')">Runtime?</button>
<button onclick="toggleCol('mature')">Maturity</button>
<button onclick="swapRC()">Swap rows/cols</button>
<button onclick="resetTable()">Reset</button>
</div>

<script>
(function(){
  const table = document.getElementById('cmp-table');
  const theadRow = table.querySelector('thead tr');
  const tbody = table.querySelector('tbody');
  // capture original data BEFORE any re-render
  const origHeaders = Array.from(theadRow.querySelectorAll('th')).map(h=>h.textContent.trim());
  // origRows[0] is header row of data (Tool column = first), rest are tool rows
  const origRows = Array.from(tbody.querySelectorAll('tr')).map(tr=>Array.from(tr.querySelectorAll('td')));
  // keys for columns 1..8 (index 0 is the row label "Tool")
  const colKeys = ['eco','store','link','fallback','lock','speed','runtime','mature'];
  const STORAGE_KEY = 'cmp_table_state';

  function getState(){
    const u = new URLSearchParams(location.search);
    let hidden = [];
    if(u.get('hide')) hidden = u.get('hide').split(',').filter(Boolean);
    let swapped = u.get('swap')==='1';
    const saved = localStorage.getItem(STORAGE_KEY);
    if(saved){
      try{
        const s = JSON.parse(saved);
        if(Array.isArray(s.hidden)) hidden = s.hidden;
        if(typeof s.swapped==='boolean') swapped = s.swapped;
      }catch(e){}
    }
    return {hidden: new Set(hidden), swapped};
  }

  function setState(hiddenSet, swapped){
    const u = new URLSearchParams(location.search);
    const hiddenArr = Array.from(hiddenSet);
    if(hiddenArr.length) u.set('hide', hiddenArr.join(',')); else u.delete('hide');
    if(swapped) u.set('swap','1'); else u.delete('swap');
    history.replaceState(null,'',location.pathname+(u.toString()?'?'+u.toString():''));
    localStorage.setItem(STORAGE_KEY, JSON.stringify({hidden:hiddenArr, swapped}));
  }

  function render(){
    const {hidden, swapped} = getState();
    // Determine which data columns (1..8) are visible
    const visibleIdx = colKeys.map((k,i)=>hidden.has(k)?-1:i+1).filter(i=>i!==-1);
    // Clear
    theadRow.innerHTML = '';
    tbody.innerHTML = '';
    if(swapped){
      // Transpose: each tool becomes a column, each attribute becomes a row
      // Header: [Attribute] npm pnpm Bun pip uv
      const th0 = document.createElement('th'); th0.textContent = 'Attribute'; theadRow.appendChild(th0);
      origRows.forEach(row=>{
        const th = document.createElement('th'); th.textContent = row[0].textContent.trim(); theadRow.appendChild(th);
      });
      // Rows: one per visible attribute
      const labels = origHeaders.slice(1); // ["Ecosystem", "Store/cache", ...]
      colKeys.forEach((k,ci)=>{
        if(hidden.has(k)) return;
        const tr = document.createElement('tr');
        const td0 = document.createElement('td'); td0.textContent = labels[ci]; tr.appendChild(td0);
        origRows.forEach(row=>{
          const td = document.createElement('td'); td.textContent = row[ci+1].textContent.trim(); tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    } else {
      // Normal orientation
      origHeaders.forEach((h,i)=>{
        if(i===0){const th=document.createElement('th'); th.textContent=h; theadRow.appendChild(th);}
        else if(!hidden.has(colKeys[i-1])){const th=document.createElement('th'); th.textContent=h; theadRow.appendChild(th);}
      });
      origRows.forEach(row=>{
        const tr = document.createElement('tr');
        // first col always
        const td0 = document.createElement('td'); td0.textContent = row[0].textContent.trim(); tr.appendChild(td0);
        row.slice(1).forEach((td,ci)=>{
          if(!hidden.has(colKeys[ci])){
            const tdc = document.createElement('td'); tdc.textContent = td.textContent.trim(); tr.appendChild(tdc);
          }
        });
        tbody.appendChild(tr);
      });
    }
  }

  window.toggleCol = function(key){
    if(!colKeys.includes(key)) return;
    const {hidden, swapped} = getState();
    if(hidden.has(key)) hidden.delete(key); else hidden.add(key);
    setState(hidden, swapped);
    render();
  };

  window.swapRC = function(){
    const {hidden, swapped} = getState();
    setState(hidden, !swapped);
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
