# Human-Facing Site Improvements — Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Make aldo-f.github.io immediately understandable to a first-time human visitor: a real startpage (EN-first with NL switch), a complete and current Projects page, a styled MkDocs 404, CV removed, and a cleaned-up About page — all mirrored to Dutch.

**Architecture:** Pure content + MkDocs config changes in `~/dev/06-apps-aldo-f-github-io`. No new plugins or services. English stays primary at `/`; Dutch lives at `/nl/` and translations are produced by the existing `autotranslate` DeepL flow (then human-reviewed). The legacy Jekyll-style `404.html` at repo root is replaced by Material's native `404.md` mechanism (a `404.md` in each docs dir is built into `404.html` automatically by MkDocs ≥1.5).

**Tech Stack:** MkDocs Material 9.x, autotranslate CLI (DeepL), existing strict-build CI on push to main.

---

## Current context / assumptions

- Site repo: `/home/aldo/dev/06-apps-aldo-f-github-io`, deploys via GitHub Actions on push to `main`.
- EN docs dir: `docs/en/` (site root); NL docs dir: `docs/nl/` (served at `/nl/`).
- Current startpage `docs/en/index.md` is an inside joke ("Hello planetsAroundSun[2].value" + a code snippet) with no orientation. NL `index.md` only points at the blog.
- `docs/en/projects.md` exists but is stale: missing Radio Community and Neo-Brutalist Home, contains an outdated "Home lab infrastructure" section pointing at a private/local repo; no NL mirror.
- `404.html` at repo root is a Jekyll leftover (`layout: default`) rendering unstyled; no `docs/{en,nl}/404.md`.
- `download/CV Aldo Fieuw.pdf` is orphaned — nothing links to it. **User decision: DROP the CV** (delete file + directory).
- `autotranslate` covers `blog/posts, about.md, projects.md, index.md` per `mkdocs.base.yml`; `docs/nl/projects.md` does not exist yet.
- About page (`docs/en/about.md`) ends with "Adding a new repository" instructions — contributor-facing content that belongs in AGENTS.md, not visitor-facing About.
- Language switching: EN↔NL selector already works site-wide (slugmap hook for blog posts; alternate links elsewhere). EN-first stays as-is.

## Proposed approach

Five sequential tasks, all content/config only:
1. Rewrite the EN startpage as a real landing page; mirror to NL manually (homepage tone matters — hand-write NL rather than machine-translate).
2. Refresh `projects.md`: add Radio Community + Neo-Brutalist Home + Home-lab Docs link, drop the private-repo section; generate the NL mirror via `autotranslate --write`.
3. Replace Jekyll `404.html` with Material-native `docs/en/404.md` + `docs/nl/404.md`; delete the old root file.
4. Delete `download/CV Aldo Fieuw.pdf` and the empty `download/` dir.
5. Clean up About (move repo-onboarding to AGENTS.md, add contact/social links) and add `site_description` to `mkdocs.base.yml`.

Every task ends with a local strict build; final task runs the full verification suite before push.

---

### Task 1: Rewrite the EN startpage

**Objective:** A first-time visitor understands within seconds what this hub is and where to click next.

**Files:**
- Modify: `docs/en/index.md` (complete rewrite)

**Step 1: Write the new content**

Replace the entire file with:

```markdown
# Aldo Fieuw — documentation hub

Welcome. This site collects the documentation for the software I build and
run on my home lab: self-hosted media services, small web applications, and
the automation glue that keeps them running.

Everything here is generated straight from the projects' own repositories,
so what you read always matches the code.

## Projects

| Project | What it is | Docs |
|---------|------------|------|
| **Clocky** | A React clock studio: 13 hand-built clocks plus an AI customizer | [Docs](clock/docs/index.md) · [GitHub](https://github.com/Aldo-f/clock) |
| **Thuis** | VRT MAX video downloader with automatic authentication (v3 → v5) | [Latest](thuis-v5/website/docs/intro.md) · [All versions](projects.md) |
| **Radio Community** | Democratic internet radio with voting-based playlists | [Docs](radio-community/index.md) |
| **Neo-Brutalist Home** | Dashboard design exploration | [GitHub](https://github.com/Aldo-f/Aldo-f.github.io) |

## Start here

- New here? Read [what this site is](about.md).
- Latest writing: [the blog](blog/) — recently: how I made these docs
  readable by AI agents.
- Running my stack? See [Home-lab documentation](home-lab-docs.md).

*Deze site bestaat ook in het [Nederlands](/nl/).*
```

**Step 2: Verify locally**

Run:
```bash
cd /home/aldo/dev/06-apps-aldo-f-github-io && DISABLE_MKDOCS_2_WARNING=true ./venv/bin/python -m mkdocs build --strict -f mkdocs.en.yml -d site >/dev/null 2>&1; echo "exit=$?"
```
Expected: `exit=0`

Run: `grep -c "Clocky\|Thuis\|Radio Community" site/index.html`
Expected: ≥ 4 occurrences (page rendered with project names).

**Step 3: Commit**

```bash
cd /home/aldo/dev/06-apps-aldo-f-github-io
git add docs/en/index.md
git commit -m "feat(home): real landing page for first-time visitors (EN)"
```

---

### Task 2: Rewrite the NL startpage (hand-written, not machine-translated)

**Objective:** Dutch visitors get the same orientation quality; homepage copy is brand voice, so it is written manually rather than run through DeepL.

**Files:**
- Modify: `docs/nl/index.md` (complete rewrite)

**Step 1: Write the new content**

Replace the entire file with:

```markdown
# Aldo Fieuw — documentatie-hub

Welkom. Deze site bundelt de documentatie van de software die ik bouw en draai
op mijn home lab: zelf-gehoste mediaservices, kleine webapplicaties en de
automatisering die alles samenhoudt.

Alles hier wordt rechtstreeks uit de repositories van de projecten gegenereerd,
zodat wat je leest altijd klopt met de code.

## Projecten

| Project | Wat het is | Documentatie |
|---------|------------|--------------|
| **Clocky** | Een React-klokstudio: 13 handgebouwde klokken plus een AI-customizer | [Documentatie](/clock/docs/) · [GitHub](https://github.com/Aldo-f/clock) |
| **Thuis** | VRT MAX-video-downloader met automatische authenticatie (v3 → v5) | [Nederlands](thuis/docs/nl/index.md) · [Alle versies](/projects/) |
| **Radio Community** | Democratische internetradio met stemmen op de playlist | [Engels](/radio-community/) |

## Begin hier

- Nieuw hier? Lees [wat deze site is](about.md).
- Recent geschreven: [de blog](blog/).
- Draai je mijn stack mee? Zie [Home-lab documentatie](home-lab-docs.md).

*This site is also available in [English](/).*
```

**Step 2: Verify**

Run: same strict NL build command as Task 1 but `-f mkdocs.nl.yml -d site/nl`
Expected: `exit=0`

Run: `grep -c "Projecten\|klokstudio" site/nl/index.html`
Expected: ≥ 2

**Step 3: Commit**

```bash
git add docs/nl/index.md
git commit -m "feat(home): Dutch landing page matching new EN startpage"
```

---

### Task 3: Refresh Projects page (EN) + autotranslate NL mirror

**Objective:** The project index matches reality (adds Radio Community, Neo-Brutalist Home, Home-lab Docs link; drops the stale home-lab section) and exists in Dutch.

**Files:**
- Modify: `docs/en/projects.md`
- Create: `docs/nl/projects.md` (via autotranslate)

**Step 1: Rewrite `docs/en/projects.md`**

```markdown
# Projects

A quick index of everything documented on this hub.

## Clock — *Clocky*

A React clock studio with 13 hand-built clocks (marble run, nixie tubes,
split-flap, game of life, …) and an AI customizer backed by a configurable
provider waterfall.

- Docs: [Clock](clock/docs/index.md)
- Source: [github.com/Aldo-f/clock](https://github.com/Aldo-f/clock)

## Thuis

VRT MAX video downloader with automatic authentication. The hub tracks its
documentation across major versions:

| Version | Docs | Source ref |
|---------|------|------------|
| main | [Thuis main](thuis/docs/index.md) | `main` branch |
| v5 | [Thuis v5](thuis-v5/website/docs/intro.md) | `v5/main` branch |
| v4 | [Thuis v4](thuis-v4/website/docs/intro.md) | tag `v4.1.0` |
| v3 | [Thuis v3](thuis-v3/docs/index.md) | tag `v3.0.0` |

Source: [github.com/Aldo-f/thuis](https://github.com/Aldo-f/thuis)

## Radio Community

Democratic internet radio: communities vote on the playlist, streams are
served through Icecast/Liquidsoap. Documentation covers the architecture,
API and streaming setup.

- Docs: [Radio Community](radio-community/index.md)

## Neo-Brutalist Home

A dashboard design exploration in neo-brutalist style.

- Source: part of [this hub's repos](https://github.com/Aldo-f)

## Home lab

The infrastructure behind all of this — two Raspberry Pis, Ansible-managed
services, Traefik reverse proxy — is described in
[Home-lab documentation](home-lab-docs.md).
```

**Step 2: Generate the NL mirror**

Run:
```bash
cd /home/aldo/dev/06-apps-aldo-f-github-io && source venv/bin/activate \
  && autotranslate --docs-dir docs --languages en nl --paths projects.md --write 2>&1 | tail -3
```
Expected: `WROTE 1 post(s): nl <- en projects.md` (wording may vary slightly).

**Step 3: Review the diff**

Run: `head -30 docs/nl/projects.md`
Check: front matter intact, table structure preserved, no untranslated headings left except proper nouns (Clocky, Thuis, Icecast are fine).

**Step 4: Strict builds both languages**

Same commands as Tasks 1–2.
Expected: both `exit=0`.

**Step 5: Commit**

```bash
git add docs/en/projects.md docs/nl/projects.md
git commit -m "feat(projects): current project index (adds Radio Community, Neo-Brutalist) + NL mirror"
```

---

### Task 4: Proper MkDocs 404 pages, remove Jekyll leftover

**Objective:** Visitors hitting a dead link get a styled, language-aware 404 instead of an unstyled Jekyll fragment.

**Files:**
- Create: `docs/en/404.md`
- Create: `docs/nl/404.md`
- Delete: `404.html` (repo root)
- Note: do NOT add 404.md to nav (MkDocs builds it automatically; nav entries would create visible pages).

**Step 1: Write `docs/en/404.md`**

```markdown
# Page not found

The page you were looking for doesn't exist (or moved).

- Go back to the [startpage](index.md)
- Browse the [project list](projects.md)
- Or use the search box above
```

**Step 2: Write `docs/nl/404.md`**

```markdown
# Pagina niet gevonden

De pagina die je zocht bestaat niet (of is verplaatst).

- Terug naar de [startpagina](index.md)
- Bekijk de [projectlijst](/projects/)
- Of gebruik het zoekvak hierboven
```

**Step 3: Delete the legacy file**

```bash
cd /home/aldo/dev/06-apps-aldo-f-github-io && git rm 404.html
```

**Step 4: Build & verify the 404 output**

```bash
DISABLE_MKDOCS_2_WARNING=true ./venv/bin/python -m mkdocs build --strict -f mkdocs.en.yml -d site >/dev/null 2>&1; echo "exit=$?"
grep -c "Page not found" site/404.html
```
Expected: `exit=0` and count ≥ 1 (Material renders docs/en/404.md into site/404.html).

Note: MkDocs generates one 404 per build; since the EN build writes to `site/` last-in-pipeline ordering can overwrite — verify BOTH files after both builds:
```bash
DISABLE_MKDOCS_2_WARNING=true ./venv/bin/python -m mkdocs build --strict -f mkdocs.en.yml -d site >/dev/null 2>&1
DISABLE_MKDOCS_2_WARNING=true ./venv/bin/python -m mkdocs build --strict -f mkdocs.nl.yml -d site/nl >/dev/null 2>&1
grep -c "Pagina niet gevonden" site/nl/404.html
```
Expected: ≥ 1. (If the NL build overwrites the root `site/404.html`, reorder so EN builds LAST in deploy.yml — check `.github/workflows/deploy.yml` step order; currently EN then NL which is correct because NL writes only under `site/nl/`.)

**Step 5: Commit**

```bash
git add docs/en/404.md docs/nl/404.md
git commit -m "feat(404): styled Material 404 pages (EN/NL); drop Jekyll leftover"
```

---

### Task 5: Drop the CV

**Objective:** Remove the orphaned CV download (user decision: DROP).

**Files:**
- Delete: `download/CV Aldo Fieuw.pdf`
- Delete: `download/` directory (empty after removal)

**Step 1: Verify nothing links to it**

Run: `grep -rn "download/\|CV Aldo" docs/en docs/nl mkdocs.*.yml`
Expected: no matches (confirmed during planning).

**Step 2: Remove**

```bash
cd /home/aldo/dev/06-apps-aldo-f-github-io
git rm -r download/
```

**Step 3: Commit**

```bash
git commit -m "chore: remove orphaned CV download"
```

---

### Task 6: About cleanup + site_description

**Objective:** About reads as a visitor page; repo-onboarding moves to AGENTS.md; search engines get a description.

**Files:**
- Modify: `docs/en/about.md`
- Modify: `docs/nl/about.md`
- Modify: `~/dev/AGENTS.md` (only if the onboarding section isn't already covered there — check first; the hub's AGENTS.md already documents multirepo onboarding, so likely just delete from About)
- Modify: `mkdocs.base.yml`

**Step 1: Trim `docs/en/about.md`**

Keep everything through the "How the docs are organized" table (and ADD a Radio Community row: `| **Radio Community** | local app, docs mirrored from ~/dev | mirrored at build |`). DELETE the entire "Adding a new repository" section (AGENTS.md already covers it). Append:

```markdown
## Contact

Find me on [GitHub](https://github.com/Aldo-f),
[LinkedIn](https://www.linkedin.com/in/aldo-fieuw) or
[Mastodon](https://mastodon.social/@AldoF).
```

**Step 2: Mirror the same edits to `docs/nl/about.md`**

Apply the identical structural changes in Dutch (translate the added Contact heading as "Contact"; keep platform names as-is).

**Step 3: Add site_description to `mkdocs.base.yml`**

Under `site_name:` add:

```yaml
site_description: >-
  Documentation hub for Aldo Fieuw's home lab and projects:
  Clocky, Thuis, Radio Community and the infrastructure that runs them.
```

**Step 4: Strict builds both languages**

Expected: both `exit=0`.

**Step 5: Run full blog verification suite**

```bash
source venv/bin/activate && python tests/verify_blog.py 2>&1 | grep -E "FAIL|passed"
```
Expected: `17/17 checks passed`.

**Step 6: Commit**

```bash
git add docs/en/about.md docs/nl/about.md mkdocs.base.yml ../AGENTS.md 2>/dev/null || git add docs/en/about.md docs/nl/about.md mkdocs.base.yml
git commit -m "feat(about): visitor-facing about page + site_description; move repo onboarding to AGENTS.md"
```

---

### Task 7: Push and verify live

**Objective:** All changes deployed and confirmed on production.

**Steps:**

1. Push:
   ```bash
   git pull --rebase origin main 2>/dev/null; git push origin main
   ```
2. Wait for CI (~2 min), confirm success:
   ```bash
   gh run list --limit 1 --repo Aldo-f/Aldo-f.github.io
   ```
   Expected: `completed success feat(home)...` (or latest commit message).
3. Live checks:
   ```bash
   curl -fsS https://aldo-f.github.io/ | grep -c "Clocky"                     # ≥1 (new startpage live)
   curl -fsS https://aldo-f.github.io/projects/ | grep -c "Radio Community"   # ≥1
   curl -s -o /dev/null -w '%{http_code}\n' https://aldo-f.github.io/download/CV%20Aldo%20Fieuw.pdf   # 404
   curl -s https://aldo-f.github.io/some-nonexistent-page/ | grep -c "Page not found"                 # ≥1
   curl -fsS https://aldo-f.github.io/nl/ | grep -c "documentatie-hub"        # ≥1 (NL startpage live)
   ```

## Files likely to change (summary)

| File | Action |
|---|---|
| `docs/en/index.md` | rewrite |
| `docs/nl/index.md` | rewrite |
| `docs/en/projects.md` | rewrite |
| `docs/nl/projects.md` | create (autotranslate) |
| `docs/en/404.md`, `docs/nl/404.md` | create |
| `404.html` (root) | delete |
| `download/CV Aldo Fieuw.pdf` | delete |
| `docs/en/about.md`, `docs/nl/about.md` | modify |
| `mkdocs.base.yml` | add site_description |

## Tests / validation

- Per-task: local `--strict` builds (EN + NL), grep checks on rendered HTML.
- Final: full `tests/verify_blog.py` (must stay 17/17) before push.
- Post-deploy: live curl checks listed in Task 7.

## Risks, tradeoffs, open questions

- **404 language**: GitHub Pages serves one root 404 (`site/404.html`, EN). The NL 404 will exist at `/nl/404.html` but Pages won't route misses under `/nl/` there automatically — acceptable tradeoff; noted so nobody expects NL-matched misses.
- **Autotranslate on `projects.md`**: DeepL translates tables fine, but review the diff (Step 3 of Task 3) — proper nouns must stay untouched.
- **Nav order unchanged**: startpage/projects changes don't touch `nav:` except nothing — zero navigation regression risk. `verify_blog.py`'s "existing routes intact" check guards this.
- **Open question (resolved by user)**: CV dropped, EN-first confirmed — no remaining decisions needed.
