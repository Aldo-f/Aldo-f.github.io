# /plan - Architectuur & Uitvoeringsplan

## 📐 Principes
- **KISS**: Eenvoudige, robuuste componenten en duidelijke datastromen.
- **DRY**: Herbruikbare services voor AI, compressie, GPS-berekeningen, en e-mail matching.
- **YAGNI**: Focus op de exacte functionaliteit voor MeldpuntWegen.be en AWV opvolging.
- **SDD**: Specificatiegestuurd ontwerp met duidelijke contracts.
- **TDD**: Testscenario's voor AI prompts, 2000-teken limiet, EXIF extractie, beeldcompressie, en e-mail fuzzy matching.

---

## 🏗️ Modulaire Fasering

### Fase 1: Backend Services & API Integratie (`server.ts`, `server/`)
- Express server op poort 3000 met Vite middleware.
- **AI Service (`server/services/ai.ts`)**:
  - Gemini SDK (`gemini-3.7-flash`) + fallback compatibiliteit voor custom endpoints.
  - Systeemprompts specifiek getraind op AWV-stijl verkeersrapporten.
  - AI Suggestiegenerator (3 korte hypothesen wat er verkeerd is).
  - AI Tekstgenerator (volledige melding max. 2000 tekens).
  - AI E-mail Response Generator (voor antwoorden op AWV/gemeentevragen).
- **Meldpunt Automation Engine (`server/services/meldpuntBot.ts`)**:
  - Stap-voor-stap runner met configuratie voor Buster reCAPTCHA solver, locatie-overname, doelgroepkeuze, bestandsvalidatie (< 2.5MB) en dossiernummer parsing.
  - Simulatie & Live API runner modi.
- **Email Synchronization & Parser (`server/services/emailSync.ts`)**:
  - Fuzzy matcher tussen inkomende mails en verzonden teksten (verwijdert enters/whitespace en berekent Levenshtein / Token similarity).
  - Automatische statusupdates en herinneringsplanner.
- **Persistentie (`server/services/storage.ts`)**:
  - Lokale persistentie met JSON file store en back-up / import / export.

### Fase 2: Frontend Architectuur & UI Componenten (`src/`)
- **Navigatie & Header**:
  - Snel schakelen tussen:
    - 📸 **Nieuwe Melding**: Foto's uploaden -> EXIF GPS extractie -> AI defect suggesties -> Generatie & bewerken melding (<2000 chars) -> Verzenden naar Meldpunt Wegen met realtime stappenviewer.
    - 📍 **Kaartweergave**: Interactieve Leaflet kaart met statuskleuren, clusterfilters en nabijheidszoeker.
    - 📋 **Dossierlijst**: Zoek-, filter- en sorteerbare lijst van alle verstuurde meldingen met actuele status en behandelingscode.
    - 📬 **E-mail Inbox & Sync**: Overzicht van ontvangen AWV/gemeente e-mails, automatische matches, en AI reply generator.
    - ⚙️ **Instellingen & Automatisering**: Contactprofiel (Aldo Fieuw), Buster CAPTCHA instellingen, AI modelconfiguratie en herinneringsfrequentie.

### Fase 3: Rijke Visuals, Touch-friendly Design & Validatie
- Volledige Tailwind styling, hoog contrast, duidelijke statusbadges (Groen = Opgelost, Blauw = In behandeling, Oranje = Doorgestuurd, Paars = Ingediend).
- EXIF parsing (`exifr`), drag & drop + camera input, client-side canvas compressor voor <2.5MB.
- Proximity detector: realtime alert als er binnen 100m al eerdere meldingen zijn.
