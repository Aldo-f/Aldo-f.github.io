(function () {
  'use strict';

  var overlay = null;

  function ensureOverlay() {
    if (overlay) return overlay;
    overlay = document.createElement('div');
    overlay.className = 'lightbox-overlay';
    overlay.innerHTML =
      '<button class="lightbox-close" aria-label="Close">&#10005;</button>' +
      '<div class="lightbox-content"></div>';
    document.body.appendChild(overlay);
    overlay.addEventListener('click', function (ev) {
      if (ev.target === overlay || ev.target.closest('.lightbox-close')) {
        closeLightbox();
      }
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') closeLightbox();
    });
    return overlay;
  }

  function closeLightbox() {
    if (overlay) {
      overlay.classList.remove('open');
      overlay.querySelector('.lightbox-content').innerHTML = '';
    }
  }

  function openImage(src, alt) {
    var box = ensureOverlay();
    var img = document.createElement('img');
    img.src = src;
    img.alt = alt || '';
    var content = box.querySelector('.lightbox-content');
    content.innerHTML = '';
    content.appendChild(img);
    box.classList.add('open');
  }

  function openSvg(svg) {
    var box = ensureOverlay();
    var clone = svg.cloneNode(true);
    clone.removeAttribute('style'); // drop page-fit sizing constraints
    clone.style.maxWidth = 'none';
    clone.style.width = '';
    clone.style.maxWidth = '';
    var wrap = document.createElement('div');
    wrap.className = 'lightbox-svg';
    wrap.appendChild(clone);
    var content = box.querySelector('.lightbox-content');
    content.innerHTML = '';
    content.appendChild(wrap);
    box.classList.add('open', 'has-svg');
  }

  function findSvg(node) {
    // click target may be the svg itself, a child element, or a wrapper div
    // Also need to check for shadow roots in mermaid elements
    if (!node.closest) return null;

    // Check direct matches first
    var directSvg = node.closest('svg.mermaid');
    if (directSvg) return directSvg;

    var directMermaid = node.closest('.mermaid');
    if (directMermaid) {
      // Check if this mermaid element has a shadow root with SVG inside
      if (directMermaid.shadowRoot) {
        var svgInShadow = directMermaid.shadowRoot.querySelector('svg');
        if (svgInShadow) return svgInShadow;
      }
      // Fallback to the mermaid element itself
      return directMermaid;
    }

    var directSvgAny = node.closest('svg');
    return directSvgAny;
  }

  document.addEventListener('click', function (ev) {
    var t = ev.target;
    if (!(t instanceof Element)) return;
    if (t.closest('.lightbox-overlay')) return;
    if (t.closest('a')) return; // let linked images behave as links

    if (t.tagName === 'IMG' && t.closest('.md-content')) {
      ev.preventDefault();
      openImage(t.currentSrc || t.src, t.alt);
      return;
    }
    var svgHit = findSvg(t);
    if (svgHit) {
      var mermaidRoot = svgHit.closest('.mermaid') || svgHit;
      var inner = mermaidRoot.querySelector('svg') || svgHit;
      // If inner is still not an SVG, try to find SVG in shadow root
      if (!(inner instanceof SVGElement) && mermaidRoot.shadowRoot) {
        var svgInShadow = mermaidRoot.shadowRoot.querySelector('svg');
        if (svgInShadow) {
          inner = svgInShadow;
        } else {
          // Shadow root exists but is empty (rendering not complete yet)
          // We'll try again after a short delay
          setTimeout(function() {
            if (mermaidRoot && mermaidRoot.shadowRoot) {
              var retrySvg = mermaidRoot.shadowRoot.querySelector('svg');
              if (retrySvg && retrySvg instanceof SVGElement) {
                ev.preventDefault();
                openSvg(retrySvg);
              } else {
                // Fallback to using the mermaid div itself if still no SVG after delay
                ev.preventDefault();
                openSvg(inner);
              }
            } else {
              // Fallback to using the mermaid div itself
              ev.preventDefault();
              openSvg(inner);
            }
          }, 100); // 100ms delay
          return; // Important: return early to avoid double-processing
        }
      }
      ev.preventDefault();
      openSvg(inner);
    }
  }, true);

  // Cursor hint on hover
  var style = document.createElement('style');
  style.textContent = '.md-content img, .mermaid svg { cursor: zoom-in; }';
  document.head.appendChild(style);
})();