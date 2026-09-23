---
title: Abbreviations Cheatsheet
---

<div id=\"abbreviations-page\">
  <header class=\"page-header\">
    <p class=\"subtitle\">
      DRY, YAGNI, TDD, SDD — and more.
      <span id=\"count-badge\" class=\"count-badge\"></span>
    </p>
  </header>

  <div class=\"toolbar\">
    <div class=\"search-container\">
      <span class=\"search-icon\" aria-hidden=\"true\">🔍</span>
      <input
        type=\"search\"
        id=\"search\"
        class=\"search\"
        placeholder=\"Search abbreviations or definitions…\"
        aria-label=\"Search abbreviations\"
        autocomplete=\"off\"
      >
    </div>
    <select id=\"filter\" class=\"filter\" aria-label=\"Filter by category\">
      <option value=\"\">All categories</option>
    </select>
    <button
      id=\"add-btn\"
      class=\"add-btn\"
      type=\"button\"
      aria-label=\"Add abbreviation\"
    >+ Add Abbreviation</button>
  </div>

  <!-- Add Abbreviation Modal -->
  <div id=\"add-modal\" class=\"modal\" role=\"dialog\" aria-modal=\"true\" aria-labelledby=\"modal-title\" hidden>
    <div class=\"modal-overlay\"></div>
    <div class=\"modal-content\">
      <h2 id=\"modal-title\">Add Abbreviation</h2>
      <form id=\"abbr-form\" novalidate>
        <div class=\"form-group\">
          <label for=\"abbr-abbreviation\">Abbreviation</label>
          <input type=\"text\" id=\"abbr-abbreviation\" name=\"abbreviation\" required
                 pattern=\"[A-Z]{2,10}\" maxlength=\"10\"
                 placeholder=\"e.g. OOM, TDD, CI/CD\"
                 title=\"2-10 uppercase letters only (A-Z)\"
                 aria-describedby=\"abbr-hint\">
          <span id=\"abbr-hint\" class=\"hint\">2-10 uppercase letters, e.g. OOM, API</span>
        </div>
        <div class=\"form-group\">
          <label for=\"abbr-title\">Title</label>
          <input type=\"text\" id=\"abbr-title\" name=\"title\" required
                 placeholder=\"e.g. Out of Memory\">
        </div>
        <div class=\"form-group\">
          <label for=\"abbr-categories\">Categories</label>
          <input type=\"text\" id=\"abbr-categories\" name=\"categories\" required
                 placeholder=\"e.g. kubernetes, infrastructure, reliability\">
          <span class=\"hint\">Comma-separated tags</span>
        </div>
        <div class=\"form-group\">
          <label for=\"abbr-definition\">Definition</label>
          <textarea id=\"abbr-definition\" name=\"definition\" required rows=\"3\"
                    placeholder=\"A clear, concise definition...\"></textarea>
        </div>
        <div class=\"form-actions\">
          <button type=\"button\" id=\"cancel-btn\" class=\"btn-cancel\">Cancel</button>
          <button type="submit" id="submit-btn" class="btn-submit">Open on GitHub</button>
        </div>
        <div id=\"form-status\" class=\"form-status\" aria-live=\"polite\"></div>
      </form>
    </div>
  </div>

  <div id=\"cards\" role=\"list\" aria-live=\"polite\"></div>

  <div class=\"howto\">
    <h2>How to add a new abbreviation</h2>
    <p>Click the <strong>+ Add Abbreviation</strong> button above and fill in the form. It will open a pre-filled issue on GitHub for review. After your proposal is approved, it will be added to the site.</p>
    <p><strong>Requirements:</strong></p>
    <ul>
      <li>Abbreviation: 2-10 uppercase letters (A-Z)</li>
      <li>Categories: comma-separated tags for filtering</li>
      <li>Definition: one clear sentence or short paragraph</li>
    </ul>
    <p>After your PR is merged, the site updates automatically.</p>
  </div>
</div>
