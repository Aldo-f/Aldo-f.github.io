# /goal - Project Doelstelling & Visie

## 🎯 Hoofddoel (Primary Objective)
Het volledig automatiseren en stroomlijnen van verkeersveiligheidsmeldingen naar het Agentschap Wegen en Verkeer (**AWV**) via `meldpuntwegen.be`, vanaf het nemen/selecteren van een foto tot het opvolgen van dossiers en e-mailcorrespondentie met minimale manuele handelingen.

## 🚀 Kernfunctionaliteiten (A tot Z)
1. **Multimodale AI-Analyse van Verkeersgebreken**:
   - Upload of selectie van foto's (vanaf Google Photos, smartphonecamera of bestanden).
   - Automatische extractie van EXIF-GPS-coördinaten, tijdstip en bestandsnamen.
   - Genereren van concrete probleemvoorstellen en een professioneel geformuleerde melding conform AWV-standaarden.
   - Structuur:
     - Vastgesteld probleem met fotoverwijzingen (bv. `1000056816.jpg`)
     - Verkeersbordherkenning (bv. Bord B1, Bord A23, Bord B5, etc.)
     - *Vastgesteld veiligheidsrisico* / *Vastgesteld knelpunt* / *Hinder en risico's*
     - *Verzoek om proactieve / structurele maatregelen*
   - Harde limiet: max. 2000 tekens (met live teller en optimalisatie).

2. **Slimme Beeldverwerking & Compressie**:
   - AWV-limiet van maximaal 2.5 MB per afbeelding automatisch afdwingen.
   - Automatische verliesvrije of intelligente JPEG-compressie indien > 2.5 MB.

3. **MeldpuntWegen.be Automatiseringsmotor (Stappen-gebaseerd)**:
   - Flexibele stappenvolgorde afhandeling:
     - **Stap 1: Captcha-afhandeling** (reCAPTCHA v2 met Buster audio challenge solver integratie).
     - **Stap 2: Kaart & Locatie** (GPS-coördinaten projecteren op Vlaamse kaart + reverse geocoding adres).
     - **Stap 3: FAQ-detectie** (automatisch passeren indien getoond).
     - **Stap 4: Doelgroepselectie** (Voetgangers, Fietsers, Openbaar vervoer, Gemotoriseerd verkeer - min. 1) + tekst + foto's.
     - **Stap 5: Contactgegevens** (Aldo Fieuw, aldo.fieuw@gmail.com, "Ja, ik wens een reactie").
     - **Stap 6: Verzending & Dossierbevestiging** (ontvangen en opslaan van unieke behandelingscode).

4. **E-mail Synchronisatie & Automatische Koppeling**:
   - Automatisch matchen van inkomende AWV-mails aan verstuurde meldingen op basis van de tekst (fuzzy text matching zonder witregels/enters) en/of behandelingscode.
   - Real-time statusopvolging (Ingediend, In behandeling AWV, Doorgestuurd naar gemeente/politie/andere wegbeheerder, Opgelost, Gesloten).
   - Volledige e-mail thread historiek per dossier.

5. **AI-Antwoordgenerator & Herinneringsmotor**:
   - Korte notitie van gebruiker omzetten in een formele, beleefde Nederlandse opvolgingsmail naar AWV.
   - 1-klik en automatische herinneringen ("Herinnering sturen" bij stilstand na X dagen).

6. **Interactieve Kaart & Proximity Waarschuwing**:
   - Kaart met alle historische en actieve meldingen.
   - Nabijheidswaarschuwing: detecteert of er reeds eerdere meldingen binnen 100m liggen om dubbele meldingen te voorkomen en opvolging te vergemakkelijken.
