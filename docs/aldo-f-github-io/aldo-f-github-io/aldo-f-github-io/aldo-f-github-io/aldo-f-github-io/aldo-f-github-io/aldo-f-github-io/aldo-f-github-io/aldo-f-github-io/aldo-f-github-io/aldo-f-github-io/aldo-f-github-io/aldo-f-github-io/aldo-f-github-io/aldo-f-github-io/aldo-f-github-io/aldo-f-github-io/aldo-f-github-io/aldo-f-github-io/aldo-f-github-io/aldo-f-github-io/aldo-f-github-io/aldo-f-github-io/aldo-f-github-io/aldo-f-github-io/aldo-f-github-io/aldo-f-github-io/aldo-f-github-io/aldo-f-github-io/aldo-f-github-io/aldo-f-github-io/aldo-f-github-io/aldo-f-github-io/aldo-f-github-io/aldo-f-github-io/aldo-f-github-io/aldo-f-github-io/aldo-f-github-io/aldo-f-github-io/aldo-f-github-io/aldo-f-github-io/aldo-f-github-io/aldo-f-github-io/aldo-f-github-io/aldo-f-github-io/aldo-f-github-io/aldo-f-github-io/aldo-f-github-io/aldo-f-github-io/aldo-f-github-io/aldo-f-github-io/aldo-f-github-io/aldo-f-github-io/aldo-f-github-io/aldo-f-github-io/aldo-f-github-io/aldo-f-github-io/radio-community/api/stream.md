---
title: Stream API
description: Stream API endpoints reference
---

# Stream API

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/communities/:id/stream` | Yes | Get stream status |
| POST | `/api/communities/:id/stream/start` | Yes | Start stream |
| POST | `/api/communities/:id/stream/stop` | Yes | Stop stream |
| POST | `/api/communities/:id/stream/restart` | Yes | Restart stream |
| GET | `/api/stream` | No | Redirect to Icecast |
| GET | `/stream` | Yes | Proxy to Icecast |

## GET /api/communities/:id/stream

Get stream status for a community. Requires authentication and membership.

### Response

```json
{
  "success": true,
  "data": {
    "exists": true,
    "running": true,
    "container_name": "liquidsoap-kanjers"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `exists` | boolean | Whether stream container exists |
| `running` | boolean | Whether stream is running (null if not exists) |
| `container_name` | string | Docker container name (null if not exists) |

## POST /api/communities/:id/stream/start

Start or create a stream. Requires admin permissions.

!!! note "Prerequisites"
    Stream can only start if the community has at least one track with a file path.

## POST /api/communities/:id/stream/stop

Stop a running stream. Requires admin permissions.

## POST /api/communities/:id/stream/restart

Restart a stream. Requires admin permissions.

!!! note "Use Cases"
    Use restart after adding new tracks to refresh the playlist.

## GET /api/stream

Public endpoint to access stream. Requires valid stream key.

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | string | Member's stream key |

### Response

Redirects to Icecast stream URL if key is valid.

## GET /stream

Proxy endpoint to access stream. Requires authentication.

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | string | Member's stream key |

### Response

Proxies audio stream from Icecast.

## Stream URL Format

Members access streams at:

```
https://your-domain.com/stream?key=YOUR_STREAM_KEY
```

Each member receives a unique stream key from the admin.