---
title: "Hoe JPG's Eigenlijk Werken: Compressie Zonder Gokken"
date: 2026-09-03
categories:
  - Techniek
  - Multimedia
tags:
  - jpeg
  - compressie
  - dct
  - quantization
  - pixel
---

Terwijl AI-compressietools zoals vibecompress je foto's vervangen door hallucinaties, werkt de vertrouwde JPG-formaat al decennia op een heel ander principe: wiskunde in plaats van gokken. Hier is hoe dat precies werkt.

<!-- more -->

## Wat Is JPEG?

JPEG (afgekort van Joint Photographic Experts Group) is een compressieformaat voor digitale foto's, geïntroduceerd in 1992. Het is ontworpen om grote beelden — vaak meerdere MB's — terug te brengen naar kilobytes, zonder dat het menselijk oog het verlies meteen opvalt.

Het gaat om **lossy compressie**: bepaalde informatie wordt permanent verwijderd, maar de resterende data blijft visueel herkenbaar.

## Stap 1: Kleur Ruimte Converteren

Digitale foto's starten meestal als RGB (Rood, Groen, Blauw). JPEG zet ze eerst om naar **YCbCr**:

- **Y** = helderheid (luminantie)
- **Cb** = blauwe kleurverschil
- **Cr** = rode kleurverschil

Waarom? Het menselijk oog is veel gevoeliger voor helderheidsveranderingen dan voor kleurdetails. Dat geeft ons de ruimte om kleurinformatie te verdubbelen in de volgende stap.

## Stap 2: Subsampling

Omdat we kleur minder goed zien, halveren we de resolutie van Cb en Cr. Een 4x4 blok pixels gaat van 16 kleuren naar 8 kleurwaarden, maar behoudt de helderheid. Dit heet **4:2:0 chroma subsampling**.

Resultaat: 50% minder kleurgegevens, met minimaal zichtbaar effect.

## Stap 3: Discrete Cosine Transform (DCT)

Hier wordt het interessant. De JPEG-codec verdeelt de afbeelding in blokjes van 8x8 pixels. Voor elk blokje voert het de **Discrete Cosine Transform** uit — een wiskundige transformatie die de pixels omzet in frequenties.

In plaats van te zeggen "pixel (2,3) is rood met waarde 187", zegt DCT: "dit blokje bestaat uit:
- 1 gemiddelde helderheid (lage frequentie)
- Een paar lichte schaduwen (middelhoge frequenties)
- Geen harde randen (geen hoge frequenties)"

De output is een 8x8 matrix van frequentiecoëfficiënten. De linkerbovenhoek bevat de laagste frequenties (de "grote vormen"), de rechtsonderhoek de hoogste frequenties (de "fijne details").

## Stap 4: Quantisatie

Nu komt het echte compressiegeheim. Elke frequentiecoëfficiënt wordt gedeeld door een **kwantisatietabel** en afgerond naar een geheel getal.

- Lage frequenties (belangrijk voor de look): blijven behouden
- Hoge frequenties (fijne textuur): worden kleiner of nul

Dit is de **lossy** stap. Details die we minder goed zien (hoogfrequente kleuren, fijne patronen) gaan verloren. Hoe hoger de compressie, hoe ruwer de afronding, hoe meer blokvormige artefacten ("blockiness") je ziet bij vergroting.

De kwantisatietabel is instelbaar: hogere waarden = meer compressie = slechtere kwaliteit.

## Stap 5: Zig-Zag Scannen

De 8x8 matrix wordt nu in één lange rij gezet via een **zig-zag patroon**: van linksboven (laagste frequentie) naar rechtsonder (hoogste frequentie). 

Waarom? Omdat na kwantisatie de rechteronderhoek vol nul wordt. Die nullen kunnen we efficiënt comprimeren met RUNLENGTH-codering.

## Stap 6: Entropy Coding

De laatste stap is **entropy coding** (meestal Huffman-codering). Herhalende patronen — zoals lange reeksen nullen — krijgen korte codes, zeldzame combinaties krijgen langere codes.

Resultaat: een compact bitstream die de foto kan opslaan.

## Het Resultaat: Hoe Klinkt JPEG-Compressie in Getallen?

| Origineel (RAW) | JPEG (kwaliteit 85) | JPEG (kwaliteit 50) |
|-----------------|---------------------|---------------------|
| 20.000 KB       | ~800 KB (96% klein) | ~200 KB (99% klein) |

Opvallend: de "kwaliteit 50"-versie ziet er nog redelijk goed uit op schermgrootte, maar krijgt duidelijke blokkende artefacten bij close-up.

## Waarom Werkt Dit Beter dan Bitmap?

Een ongeverfd PNG bevat 24 bits per pixel (RGB). 1920x1080 = 2.073.600 pixels × 3 bytes = 6 MB.

JPEG bereikt dezelfde resolutie met 100–500 KB. Dat verschil zit in de herkenning dat foto's natuurlijk zachte overgangen bevatten, geen scherpe grafische lijnen. JPEG is ontworpen voor fotografie, niet voor screenshots.

## Limitaties

- **Herhaald opslaan**: elke keer dat je een JPEG opnieuw opslaat, verlies je meer details. De artefacten accumuleren.
- **Niet geschikt voor tekst**: scherpe randen en kleine letters worden snel onscherp.
- **Blokkende artefacten**: bij hoge compressie zie je een rasterpatroon in vlakke gebieden.

Voor die doeleinden bestaat PNG (lossless) of WebP (moderne opvolger). Maar voor foto's blijft JPEG de koning van schaalbaarheid.

## Samengevat

JPEG werkt niet door te gissen wat de foto voorstelt (zoals AI-tools), maar door de foto wiskundig te ontleeden in frequenties, onbelangrijke details weg te knippen, en de rest compacter op te slaan. Het is compressie door slimme verwijdering, niet door hallucinatie.

En dat is het essentiële verschil: bij JPEG weet je wat er op de foto zat. Bij AI-compressie weet je alleen wat *vibe* de foto had.

---

*Lees ook: waarom we vibecompress niet serieus moeten nemen — [Waarom pixels opslaan als je vibes kan opslaan?](../2026/09/05/waarom-pixels-opslaan-als-je-vibes-kan-opslaan-ontmoet-vibecompress/)*