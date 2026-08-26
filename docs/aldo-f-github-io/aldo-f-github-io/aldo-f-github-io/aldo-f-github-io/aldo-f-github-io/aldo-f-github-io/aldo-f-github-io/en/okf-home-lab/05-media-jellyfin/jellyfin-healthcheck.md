---
type: Attested Computation
title: Jellyfin Health Check
description: Verifies that the Jellyfin media server is responding to health check requests
resource: ./jellyfin-healthcheck.md
tags: [attested-computation, health-check, jellyfin, monitoring]
sources:
  - id: jellyfin-service-config
    resource: ./jellyfin-service.md
    title: Jellyfin Media Server Service
    author: human:aldo
    usage_count: 1
    last_modified: 2026-08-25T09:15:00Z
  - id: jellyfin-docker-compose
    resource: ./docker-compose.yml
    title: Jellyfin Docker Compose Configuration
    author: aldo
    usage_count: 1
    last_modified: 2026-08-25T09:15:00Z
generated:
  by: reference_agent/gemini-2.5-pro
  at: 2026-08-25T09:15:00Z
verified:
  - by: human:aldo
    at: 2026-08-25T09:15:00Z
status: stable
stale_after: 2027-02-25T09:15:00Z
runtime: bash
parameters:
  - name: endpoint
    type: string
    required: true
    description: The HTTP endpoint to check for health status
executor:
  resource: ./references/skills/run-jellyfin-check.sh
  receipt:
    - job_id
    - executed_command
    - exit_code
    - stdout
attester:
  resource: ./references/attesters/check-http.py
---

# Jellyfin Health Check

This Attested Computation verifies that the Jellyfin media server is responding correctly to health check requests by executing a curl command against the health endpoint.

## Computation

```bash
curl -fsS -m 5 http://127.0.0.1:8096/health
```

## Expected Result
- Exit code 0 indicates healthy service
- Any non-zero exit code indicates unhealthy service
- Output should be empty on success (due to `>/dev/null` redirect in actual usage)
- The `-f` flag makes curl fail silently on HTTP errors
- The `-s` flag enables silent mode
- The `-S` flag shows errors if they occur
- The `-m 5` flag sets a 5-second timeout

## Verification
This computation is verified by the attester script at `./references/attesters/check-http.py` which validates:
1. The command was executed correctly
2. The exit code matches expected values
3. The output indicates a healthy service when appropriate