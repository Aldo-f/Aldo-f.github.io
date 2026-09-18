---
title: Afkortingen Overzicht
---
<div id="abbreviations-page">
  <header class="page-header">
    <p class="subtitle">
      DRY, YAGNI, TDD, SDD — en meer.
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
        placeholder="Zoek afkortingen of definities…"
        aria-label="Zoek afkortingen"
        autocomplete="off"
      >
    </div>
    <select id="filter" class="filter" aria-label="Filter op categorie">
      <option value="">Alle categorieën</option>
    </select>
    <a
      id="add-link"
      class="add-link"
      href="https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md"
      target="_blank"
      rel="noopener"
      aria-label="Voeg een nieuwe afkorting toe op GitHub"
    >+ Voeg Afkorting Toe</a>
  </div>

  <div id="cards" role="list" aria-live="polite"></div>

  <div class="howto">
    <h2>Hoe een nieuwe afkorting toevoegen</h2>
    <ol>
      <li>
        <strong>Maak een nieuw <code>.md</code> bestand</strong> genaamd naar de afkorting:
        <code>MYABBR.md</code> (bijv. <code>FOMO.md</code>).
      </li>
      <li>
        <strong>Front-matter</strong> — één verplichte sleutel:
        <pre><code>---
abbreviation: FOMO
---</code></pre>
      </li>
      <li>
        <strong>Voeg je antwoord(en) toe</strong>, elk als een <code>##</code> kop met verplichte metadata:
        <pre><code>## Fear of Missing Out
**Category:** psychology, marketing
**Definition:** A feeling that others are experiencing something better than you.</code></pre>
      </li>
      <li>
        <strong>Categorieën</strong> zijn komma-gescheiden tags; dezelfde namen in verschillende bestanden produceren filter-opties.
      </li>
      <li>
        <strong>Opslaan</strong> en rebuild; de entry verschijnt alfabetisch.
      </li>
    </ol>
    <p>
      <a href="https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/TEMPLATE.md" target="_blank" rel="noopener">
        GitHub shortcut: open de template
      </a>
    </p>
  </div>
</div>