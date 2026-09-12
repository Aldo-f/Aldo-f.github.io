---
title: Abbreviations Cheatsheet
---

<div id="abbreviations-page">
  <p class="subtitle">DRY, YAGNI, TDD, SDD — and more. Add new ones via the GitHub link.</p>
  <div class="toolbar">
    <input type="search" id="search" class="search" placeholder="Search abbreviations or definitions…">
    <select id="filter" class="filter">
      <option value="">All categories</option>
    </select>
    <a id="add-link" class="add-link" href="https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md" target="_blank" rel="noopener">+ Add Abbreviation</a>
  </div>
  <div id="cards"></div>
</div>

<style>
  :root { --accent: #ab57ff; --bg: #1e1e2e; --card: #2a2a3e; --text: #cdd6f4; --muted: #a6adc8; --border: #45475a; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: 'Inter', system-ui, sans-serif; padding: 2rem; line-height: 1.6; }
  h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
  .subtitle { color: var(--muted); margin-bottom: 1.5rem; }
  .toolbar { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
  .search { flex: 1; min-width: 200px; padding: 0.6rem 1rem; border: 1px solid var(--border); border-radius: 8px; background: var(--card); color: var(--text); font-size: 1rem; }
  .search:focus { outline: 2px solid var(--accent); }
  .filter { padding: 0.6rem 1rem; border: 1px solid var(--border); border-radius: 8px; background: var(--card); color: var(--text); font-size: 1rem; cursor: pointer; }
  .filter:focus { outline: 2px solid var(--accent); }
  .add-link { margin-left: auto; padding: 0.6rem 1.2rem; background: var(--accent); color: #fff; text-decoration: none; border-radius: 8px; font-weight: 600; transition: opacity 0.2s; }
  .add-link:hover { opacity: 0.85; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem; margin-bottom: 1rem; transition: border-color 0.2s; }
  .card:hover { border-color: var(--accent); }
  .card-header { display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none; }
  .card-header h2 { font-size: 1.3rem; color: var(--accent); }
  .card-header .arrow { font-size: 1.2rem; transition: transform 0.2s; }
  .card.open .arrow { transform: rotate(180deg); }
  .card-body { max-height: 0; overflow: hidden; transition: max-height 0.3s ease; }
  .card.open .card-body { max-height: 800px; margin-top: 1rem; }
  .answer { border-left: 3px solid var(--accent); padding: 0.5rem 1rem; margin-bottom: 0.5rem; background: rgba(171,87,255,0.05); border-radius: 0 6px 6px 0; }
  .answer h3 { font-size: 1rem; color: var(--text); margin-bottom: 0.2rem; }
  .tags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.4rem; }
  .tag { font-size: 0.75rem; padding: 0.15rem 0.6rem; border-radius: 999px; background: var(--border); color: var(--muted); }
  .definition { color: var(--muted); font-size: 0.95rem; }
  .no-results { color: var(--muted); padding: 2rem 0; }
  .hidden { display: none; }
  .howto { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem; margin-bottom: 1.5rem; }
  .howto h2 { color: var(--accent); margin-bottom: 0.8rem; }
  .howto ul { padding-left: 1.2rem; margin-top: 0.5rem; }
  .howto li { margin-bottom: 0.3rem; }
  .howto code { background: var(--border); padding: 0.1rem 0.4rem; border-radius: 4px; color: var(--text); }
  .copy-link { color: var(--accent); font-size: 0.85rem; word-break: break-all; }
</style>

<div class="howto">
  <h2>How to add a new abbreviation</h2>
  <ol>
    <li><strong>Create a new <code>.md</code> file</strong> named after the abbreviation:
      <code>MYABBR.md</code> (e.g. <code>FOMO.md</code>).</li>
    <li><strong>Front-matter</strong> — one required key:
      <pre><code>---
abbreviation: FOMO
---</code></pre></li>
    <li><strong>Add your answer(s)</strong>, each as an <code>H2</code> with the required metadata:
      <pre><code>## Fear of Missing Out
**Category:** psychology, marketing
**Definition:** A feeling that others are experiencing something better than you.</code></pre>
    <li><strong>Categories</strong> are comma-separated tags; same names across files produce filter options.</li>
    <li><strong>Save</strong> and rebuild; the entry appears alphabetically.</li>
  </ol>
  <p class="copy-link">GitHub shortcut: <a class="copy-link" href="https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md" target="_blank" rel="noopener">https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md</a></p>
</div>

<style>

<script>
(function() {
  'use strict';

  const DATA = window.ABBREVIATIONS || [];
  const searchInput = document.getElementById('search');
  const filterSelect = document.getElementById('filter');
  const cardsContainer = document.getElementById('cards');
  const addLink = document.getElementById('add-link');

  // Collect all unique categories for dynamic filter options
  const allCategories = new Set();
  DATA.forEach(a => a.answers.forEach(ans => (ans.categories || ['general']).forEach(c => allCategories.add(c))));
  const categories = [...allCategories].sort();

  function populateFilter() {
    filterSelect.innerHTML = '<option value="">All categories</option>' +
      categories.map(c => `<option value="${c}">${c}</option>`).join('');
    if (DATA.length > 0) {
      const firstAbbr = DATA[0].abbreviation.toLowerCase();
      addLink.href = `https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/${firstAbbr}.md`;
    }
  }

  function render() {
    const q = (searchInput.value || '').toLowerCase();
    const cat = filterSelect.value;

    cardsContainer.innerHTML = '';
    let visibleCount = 0;

    DATA.forEach(abbr => {
      const answers = (abbr.answers || []).filter(ans => {
        const matchCat = !cat || (ans.categories || []).includes(cat);
        const matchQ = !q || abbr.abbreviation.toLowerCase().includes(q) ||
          (ans.definition || '').toLowerCase().includes(q) ||
          (ans.title || '').toLowerCase().includes(q) ||
          (ans.categories || []).some(c => c.toLowerCase().includes(q));
        return matchCat && matchQ;
      });

      if (answers.length === 0) return;

      // Alphabetical answers
      answers.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
      visibleCount++;

      const card = document.createElement('div');
      card.className = 'card' + (visibleCount === 1 ? ' open' : '');
      card.innerHTML = `
        <div class="card-header" onclick="this.parentElement.classList.toggle('open')">
          <h2>${abbr.abbreviation}</h2>
          <span class="arrow">▼</span>
        </div>
        <div class="card-body">
          ${answers.map(a => `
            <div class="answer">
              <h3>${a.title}</h3>
              <div class="tags">${(a.categories || []).map(c => `<span class="tag">${c}</span>`).join('')}</div>
              <p class="definition">${a.definition || ''}</p>
            </div>
          `).join('')}
        </div>
      `;
      cardsContainer.appendChild(card);
    });

    if (visibleCount === 0) {
      cardsContainer.innerHTML = '<p class="no-results">No abbreviations found matching your criteria.</p>';
    }
  }

  searchInput.addEventListener('input', render);
  filterSelect.addEventListener('change', render);

  populateFilter();
  render();
})();
</script>