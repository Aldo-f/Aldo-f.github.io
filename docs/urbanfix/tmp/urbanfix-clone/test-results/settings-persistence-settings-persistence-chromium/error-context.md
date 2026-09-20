# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: settings-persistence.spec.ts >> settings persistence
- Location: test/e2e/settings-persistence.spec.ts:3:1

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: 2
Received: 5
```

# Page snapshot

```yaml
- generic [ref=f1e3]:
  - banner [ref=f1e4]:
    - generic [ref=f1e5]:
      - generic [ref=f1e6]:
        - generic [ref=f1e7] [cursor=pointer]:
          - generic [ref=f1e8]: UF
          - generic [ref=f1e9]:
            - generic [ref=f1e10]:
              - generic [ref=f1e11]: UrbanFix
              - generic [ref=f1e12]: Wegen & verkeersveiligheid
              - generic "Verbonden met Firebase Firestore cloud database" [ref=f1e13]: Firestore Cloud
            - paragraph [ref=f1e19]: Burgerparticipatie • FixMyStreet Open Data • Wegbeheer
        - generic [ref=f1e20]:
          - generic [ref=f1e21]:
            - generic [ref=f1e26]:
              - text: "In behandeling:"
              - strong [ref=f1e27]: "3"
            - generic [ref=f1e28]: "|"
            - generic [ref=f1e33]:
              - text: "Opgelost:"
              - strong [ref=f1e34]: "0"
          - button "AF Aldo Fieuw Admin" [ref=f1e37] [cursor=pointer]:
            - generic [ref=f1e38]: AF
            - generic [ref=f1e39]:
              - paragraph [ref=f1e40]: Aldo Fieuw
              - generic [ref=f1e41]: Admin
        - button "+ Nieuwe melding" [ref=f1e48] [cursor=pointer]
      - navigation [ref=f1e52]:
        - button "Incidenten & kaart (3)" [ref=f1e53] [cursor=pointer]
        - button "Nieuwe melding" [ref=f1e58] [cursor=pointer]
        - button "FAQ" [ref=f1e62] [cursor=pointer]
        - button "Over ons" [ref=f1e67] [cursor=pointer]
        - button "Contact" [ref=f1e73] [cursor=pointer]
        - button "E-mail tracking 3" [ref=f1e77] [cursor=pointer]:
          - generic [ref=f1e81]: E-mail tracking
          - generic [ref=f1e82]: "3"
        - button "Instellingen" [ref=f1e83] [cursor=pointer]
  - main [ref=f1e88]:
    - generic [ref=f1e90]:
      - generic [ref=f1e91]:
        - generic [ref=f1e97]:
          - heading "Instellingen" [level=1] [ref=f1e98]
          - paragraph [ref=f1e99]: UrbanFix AI-waterval, beveiliging, contactgegevens en rollen.
        - generic [ref=f1e100]: "Beheerder: aldo.fieuw@gmail.com"
      - generic [ref=f1e101]:
        - button "AI-modellenwaterval (5 actief)" [active] [ref=f1e102]
        - button "Dev e-mailbeveiliging" [ref=f1e108]
        - button "Contactgegevens (AWV)" [ref=f1e112]
        - button "Rollen & rechten" [ref=f1e117]
        - button "E-mailsync" [ref=f1e122]
      - generic [ref=f1e127]:
        - generic [ref=f1e128]:
          - generic [ref=f1e129]:
            - generic [ref=f1e130]:
              - heading "AI-modellenwaterval & providerauthenticatie" [level=2] [ref=f1e136]
              - paragraph [ref=f1e137]: Configureer meerdere AI providers en koppel meerdere modellen aan de waterval. Reorganiseer modellen via drag & drop om de prioriteitsvolgorde te bepalen.
            - generic [ref=f1e138]:
              - button "Watervalvolgorde (5)" [ref=f1e139]
              - button "Provideraccounts (6)" [ref=f1e145]
          - generic [ref=f1e151]:
            - generic [ref=f1e152]:
              - generic [ref=f1e153]:
                - generic [ref=f1e154]: "Filter:"
                - button "Alle (5)" [ref=f1e155]
                - button "Enkel vision-foto-AI (4)" [ref=f1e156]
                - button "Tekst & Rapporten (1)" [ref=f1e161]
              - button "+ Model toevoegen aan waterval" [ref=f1e167] [cursor=pointer]
            - generic [ref=f1e173]:
              - paragraph [ref=f1e174]: Hoe werkt de AI-waterval en vision-analyse?
              - paragraph [ref=f1e175]:
                - text: Sleep kaarten omhoog of omlaag via het handvat om de volgorde te wijzigen. Modellen met het groene
                - generic [ref=f1e183]: Vision
                - text: label worden gebruikt voor automatische foto-inspectie en verkeersbordherkenning. Tekstmodellen worden ingezet voor het genereren van formele AWV rapporten en rappel e-mails.
            - generic [ref=f1e187]:
              - generic [ref=f1e189]:
                - generic [ref=f1e190]:
                  - generic [ref=f1e191]:
                    - generic "Sleep om volgorde te wijzigen" [ref=f1e192]
                    - generic [ref=f1e200]: "#1"
                    - generic [ref=f1e201]:
                      - button "Hogere prioriteit" [disabled] [ref=f1e202]
                      - button "Lagere prioriteit" [ref=f1e205]
                  - generic [ref=f1e208]:
                    - generic [ref=f1e209]:
                      - generic [ref=f1e210]: Gemini 3.7 Flash (Custom OpenAI Endpoint)
                      - generic [ref=f1e211]: gemini-3.7-flash
                      - generic [ref=f1e212]: openai_compatible
                      - button "Vision-foto-AI" [ref=f1e217]
                    - generic [ref=f1e222]:
                      - generic [ref=f1e223]: "Endpoint: http://freellm.aldof.duckdns.org/v1"
                      - generic [ref=f1e224]: "· Temp: 0.2"
                - generic [ref=f1e225]:
                  - button "Test ping" [ref=f1e226]
                  - button "Model bewerken" [ref=f1e230]
                  - button "Actief" [ref=f1e233]
                  - button "Model verwijderen uit waterval" [ref=f1e234]
              - generic [ref=f1e239]:
                - generic [ref=f1e240]:
                  - generic [ref=f1e241]:
                    - generic "Sleep om volgorde te wijzigen" [ref=f1e242]
                    - generic [ref=f1e250]: "#2"
                    - generic [ref=f1e251]:
                      - button "Hogere prioriteit" [ref=f1e252]
                      - button "Lagere prioriteit" [ref=f1e255]
                  - generic [ref=f1e258]:
                    - generic [ref=f1e259]:
                      - generic [ref=f1e260]: Google Gemini 3.7 Flash (Official SDK)
                      - generic [ref=f1e261]: gemini-3.7-flash
                      - generic [ref=f1e262]: google
                      - button "Vision-foto-AI" [ref=f1e267]
                    - generic [ref=f1e272]:
                      - generic [ref=f1e273]: "Endpoint: Google GenAI SDK"
                      - generic [ref=f1e274]: "· Temp: 0.2"
                - generic [ref=f1e275]:
                  - button "Test ping" [ref=f1e276]
                  - button "Model bewerken" [ref=f1e280]
                  - button "Actief" [ref=f1e283]
                  - button "Model verwijderen uit waterval" [ref=f1e284]
              - generic [ref=f1e289]:
                - generic [ref=f1e290]:
                  - generic [ref=f1e291]:
                    - generic "Sleep om volgorde te wijzigen" [ref=f1e292]
                    - generic [ref=f1e300]: "#3"
                    - generic [ref=f1e301]:
                      - button "Hogere prioriteit" [ref=f1e302]
                      - button "Lagere prioriteit" [ref=f1e305]
                  - generic [ref=f1e308]:
                    - generic [ref=f1e309]:
                      - generic [ref=f1e310]: OpenCode Custom Model (vLLM / Local)
                      - generic [ref=f1e311]: opencode-v1
                      - generic [ref=f1e312]: openai_compatible
                      - button "Tekst / alleen rapport" [ref=f1e317]
                    - generic [ref=f1e322]:
                      - generic [ref=f1e323]: "Endpoint: http://freellm.aldof.duckdns.org/v1"
                      - generic [ref=f1e324]: "· Temp: 0.3"
                - generic [ref=f1e325]:
                  - button "Test ping" [ref=f1e326]
                  - button "Model bewerken" [ref=f1e330]
                  - button "Actief" [ref=f1e333]
                  - button "Model verwijderen uit waterval" [ref=f1e334]
              - generic [ref=f1e339]:
                - generic [ref=f1e340]:
                  - generic [ref=f1e341]:
                    - generic "Sleep om volgorde te wijzigen" [ref=f1e342]
                    - generic [ref=f1e350]: "#4"
                    - generic [ref=f1e351]:
                      - button "Hogere prioriteit" [ref=f1e352]
                      - button "Lagere prioriteit" [ref=f1e355]
                  - generic [ref=f1e358]:
                    - generic [ref=f1e359]:
                      - generic [ref=f1e360]: Google Gemini 2.5 Flash
                      - generic [ref=f1e361]: gemini-2.5-flash
                      - generic [ref=f1e362]: google
                      - button "Vision-foto-AI" [ref=f1e367]
                    - generic [ref=f1e372]:
                      - generic [ref=f1e373]: "Endpoint: Google GenAI SDK"
                      - generic [ref=f1e374]: "· Temp: 0.2"
                - generic [ref=f1e375]:
                  - button "Test ping" [ref=f1e376]
                  - button "Model bewerken" [ref=f1e380]
                  - button "Actief" [ref=f1e383]
                  - button "Model verwijderen uit waterval" [ref=f1e384]
              - generic [ref=f1e389]:
                - generic [ref=f1e390]:
                  - generic [ref=f1e391]:
                    - generic "Sleep om volgorde te wijzigen" [ref=f1e392]
                    - generic [ref=f1e400]: "#5"
                    - generic [ref=f1e401]:
                      - button "Hogere prioriteit" [ref=f1e402]
                      - button "Lagere prioriteit" [disabled] [ref=f1e405]
                  - generic [ref=f1e408]:
                    - generic [ref=f1e409]:
                      - generic [ref=f1e410]: OpenRouter Free / Fallback
                      - generic [ref=f1e411]: google/gemini-2.0-flash-exp:free
                      - generic [ref=f1e412]: openrouter
                      - button "Vision-foto-AI" [ref=f1e417]
                    - generic [ref=f1e422]:
                      - generic [ref=f1e423]: "Endpoint: https://openrouter.ai/api/v1"
                      - generic [ref=f1e424]: "· Temp: 0.2"
                - generic [ref=f1e425]:
                  - button "Test ping" [ref=f1e426]
                  - button "Model bewerken" [ref=f1e430]
                  - button "Actief" [ref=f1e433]
                  - button "Model verwijderen uit waterval" [ref=f1e434]
        - button "Instellingen opslaan" [ref=f1e439] [cursor=pointer]
  - contentinfo [ref=f1e445]:
    - generic [ref=f1e446]:
      - generic [ref=f1e447]:
        - generic [ref=f1e448]:
          - generic [ref=f1e449]:
            - generic [ref=f1e450]: UF
            - generic [ref=f1e451]: UrbanFix
          - paragraph [ref=f1e452]: Het sobere, onafhankelijke meldingsplatform voor de openbare ruimte en verkeersveiligheid.
          - generic [ref=f1e453]: Gebaseerd op de FixMyStreet open-data filosofie.
        - generic [ref=f1e454]:
          - heading "Navigatie" [level=4] [ref=f1e455]
          - list [ref=f1e456]:
            - listitem [ref=f1e457]:
              - button "Incidenten & kaart" [ref=f1e458] [cursor=pointer]
            - listitem [ref=f1e459]:
              - button "+ Nieuwe melding toevoegen" [ref=f1e460] [cursor=pointer]
        - generic [ref=f1e461]:
          - heading "Informatie & diensten" [level=4] [ref=f1e462]
          - list [ref=f1e463]:
            - listitem [ref=f1e464]:
              - button "Veelgestelde vragen" [ref=f1e465]
            - listitem [ref=f1e466]:
              - button "Over ons & besturen" [ref=f1e467] [cursor=pointer]
            - listitem [ref=f1e468]:
              - button "Contact & aansluiten" [ref=f1e469] [cursor=pointer]
            - listitem [ref=f1e470]:
              - button "API-documentatie" [ref=f1e471]
        - generic [ref=f1e472]:
          - heading "Juridisch & privacy" [level=4] [ref=f1e473]
          - list [ref=f1e474]:
            - listitem [ref=f1e475]:
              - button "Privacyverklaring & GDPR" [ref=f1e476]
            - listitem [ref=f1e477]:
              - button "Gebruiksvoorwaarden" [ref=f1e478]
            - listitem [ref=f1e479]:
              - generic [ref=f1e482]: Levensgevaar? Bel direct 112
      - generic [ref=f1e483]:
        - generic [ref=f1e484]: © 2026 UrbanFix. Vrij en onafhankelijk platform voor burgerparticipatie.
        - generic [ref=f1e485]:
          - paragraph [ref=f1e486]:
            - generic [ref=f1e487]: Made with
            - img "love" [ref=f1e488]: ♥
            - generic [ref=f1e489]: and a tiny bit of AI by Usful
            - generic [ref=f1e490]: —
            - generic [ref=f1e491]: Build 2026-09-11 13:51:15 CEST
          - generic [ref=f1e492]: "Server: AWV Integration REST Service v2.4"
```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | 
  3  | test("settings persistence", async ({ page }) => {
  4  |   // Navigate to settings
  5  |   await page.goto("https://urbanfix.dev.aldof.duckdns.org/settings");
  6  |   await page.waitForSelector("text=Instellingen", { timeout: 10_000 });
  7  | 
  8  |   // Switch to AI tab to access models
  9  |   await page.getByRole("button", { name: /AI-modellenwaterval/ }).click();
  10 |   await page.waitForTimeout(500);
  11 | 
  12 |   // Get initial provider count
  13 |   const providerCards = page.locator("button[title='Model verwijderen uit waterval']");
  14 |   const beforeCount = await providerCards.count();
  15 |   console.log(`Initial provider count: ${beforeCount}`);
  16 | 
  17 |   // Delete all but first 2 providers
  18 |   while ((await providerCards.count()) > 2) {
  19 |     await providerCards.first().click();
  20 |     await page.waitForTimeout(300);
  21 |   }
  22 | 
  23 |   const afterDeleteCount = await providerCards.count();
  24 |   console.log(`Provider count after deletion: ${afterDeleteCount}`);
  25 |   expect(afterDeleteCount).toBe(2);
  26 | 
  27 |   // Save the settings
  28 |   await page.getByRole("button", { name: "Instellingen opslaan" }).click();
  29 |   await page.waitForTimeout(1000);
  30 | 
  31 |   // Navigate back to settings (simulates reload/refresh)
  32 |   await page.goto("https://urbanfix.dev.aldof.duckdns.org/settings");
  33 |   await page.waitForSelector("text=Instellingen", { timeout: 10_000 });
  34 | 
  35 |   // Switch to AI tab
  36 |   await page.getByRole("button", { name: /AI-modellenwaterval/ }).click();
  37 |   await page.waitForTimeout(500);
  38 | 
  39 |   const afterReloadCount = await providerCards.count();
  40 |   console.log(`Provider count after reload: ${afterReloadCount}`);
  41 | 
  42 |   // The critical assertion: providers should still be 2, not the original count
> 43 |   expect(afterReloadCount).toBe(2, `Providers were not persisted: got ${afterReloadCount}, expected 2`);
     |                            ^ Error: expect(received).toBe(expected) // Object.is equality
  44 | });
  45 | 
```