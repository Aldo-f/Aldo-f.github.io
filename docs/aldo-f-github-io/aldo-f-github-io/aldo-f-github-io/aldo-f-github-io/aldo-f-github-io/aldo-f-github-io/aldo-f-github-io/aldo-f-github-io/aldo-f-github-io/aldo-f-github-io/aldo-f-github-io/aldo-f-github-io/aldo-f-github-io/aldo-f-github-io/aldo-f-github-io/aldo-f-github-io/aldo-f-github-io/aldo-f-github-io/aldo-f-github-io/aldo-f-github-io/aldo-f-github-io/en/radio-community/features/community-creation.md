---
title: Community Creation
description: Radio Community creation flow documentation
---

# Community Creation

## 2-Step Creation Flow

The community creation process is split into two steps to ensure proper setup:

```
┌─────────────────┐     ┌─────────────────┐
│  Step 1:        │     │  Step 2:        │
│  Community      │────▶│  Source         │
│  Info           │     │  Selection      │
└─────────────────┘     └─────────────────┘
        │                       │
        ▼                       ▼
   name (required)        type: joe_easy
   description (optional)   deezer
                           manual
```

## Step 1: Community Info

Enter basic community information:

| Field | Required | Description |
|-------|----------|-------------|
| **Name** | Yes | Community name |
| **Description** | No | Community description |

The name is converted to a URL-safe slug for the community URL.

## Step 2: Source Selection

Choose a music source type and configure it:

### Joe.be

| Option | Station ID |
|--------|------------|
| All Hits | `all_hits` |
| 70s | `70s` |
| 80s | `80s` |
| 90s | `90s` |
| 00s | `00s` |
| Hot | `hot` |

### Deezer

| Field | Description |
|-------|-------------|
| Playlist URL | Deezer playlist URL to import |

### Manual

No configuration needed. Add tracks manually after creation.

## Backend Flow

The creation process makes the following API calls:

1. `POST /api/communities` - Create community
2. `POST /api/communities/:id/sources` - Create source
3. `POST /api/communities/:id/sources/:sourceId/fetch` - Fetch tracks (skip for manual)
4. **Stream auto-created** after tracks exist

!!! note "Stream Timing"
    The stream is NOT created during community creation. This prevents empty playlist issues. The stream is automatically created once tracks exist.

## Stream Auto-Creation

After tracks are added:
1. System detects tracks exist
2. Stream is automatically created and started
3. Members can now listen

## Manual Stream Control

After creation, admins can control the stream from the Manage Community page:
- **Start**: Create and start stream
- **Stop**: Stop running stream
- **Restart**: Restart to pick up new tracks