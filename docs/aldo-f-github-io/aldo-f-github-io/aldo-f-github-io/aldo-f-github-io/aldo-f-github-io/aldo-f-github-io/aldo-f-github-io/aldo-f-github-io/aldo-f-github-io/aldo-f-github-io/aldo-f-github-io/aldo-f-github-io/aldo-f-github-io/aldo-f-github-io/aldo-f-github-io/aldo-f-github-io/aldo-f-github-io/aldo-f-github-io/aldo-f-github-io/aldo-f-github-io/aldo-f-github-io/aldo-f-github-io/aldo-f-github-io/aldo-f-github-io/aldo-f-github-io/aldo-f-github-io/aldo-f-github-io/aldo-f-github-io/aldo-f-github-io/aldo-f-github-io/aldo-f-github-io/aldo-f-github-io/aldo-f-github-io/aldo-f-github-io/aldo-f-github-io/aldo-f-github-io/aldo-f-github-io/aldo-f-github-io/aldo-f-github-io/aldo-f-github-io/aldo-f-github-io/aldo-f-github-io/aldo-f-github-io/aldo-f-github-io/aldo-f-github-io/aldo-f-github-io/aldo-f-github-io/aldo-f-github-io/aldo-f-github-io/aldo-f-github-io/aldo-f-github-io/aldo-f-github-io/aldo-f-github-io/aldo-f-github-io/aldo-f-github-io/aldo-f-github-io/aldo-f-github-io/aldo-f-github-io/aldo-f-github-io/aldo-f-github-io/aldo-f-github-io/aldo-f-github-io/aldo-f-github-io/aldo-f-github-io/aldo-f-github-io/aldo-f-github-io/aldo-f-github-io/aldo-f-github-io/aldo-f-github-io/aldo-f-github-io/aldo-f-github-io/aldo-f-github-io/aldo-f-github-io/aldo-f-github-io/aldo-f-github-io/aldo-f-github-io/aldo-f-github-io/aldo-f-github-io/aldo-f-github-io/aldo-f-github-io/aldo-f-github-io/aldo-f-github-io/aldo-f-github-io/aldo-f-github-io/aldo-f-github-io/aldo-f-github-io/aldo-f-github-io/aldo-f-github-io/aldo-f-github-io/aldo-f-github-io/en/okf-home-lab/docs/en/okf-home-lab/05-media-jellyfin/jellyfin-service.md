---
type: Service
title: Jellyfin Media Server
description: Jellyfin media server running as a Docker container on the home-lab infrastructure
resource: ./jellyfin-service.md
tags: [service, jellyfin, media-server, docker, streaming]
sources:
  - id: jellyfin-docker-compose
    resource: ./docker-compose.yml
    title: Jellyfin Docker Compose Configuration
    author: aldo
    usage_count: 1
    last_modified: 2026-08-25T09:15:00Z
  - id: jellyfin-healthcheck-attested
    resource: ./jellyfin-healthcheck.md
    title: Jellyfin Health Check Attested Computation
    author: reference_agent/gemini-2.5-pro
    usage_count: 0
    last_modified: 2026-08-25T09:15:00Z
generated:
  by: human:aldo
  at: 2026-08-25T09:15:00Z
verified:
  - by: human:aldo
    at: 2026-08-25T09:15:00Z
status: stable
stale_after: 2027-02-25T09:15:00Z
---

# Jellyfin Media Server

## Overview
Jellyfin is a free and open-source media system that allows you to manage and stream your media collection. In Aldo's home-lab, it runs as a Docker container with access to media files stored on the shared HDD1 mount.

## Configuration
- Runs as user `33:33` (www-data) for proper file permissions
- Configuration stored in `./config`
- Cache stored in `./cache`
- Media files accessed from `/mnt/HDD1/nextcloud/data/aldo/files:/media`
- Exposed on port 8096
- Connected to the external `traefik_net` network for reverse proxy integration

## Health Check
The service includes a health check that verifies the Jellyfin API is responsive:
- Command: `curl -fsS -m 5 http://127.0.0.1:8096/health >/dev/null || exit 1`
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3
- Start period: 30 seconds

This health check is also documented as an Attested Computation in `jellyfin-healthcheck.md`.

## Dependencies
- Docker Engine
- External Traefik network (`traefik_net`)
- Shared storage mount at `/mnt/HDD1/`

## Related Concepts
- Node: pi3-node.md, pi5-node.md (where this service may be deployed)
- Docker Compose: docker-compose-template.md
- Attested Computation: jellyfin-healthcheck.md