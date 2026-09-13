# npm Scripts Documentation

| Script | Command | Description |
|--------|---------|-------------|
| `dev` | `tsx server.ts` | Starts the development server with hot‑reloading (Vite frontend + Express backend). |
| `build` | `vite build && esbuild server.ts --bundle --platform=node --format=cjs --packages=external --sourcemap --outfile=dist/server.cjs` | Builds the frontend assets and bundles the backend for production. |
| `start` | `node dist/server.cjs` | Runs the compiled production server. |
| `clean` | `rm -rf dist server.js` | Removes build artifacts. |
| `test` | `vitest run` | Executes the test suite. |
| `lint` | `eslint src/**/*.ts src/**/*.tsx --fix` | Lints and automatically fixes source files. |
| `prepare` | `husky` | Sets up Git hooks via Husky (run `npm install` first). |

## Usage Examples

```bash
# Start development environment
npm run dev

# Run lint and fix issues
npm run lint

# Run tests
npm run test

# Build for production
npm run build && npm start
```