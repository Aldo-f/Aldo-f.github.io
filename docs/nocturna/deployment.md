# Nocturna Deployment Guide

This guide covers deploying Nocturna to production with Docker, Traefik, TLS, and various connectivity options.

---

## Quick Start (Docker Compose)

```bash
# Clone
git clone https://github.com/Aldo-f/Nocturna.git
cd Nocturna

# Build and start
docker compose up -d --build

# Check logs
docker logs nocturna -f
```

The shipped `docker-compose.yml`:
- Mounts `~/.hermes` read-only so the in-container `hermes` CLI works
- Mounts a persistent `nocturna_data` volume for the SQLite database
- Exposes port `3000`, integrates with Traefik via Docker labels

---

## Docker Configuration

### docker-compose.yml (Production)

```yaml
services:
  nocturna:
    build: .
    container_name: nocturna
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - PORT=3000
      - NOCTURNA_ALLOW_REMOTE=1
      - NOCTURNA_CORS_ORIGINS=https://nocturna.hermes.dev.aldof.duckdns.org
      - NOCTURNA_HERMES_BIN=hermes
      - HERMES_KANBAN_BOARD=nocturna
    volumes:
      - type: bind
        source: /home/aldo/.hermes
        target: /home/nocturna/.hermes
        read_only: true
      - nocturna_data:/app/data
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nocturna.rule=Host(`nocturna.hermes.dev.aldof.duckdns.org`)"
      - "traefik.http.routers.nocturna.entrypoints=websecure"
      - "traefik.http.routers.nocturna.tls.certresolver=letsencrypt"
      - "traefik.http.services.nocturna.loadbalancer.server.port=3000"
      - "traefik.http.middlewares.nocturna-ipallow.ipallowlist.sourcerange=192.168.0.0/16,10.0.0.0/8"
      - "traefik.http.routers.nocturna.middlewares=nocturna-ipallow"
    networks:
      - traefik-net

volumes:
  nocturna_data:

networks:
  traefik-net:
    external: true
```

### Dockerfile

```dockerfile
# --- Stage 1: build the SPA ---
FROM node:20-slim AS webbuild
WORKDIR /app/web
COPY web/package.json web/package-lock.json ./
RUN npm ci
COPY web/ ./
ARG APP_VERSION=1.0.0
ENV APP_VERSION=${APP_VERSION}
RUN npm run build

# --- Stage 2: Node runtime serving SPA + API ---
FROM node:20-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 nocturna
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production
COPY server/ ./server/
COPY --from=webbuild /app/web/dist ./web/dist
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh \
    && chown -R nocturna:nocturna /app
USER nocturna
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -fsS http://localhost:3000/api/health || exit 1
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
```

### docker-entrypoint.sh

```bash
#!/bin/sh
# Nocturna container entrypoint.
# Mount the host's Hermes home at /home/nocturna/.hermes so the CLI works.
set -e

# Prefer system hermes on PATH; otherwise use the bind-mounted one.
if command -v hermes >/dev/null 2>&1; then
    : "${NOCTURNA_HERMES_BIN:=hermes}"
else
    HERMES_HOME="${NOCTURNA_ENGINE_HOME:-/home/nocturna/.hermes}"
    ENGINE_SRC="$HERMES_HOME/hermes-agent"
    mkdir -p /app/bin
    cat > /app/bin/hermes <<EOF
#!/bin/sh
export PYTHONPATH="$ENGINE_SRC"
exec python3 "$ENGINE_SRC/hermes" "$@"
EOF
    chmod +x /app/bin/hermes
    : "${NOCTURNA_HERMES_BIN:=/app/bin/hermes}"
fi
export NOCTURNA_HERMES_BIN

# Ensure the engine sees the shared hermes home, not the container user's HOME.
: "${NOCTURNA_ENGINE_HOME:=/home/nocturna/.hermes}"
export HOME="${NOCTURNA_HOME:-$(dirname "$NOCTURNA_ENGINE_HOME")}"

exec node dist/server.mjs
```

---

## Traefik Integration

### Traefik Labels (Auto-applied via docker-compose)

| Label | Purpose |
|-------|---------|
| `traefik.enable=true` | Enable Traefik routing |
| `traefik.http.routers.nocturna.rule=Host(\`...\`)` | Host-based routing |
| `traefik.http.routers.nocturna.tls.certresolver=letsencrypt` | Auto-TLS via Let's Encrypt |
| `traefik.http.middlewares.nocturna-ipallow.ipallowlist.sourcerange=...` | IP allowlist (LAN only) |

### IP Allowlist (Security)

Restrict access to your LAN subnets:

```yaml
labels:
  - "traefik.http.middlewares.nocturna-ipallow.ipallowlist.sourcerange=192.168.0.0/16,10.0.0.0/8,172.16.0.0/12"
```

> **Important:** Only set `NOCTURNA_ALLOW_REMOTE=1` if you have network-level access control (Traefik `ipAllowList`, Tailscale, Cloudflare Access, etc.). Never bind `0.0.0.0` unauthenticated on the public internet.

---

## Connectivity Methods

### Method A: Hermes Gateway (Recommended for Remote)

**On your home server (where Hermes runs):**

```bash
# 1. Set a gateway password
hermes config set web.basic_auth.password "your-secure-password"

# 2. Start the gateway (systemd)
sudo systemctl enable --now hermes-gateway

# 3. Or run in foreground for testing
hermes gateway run
```

**In Nocturna Instance Manager:**
- Add Instance → **Hermes Gateway**
- URL: `https://gateway.yourdomain.com` (or tunnel URL)
- Password: the one you set above
- Or API Key (takes precedence): `HERMES_CUSTOM_FREELLM_ALDOF_DUCKDNS_ORG_API_KEY`

---

### Method B: Reverse Tunnel (ngrok / Cloudflare / Tailscale)

**ngrok:**
```bash
ngrok http 8787
# Copy the https://xxxx.ngrok-free.app URL
```

**Cloudflare Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8787
```

**Tailscale (simplest — no public exposure):**
```bash
# On Hermes machine
tailscale up
# Access via Tailscale IP: http://100.x.x.x:8787
```

Use the tunnel URL in Nocturna's Gateway instance form.

---

### Method C: SSH Remote

Connect via SSH to a host that has Hermes installed.

**Requirements:**
- SSH access to the host
- Hermes installed there
- Firewall allowing inbound SSH (port 22)

**In Nocturna Instance Manager:**
- Add Instance → **SSH Remote**
- Host, port, username
- Password or SSH key path
- Remote `hermes` binary path (usually `~/.local/bin/hermes`)

> Some cloud platforms (Google AI Studio, Railway, Vercel) block outbound SSH. Use Method A or B instead.

---

### Method D: Local CLI (Same Machine)

Nocturna auto-detects `hermes` at `~/.hermes/hermes-agent/hermes` or on `PATH`.

**In Nocturna Instance Manager:**
- Add Instance → **Local CLI**
- Binary path (optional, auto-detected)
- Board slug (default: `nocturna`)

---

## Ansible Deployment (Home Lab)

The home-lab infra uses Ansible to deploy Nocturna as a systemd service behind Traefik.

### Playbook Entry

```yaml
# 01-core-infra/ansible/playbooks/deploy.yml
- name: Deploy Nocturna
  hosts: pi5
  roles:
    - role: containers
      vars:
        containers:
          - name: nocturna
            compose_file: "{{ infra_templates_dir }}/06-apps-nocturna/docker-compose.yml"
            env_file: "{{ secrets_dir }}/nocturna.env"
```

### Secrets File (`secrets/nocturna.env`)

```bash
NODE_ENV=production
PORT=3000
NOCTURNA_ALLOW_REMOTE=1
NOCTURNA_CORS_ORIGINS=https://nocturna.hermes.dev.aldof.duckdns.org
NOCTURNA_HERMES_BIN=hermes
HERMES_KANBAN_BOARD=nocturna
```

### Deploy Command

```bash
cd ~/dev
./install.sh --tags containers --limit-services '["06-apps-nocturna"]'
```

---

## Cloud Deployment (Railway / Render / Fly.io)

### Railway

```bash
railway login
railway init
railway add --database sqlite  # or use persistent volume
railway up
```

**Environment Variables:**
```bash
NODE_ENV=production
PORT=3000
NOCTURNA_ALLOW_REMOTE=1
NOCTURNA_CORS_ORIGINS=https://your-app.railway.app
NOCTURNA_HERMES_BIN=hermes
HERMES_KANBAN_BOARD=nocturna
```

### Render

```yaml
# render.yaml
services:
  - type: web
    name: nocturna
    env: node
    buildCommand: npm ci && npm run build
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 3000
      - key: NOCTURNA_ALLOW_REMOTE
        value: "1"
      - key: NOCTURNA_CORS_ORIGINS
        value: https://your-app.onrender.com
```

### Fly.io

```bash
fly launch
fly deploy
```

**fly.toml:**
```toml
[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  PORT = "3000"
  NOCTURNA_ALLOW_REMOTE = "1"
  NOCTURNA_CORS_ORIGINS = "https://nocturna.fly.dev"

[[services]]
  internal_port = 3000
  protocol = "tcp"
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
  [[services.ports]]
    port = 80
    handlers = ["http"]
```

---

## Environment Variable Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | No | `3000` | Express listen port |
| `NODE_ENV` | No | — | `production` for prod build |
| `NOCTURNA_HERMES_BIN` | No | auto | Path to `hermes` binary |
| `NOCTURNA_ALLOW_REMOTE` | No | `false` | Bind `0.0.0.0` (needs network ACL) |
| `NOCTURNA_CORS_ORIGINS` | No | — | Comma-separated CORS allowlist |
| `NOCTURNA_ENGINE_HOME` | No | `~/.hermes` | Hermes data directory |
| `HERMES_KANBAN_BOARD` | No | `nocturna` | Default board slug |
| `SQLITE_DB_PATH` | No | `./data/nocturna.db` | Override DB file |
| `DISABLE_HMR` | No | `false` | Disable Vite HMR |
| `TEST_GATEWAY` | No | `false` | Force gateway mode in tests |

---

## Health Checks

```bash
# Local
curl http://localhost:3000/api/health

# Remote (through Traefik)
curl -sk https://nocturna.hermes.dev.aldof.duckdns.org/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "engine": "cli|gateway|lan",
  "stats": { "tasks": 42, "running": 3, "blocked": 1 }
}
```

---

## Backup & Restore

### Backup
```bash
# From host
docker exec nocturna cp /app/data/nocturna.db /app/data/nocturna.db.backup.$(date +%F)

# Or copy from volume
docker run --rm -v nocturna_data:/data -v $(pwd):/backup alpine \
  cp /data/nocturna.db /backup/nocturna-$(date +%F).db
```

### Restore
```bash
# Stop container
docker compose stop nocturna

# Restore DB
docker run --rm -v nocturna_data:/data -v $(pwd):/backup alpine \
  cp /backup/nocturna-2026-09-17.db /data/nocturna.db

# Start
docker compose up -d
```

---

## Troubleshooting

### Container Won't Start
```bash
docker logs nocturna --tail 50
# Check: hermes binary found? DB writable? Port 3000 free?
```

### "Engine Unreachable"
- Local CLI: `hermes version` works inside container?
- Gateway: URL reachable? Password/API key correct?
- LAN: Target Hermes gateway running? Same subnet?

### Traefik 404 / 502
- Check Traefik dashboard: `http://traefik.yourdomain.com`
- Verify router rule matches hostname
- Check middleware IP allowlist isn't blocking you

### Database Locked
```bash
# If "database is locked"
docker compose down
rm -f data/nocturna.db-wal data/nocturna.db-shm
docker compose up -d
```

---

## Monitoring

### Prometheus (Optional)

Add to `docker-compose.yml`:
```yaml
services:
  nocturna:
    # ... existing config
    labels:
      - "prometheus.io/scrape=true"
      - "prometheus.io/port=3000"
      - "prometheus.io/path=/metrics"
```

Then expose `/metrics` endpoint in `server/routes/system.ts`.

### Log Aggregation

```bash
# Loki / Grafana
docker run -d --name loki -v $(pwd)/loki:/etc/loki grafana/loki:2.9
docker run -d --name promtail -v /var/log:/var/log grafana/promtail:2.9
```

---

## Upgrading

```bash
cd /path/to/Nocturna
git pull
docker compose build --no-cache
docker compose up -d
docker image prune -f
```

**Database migrations:** Currently none — schema changes are additive only. If needed, a migration script will be added to `server/migrations/`.