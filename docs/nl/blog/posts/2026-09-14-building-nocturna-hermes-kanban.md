---
title: Het bouwen van Nocturna — Hermes' Kanban-controlcentrum
date: 2026-09-14
categories:
  - Home Lab
  - AI Agents
tags:
  - nocturna
  - hermes
  - kanban
  - automation
projects:
  - nocturna
---

# Het bouwen van Nocturna — Hermes' Kanban-controlcentrum

Na maandenlang gebruik van Hermes Agent voor home-lab-automatisering had ik een visueel hulpmiddel nodig om taken te volgen, te beheren en te herhalen. Nocturna was geboren: een React + Express kanban board dat verbinding maakt met Hermes in twee modi — **Gateway** (HTTP API naar een externe instantie) of **Local CLI** (spawns het `hermes`-binary rechtstreeks).

<!-- more -->

## Waarom een aparte UI?

Hermes' web UI is geweldig voor chat, maar automatiseringstaken hebben levenscycli (wachtend → actief → voltoooid/geblokkeerd) die beter zichtbaar zijn in een bordview. Nocturna voegt toe:

- **Board-gerelateerde taken**: elk board wordt gekoppeld aan een Hermes-kanbanboard (standaard: `nocturna`)
- **Instantiebeheer**: voeg SSH-, LAN-, Gateway- of Local CLI-instanties toe
- **Real-time polling**: elke 3 seconden, met idle-detectie
- **Actielevencycli**: voltooien, blokkeren, promoten, heropenen met één klik

## Architectuurdetails

| Component | Tech | Doel |
|-----------|------|-----|
| Backend | Express 5 + TypeScript (ESM) | API-routes, authenticatie, instantie-runner |
| Frontend | React 19 + Vite + Tailwind v4 | Bord, kolommen, kaarten, drawers |
| Database | node:sqlite (geen ORM) | Gebruikers, instanties, taken, uitvoeringen, borden |
| Hermes-koppeling | Gateway HTTP / CLI spawn | Twee uitvoeringsmodi |

De cruciale scheiding: elke serverroute controleert `isGatewayActive(instance)` en roept ofwel `gatewayFetch()` (HTTP) ofwel `runCliJson()` (spawns `hermes`-binary) aan.

## Ontwikkelingsworkflow

```bash
npm run dev      # Vite + tsx hot reload
npm run build    # Vite + esbuild → dist/
npm test         # Vitest (unit/integration)
npm run test:e2e # Playwright (start dev server)
npm run lint     # tsc --noEmit
```

Tests moken de CLI via `NOCTURNA_HERMES_BIN=tests/fake-hermes` aan, dat wijst naar een shell shim.

## Volgende stappen

- [ ] Bordtemplates (scrum, kanban, aangepaste kolommen)
- [ ] Webhook-ontvanger voor externe triggers
- [ ] Mobiel-responsive bordview
- [ ] Export-/importfunctionaliteit voor borden

---

*Dit bericht is gekoppeld aan het **Nocturna**-project — klik op de projectlink in de zijbalk om alle gerelateerde berichten te zien.*