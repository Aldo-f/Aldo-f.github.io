# Traffmonetizer

A passive income app that generates revenue from affiliate clicks and ads.

## How to Obtain Credentials
1. Sign up at https://traffmonetizer.com
2. Install the Traffmonetizer app on your device
3. Complete the sign-up flow to link your account
4. Once linked, Traffmonetizer will generate a unique token
5. Place the credentials below in `credentials.local.jsonc`

## Environment Variables
- `TOKEN` – Your generated Traffmonetizer API token

## Usage
- Configure `PINO_SECRETS_FILE` to point to `credentials.local.jsonc`
- The orchestrator will read these credentials and start the traffmonetizer container

## Troubleshooting
- If the container fails to start, ensure the Traffmonetizer app is installed and linked
- If credentials are invalid, regenerate them in the Traffmonetizer app
