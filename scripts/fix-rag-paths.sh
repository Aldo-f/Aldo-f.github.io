#!/usr/bin/env bash
set -euo pipefail

# Fix systemd unit paths from okf-home-lab to 02-ai-okf-home-lab
SERVICE_FILE="/etc/systemd/system/app-okf-rag.service"
OLD_PATH="/home/aldo/dev/okf-home-lab"
NEW_PATH="/home/aldo/dev/02-ai-okf-home-lab"

if [ -f "$SERVICE_FILE" ]; then
    sudo sed -i "s|${OLD_PATH}|${NEW_PATH}|g" "$SERVICE_FILE"
    echo "Updated service file paths"
else
    echo "Service file not found: $SERVICE_FILE"
    exit 1
fi

sudo systemctl daemon-reload
sudo systemctl restart app-okf-rag
sleep 3
sudo systemctl status app-okf-rag --no-pager -l