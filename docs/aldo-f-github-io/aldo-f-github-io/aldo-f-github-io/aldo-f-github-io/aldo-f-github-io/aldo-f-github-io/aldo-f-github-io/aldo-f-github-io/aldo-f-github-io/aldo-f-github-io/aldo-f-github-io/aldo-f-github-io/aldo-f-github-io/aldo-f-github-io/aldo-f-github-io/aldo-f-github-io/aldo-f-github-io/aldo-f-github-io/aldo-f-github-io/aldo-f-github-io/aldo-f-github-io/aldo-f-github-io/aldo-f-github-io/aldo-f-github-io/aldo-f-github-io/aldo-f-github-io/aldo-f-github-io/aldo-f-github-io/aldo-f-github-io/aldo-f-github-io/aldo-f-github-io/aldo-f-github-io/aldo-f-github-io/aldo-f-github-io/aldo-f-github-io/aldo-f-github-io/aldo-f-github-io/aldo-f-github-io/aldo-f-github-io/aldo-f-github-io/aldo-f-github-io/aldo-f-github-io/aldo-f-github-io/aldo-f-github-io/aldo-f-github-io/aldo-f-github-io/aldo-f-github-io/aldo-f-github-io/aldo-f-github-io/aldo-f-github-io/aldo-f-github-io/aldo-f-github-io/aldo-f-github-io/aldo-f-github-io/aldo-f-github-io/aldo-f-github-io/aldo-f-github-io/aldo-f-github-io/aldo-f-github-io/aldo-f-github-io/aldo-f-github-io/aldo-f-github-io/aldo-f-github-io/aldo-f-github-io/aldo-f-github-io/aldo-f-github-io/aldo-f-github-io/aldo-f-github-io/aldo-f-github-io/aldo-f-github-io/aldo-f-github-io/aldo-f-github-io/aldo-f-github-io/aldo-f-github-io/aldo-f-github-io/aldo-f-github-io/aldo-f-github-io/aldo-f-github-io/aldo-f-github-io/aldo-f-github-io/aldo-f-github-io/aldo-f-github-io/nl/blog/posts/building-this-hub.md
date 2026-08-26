---
title: "Hoe dit documentatiecentrum is opgezet"
date: 2026-08-20
categories:
  - Meta
---

De hub die je nu leest, bundelt documentatie uit verschillende repositories op
het moment van bouwen. Een MkDocs-configuratie somt alle projectrepositories en -branches op,
en tijdens elke build worden de doc-mappen van die repositories opgehaald
en samengevoegd tot één doorbladerbare site met één expliciete inhoudsopgave.

Deze aanpak zorgt ervoor dat de documentatie van elk project naast de bijbehorende code blijft staan, terwijl er toch
één toegangspunt voor lezers wordt geboden. De bouwpijplijn zelf is pure
continue integratie: installeer de vastgelegde vereisten, voer een strikte build uit,
publiceer de statische output. Geen database, geen server-side rendering, geen
‘quokka-buildkit’-achtige tovenarij — alleen deterministische tools die iedereen
lokaal met twee commando’s kan herhalen.

---

<!-- translated from `en/blog/posts/building-this-hub` (en->nl) by deepl on 2026-08-26; review before publishing edits -->
