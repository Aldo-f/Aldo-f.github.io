---
title: Environment Variables
description: Radio Community environment variables reference
---

# Environment Variables

## Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | No | 3000 | Server port |
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `MUSIC_PATH` | No | /music | Path to music files |
| `AUTH_SERVICE_URL` | No | http://auth-service:3008 | Auth service URL |
| `SOURCE_JOE` | No | https://api.joe.be/2.0 | Joe.be API base URL |
| `JOE_STATION_ID` | No | joe_easy | Default Joe.be station |
| `DEEZER_ARL` | No | - | Deezer ARL token for downloading |
| `DEEZER_API_BASE` | No | https://api.deezer.com | Deezer API base |
| `ICECAST_HOST` | No | icecast | Icecast server host |
| `ICECAST_PORT` | No | 8000 | Icecast server port |
| `ADMIN_EMAIL` | No | aldo@test.be | Platform admin email |

## Required Variables

### DATABASE_URL

PostgreSQL connection string. This is required for the application to function.

Example:
```
postgresql://user:password@localhost:5432/radiocommunity
```

## Optional Variables

### MUSIC_PATH

Path to the music files directory. Default is `/music`.

### AUTH_SERVICE_URL

URL of the external authentication service. Default is `http://auth-service:3008`.

### DEEZER_ARL

Deeezer ARL token required for downloading tracks. Obtain this from your Deezer account.

### ADMIN_EMAIL

Email address of the platform admin. Default is `aldo@test.be`. This user has global admin access to all communities.

!!! note "Joe.be Auto-Fetch"
    The Joe.be API auto-fetches every 6 hours if SOURCE_JOE is configured.

## Docker Configuration

When running in Docker, these variables are typically set in the `.env` file or passed via docker-compose:

```yaml
services:
  radio-community:
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/radiocommunity
      - ADMIN_EMAIL=admin@example.com
```

## Traefik Configuration

The service runs on port 3011 externally. To add to Traefik:

```yaml
# Add to docker-compose.yml labels
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.radio-community.rule=Host(`your-domain.duckdns.org`)"
  - "traefik.http.routers.radio-community.entrypoints=websecure"
  - "traefik.http.routers.radio-community.tls=true"
```