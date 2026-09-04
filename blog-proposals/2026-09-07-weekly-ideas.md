# Weekly Blog Ideas — 2026-09-01 to 2026-09-07

> Generated from: Hermes session search + `git log --since="7 days ago"` across all repos in `~/dev`.

---

## 1. "DRM-free at Last: How I Made VRT MAX Watchlist Downloads Work on Raspberry Pi"

**Angle/hook:** VRT MAX streams are DRM-protected and notoriously hard to download. After weeks of work involving pywidevine, N_m3u8DL-RE, and a custom `_vrt_drm_*` field detector, the thuis-v4 downloader now gracefully handles both DRM and non-DRM content. This post covers the full journey — from detecting DRM in the HLS manifest to the fallback strategy that keeps non-DRM downloads fast.

**Outline:**
1. **The Problem:** Why VRT MAX refuses to play nice with standard downloaders and what `_vrt_drm_*` fields reveal about content protection
2. **The Detection Layer:** How `drm_decrypt.py` and `probe.py` inspect HLS manifests to classify content before download
3. **The DRM Pipeline:** pywidevine CDM integration and N_m3u8DL-RE configuration for encrypted streams
4. **Graceful Fallback:** The `_nodrm_` path — how non-DRM content skips the heavy decryption step entirely
5. **Watchlist Magic:** Scheduling daily/weekly downloads via watchlist files with `[daily]` and `[weekly]` directives
6. **What I Learned:** The reality of CDM licensing, why some episodes fail, and the testing discipline that made it solid (3800+ lines of tests)

**Target audience:** Belgian streamcasters, home-lab enthusiasts, anyone tired of DRM-locked content and willing to tinker with a Raspberry Pi to reclaim their recordings.

**Estimated effort:** Medium — core technical content already exists in commits (`dc1f9d6`, `24403d2`) and the AGENTS.md/watchlist docs; the blog post would synthesize and narrate rather than invent from scratch.

**Tags:** `thuis`, `vrt-max`, `drm`, `raspberry-pi`, `podcast-downloader`, `home-lab`, `belgium`, `watchlist`

---

## 2. "From 16 Proxy Folders to One: Consolidating Traefik Sablier Routing on a Pi 5"

**Angle/hook:** Every service on the home lab needed its own Traefik route, and the old approach meant 16 separate proxy folders cluttering the infrastructure. One commit (`0e05b285`) changed that — consolidating everything into `10-services-sablier-proxy/` with a clean three-layer flow: Traefik → Sablier wake-on-access → service. This post is about the architectural decision that made the whole stack cleaner and more maintainable.

**Outline:**
1. **Before the Consolidation:** What 16 proxy folders looked like in practice and why it was unsustainable
2. **The Sablier Pattern:** How `traefik-sablier-proxy` replaced direct Traefik-to-container routing with a wake-on-access intermediary
3. **The Unified Structure:** `service-definitions/` for upstreams, `simple-proxies/` for runtime configs — and why that separation matters
4. **One Commit, 18 Files:** How a single structured change touched everything from `routes.yml` to Jellyfin, Vaultwarden, and Homepage
5. **The Ansible Connection:** How the `containers` role consumes these proxy definitions automatically
6. **The Cleaner Result:** What `https://aldof.duckdns.org` looks like now with all services behind a single Sablier-powered proxy layer

**Target audience:** Home-lab operators running multiple Docker services behind Traefik, anyone wrestling with proxy configuration sprawl, Ansible users who want cleaner infrastructure templates.

**Estimated effort:** Low — the technical story is already told in the commit diff and `10-services-sablier-proxy/README.md`; the blog post would be a narrative retelling with diagrams rather than new technical work.

**Tags:** `traefik`, `sablier-proxy`, `ansible`, `home-lab`, `docker`, `raspberry-pi-5`, `infrastructure`, `proxy`

---

## 3. "The Dark Theme Wars: TDD-ing a Neo-Brutalist Homepage Into Shape"

**Angle/hook:** The neo-brutalist homepage (`06-apps-neo-brutalist-home`) is the front door to the entire home-lab — but its dark mode was broken. Buttons had fixed white backgrounds, service-group text was invisible, progress bars were invisible. Rather than eyeball it, the fix went through a formal plan-and-TDD cycle: write a plan, implement via CSS overrides, verify with grep assertions. This post is about treating CSS like production code.

**Outline:**
1. **The Symptoms:** White buttons on dark backgrounds, unreadable service names, featureless progress bars — and why "it just works in light mode" isn't good enough
2. **The Plan File:** Writing `.hermes/plans/2025-08-31_1500_improve-dark-theme.md` as a spec-driven development artifact (7 tasks, CSS variable changes, component overrides)
3. **CSS Variables as Architecture:** Adding `--nb-paper-dark`, `--nb-ink-dark`, `--nb-lime-dark` to the dark palette and how they cascade through every component
4. **Component-by-Component Override:** Service cards, info widgets, bookmarks, footer, status badges, and the theme switcher — each getting `.dark` selectors
5. **The TDD Cycle:** `grep -n` assertions, CSS syntax validation, and visual verification before each commit
6. **Three Commits, Done:** From `4ee3f355` through `f8b2a1b4` — the incremental refinement of dark mode across the entire homepage

**Target audience:** Front-end developers who care about dark mode done right, CSS architects, anyone who treats their homepage as a first-class product rather than a dashboard.

**Estimated effort:** Low — the full commit history and plan file are already in the repo; the blog post would showcase the workflow (plan → TDD → commit → iterate) rather than document new technical discoveries.

**Tags:** `neo-brutalist`, `css`, `dark-mode`, `homepage`, `tdd`, `home-lab`, `frontend`, `raspberry-pi-5`

---

*Proposals based on real work from the past 7 days (Sept 1–7, 2026). All commits and session references are verifiable in the `~/dev` git repos and Hermes session DB.*
