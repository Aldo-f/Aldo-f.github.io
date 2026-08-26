---
type: Docker Compose
title: Standard Docker Compose Template
description: Template for creating standardized Docker Compose files in the home-lab infrastructure
resource: ./docker-compose-template.md
tags: [docker, compose, template, infrastructure]
sources:
  - id: docker-compose-convention
    resource: human:aldo
    title: Aldo's Docker Compose Convention
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

# Standard Docker Compose Template

## Overview
This document describes the standard structure and conventions for Docker Compose files used in Aldo's home-lab infrastructure.

## Basic Structure
```yaml
version: '3.8'

services:
  service_name:
    image: image_name:tag
    container_name: service_name
    restart: unless-stopped
    ports:
      - "host_port:container_port"
    environment:
      - VARIABLE_NAME=value
    volumes:
      - ./local_path:/container_path
      - shared_volume:/shared_path
    networks:
      - service_network

volumes:
  shared_volume:

networks:
  service_network:
    driver: bridge
```

## Conventions
1. **Version**: Use version '3.8' for compatibility with Docker Engine 19.03+
2. **Service Naming**: Use lowercase with underscores (e.g., `jellyfin`, `nextcloud`)
3. **Container Naming**: Match service name for easy identification
4. **Restart Policy**: Use `unless-stopped` for services that should survive reboots
5. **Ports**: 
   - Map only necessary ports to host
   - Comment why each port is needed
   - Use consistent host port ranges when possible
6. **Environment**:
   - Use environment variables for configuration
   - Reference `.env` files for secrets (not committed)
   - Document required variables in service documentation
7. **Volumes**:
   - Use named volumes for persistent data
   - Use bind mounts for configuration that needs host access
   - Follow `__HOME__` macro convention for paths
8. **Networks**:
   - Create explicit networks for service isolation
   - Use descriptive network names
   - Consider bridge vs overlay based on deployment needs

## Best Practices
- Pin image tags (avoid `:latest` in production)
- Use healthchecks where available
- Limit container capabilities with `cap_drop` and `cap_add`
- Set appropriate resource limits (memory, CPU)
- Use read-only root filesystem when possible
- Document external dependencies
- Keep compose files in service-specific directories
- Use `.dockerignore` to exclude unnecessary files from build context

## Example: Media Service
```yaml
version: '3.8'

services:
  mediaservice:
    image: linuxserver/mediaservice:latest
    container_name: mediaservice
    restart: unless-stopped
    ports:
      - "8096:8096"          # HTTP API
      - "8920:8920"          # HTTPS (if enabled)
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Brussels
    volumes:
      - /mnt/hdd1/media:/media
      - ./config:/config
    networks:
      - media_net

networks:
  media_net:
    driver: bridge
```