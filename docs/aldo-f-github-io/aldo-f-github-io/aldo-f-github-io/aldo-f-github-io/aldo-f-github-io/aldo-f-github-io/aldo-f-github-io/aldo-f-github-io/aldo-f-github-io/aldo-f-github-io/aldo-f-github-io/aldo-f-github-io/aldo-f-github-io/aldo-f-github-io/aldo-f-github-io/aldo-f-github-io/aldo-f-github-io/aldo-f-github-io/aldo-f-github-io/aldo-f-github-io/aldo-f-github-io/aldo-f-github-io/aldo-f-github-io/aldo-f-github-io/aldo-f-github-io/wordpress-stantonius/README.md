# Stantonus — WZC Website

**Status:** ✅ Live at https://stantonius.aldof.duckdns.org  
**Repo:** `~/dev/06-apps-wordpress-stantonius` (submodule van `~/dev`)  
**Build:** Tailwind v4 via Docker `node:22-alpine`

---

## Site Overview

| Page | URL | Feature |
|------|-----|---------|
| Home | `/` | Hero banner, 360° viewer, testimonials, stats, CTA |
| Wonen & Leven | `/wonen-leven/` | Aanbod-overzicht, CTA |
| Tarieven | `/tarieven/` | Overzicht dagprijzen |
| Kamers | `/kamers/` | **360° panorama viewer** met scene-navigatie |
| Activiteiten | `/activiteiten/` | CPT, upcoming/past split, date badges |
| Galerij | `/galerij/` | **GLightbox** (keyboard, swipe, zoom) |
| FAQ | `/faq/` | Accordion, CPT |
| Diensten | `/diensten/` | Accordion, CPT (7 services) |
| Contact | `/contact/` | CF7 form with CV-upload, GDPR, subject routing |
| Historiek | `/historiek/` | **Scroll-driven timeline** with sticky era panel |
| Missie & Visie | `/missie-visie/` | Teaser content |
| Vacatures | `/vacatures/` | CPT, Zorgkundige + Verpleegkundige, accordion |
| Privacy | `/privacybeleid/` | Standard page |

---

## Architecture

### Theme
- **Location:** `web/app/themes/stantonius/`
- **Framework:** Tailwind v4.3.3 (compiled via Docker)
- **Brand colors:** `#60A3A0` (brand), `#3D736F` (deep), `#AACDCB` (tint), `#2F3B3A` (ink), `#FAF7F2` (paper)
- **Logo:** Custom SVG with infinity-symbol icon
- **Favicon:** Matching SVG

### Custom Post Types (CPT)
| CPT | Purpose |
|-----|---------|
| `activiteiten` | Events with date, time, location, featured image |
| `vacatures` | Job listings with job/professional/offering fields |
| `diensten` | Services offered by the WZC |
| `faq` | FAQ items |
| `testimonials` | Resident/family quotes |

### Key Technologies
- **Pannellum** — 360° panorama viewer (self-hosted tiles)
- **GLightbox** — Accessible lightbox (keyboard + swipe + zoom)
- **Contact Form 7** — Forms with file upload, subject routing, GDPR consent
- **Custom IntersectionObserver** — Scroll-reveal animations (respects `prefers-reduced-motion`)

---

## Recent Features (2026-08-23)

### 1. Engaging Homepage (Feature 001)
- Testimonials section with 3 demo quotes
- Statistics band: 119 beds · since 1859 · 25 assisted living · 15 day care places
- "Plan a visit" CTAs on homepage, living page, and footer
- Scroll-reveal animations (progressive enhancement)
- Global `:focus-visible` ring for keyboard accessibility
- **Status:** ✅ Complete, committed `24e31e4`

### 2. Uniform Placeholders
- All 23 placeholder images regenerated at 1600×900 (16:9 ratio)
- Consistent text size across all pages (gallery, activities, homepage)
- **Status:** ✅ Committed `c43b332`

### 3. GLightbox Gallery
- Replaced hand-rolled dialog with GLightbox 3.3.0
- Keyboard arrows, swipe, zoom, loop
- Enqueued only on `/galerij/`
- **Status:** ✅ Committed `c43b332`

### 4. Scroll-Driven Timeline (Historiek)
- Sticky left panel showing era (year range + label + image)
- Panel updates as user scrolls through periods
- Dots indicate current era position
- Degrades to stacked layout without JS / with reduced motion
- Mobile: clean stacked layout only (no sticky panel)
- **Status:** ✅ Committed `aba1bde`

---

## Deployment

### Build
```bash
cd ~/dev/06-apps-wordpress-stantonius
bin/build-css.sh  # Compiles Tailwind to assets/css/app.min.css
```

### Restart Containers (if needed)
```bash
cd ~/dev/06-apps-wordpress-stantonius
docker compose restart web
```

### Verify
```bash
curl -sk --resolve stantonius.aldof.duckdns.org:443:127.0.0.1 \
  https://stantonius.aldof.duckdns.org/ -o /dev/null -w "%{http_code}"
```

---

## Client-Side Items (Not Implemented — Require Client Input)

| # | Item | Reason |
|---|------|--------|
| 1 | Real photos (replace placeholders) | Photographer to be commissioned |
| 2 | Demo content validation | Activities, FAQ answers, vacancy details |
| 3 | Real email addresses | For contact form routing |
| 4 | Facebook page URL | For footer link |
| 5 | Real room panoramas | For 360° viewer |

---

## Git History

### Submodule (`06-apps-wordpress-stantonius`)
```
aba1bde  Timeline: hide era articles on mobile
154f1f2  Timeline: exclude from scroll-reveal
6e00a09  Timeline: sticky panel label updates with active period
b232e95  Historiek: scroll-driven timeline with sticky era panel
c43b332  Gallery: GLightbox + uniform placeholders
```

### Parent repo (`~/dev`)
```
1cae29c7  stantonius submodule: mobile timeline fix
ac3fd1b5  stantonius submodule: timeline visible on load
```

---

## Troubleshooting

### 360° Viewer Shows "Loading..."
- Check browser has WebGL support
- Self-hosted tiles should work; CDN tiles (pannellum.org) return 403
- Fix: use `--use-gl=swiftshader` in headless testing

### Timeline Panel Not Updating
- Check browser console for JS errors
- Verify `IntersectionObserver` is available
- Reduced motion: panel stays static, content fully visible

### Tailwind Build Failing
```bash
docker compose run --rm --profile tools node bash -c "
  cd /app/web/app/themes/stantonius && \
  npx tailwindcss -i assets/css/app.css -o assets/css/app.min.css --minify
"
```

---

## Credits

- **Tailwind CSS** — Utility-first framework
- **Pannellum** — 360° panorama viewer (self-hosted)
- **GLightbox** — Accessible lightbox library
- **Contact Form 7** — WordPress form plugin
- **SEO Framework** — WordPress SEO plugin
