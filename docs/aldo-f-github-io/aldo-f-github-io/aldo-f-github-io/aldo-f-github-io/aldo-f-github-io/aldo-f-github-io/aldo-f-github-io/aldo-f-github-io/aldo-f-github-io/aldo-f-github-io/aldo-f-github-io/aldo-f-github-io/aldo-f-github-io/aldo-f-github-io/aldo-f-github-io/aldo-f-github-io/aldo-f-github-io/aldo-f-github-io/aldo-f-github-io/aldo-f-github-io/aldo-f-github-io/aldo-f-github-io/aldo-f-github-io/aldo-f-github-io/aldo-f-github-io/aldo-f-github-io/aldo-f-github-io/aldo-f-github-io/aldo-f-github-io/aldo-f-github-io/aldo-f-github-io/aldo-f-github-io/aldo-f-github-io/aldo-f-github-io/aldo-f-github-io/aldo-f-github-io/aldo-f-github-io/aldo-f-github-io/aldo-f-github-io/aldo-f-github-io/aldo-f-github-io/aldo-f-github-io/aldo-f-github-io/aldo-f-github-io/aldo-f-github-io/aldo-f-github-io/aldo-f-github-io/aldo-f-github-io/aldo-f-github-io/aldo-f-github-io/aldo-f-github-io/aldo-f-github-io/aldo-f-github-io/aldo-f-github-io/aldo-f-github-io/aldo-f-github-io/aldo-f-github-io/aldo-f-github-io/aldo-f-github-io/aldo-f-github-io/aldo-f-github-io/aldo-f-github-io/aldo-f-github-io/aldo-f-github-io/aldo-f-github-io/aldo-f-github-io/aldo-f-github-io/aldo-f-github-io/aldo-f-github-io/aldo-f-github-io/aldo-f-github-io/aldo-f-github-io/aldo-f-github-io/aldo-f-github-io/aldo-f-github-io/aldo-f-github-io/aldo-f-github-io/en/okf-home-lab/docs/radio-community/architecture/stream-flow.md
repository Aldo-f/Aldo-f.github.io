---
title: Stream Flow
description: Radio Community stream creation and management flow
---

# Stream Flow

## Stream Creation Flow

### Current Flow (Fixed 2026-03-28)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Create         │     │  Select         │     │  Fetch          │     │  Auto-create   │
│  Community      │────▶│  Source         │────▶│  Tracks         │────▶│  Stream         │
│  (name+desc)    │     │  (joe/deezer)   │     │  (if applicable)│     │  (after tracks)│
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

1. **Create Community** - User creates community with name + description
2. **Select Source** - User selects music source (joe_easy/deezer/manual) during creation
3. **Fetch Tracks** - System fetches tracks from source
4. **Auto-create Stream** - Stream is automatically created/started after tracks exist

### Key Behavior

- **Stream NOT created during community creation** - prevents empty playlist issues
- **Stream auto-restarts** when new tracks are added via fetch or sync
- **Stream controls** available in admin UI (start/stop/restart)

!!! warning "Previous Issue (Fixed)"
    Previously, streams were created immediately during community creation (before sources existed), resulting in empty playlists and non-functional streams.

## Stream Management (Admin)

### Status Display

The ManageCommunityPage shows stream status:
- Stream Exists: Yes/No
- Running: Yes/No/N/A
- Container Name

### Manual Controls

| Action | Description |
|--------|-------------|
| **Start** | Create and start stream if not exists |
| **Stop** | Stop running stream (with confirmation) |
| **Restart** | Restart stream to pick up new tracks |

### Automatic Stream Restart

Stream automatically restarts when new tracks are added:

1. New tracks fetched via joe_easy source
2. New tracks fetched via deezer source
3. Tracks synced via /sync endpoint

!!! note "Track Appending"
    New tracks are APPENDED to the playlist, not replacing existing ones. The listening experience is not disrupted.

## Stream Components

### Icecast
- Stream distribution server
- Listens on port 8000 (configurable)
- Serves mount points for each community

### Liquidsoap
- Stream automation
- Generates playlists based on algorithm
- Feeds audio to Icecast

## Stream URL Format

Members access streams via:

```
https://your-domain.com/stream?key=YOUR_STREAM_KEY
```

Each member receives a unique stream key from the admin.