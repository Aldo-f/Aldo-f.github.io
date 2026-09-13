---
title: Abbreviations Cheatsheet
---

<div id="abbreviations-page">
  <header class="page-header">
    <p class="subtitle">
      DRY, YAGNI, TDD, SDD — and more.
      <span id="count-badge" class="count-badge"></span>
    </p>
  </header>

  <div class="toolbar">
    <div class="search-container">
      <span class="search-icon" aria-hidden="true">🔍</span>
      <input
        type="search"
        id="search"
        class="search"
        placeholder="Search abbreviations or definitions…"
        aria-label="Search abbreviations"
        autocomplete="off"
      >
      <span class="kbd-hint" aria-hidden="true">⌘K</span>
    </div>
    <select id="filter" class="filter" aria-label="Filter by category">
      <option value="">All categories</option>
    </select>
    <a
      id="add-link"
      class="add-link"
      href="https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md"
      target="_blank"
      rel="noopener"
      aria-label="Add a new abbreviation on GitHub"
    >+ Add Abbreviation</a>
  </div>

  <div id="cards" role="list" aria-live="polite"></div>

  <div class="howto">
    <h2>How to add a new abbreviation</h2>
    <ol>
      <li>
        <strong>Create a new <code>.md</code> file</strong> named after the abbreviation:
        <code>MYABBR.md</code> (e.g. <code>FOMO.md</code>).
      </li>
      <li>
        <strong>Front-matter</strong> — one required key:
        <pre><code>---
abbreviation: FOMO
---</code></pre>
      </li>
      <li>
        <strong>Add your answer(s)</strong>, each as an <code>##</code> heading with required metadata:
        <pre><code>## Fear of Missing Out
**Category:** psychology, marketing
**Definition:** A feeling that others are experiencing something better than you.</code></pre>
      </li>
      <li>
        <strong>Categories</strong> are comma-separated tags; same names across files produce filter options.
      </li>
      <li>
        <strong>Save</strong> and rebuild; the entry appears alphabetically.
      </li>
    </ol>
    <p>
      <a href="https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md" target="_blank" rel="noopener">
        GitHub shortcut: open the template
      </a>
    </p>
  </div>
</div>
