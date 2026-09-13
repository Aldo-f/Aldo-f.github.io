# CI Documentation

## Current Status

This repository currently does **not** include any GitHub Actions CI workflow files. The `.github/workflows/` directory does not exist.

## Available GitHub Configuration

The repository does contain GitHub-related files, but they are not CI workflows:

- `.github/skills/` - A collection of OpenCode skills and commands (unrelated to CI)

## Suggested CI Workflow

If you wish to add CI, a minimal GitHub Actions workflow could look like below:

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install deps
        run: npm ci
      - name: Lint
        run: npm run lint
      - name: Test
        run: npm test
```

**Key points**:
- **Environment variables**: none are required for the basic lint/test steps, but if you run any scripts that need `GEMINI_API_KEY` or `APP_URL` you should set them as repository secrets and expose them via `env:`.
- **Checks performed**: dependency install, TypeScript type‑check (`npm run lint`), and test execution (`npm test`).
- **Artifacts**: you can add steps to upload build artifacts or coverage reports as needed.

## Pre-commit Hooks

The repository includes pre-commit hooks configured in `package.json`:

```json
"husky": {
  "hooks": {
    "pre-commit": "lint-staged"
  }
},
"lint-staged": {
  "*.{ts,tsx}": [
    "eslint --fix",
    "prettier --write"
  ]
}
```

These hooks run on staged changes before commit and automatically format and lint TypeScript/TypeScriptReact files.

## Adding CI to This Repository

To add CI, create a `.github/workflows/ci.yml` file in your repository with the workflow above or a more comprehensive one including:

1. **Multiple jobs** for different environments (dev, test, staging, prod)
2. **Conditional execution** to run only on relevant branches
3. **Caching** for npm dependencies and build artifacts
4. **Security scanning** (SAST, secret detection)
5. **Coverage reporting**
6. **Notification integrations** (Slack, Teams, etc.)
