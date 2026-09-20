# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visual-steps.spec.ts >> visual steps
- Location: test/e2e/visual-steps.spec.ts:4:5

# Error details

```
Test timeout of 60000ms exceeded.
```

# Page snapshot

```yaml
- generic [ref=e1]:
  - link "Overslaan en naar de inhoud gaan" [ref=e2] [cursor=pointer]:
    - /url: "#main"
  - generic:   
  - generic [ref=e7]:
    - generic:
      - generic [ref=e8]:
        - link "Vlaanderen" [ref=e9] [cursor=pointer]:
          - /url: https://www.vlaanderen.be/nl
        - link "meldpuntwegen.be" [ref=e14] [cursor=pointer]:
          - /url: http://meldpuntwegen.be/
      - link "Toon menu Contacteer ons" [ref=e17] [cursor=pointer]:
        - /url: http://meldpuntwegen.be/
        - generic [ref=e18]: Toon menu
        - text: Contacteer ons
  - main [ref=e21]:
    - generic [ref=e22]:
      - generic [ref=e23]:
        - generic [ref=e25]:
          - img "Tunnel" [ref=e27]
          - generic [ref=e28]: Welkom op het Meldpunt Wegen
        - generic [ref=e34]:
          - paragraph [ref=e36]: Hier vind je alle informatie rond het wegennet in Vlaanderen.
          - generic [ref=e38]:
            - generic [aria-hidden] [ref=e40]: 
            - generic [ref=e41]:
              - paragraph [ref=e42]: Opgelet!
              - paragraph [ref=e44]: Een dringende, gevaarlijke situatie melden? Bel onmiddellijk de politie via het nummer 101.
          - paragraph [ref=e47]: Meldpunt Wegen gebruikt analytische cookies. Voor meer info, zie 'Cookieverklaring' in de footer onderaan. Door verder te gaan, gaat u akkoord met het gebruik hiervan.
          - generic [ref=e48]:
            - heading "Heb je een melding over het wegennet in Vlaanderen?" [level=2] [ref=e49]
            - paragraph [ref=e51]: Een melding maken over een bepaald onderwerp dat aangepakt moet worden, kun je doen via het online formulier.
          - generic [ref=e52]:
            - iframe [ref=e56]:
              - generic [ref=f1e2]:
                - generic [ref=f1e3]:
                  - checkbox "Ik ben geen robot" [ref=f1e7]
                  - generic [aria-hidden] [ref=f1e11]: Ik ben geen robot
                  - generic [ref=f1e13]:
                    - text: reCAPTCHA wijzigt de servicevoorwaarden.
                    - link "Onderneem actie." [ref=f1e14] [cursor=pointer]:
                      - /url: https://google.com/recaptcha/admin/migrate
                - generic [ref=f1e15]: reCAPTCHA
            - paragraph [ref=e57]: Bevestig eerst dat je geen robot bent
          - link "Ga naar het online formulier" [active] [ref=e59]:
            - /url: javascript:void(0)
      - text:               
  - contentinfo [ref=e63]:
    - generic [ref=e68]:
      - generic [ref=e72]:
        - generic [ref=e73]: Vlaanderen
        - generic [ref=e74]: verbeelding werkt
      - generic [ref=e75]:
        - heading "Meldpuntwegen.be is een officiële website van de Vlaamse overheid" [level=2] [ref=e76]
        - generic [ref=e77]:
          - text: uitgegeven door
          - link "Agentschap Wegen en Verkeer" [ref=e79] [cursor=pointer]:
            - /url: https://www.vlaanderen.be/nl/contact/adressengids/administratieve-diensten-van-de-vlaamse-overheid/beleidsdomein-mobiliteit-en-openbare-werken/agentschap-wegen-en-verkeer
        - generic [ref=e80]:
          - list:
            - listitem [ref=e81]:
              - link "Cookieverklaring" [ref=e82] [cursor=pointer]:
                - /url: https://wegenenverkeer.be/cookies
            - listitem [ref=e83]:
              - link "Privacyverklaring" [ref=e84] [cursor=pointer]:
                - /url: https://wegenenverkeer.be/privacy
      - generic:
        - list
```