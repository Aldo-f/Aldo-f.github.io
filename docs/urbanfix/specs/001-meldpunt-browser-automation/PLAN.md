# Plan: Real Meldpunt Browser Automation with Playwright & Buster

## Goal
Replace the simulated `meldpuntBot.ts` with a true Playwright automation that:
1. Opens a Chromium browser.
2. Navigates to https://meldpuntwegen.be/meldpuntwegen/index.html.
3. Solves the reCAPTCHA v2 challenge using Buster (audio‑solver).
4. Verifies form field statuses via image checks.
5. Fills the incident form (location, impact groups, description, photos, contact).
6. Submits the form.
7. Captures the confirmation page and extracts the tracking code (e.g., `MWV‑2026‑XXXXXX`).

## Tasks (TDD style)
| ID | Description | Test | Status |
|----|-------------|------|--------|
| T001 | Add Playwright (and browsers) as a dev dependency via `bun add -d @playwright/test` | `playwright-test` fails until implementation | ☐ |
| T002 | Install Buster (`git clone https://github.com/dessant/buster.git && npm install` inside project) and expose a helper `solveCaptcha(page)` | Unit test for `solveCaptcha` using a mock page | ☐ |
| T003 | Create `src/services/meldpuntBotPlaywright.ts` with class `MeldpuntBot` and method `submit(report: ReportItem): Promise<string>` | Integration test runs Playwright, submits a fixture report, asserts a non‑empty tracking code | ☐ |
| T004 | Implement navigation to the meldpunt URL and wait for the form to load | Test checks that `page.url()` ends with `/index.html` after `goto` | ☐ |
| T005 | Image/visual verification of required fields (e.g., ensure the map pin appears, photo preview thumbnails load) | Snapshot test of DOM after each step | ☐ |
| T006 | Fill location: click Leaflet map at GPS coordinates from report EXIF | Test verifies that the hidden `lat`/`lon` inputs receive correct values | ☐ |
| T007 | Select impact groups (checkboxes) based on `report.impactGroups` | Test checks that the correct checkboxes are checked | ☐ |
| T008 | Fill description textarea (max 2000 chars) | Test asserts length ≤ 2000 | ☐ |
| T009 | Upload photos (≤ 2.5 MB each) and verify upload success UI | Test uploads a small sample image and checks for preview element | ☐ |
| T010 | Pre‑fill contact info from user settings (`Aldo Fieuw`, `aldo.fieuw@gmail.com`) | Test confirms inputs contain these values | ☐ |
| T011 | Click **Versturen** and wait for confirmation page | Test waits for selector containing tracking code regex | ☐ |
| T012 | Extract tracking code (`/MWV-\d{4}-[A-Z0-9]+/`) and return it | Test parses a sample confirmation HTML | ☐ |
| T013 | Clean up: close browser, handle errors, ensure no orphan processes | Test forces a timeout and checks graceful shutdown | ☐ |
| T014 | Add Playwright CI step to `package.json` scripts (`"test:e2e": "playwright test"`) | CI job runs and passes | ☐ |

## Milestones
1. **Dependencies installed** – complete T001‑T002.
2. **Basic navigation & form fill** – complete T003‑T010.
3. **Captcha solving & submission** – complete T011‑T012.
4. **Error handling & CI integration** – complete T013‑T014.

## Acceptance Criteria
- End‑to‑end Playwright test runs against the live site (or a staging mirror) and returns a valid tracking code.
- No simulated logs remain; `meldpuntBot.ts` is deprecated.
- All new code has 100 % test coverage.
- CI pipeline passes the new E2E test on every push.

## Risks & Mitigations
- **Captcha rate‑limits** – use Buster’s audio solving; must solve automatically without manual fallback.
- **Site UI changes** – selectors are kept in a separate `selectors.ts` file for easy updates.
- **Large photo uploads** – client‑side compression before upload (reuse existing `compressImage` util).

## Next Steps
Run `bun install` to add Playwright, then create the `MeldpuntBot` skeleton and write the first failing test (T001).