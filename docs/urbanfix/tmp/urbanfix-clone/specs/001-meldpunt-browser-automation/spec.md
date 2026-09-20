# Spec: Real Browser Automation for MeldpuntWegen.be Submission

## Feature Number
001

## Short Name
meldpunt-browser-automation

## Goal
Replace the simulated `meldpuntBot.ts` with real browser automation using Playwright to actually submit incidents to https://meldpuntwegen.be/meldpuntwegen/index.html.

## Current State (Gap Analysis)
The current `server/services/meldpuntBot.ts` is a **simulation** — it generates fake logs and returns a fake tracking code. It does NOT:
- Open a real browser
- Solve reCAPTCHA with Buster
- Fill in the actual form on meldpuntwegen.be
- Submit the form
- Capture the real tracking code from the confirmation page

## Acceptance Criteria

### AC-1: Playwright Integration
- [ ] Project includes `@playwright/test` and `playwright` dependencies
- [ ] `server/services/meldpuntBot.ts` uses Playwright to launch a browser instance
- [ ] Browser navigates to `https://meldpuntwegen.be/meldpuntwegen/index.html`

### AC-2: reCAPTCHA Solver (Buster)
- [ ] Detects reCAPTCHA v2 on the page
- [ ] Integrates with Buster (https://github.com/dessant/buster) or equivalent audio challenge solver
- [ ] Solves the captcha and submits the token
- [ ] Falls back to manual override if solver fails

### AC-3: Location Step
- [ ] Projects GPS coordinates from report onto the Leaflet map
- [ ] Clicks the map pin at the correct location
- [ ] Handles "Melding zonder locatie" option if GPS unavailable
- [ ] Uses reverse geocoding to populate address field

### AC-4: FAQ Skip (if present)
- [ ] Detects if FAQ intermediate page appears
- [ ] Automatically clicks "Volgende" to skip

### AC-5: Impact Groups & Report Text
- [ ] Selects at least 1 impacted group from: voetgangers, fietsers, openbaar_vervoer, gemotoriseerd
- [ ] Fills the "Wat wilt u ons melden" textarea with the AI-generated report text
- [ ] Validates text length <= 2000 characters
- [ ] Uploads all photos (validates < 2.5 MB each)

### AC-6: Contact Information
- [ ] Pre-fills contact form with user settings (Aldo Fieuw, aldo.fieuw@gmail.com)
- [ ] Checks "Ja, ik wens een reactie te ontvangen" checkbox

### AC-7: Submission & Tracking Code Capture
- [ ] Clicks "Versturen" button
- [ ] Captures the confirmation page
- [ ] Extracts the tracking code (pattern: `MWV-2026-XXXXXX` or similar)
- [ ] Returns the real tracking code to the caller

### AC-8: Error Handling
- [ ] Handles network errors, timeouts, page changes
- [ ] Logs all steps with real timestamps
- [ ] Returns detailed error messages on failure
- [ ] Does not leave browser instances running (cleanup on exit)

## Out of Scope
- Multi-tenant support (single user: Aldo Fieuw)
- Parallel submissions (one at a time)
- Headless mode optimization (initially visible browser for debugging)

## Technical Notes
- Use Playwright with Chromium (provides best reCAPTCHA compatibility)
- Consider persisting browser cookies/session between submissions
- Store Buster integration as optional dependency (graceful fallback)
- Add `BUSTER_API_KEY` to environment variables if using external solver

## Related Specs
- Spec 002: AI Report Generation (already implemented)
- Spec 003: Email Synchronization (already implemented)
- Spec 004: Real-time Updates via SSE (already implemented)

## Implementation Tasks
1. Install Playwright and dependencies
2. Create `MeldpuntBrowserAgent` class in `server/services/meldpuntBot.ts`
3. Implement each step (1-6) from the original prompt
4. Add integration tests with mock pages
5. Update API endpoint to use real automation
6. Document setup for Buster/CAPTCHA solver
