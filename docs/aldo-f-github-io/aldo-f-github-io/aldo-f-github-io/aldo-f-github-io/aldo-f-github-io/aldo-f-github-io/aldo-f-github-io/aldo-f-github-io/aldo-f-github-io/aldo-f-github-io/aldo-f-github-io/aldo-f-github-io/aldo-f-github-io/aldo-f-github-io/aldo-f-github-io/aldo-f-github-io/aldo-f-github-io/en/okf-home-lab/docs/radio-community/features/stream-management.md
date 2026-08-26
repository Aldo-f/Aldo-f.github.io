---
title: Stream Management
description: Radio Community stream management documentation
---

# Stream Management

## Stream Components

### Icecast
- Stream distribution server
- Listens on port 8000 (configurable via ICECAST_PORT)
- Serves mount points for each community

### Liquidsoap
- Stream automation and playlist generation
- Feeds audio to Icecast
- Manages track selection based on algorithm

## Status Display

The ManageCommunityPage shows stream status:

| Field | Values |
|-------|--------|
| Stream Exists | Yes / No |
| Running | Yes / No / N/A |
| Container Name | string / null |

## Manual Controls

| Action | Description | Permission |
|--------|-------------|------------|
| **Start** | Create and start stream if not exists | Admin |
| **Stop** | Stop running stream (with confirmation) | Admin |
| **Restart** | Restart stream to pick up new tracks | Admin |

### Start Stream

Creates and starts a Liquidsoap container for the community.

!!! warning "Prerequisites"
    Stream can only start if the community has at least one track with a file path.

### Stop Stream

Stops the running Liquidsoap container.

### Restart Stream

Restarts the Liquidsoap container. Use this after adding new tracks to refresh the playlist.

## Automatic Stream Restart

Stream automatically restarts when new tracks are added:

1. New tracks fetched via joe_easy source
2. New tracks fetched via deezer source
3. Tracks synced via /sync endpoint

!!! note "Track Appending"
    New tracks are APPENDED to the playlist, not replacing existing ones. The listening experience is not disrupted.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/communities/:id/stream` | Get stream status |
| POST | `/api/communities/:id/stream/start` | Start stream |
| POST | `/api/communities/:id/stream/stop` | Stop stream |
| POST | `/api/communities/:id/stream/restart` | Restart stream |

## Stream Access

### URL Format

Members access streams at:

```
https://your-domain.com/stream?key=YOUR_STREAM_KEY
```

### Stream Key

Each member receives a unique stream key from the admin. This key is:
- Generated when member is added
- Used to validate access
- Personal to each member

### Public Access

Public access without key is also available:

```
GET /api/stream?key=xxx
```

This redirects to the Icecast stream URL if the key is valid.

## Docker Container

Streams run as Docker containers with naming convention:

```
liquidsoap-{community_slug}
```

Example: `liquidsoap-kanjers`