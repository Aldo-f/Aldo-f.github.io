# Honeygain

## Overview
Honeygain is a passive income app that generates revenue from ad views on your device.

## How to Obtain Credentials
1. Sign up at https://honeygain.com
2. Install the Honeygain app on your device (phone, tablet, or PC)
3. Follow the in-app setup to connect your device to Honeygain
4. Once connected, Honeygain will generate a unique email and password pair
5. Place the credentials below in `credentials.local.jsonc`

## Environment Variables
- `EMAIL` – Your registered email address
- `PASSWORD` – Your generated Honeygain password

## Usage
- Configure `PINO_SECRETS_FILE` to point to `credentials.local.jsonc`
- The orchestrator will read these credentials and start the honeygain container

## Troubleshooting
- If the container fails to start, ensure your device is online and the Honeygain app is installed
- If credentials are invalid, regenerate them in the Honeygain app
