# Stock photos — curation & licensing

Placeholder photography for go-live prep, until the client's own photographer
delivers the real shots (per briefing: professional photography = optional line item).

## Licensing rule

Only **CC0 / Public Domain Mark** images are candidates — no attribution required,
safe for a commercial client site. Every candidate records: source, creator,
landing page and license in `docs/photo-staging/candidates.json`.

**Important:** these are placeholders. Before final launch, replace with real
photos of the WZC (residents' gallery must show *our* residents, with consent — GDPR).

## Slots → briefing requirement

| Slot | Used for | Briefing line |
|---|---|---|
| `hero` | Homepage hero background | warme sfeer · meer spreken met beeld |
| `living` | "Wonen en leven" section | wonen en leven centraal |
| `activities` | Activities page/archive header | activiteitenverslag met foto's |
| `dining` | "Wat inbegrepen" / meals block | prijzen en wat er inclusief is |
| `room` | Rooms page | kamer kunnen bekijken |
| `garden` | Gallery starters / location feel | galerij met foto's |
| `portrait` | Contact page — social services person | contact niet zo droog, foto van persoon |
| `coffee` | Family/grandchildren angle | doelgroep kinderen en kleinkinderen |

## Final picks (2026-08-23, approved visually by Aldo)

Imported into the media library as attachments **29–35**, titles + Dutch alt-texts set:

| Slot | Attachment | Title | Wired into |
|---|---|---|---|
| `hero-0` | 29 | Zonneterras bij Sint-Antonius | Front-page hero background (+ gradient overlay) |
| `portrait-1` | 34 | Sociale dienst | Contact block avatar (`template-parts/map-contact.php`) |
| `living-0` | 33 | Thuisvoelen op de kamer | Featured image page *Wonen en leven* |
| `room-0` | 35 | Kamer met licht | Featured image page *Kamers bekijken* |
| `activities-1` | 30 | Knip- en naatjesmiddag | Featured image page *Activiteiten* |
| `garden-1` | 32 | Wandeling in de tuin | Featured image page *Galerij* |
| `dining-0` | 31 | Lekker eten samen | Featured image page *Tarieven* |

Web-optimised before import (max 1800px, q84). Replace with real WZC photos at launch.

## Review workflow

1. Open `docs/photo-staging/index.html` (contact sheet with thumbnails, licenses, flags).
2. ⚠ flags = automated suspicion of archival/artwork material (source & title heuristics).
   The agent could not visually verify this batch — human review is required.
3. Reply with the numbers you want, e.g. "hero-0, living-1, activities-1, dining-0".
4. Agent imports them via wp-cli into the media library, wires hero/portrait into the
   templates, and logs the final choice + license here.

## Import command (agent runs after your pick)

```bash
cd ~/dev/06-apps-wordpress-stantonius
docker compose run --rm wpcli media import docs/photo-staging/<file>.jpg \
  --post_title="<title>" --porcelain
```

## Sources

- [Openverse](https://openverse.org/) API, filtered `license=cc0,pdm`, min width 900px.
