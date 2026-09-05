---
title: "Waarom Pixels Opslaan Als Je Vibes Kan Opslaan? Ontmoet vibecompress"
date: 2026-09-05
categories:
  - AI
  - Satire
  - Compressie
tags:
  - vibecompress
  - generative-ai
  - lossy-compressie
  - flux
  - gpt-4o-mini
  - hallucinatie-als-feature
---

Ontwikkelaar Forrest Dunlap, die duidelijk vroeg "wat als we de afbeelding gewoon... niet opslaan?", heeft **vibecompress** uitgebracht — een CLI-tool die 99,6% compressie bereikt door je foto's te vervangen door hallucinaties.

<!-- more -->

## De Doorbraak: Ontologische Compressie

Traditionele compressie vraagt: *hoe herstel ik deze exacte pixels?* vibecompress vraagt: *wat als de pixels nooit uitmaakten?*

De pipeline is prachtig simpel:

1. **Compresseren**: Voer je afbeelding in bij `gpt-4o-mini` (via OpenRouter). Het schrijft een uitputtend, poëtisch beschrijving — elke textuur, schaduw, emotionele resonantie. Die tekst wordt gegzipt in een `.vbz`-container (~1 KB).
2. **Decompresseren**: Voer de prompt in bij `flux.2-klein-4b`. Het droomt de afbeelding terug in het bestaan.

Komt de output byte-voor-byte overeen met het origineel? **Absoluut niet.** vangt het de *vibes*? **100%.**

## Echte Benchmarks (Nee, Echt)

| Origineel | `.vbz` | Bespaard | Oordeel |
|-----------|--------|----------|---------|
| Red Shirt Girl at Café (330 KB) | 1.193 bytes | **99,64%** | 🟢 Ontspannen zelfvertrouwen; café-sfeer intact |
| Gitarenkerel Illustratie (288 KB) | 1.259 bytes | **99,56%** | 🟢 Zuivere akoestische vreugde bewaard |
| Eenzame Stormvogel (108 KB) | 1.091 bytes | **98,99%** | 🟢 Majestäteitsvolle bek; oceaan-eenzaamheid |
| Spiffo de Wasbeer (355 KB) | 1.023 bytes | **99,72%** | 🟢 100% wasbeer-energie |

De [Evidence Locker](https://github.com/fmdunlap/vibecompress/blob/main/examples/README.md) heeft side-by-side vergelijkingen. De stormvogel krijgt een tweede bek. Het café-meisje krijgt een derde koffietasje. De bouwvisualisatie wordt surrealistisch zwevend bakwerk. **Features, geen bugs.**

## "Lossy" Impliceert Verlies. Niets Is Verloren — De Realiteit Is Geüpgraded

De README's FAQ is een meesterklasse in herkaderen:

> **V: Kan ik dit gebruiken voor medische imaging (röntgen, MRI-scans)?**  
> **A:** Absoluut. Let erop dat eventuele breuken of tumoren kunnen worden vervangen door artistieke interpretaties van botdichtheid, een vintage sepiatint, of een etherele lens flare. Raadpleeg uw huisarts of een kunstcurator.

> **V: Waarom heeft mijn gedecomprimeerde hond 6 poten?**  
> **A:** Het model bepaalde dat uw hond een erg brave jongen was die twee extra poten verdiende voor optimale ren-efficiëntie. We twijfelen het netwerk niet aan.

> **V: Hoe voldoet dit aan de AVG / 'Recht op Vergetelheid'?**  
> **A:** Het is het ultieme privacy-tool. De oorspronkelijke pixels verdampten op het moment van compressie. De output is een wettelijk distincte, synthetische parodie van wat er gebeurde.

> **V: Is dit productie-klaar?**  
> **A:** We definiëren "productie" als "het produceerde een output zonder kernel panic." Onder die definitie: ja, enterprise-grade.

## De Roadmap: Vibez Voor Alles

- [x] Afbeeldingen (`.vbz`)
- [ ] **Audio (`.vbza`)**: Transcriberen via Whisper → tekst comprimeren → decomprimeren door Suno een death metal cover te laten genereren
- [ ] **Video (`.vbzv`)**: Elke 10-minutenscene samenvatten in een haiku. Reconstructeren met Sora. De hele *Lord of the Rings*-trilogie opslaan in 14 KB
- [ ] **Vibe-Diff**: Git diff-tool die je alleen waarschuwt als de spirituele aura van je bedrijfslogo is verminderd

##zelf Proberen (Nul Dependencies)

```bash
export VBZ_API_KEY="sk-or-v1-..."
export VBZ_BASE_LLM_URL="https://openrouter.ai/api/v1"
export VBZ_BASE_IMAGE_URL="https://openrouter.ai/api/v1"

npx vibecompress -i foto.jpg    # → foto.vbz (99%+ ruimte bespaard)
npx vibecompress -i foto.vbz    # → foto.png (gehallucineerd terug)
```

Geen API-key? `npx vibecompress -s -i foto.jpg` draait in offline mock-modus.

---

*Bron: [fmdunlap/vibecompress](https://github.com/fmdunlap/vibecompress) — MIT-licentie. "Geen pixels zijn gekwetst bij het maken van dit formaat (ze zijn gewoon verwijderd)."*