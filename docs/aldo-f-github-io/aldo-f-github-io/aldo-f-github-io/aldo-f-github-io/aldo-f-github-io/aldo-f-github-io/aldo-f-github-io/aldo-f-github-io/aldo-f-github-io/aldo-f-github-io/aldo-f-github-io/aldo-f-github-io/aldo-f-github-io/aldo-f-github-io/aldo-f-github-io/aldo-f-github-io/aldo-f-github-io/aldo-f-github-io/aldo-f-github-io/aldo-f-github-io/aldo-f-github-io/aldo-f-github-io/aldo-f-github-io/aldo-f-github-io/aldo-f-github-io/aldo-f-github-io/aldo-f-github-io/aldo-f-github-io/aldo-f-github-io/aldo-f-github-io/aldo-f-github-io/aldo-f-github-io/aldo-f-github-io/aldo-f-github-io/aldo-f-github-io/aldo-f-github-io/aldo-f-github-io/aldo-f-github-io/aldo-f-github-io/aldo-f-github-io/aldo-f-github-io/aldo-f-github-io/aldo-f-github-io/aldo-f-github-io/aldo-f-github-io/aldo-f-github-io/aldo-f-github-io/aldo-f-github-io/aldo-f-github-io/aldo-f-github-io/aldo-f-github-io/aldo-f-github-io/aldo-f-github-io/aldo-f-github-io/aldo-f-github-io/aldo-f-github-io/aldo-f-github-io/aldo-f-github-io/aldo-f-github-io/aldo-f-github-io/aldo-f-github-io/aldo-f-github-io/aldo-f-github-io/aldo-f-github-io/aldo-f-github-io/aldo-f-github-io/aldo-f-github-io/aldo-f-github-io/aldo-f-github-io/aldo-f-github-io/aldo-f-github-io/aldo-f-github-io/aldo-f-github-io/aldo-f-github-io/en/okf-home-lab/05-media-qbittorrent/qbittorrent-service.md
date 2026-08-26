---
type: Service
title: qBittorrent BitTorrent Client
description: qBittorrent BitTorrent client running as a Docker container in the home-lab infrastructure
resource: ./qbittorrent-service.md
tags: [service, qbittorrent, bittorrent, docker, download]
sources:
  - id: qbittorrent-docker-compose
    resource: ./docker-compose.yml
    title: qBittorrent Docker Compose Configuration
    author: aldo
    usage_count: 1
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

# qBittorrent BitTorrent Client

## Overview
qBittorrent is a free and open-source BitTorrent client that provides a lightweight, powerful, and intuitive interface for downloading and managing torrents. In Aldo's home-lab, it runs as a Docker container with access to the downloads directory on the shared HDD1 mount.

## Configuration
- Runs as user `33:33` (www-data) for proper file permissions matching the shared storage
- Configuration stored in `./config`
- Downloads stored in `/mnt/HDD1/nextcloud/data/aldo/files/Seed:/downloads`
- Web interface accessible on port 8080
- Connected to the external `traefik_net` network for reverse proxy integration
- Timezone set to Europe/Amsterdam

## Health Check
The service includes a health check that verifies the web interface is responsive:
- Command: `curl -fsS -m 5 http://127.0.0.1:8080/ >/dev/null || exit 1`
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3
- Start period: 60 seconds (allows time for application startup)

## Dependencies
- Docker Engine
- External Traefik network (`traefik_net`)
- Shared storage mount at `/mnt/HDD1/`
- Environment variables: PUID=33, PGID=33, TZ=Europe/Amsterdam, WEBUI_PORT=8080

## Usage
- Access web interface at `http://<host>:8080`
- Default credentials: admin/adminadmin (change on first login)
- Configure download directories to point to `/downloads` inside container
- Set up RSS feeds, automated downloads, and scheduling as needed

## Related Concepts
- Node: pi3-node.md, pi5-node.md (where this service may be deployed)
- Docker Compose: docker-compose-template.md
- Infrastructure: 01-core-infra/ansible-role-template.md, 01-core-infra/docker-compose-template.md