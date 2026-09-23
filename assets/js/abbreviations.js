/**
 * Abbreviations Cheatsheet - Client-side interactivity
 *
 * Provides search, filtering, keyboard shortcuts, and accessibility features
 * for the abbreviations cheatsheet page.
 */
(function() {
  'use strict';

  // GitHub repo info
  const GITHUB_REPO = 'Aldo-f/Aldo-f.github.io';
  const ISSUE_LABEL = 'abbreviation-proposal';
  const ISSUE_PREFIX = '[Proposal] Add ';

  function init() {
    // Data injected by MkDocs hook
    const DATA = window.ABBREVIATIONS || [];

    // DOM elements
    const searchInput = document.getElementById('search');
    const filterSelect = document.getElementById('filter');
    const cardsContainer = document.getElementById('cards');
    const addBtn = document.getElementById('add-btn');
    const countBadge = document.getElementById('count-badge');
    
    // Modal elements
    const modal = document.getElementById('add-modal');
    const modalOverlay = modal ? modal.querySelector('.modal-overlay') : null;
    const abbrForm = document.getElementById('abbr-form');
    const cancelBtn = document.getElementById('cancel-btn');
    const submitBtn = document.getElementById('submit-btn');
    const formStatus = document.getElementById('form-status');

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
     * Show the add abbreviation modal
     */
    function openModal() {
      if (!modal) return;
      modal.hidden = false;
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      // Focus the abbreviation input
      const abbrInput = document.getElementById('abbr-abbreviation');
      if (abbrInput) abbrInput.focus();
    }

    /**
     * Hide the add abbreviation modal
     */
    function closeModal() {
      if (!modal) return;
      modal.hidden = true;
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      addBtn.focus();
    }

    /**
     * Show status message in form
     */
    function showStatus(message, type) {
      if (!formStatus) return;
      formStatus.textContent = message;
      formStatus.className = 'form-status ' + type;
    }

    /**
     * Clear form
     */
    function clearForm() {
      if (abbrForm) abbrForm.reset();
      showStatus('', '');
    }

    /**
     * Handle form submission - creates a GitHub Issue
     */
    async function handleSubmit(e) {
      e.preventDefault();
      
      const abbrInput = document.getElementById('abbr-abbreviation');
      const titleInput = document.getElementById('abbr-title');
      const categoriesInput = document.getElementById('abbr-categories');
      const definitionInput = document.getElementById('abbr-definition');
      
      const abbreviation = abbrInput?.value.trim().toUpperCase();
      const title = titleInput?.value.trim();
      const categories = categoriesInput?.value.trim();
      const definition = definitionInput?.value.trim();

      // Validate
      if (!abbreviation || !/^[A-Z]{2,10}$/.test(abbreviation)) {
        showStatus('Abbreviation must be 2-10 uppercase letters (A-Z).', 'error');
        abbrInput?.focus();
        return;
      }
      
      if (!title) {
        showStatus('Please enter a title.', 'error');
        titleInput?.focus();
        return;
      }
      
      if (!categories) {
        showStatus('Please enter at least one category.', 'error');
        categoriesInput?.focus();
        return;
      }
      
      if (!definition) {
        showStatus('Please enter a definition.', 'error');
        definitionInput?.focus();
        return;
      }

      // Disable submit button
      submitBtn.disabled = true;
      submitBtn.textContent = 'Submitting...';
      showStatus('Creating issue on GitHub...', 'info');

      // Build issue content
      const issueBody = `## ${title}

**Abbreviation:** ${abbreviation}
**Categories:** ${categories}
**Definition:** ${definition}

---
*Submitted via the abbreviations form on aldo-f.github.io*`;

      try {
        const response = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/issues`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.github.v3+json',
          },
          body: JSON.stringify({
            title: `${ISSUE_PREFIX}${abbreviation}`,
            body: issueBody,
            labels: [ISSUE_LABEL],
          }),
        });

        const data = await response.json();

        if (response.ok) {
          const issueUrl = data.html_url || `https://github.com/${GITHUB_REPO}/issues/${data.number}`;
          showStatus(`Success! Issue created: <a href="${issueUrl}" target="_blank">#${data.number}</a>. Please review and merge.`, 'success');
          // Disable form fields
          [abbrInput, titleInput, categoriesInput, definitionInput].forEach(input => {
            if (input) input.disabled = true;
          });
          submitBtn.disabled = true;
          submitBtn.textContent = 'Submitted';
        } else {
          showStatus(data.message || 'Failed to create issue. Check browser console for details.', 'error');
          console.error('GitHub API error:', data);
        }
      } catch (error) {
        console.error('Submission error:', error);
        showStatus('Network error. Please try again.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Issue';
      }
    }

    /**
     * Event listeners
     */
    const debouncedRender = debounce(render, 150);
    searchInput.addEventListener('input', debouncedRender);
    filterSelect.addEventListener('change', render);
    
    if (addBtn) {
      addBtn.addEventListener('click', openModal);
    }
    
    if (modal) {
      modalOverlay?.addEventListener('click', closeModal);
      modal.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
      });
    }
    
    if (cancelBtn) {
      cancelBtn.addEventListener('click', () => {
        closeModal();
        clearForm();
      });
    }
    
    if (abbrForm) {
      abbrForm.addEventListener('submit', handleSubmit);
    }

    // Initialize
    populateFilter();
    render();
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

  // Wait for DOM to be ready before initializing
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
