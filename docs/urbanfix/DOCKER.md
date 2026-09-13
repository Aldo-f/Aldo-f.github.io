# Docker Documentation

## Production Setup (`docker-compose.yml`)

### Services

#### urbanfix
- **Purpose**: Production deployment of UrbanFix
- **Build context**: Current directory with Dockerfile
- **Image**: `urbanfix:local`
- **Environment variables**:
  - `NODE_ENV=production`
  - `PORT=3000`
  - `GEMINI_API_KEY` (optional)
  - `APP_URL` (defaults to `https://urbanfix.dev.aldof.duckdns.org`)
- **Ports**: Exposed internally on `3000`, mapped to Traefik router
- **Volumes**:
  - `urbanfix-data:/app/data` - Persistent data storage
- **Networks**: `traefik_net` (external network)
- **Traefik labels**:
  - Router: `Host(\`urbanfix.dev.aldof.duckdns.org\`)`
  - TLS: Auto‑provisioned via `myresolver`
  - Entrypoint: `websecure`
  - Backend port: `3000`

### Networks

- **traefik_net**: External network created by `01-core-infra`. Required for Traefik routing.

### Volumes

- **urbanfix-data**: Named volume for persistent application data (uploads, storage, etc.)

### Usage

```bash
# Build and start production deployment
docker compose up -d --build

# View logs
docker compose logs -f urbanfix

# Stop
docker compose down
```

## Development Setup (`docker-compose.dev.yml`)

### Services

#### urbanfix (development)
- **Build target**: `builder` stage (discarded at runtime)
- **Command**: `npm run dev` (Vite dev + tsx hot reload)
- **Environment**:
  - `NODE_ENV=development`
- **Ports**:
  - `4001:3000` - Application port (exposed on host)
  - `5173:5173` - Vite HMR port (exposed on host)
- **Volumes**:
  - `./:/app` - Mounts entire project for live reload
  - `/app/node_modules` - Preserves installed dependencies
  - `/app/dist` - Prevents conflicts with build output

### Usage

```bash
# Start development with live reload
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
```

### Notes

- Requires `traefik_net` to be present (from `01-core-infra`)
- Router pre‑configured in `04-network-traefik/routes.yml`
- All source code is mounted at `/app`, so changes are reflected instantly
- The `builder` stage is used only for building, not runtime

## Dockerfile

The Dockerfile builds a production-ready image with:

1. **Base image**: `node:20-alpine`
2. **Working directory**: `/app`
3. **Install dependencies** (production only)
4. **Build the application** (`npm run build`)
5. **Remove dev dependencies**
6. **Set non‑root user**
7. **Expose port 3000**
8. **Start the server** (`node dist/server.cjs`)

See the existing `Dockerfile` in the project root for the full specification.
