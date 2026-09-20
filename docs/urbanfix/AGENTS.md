# PROJECT KNOWLEDGE BASE – 06-apps-urbanfix

**Generated:** 2026-09-20

## OVERVIEW
Playwright‑based end‑to‑end test suite for the MeldpuntBot browser extension. Contains helper utilities, models, and a single E2E spec.

## STRUCTURE
```
06-apps-urbanfix/
├── src/
│   ├── models/report.ts          # Data models for test reports
│   ├── playwright/helpers.ts     # Playwright helper functions
│   └── services/meldpuntBotPlaywright.ts  # Bot service wrapper
├── test/e2e/meldpuntBot.spec.ts  # Main E2E test
├── tools/buster/buster_extension/ # Browser extension source (self‑contained)
├── playwright.config.ts          # Playwright configuration
├── package.json                  # Dependencies (Playwright, TypeScript)
└── bun.lock                      # Bun lockfile
```

## WHERE TO LOOK
| Task | Location |
|------|----------|
| E2E test logic | `test/e2e/meldpuntBot.spec.ts` |
| Playwright helpers | `src/playwright/helpers.ts` |
| Bot service abstraction | `src/services/meldpuntBotPlaywright.ts` |
| Test report model | `src/models/report.ts` |
| Extension source code | `tools/buster/buster_extension/src/` |
| Playwright config | `playwright.config.ts` |

## CONVENTIONS
- Use Bun as runtime (`bun.lock` present).
- Playwright tests are located in `test/e2e/`.
- All selectors should be stable and use `data-testid` attributes where possible.
- Helper functions live in `src/playwright/`.

## ANTI‑PATTERNS
- Do not hard‑code selectors; prefer `data-testid`.
- Do not commit `test-results/`.
- Do not add dependencies without updating `bun.lock`.

## COMMANDS
```bash
# Run E2E tests
bun test:e2e

# Run a single spec
bun test:e2e test/e2e/meldpuntBot.spec.ts

# Install dependencies
bun install
```