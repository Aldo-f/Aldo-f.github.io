---
type: Service
title: Nextcloud File Sync & Share
description: Nextcloud file synchronization and sharing service running as a Docker stack in the home-lab infrastructure
resource: ./nextcloud-service.md
tags: [service, nextcloud, file-sync, docker, cloud]
sources:
  - id: nextcloud-docker-compose
    resource: ./docker-compose.yml
    title: Nextcloud Docker Compose Configuration
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

# Nextcloud File Sync & Share

## Overview
Nextcloud is a self-hosted file sync and share server that provides access to files, calendars, contacts, mail & more from anywhere. In Aldo's home-lab, it runs as a Docker stack with separate containers for the application, database, and caching.

## Architecture
The Nextcloud deployment consists of three interconnected services:
1. **Database** (`db`): MariaDB 10.11.6 for storing metadata and file information
2. **Cache** (`redis`): Redis 7-alpine for transactional file locking and memory caching
3. **Application** (`app`): Nextcloud 34-apache serving the web interface and WebDAV endpoints

## Configuration
- Uses environment variables from `.env` file for secure configuration
- Database persists data in `./db` volume
- Redis persists data in `./redis` volume  
- Nextcloud application code in `./app` volume
- Data storage mounted from `/mnt/HDD1/nextcloud/data:/var/www/html/data`
- Custom Apache configuration for performance tuning
- Custom PHP configuration for memory limits and execution time
- Connected to external `traefik_net` network for reverse proxy integration

## Dependencies
- Docker Engine with Compose v2
- External Traefik network (`traefik_net`)
- Shared storage mount at `/mnt/HDD1/`
- Environment variables: MYSQL_ROOT_PASSWORD, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, REDIS_PASSWORD

## Health Checks
- Database: Uses `healthcheck.sh --connect --innodb_initialized`
- Redis: Uses `redis-cli -a \"$REDIS_PASSWORD\" ping | grep -q PONG`
- Application: Relies on successful startup and dependency health

## Related Concepts
- Node: pi3-node.md, pi5-node.md (where this service may be deployed)
- Docker Compose: docker-compose-template.md
- Infrastructure: 01-core-infra/ansible-role-template.md, 01-core-infra/docker-compose-template.md