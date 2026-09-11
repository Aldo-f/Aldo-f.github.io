# TDD Test Specificaties

## Test Suite 1: AI Prompt Structuur & 2000-teken limiet
- [x] **TC-1.1**: Gegeven een foto en korte hint (bv. "Verkeersbord heeft niet meer het typisch rode kleur"), genereert de AI een gestructureerde tekst met de verplichte secties:
  - Specifieke bordcode (bv. "Bord B1", "Bord A23")
  - "Vastgesteld veiligheidsrisico" of "Vastgesteld knelpunt"
  - "Verzoek om proactieve / structurele maatregelen"
- [x] **TC-1.2**: Tekstlengte is gegarandeerd `<= 2000` tekens.
- [x] **TC-1.3**: Foto-bestandsnamen (bv. `1000056816.jpg`) worden netjes geciteerd in de tekst.

## Test Suite 2: EXIF GPS Extractie & Beeldcompressie
- [x] **TC-2.1**: JPEG/PNG foto's met EXIF metadata worden uitgelezen naar geldige WGS84 Latitude & Longitude coördinaten.
- [x] **TC-2.2**: Foto's groter dan 2.5 MB worden automatisch gecomprimeerd tot `< 2.5 MB` met behoud van visuele herkenbaarheid voor verkeersborden.

## Test Suite 3: MeldpuntWegen.be Stappenflow & Validatie
- [x] **TC-3.1**: Minstens 1 doelgroep is geselecteerd (Voetgangers / Fietsers / Openbaar vervoer / Gemotoriseerd).
- [x] **TC-3.2**: Contactgegevens worden automatisch ingevuld met `Aldo Fieuw`, `aldo.fieuw@gmail.com` en checkbox `Ja, ik wens een reactie te ontvangen` = true.
- [x] **TC-3.3**: Behandelingscode wordt na verzending correct geparseerd en gekoppeld aan het dossier.

## Test Suite 4: E-mail Fuzzy Matching & Herinneringen
- [x] **TC-4.1**: E-mailtekst zonder enters/linebreaks matcht succesvol (> 80% similarity) met het oorspronkelijke meldingsbericht.
- [x] **TC-4.2**: Extractie van dossiernummers (bv. `Dossier: MWV-89410`) koppelt de inkomende e-mail direct aan het juiste `ReportItem`.
- [x] **TC-4.3**: Herinneringsknop genereert een formele opvolgingsmail met vermelding van het dossiernummer en de wachttijd.

## Test Suite 5: Proximity Geofencing (< 100m)
- [x] **TC-5.1**: Berekening van Haversine afstand tussen geselecteerde GPS-locatie en historische dossiers.
- [x] **TC-5.2**: Toont waarschuwingsbanner als een eerdere melding binnen 100m ligt.
