---
title: Development Workflow
description: Radio Community development workflow guide
---

# Development Workflow

## Running the Application

### Start Services

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f radio-community
```

### Stop Services

```bash
docker compose down
```

## Making Changes

### Frontend Changes

The container mounts `./frontend/dist` as read-only. This means:

1. **Make frontend changes** in `frontend/src/`
2. **Build locally:** `cd frontend && npm run build`
3. **Restart container:** `docker compose up -d` (no `--build` needed!)
4. **Changes are immediately visible** - no Docker rebuild required

Why this works:
- Local `npm run build` writes to `frontend/dist/`
- Container reads from mounted volume
- No need to rebuild Docker image for frontend changes

### Backend Changes

Rebuild required when changing:
- `server.js` (backend code)
- Adding new npm dependencies
- Changing `Dockerfile` or `docker-compose.yml`

```bash
docker compose up -d --build
```

## Code Style

### Backend (JavaScript)

- Language: JavaScript (ES6+) with CommonJS modules
- Indentation: 4 spaces (no tabs)
- Line Length: Soft limit 120 characters
- Functions: Prefer async/await with early returns

### Frontend (TypeScript/React)

- Language: TypeScript with React 18
- Styling: Tailwind CSS + DaisyUI
- Indentation: 2 spaces
- TypeScript: Strict mode enabled, no `any` allowed
- Hooks: Follow react-hooks rules (exhaustive deps)

## Linting

```bash
# Lint frontend
cd frontend && npm run lint

# Lint backend
npx eslint server.js
```

## Database

### Schema

The database schema is defined in `db/init.postgres.sql`.

### Operations

- Use `dbGet(sql, params)` - Get single row
- Use `dbAll(sql, params)` - Get multiple rows
- Use `dbRun(sql, params)` - Insert/Update/Delete
- Call `saveDatabase()` after mutations

## File Ownership

Downloaded music files are chowned to www-data:www-data (Dockerfile creates user if not exists).

## Music Storage

Music files are stored in the mounted host folder:
```
/mnt/HDD1/nextcloud/data/aldo/files/Documents/Torrents/music/
```

- Community subfolder: `community/` (e.g., `community/kanjers/`)
- Database stores relative paths: `community/kanjers/track.mp3`