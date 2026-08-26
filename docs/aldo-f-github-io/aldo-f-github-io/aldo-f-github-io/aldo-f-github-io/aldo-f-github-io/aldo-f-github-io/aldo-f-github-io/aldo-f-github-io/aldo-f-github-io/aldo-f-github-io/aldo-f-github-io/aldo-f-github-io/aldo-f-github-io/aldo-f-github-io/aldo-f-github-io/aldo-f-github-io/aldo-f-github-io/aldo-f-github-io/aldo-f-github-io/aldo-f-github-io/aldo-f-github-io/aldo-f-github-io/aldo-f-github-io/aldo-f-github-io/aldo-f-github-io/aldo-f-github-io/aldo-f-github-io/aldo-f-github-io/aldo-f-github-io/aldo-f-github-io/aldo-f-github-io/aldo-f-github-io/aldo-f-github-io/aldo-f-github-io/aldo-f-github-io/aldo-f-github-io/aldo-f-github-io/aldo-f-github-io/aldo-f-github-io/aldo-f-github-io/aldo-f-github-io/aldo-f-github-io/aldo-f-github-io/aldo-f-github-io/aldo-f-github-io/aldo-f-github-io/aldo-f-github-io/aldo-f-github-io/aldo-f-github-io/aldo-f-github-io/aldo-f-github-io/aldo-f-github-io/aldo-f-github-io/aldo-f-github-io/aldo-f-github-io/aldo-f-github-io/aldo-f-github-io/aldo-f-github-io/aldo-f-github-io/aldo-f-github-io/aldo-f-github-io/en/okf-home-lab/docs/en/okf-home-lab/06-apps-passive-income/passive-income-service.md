---
type: Service
title: Passive Income Orchestrator
description: Passive income orchestrator application managing various income-generating services in the home-lab
resource: ./passive-income-service.md
tags: [service, apps, passive-income, orchestrator, docker]
sources:
  - id: passive-income-docker-compose
    resource: ./docker-compose.yml
    title: Passive Income Orchestrator Docker Compose Configuration
    author: aldo
    usage_count: 1
    last_modified: 2026-08-25T09:15:00Z
  - id: passive-income-readme
    resource: ./README.md
    title: Passive Income Orchestrator README
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

# Passive Income Orchestrator

## Overview
The Passive Income Orchestrator (PINO) is a Python-based application that manages various passive income providers (such as Honeygain, Earnapp, and Traffmonetizer) in a Dockerized environment. It provides a web interface for monitoring and controlling these services.

## Architecture
The orchestrator consists of several components:
- **Web Interface** (`webui.py`): Flask-based dashboard for monitoring provider status and earnings
- **Orchestrator** (`orchestrator.py`): Main application logic for managing provider connections and data flow
- **Provider Modules** (`/providers/`): Individual implementations for each passive income service
- **Rendering Engine** (`render.py`): Handles data presentation and report generation
- **Registry** (`registry.py`): Manages provider registration and discovery
- **Styling** (`style.py`): CSS and styling for the web interface

## Configuration
- Runs as a Docker container with access to the Docker socket for managing other containers
- Configuration stored in `./credentials.jsonc` (encrypted credentials)
- Provider-specific configurations in `/providers/` directory
- Secrets stored in `~/.config/pino/` directory (mounted as `/secrets` in container)
- Web interface accessible on port 4747
- Read-only access to provider source code for security

## Dependencies
- Docker Engine (for managing provider containers)
- Python 3.8+ with dependencies:
  - Flask (web interface)
  - Requests (HTTP communications)
  - Cryptography (credential encryption)
  - YAML (configuration parsing)
- Access to `/var/run/docker.sock` for container management
- Provider-specific dependencies (varies by service)

## Health Check
The service includes a health check endpoint at `http://localhost:4747/health` that returns:
- Status: OK when all components are functioning
- Provider connection status
- System resource usage
- Last update timestamps

## Data Flow
1. Provider credentials loaded from encrypted `credentials.jsonc`
2. Orchestrator initializes provider connections via their respective APIs
3. Provider modules handle authentication, data retrieval, and earnings calculation
4. Data processed through registry and rendering engines
5. Results displayed in web interface and available via API
6. Logs and metrics stored for historical analysis

## Security Features
- Credentials encrypted at rest using AES-256
- Provider configurations mounted read-only where possible
- Secrets stored in dedicated directory separate from application code
- Network isolation - only necessary ports exposed
- Regular credential rotation supported

## Related Concepts
- Node: pi3-node.md, pi5-node.md (where this service may be deployed)
- Docker Compose: docker-compose-template.md
- Infrastructure: 01-core-infra/ansible-role-template.md, 01-core-infra/docker-compose-template.md
- Providers: Individual provider documentation in `/providers/` directory