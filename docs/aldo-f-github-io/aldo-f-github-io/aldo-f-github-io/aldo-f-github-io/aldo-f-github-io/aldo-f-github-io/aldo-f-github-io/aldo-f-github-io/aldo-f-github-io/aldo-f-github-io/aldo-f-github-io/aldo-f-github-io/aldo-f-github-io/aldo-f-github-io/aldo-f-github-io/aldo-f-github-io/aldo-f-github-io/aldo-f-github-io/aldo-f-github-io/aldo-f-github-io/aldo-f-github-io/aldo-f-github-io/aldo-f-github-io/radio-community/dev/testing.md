---
title: Testing
description: Radio Community testing guide
---

# Testing

## Test Commands

| Command | Purpose |
|---------|---------|
| `npm test` | Run all Playwright E2E tests |
| `npm run test:ui` | Run tests with UI |
| `npm run test:headed` | Run tests in headed mode |
| `npm run test:unit` | Run Jest unit tests |
| `npm run test:integration` | Run Jest integration tests |
| `npm run test:e2e` | Run Playwright E2E tests only |

## Single Test File

Run a specific test file:

```bash
npx playwright test tests/e2e/filename.spec.js
```

## Test Types

### Playwright E2E Tests

End-to-end tests in `tests/e2e/`:
- API flow testing
- Community creation flows
- Source management
- Member operations

### Jest Unit Tests

Unit tests in `tests/unit/`:
- Utility functions
- Helper functions
- Business logic

### Jest Integration Tests

Integration tests in `tests/integration/`:
- Database operations
- API endpoint combinations

## Test Configuration

Tests are configured via `playwright.config.js`.

!!! note "Unit Test Exclusion"
    Unit tests are excluded from Playwright runs via `testIgnore` in the configuration.

## Running Tests in Development

```bash
# Run E2E tests
npm test

# Run with visible browser (headed mode)
npm run test:headed

# Run with Playwright UI
npm run test:ui

# Run unit tests only
npm run test:unit

# Run integration tests
npm run test:integration
```

## Test Environment

Tests require:
- Docker services running (`docker compose up -d`)
- PostgreSQL database accessible
- Auth service available
- Icecast server running

## Debugging Tests

Use headed mode to see browser interactions:

```bash
npm run test:headed
```

Use UI mode for interactive test development:

```bash
npm run test:ui
```