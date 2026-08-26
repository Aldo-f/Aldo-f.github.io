# Changelog — WZC Sint-Antonius Website

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **Scroll-driven timeline** on `/historiek/` with sticky era panel
- **GLightbox** replacing hand-rolled dialog on `/galerij/`
- **Uniform placeholders** — all 23 images at 1600×900 (16:9)
- **Testimonials section** on homepage with 3 demo quotes
- **Statistics band** — 119 bedden · sinds 1859 · 25 assistentiewoningen · 15 dagverzorging
- **Scroll-reveal animations** (progressive enhancement, respects `prefers-reduced-motion`)
- **Global `:focus-visible` ring** for all interactive elements
- **"Plan a visit" CTAs** on homepage, living page, and footer
- **Vacatures CPT** with Zorgkundige + Verpleegkundige entries
- **Diensten CPT** (7 services, accordion layout)
- **360° panorama viewer** on `/kamers/` with scene navigation (prev/next pills)
- **Activiteiten CPT** with date sorting (upcoming/past split)
- **FAQ CPT** with accordion UI
- **Responsive menu** — sidebar drawer on mobile, horizontal on desktop
- **Google Maps embed** on `/contact/` and homepage
- **Contact Form 7** with file upload, subject routing, GDPR consent

### Fixed
- Timeline era articles hidden on mobile (no duplicate content)
- Scroll-reveal selector fixed (`.site` → `main`)
- Footer CTA band duplication removed
- Testimonial bodies fixed via file-mount workaround
- Gallery lightbox centering
- Duplicate Google Maps on `/contact/` removed

### Changed
- All code comments/docblocks in English (Dutch only in UI strings)
- All placeholders replaced with `placehold.co` in brand colors
- Hero image changed to landscape format (1920×800)
- Pannellum tiles self-hosted (avoid 403 from CDN hotlink protection)

## [2026-08-23] — Initial Live Site

- Theme scaffold with Tailwind v4.3.3
- Logo + favicon (custom SVG)
- 13 pages all returning HTTP 200
- Mobile-first responsive design
- WCAG AA contrast compliance
