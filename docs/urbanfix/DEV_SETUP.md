# Development Setup Documentation

## Pre-commit Hooks

The repository includes automated linting and formatting using **Husky** and **lint-staged** to maintain code quality.

### Setup

The pre-commit hooks are automatically installed via the `prepare` npm script:

```bash
npm install  # This runs `npm run prepare` which installs Husky
```

### Hooks Configuration

The hooks are configured in `package.json`:

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

### How It Works

1. **Husky** creates Git hooks that run before commits
2. **lint-staged** processes only the files being staged
3. For TypeScript files (`*.{ts,tsx}`), it runs:
   - `eslint --fix` – Automatically fixes linting issues
   - `prettier --write` – Formats code according to project style

### Usage

```bash
# When committing, staged files will be automatically linted and formatted

git add <file>
git commit -m "Your message"

# To run hooks manually on all files (without committing):
npx lint-staged

# To bypass hooks (use with caution):
git commit --no-verify -m "Your message"
```

### Configuration Files

The hooks rely on configuration files in the repository root:

- `eslint.config.js` or `eslint.config.cjs` – ESLint configuration
- `.prettierrc` – Prettier configuration
- `tsconfig.json` – TypeScript configuration

### Troubleshooting

If hooks are not working:

1. **Ensure Husky is installed**: `npm install --save-dev husky lint-staged`
2. **Verify configuration**: Check that `prepare` script exists in package.json
3. **Force reinstall**: `rm -rf .git/hooks && npm install`
4. **Temporarily disable**: `husky disable`
5. **Clear staged changes and retry**: `git reset HEAD --mixed`

## Development Environment

### Quick Commands

| Purpose | Command |
|---------|---------|
| Start dev server | `npm run dev` |
| Build for production | `npm run build` |
| Start production | `npm start` |
| Run tests | `npm test` |
| Lint and fix | `npm run lint` |
| Clean artifacts | `npm run clean` |

### Dependencies

```bash
# Install all dependencies
cp .env.example .env  # Configure if needed
npm install
```

### Running the Application

```bash
# Local development with hot reload
npm run dev

# Production build
npm run build

# Start production server
npm start
```

## Environment Variables

The application uses environment variables defined in `.env`:

```env
# Required for AI services
GEMINI_API_KEY=your_gemini_api_key

# Application configuration
APP_URL=https://your-domain.com

# Local development (use .env.local)
PORT=3000
NODE_ENV=development
```

See `.env.example` for the complete list of variables.

## Project Structure

```
.
├── src/          # Frontend React application
│   ├── components/   # UI components
│   ├── pages/      # Page components
│   ├── types.ts    # Type definitions
│   └── utils/      # Helper functions
├── server/       # Backend Express server
│   └── services/ # Business logic services
├── docs/         # Documentation (including this file)
├── assets/       # Static assets
├── server.ts     # Main Express server entry
└── vite.config.ts # Vite configuration
```

## Docker Development

### Local Development with Docker

```bash
# Start with live reload
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

# Stop
docker compose down
```

### Production Deployment

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f urbanfix
```

## Version Control

### Branching Strategy

- **main** – Production-ready code
- **feature/*** – Feature development
- **bugfix/*** – Bug fixes
- **docs/*** – Documentation updates

### Commit Message Guidelines

Use conventional commit format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

Types:

- `feat` – New feature
- `fix` – Bug fix
- `docs` – Documentation
- `style` – Formatting (no functional change)
- `refactor` – Code refactor
- `test` – Adding tests
- `chore` – Maintenance
```