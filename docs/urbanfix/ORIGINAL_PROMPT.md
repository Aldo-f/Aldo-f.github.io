# Original Project Prompt

> This is the original prompt that started this project. Preserved for historical reference.

---

Lets create a new application.

   The global thing that it should do is: Automate sending issues to the government with so less manual actions.

   https://meldpuntwegen.be/meldpuntwegen/index.html

   I will continue in Dutch:
   Als het volledig af is moet het:
   Alles doen van A tot Z voor het melden en opvolgen van meldingen over het verkeer.
   Ik zou het dus willen in verschillende losse 'acties' opbouwen.

   Een melding gaat nu op deze manier:
   Foto nemen
   De foto doorgeven aan een AI met een korte vermelding wat er verkeerd is.
   Voorbeeld: Verkeersbord heeft niet meer het typisch rode kleur
   De AI maakt daar dan een duidelijke melding van.
   Daarna stuur ik de melding door via https://meldpuntwegen.be/meldpuntwegen/index.html
   Daar is er een google reCAPTCHA die moet ingevuld worden om de melding te maken. We gebruikten daarvoor vroeger al 'Buster' https://github.com/dessant/buster

   Nadien zijn er enkel stappen die moeten doorlopen worden.
   De volgorde van de stappen is meestal wel gelijk, maar daar mag je niet vanuit gaan omdat er soms een extra stap is en soms niet. Je kan dus best gewoon rekening houden met wat er gevraagd wordt dan een vaste volgorde.
   De stappen omvatten (neem dus aan dat het in een random volgorde is):
   1) I'm not a robot (Maak gebruik van 'Buster')
   2) Een locatie aanduiden. Dit lijkt mij een moeilijke stap. Er is dus een kaartje, en aan de hand van de meta gegevens van de foto (gps) coördinaat moet je op de kaart dat coördinaat aanduiden. Er is ook de mogelijkheid van te zeggen "Melding is zonder locatie", maar dat is normaal nooit het geval. De kaart bevat meldingen die reeds binnengekomen zijn, maar niet allemaal.
   3) Deze komt niet altijd, een pagina 'Veelgestelde vragen'. Hier is niets in te vullen, we kunnen gewoon naar de volgende stap gaan.
   4) Hier moeten we aanduiden voor wie de melding problemen veroorzaakt. Er zijn 4 opties, meerdere opties zijn aan te duiden. Maar minstens 1.
   Daar staat ook een veld "Wat wilt u ons melden", max 2000 tekens. Daar moeten we dus via de foto en wat de melder zelf toevoegt aan de foto een duidelijke melding plaatsen.
   
   [Examples of report texts omitted for brevity - see GOAL.md for full examples]
   
   De meldingen worden nu gedaan via Gemini (dus eventueel gebruikmakend van hetzelfde model of recentere -> freellmapi/gemini-flash-3.6 of iets dergelijks; dat moet je dus achterhalen via http://freellm.aldof.duckdns.org/v1/models met API key: freellmapi-f19ae62770dd60a1f67dd9369ffbc062199354f212040db8)

   In deze stap moeten ook de foto's toegevoegd worden. Er is een maximale grootte van 2.5 MB. Conversie naar een kleinere grootte van afbeelding kan soms dus nodig zijn.

   5) "Hoe kunnen wij u contacteren". Hier moet de contactinfo komen. Er zijn 3 verplichte velden:
   Voornaam: Aldo
   Naam: Fieuw
   E-mail: aldo.fieuw@gmail.com
   En onderaan is er ook nog een checkbox die we moeten aanduiden: "Ja, ik wens een reactie te ontvangen"

   Bij "Verstuur" is de melding verstuurd. En hebben we de mogelijkheid, er staat een knop, om nog een melding te versturen.

   Dan krijgen we een email naar ons emailadres waarbij we een behandelingscode toegewezen krijgen.
   Het is handig dat we die code bij onze melding bijhouden.

   Mijn foto's komen binnen via Google Photos. Daar selecteer ik ze. Soms zijn er meerdere foto's bij een melding, soms maar 1. Meestal zijn de foto's van een melding op quasi dezelfde GPS coördinaat.

   Doelstelling:
   Een app waarmee je een foto maakt. Enkele voorstellen krijgt van wat er verkeerd aan is. Dan een volledige tekst krijgt van de melding, deze kan nakijken of opnieuw kan genereren met eventuele wijzigingen die je wilt hebben. Dan klikt op verstuurd en dan wordt de melding verstuurd naar Meldpunt wegen en verkeer (Agentschap Wegen en Verkeer = AWV).
   Dan lezen we de mail na die we krijgen, dat is niet altijd meteen. Omdat er soms nog een manuele actie moet gedaan worden door AWV omdat ze niet op basis van het GPS coördinaat de correcte verantwoordelijke kunnen aanduiden.
   Dus via een croncheck van de mails moeten we dan deze melding kunnen linken aan de melding die we verstuurd hebben. De tekst die er in staat is altijd net deze die we verstuurd hebben. Maar dan soms zonder enters.

   Nadien zou ik makkelijk via de app willen kunnen zien welke meldingen ik verstuurd heb, en wat de status is (kreeg ik al een antwoord, werd er een melding van gemaakt door AWV, werd het doorgestuurd aan een andere verantwoordelijke of werd het intern opgevolgd, ...).
   Dat via een lijst van meldingen en ook via een kaartje te zien. Zo weet ik wanneer ik ergens ben meteen of ik op die locatie al een melding heb gedaan, en eventueel opnieuw dezelfde melding wil doen van het probleem, of een andere in de buurt.
   Alles zou rechtstreeks via de app moeten kunnen opgevolgd worden. Mails versturen (m.a.w. kort zeggen wat ik wil antwoorden waarna de AI daarvan een duidelijke mail van maakt die dan automatisch wordt verstuurd)

   Automatische herinneringen zou ik ook meteen, eventueel automatisch, moeten kunnen versturen. Of een knop bij de melding (de thread van de mail) "Herinnering sturen".

   Kortom, een full package om het verbeteren van de verkeersveiligheid.

   Ik zie alles als een volledig project, maar elk met een apart doel dat toch naadloos in elkaar past.

   Het is belangrijk dat je start met het maken van een mapje onder ~/dev waarbij we dan alles kunnen bijhouden van dit project.
   Alles uit deze prompt moet gebruikt worden.

   Maak gebruik van onder andere, maar niet alleen deze: TDD, SDD (spec kit, specify), KISS, DRY, YAGNI, /goal, /plan.

   IK wil dat dit geheel automatisch gemaakt zal worden, zonder later input te moeten geven terwijl het al begonnen is.
   Maak dus een concreet plan en zorg dat je alle zaken nadien automatisch kan vervolledigen.

---

**Original Author**: Aldo Fieuw
**Date**: 2026-08 (project inception)
**Related**: See `dev/GOAL.md`, `dev/PLAN.md`, `dev/SDD_SPEC.md`, `dev/TDD_TESTS.md` for structured specifications derived from this prompt.
