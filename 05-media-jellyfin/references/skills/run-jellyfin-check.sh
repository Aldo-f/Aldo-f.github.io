#!/bin/bash
# Jellyfin Health Check Script
# Executes the health check command for Jellyfin service

# Parameters
ENDPOINT="${1:-http://127.0.0.1:8096/health}"

# Execute the health check
curl -fsS -m 5 "$ENDPOINT"

# Exit with the same code as curl
exit $?