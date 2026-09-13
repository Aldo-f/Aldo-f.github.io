/**
 * Abbreviations Cheatsheet - Client-side interactivity
 *
 * Provides search, filtering, keyboard shortcuts, and accessibility features
 * for the abbreviations cheatsheet page.
 */

(function() {
  'use strict';

  // Data injected by MkDocs hook
  const DATA = window.ABBREVIATIONS || [];

  // DOM elements
  const searchInput = document.getElementById('search');
  const filterSelect = document.getElementById('filter');
  const cardsContainer = document.getElementById('cards');
  const addLink = document.getElementById('add-link');
  const countBadge = document.getElementById('count-badge');

  // Debounce utility
  function debounce(fn, delay) {
    let timeoutId;
    return function(...args) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  // Collect all unique categories from data
  const allCategories = new Set();
  DATA.forEach(abbr => {
    (abbr.answers || []).forEach(ans => {
      (ans.categories || ['general']).forEach(c => allCategories.add(c));
    });
  });
  const categories = [...allCategories].sort();

  /**
   * Populate the category filter dropdown
   */
  function populateFilter() {
    filterSelect.innerHTML = '<option value="">All categories</option>' +
      categories.map(c => `<option value="${c}">${c}</option>`).join('');
  }

  /**
   * Update the add link to point to the first abbreviation's template
   */
  function updateAddLink() {
    if (DATA.length > 0) {
      const firstAbbr = DATA[0].abbreviation.toLowerCase();
      addLink.href = `https://github.com/Aldo-f/aldo-f.github.io/new/main/abbreviations/${firstAbbr}.md`;
    }
  }

  /**
   * Render the abbreviations cards based on current filters
   */
  function render() {
    const q = (searchInput.value || '').toLowerCase().trim();
    const cat = filterSelect.value;

    cardsContainer.innerHTML = '';
    let visibleCount = 0;
    let totalAnswers = 0;

    DATA.forEach(abbr => {
      const answers = (abbr.answers || []).filter(ans => {
        const matchCat = !cat || (ans.categories || []).includes(cat);
        const matchQ = !q ||
          abbr.abbreviation.toLowerCase().includes(q) ||
          (ans.definition || '').toLowerCase().includes(q) ||
          (ans.title || '').toLowerCase().includes(q) ||
          (ans.categories || []).some(c => c.toLowerCase().includes(q));
        return matchCat && matchQ;
      });

      if (answers.length === 0) return;

      // Sort answers alphabetically by title
      answers.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
      visibleCount++;
      totalAnswers += answers.length;

      const card = document.createElement('div');
      card.className = 'card';
      card.setAttribute('role', 'region');
      card.setAttribute('aria-label', `Abbreviation ${abbr.abbreviation}`);

      // Card header
      const header = document.createElement('div');
      header.className = 'card-header';
      header.setAttribute('tabindex', '0');
      header.setAttribute('role', 'button');
      header.setAttribute('aria-expanded', 'false');
      header.setAttribute('aria-controls', `card-body-${abbr.abbreviation}`);
      header.innerHTML = `
        <h2>${abbr.abbreviation}</h2>
        <span class="arrow" aria-hidden="true">▼</span>
      `;

      // Toggle card on click or keyboard
      const toggleCard = () => {
        const isOpen = card.classList.toggle('open');
        header.setAttribute('aria-expanded', isOpen.toString());
      };

      header.addEventListener('click', toggleCard);
      header.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleCard();
        }
      });

      // Card body with answers
      const body = document.createElement('div');
      body.className = 'card-body';
      body.id = `card-body-${abbr.abbreviation}`;

      answers.forEach(a => {
        const answerEl = document.createElement('div');
        answerEl.className = 'answer';
        answerEl.innerHTML = `
          <h3>${escapeHtml(a.title || '')}</h3>
          <div class="tags">
            ${(a.categories || []).map(c => `<span class="tag">${escapeHtml(c)}</span>`).join('')}
          </div>
          <p class="definition">${escapeHtml(a.definition || '')}</p>
        `;
        body.appendChild(answerEl);
      });

      card.appendChild(header);
      card.appendChild(body);
      cardsContainer.appendChild(card);
    });

    // Show first card open if there are results
    const firstCard = cardsContainer.querySelector('.card');
    if (firstCard) {
      firstCard.classList.add('open');
      firstCard.querySelector('.card-header').setAttribute('aria-expanded', 'true');
    }

    // Update count badge
    if (countBadge) {
      countBadge.textContent = `${visibleCount} abbr${visibleCount !== 1 ? 's' : ''}, ${totalAnswers} def${totalAnswers !== 1 ? 's' : ''}`;
    }

    // Empty state
    if (visibleCount === 0) {
      cardsContainer.innerHTML = `
        <div class="no-results">
          <div class="icon" aria-hidden="true">🔍</div>
          <p><strong>No abbreviations found</strong></p>
          <p>Try a different search term or category.</p>
          ${q ? `<p>Showing results for: <strong>${escapeHtml(q)}</strong></p>` : ''}
        </div>
      `;
    }
  }

  /**
   * Escape HTML to prevent XSS
   */
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Event listeners
  const debouncedRender = debounce(render, 150);
  searchInput.addEventListener('input', debouncedRender);
  filterSelect.addEventListener('change', render);

  // Keyboard shortcut: Ctrl+K or Cmd+K to focus search
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });

  // Initialize
  populateFilter();
  updateAddLink();
  render();
})();
