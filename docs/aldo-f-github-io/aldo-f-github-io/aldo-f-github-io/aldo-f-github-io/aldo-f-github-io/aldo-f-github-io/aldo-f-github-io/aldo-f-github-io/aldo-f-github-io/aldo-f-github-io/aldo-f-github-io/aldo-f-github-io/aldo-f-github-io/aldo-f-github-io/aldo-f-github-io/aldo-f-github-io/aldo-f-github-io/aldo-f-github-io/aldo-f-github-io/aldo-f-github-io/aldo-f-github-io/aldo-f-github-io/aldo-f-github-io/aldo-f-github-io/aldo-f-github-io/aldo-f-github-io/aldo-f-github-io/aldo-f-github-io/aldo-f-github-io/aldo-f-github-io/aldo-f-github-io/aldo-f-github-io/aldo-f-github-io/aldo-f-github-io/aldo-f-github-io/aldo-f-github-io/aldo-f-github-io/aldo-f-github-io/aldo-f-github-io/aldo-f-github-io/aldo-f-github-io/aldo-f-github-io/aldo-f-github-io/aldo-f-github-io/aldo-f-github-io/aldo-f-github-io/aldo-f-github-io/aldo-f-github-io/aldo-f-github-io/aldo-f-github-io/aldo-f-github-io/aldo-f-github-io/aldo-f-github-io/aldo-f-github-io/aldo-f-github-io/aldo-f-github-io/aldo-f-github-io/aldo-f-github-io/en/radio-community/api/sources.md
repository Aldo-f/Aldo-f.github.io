---
title: Sources API
description: Sources API endpoints reference
---

# Sources API

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/communities/:id/sources` | Yes | List sources |
| POST | `/api/communities/:id/sources` | Yes | Create source |
| PUT | `/api/communities/:id/sources/:sourceId` | Yes | Update source |
| DELETE | `/api/communities/:id/sources/:sourceId` | Yes | Delete source |
| POST | `/api/communities/:id/sources/:sourceId/fetch` | Yes | Fetch tracks |
| POST | `/api/communities/:id/sources/deezer/import` | Yes | Import from Deezer |
| GET | `/api/sources` | Yes | List all sources (global) |

## GET /api/communities/:id/sources

List all sources for a community. Requires authentication and membership.

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "community_id": 1,
      "type": "joe_easy",
      "name": "All Hits",
      "config_json": "{\"station_id\": \"all_hits\"}",
      "enabled": true
    }
  ]
}
```

## POST /api/communities/:id/sources

Create a source for a community. Requires admin permissions.

### Request Body

```json
{
  "type": "joe_easy",
  "name": "80s Hits",
  "config": {
    "station_id": "80s"
  }
}
```

### Source Types

| Type | Description | Config |
|------|-------------|--------|
| `joe_easy` | Joe.be Belgian radio | `station_id` (all_hits, 70s, 80s, 90s, 00s, hot) |
| `deezer` | Deezer playlist import | `playlist_url` |
| `manual` | Manual file uploads | No config needed |

## PUT /api/communities/:id/sources/:sourceId

Update source configuration. Requires admin permissions.

### Request Body

```json
{
  "name": "Updated Name",
  "enabled": true,
  "config": {
    "station_id": "90s"
  }
}
```

## DELETE /api/communities/:id/sources/:sourceId

Delete a source and optionally its tracks. Requires admin permissions.

## POST /api/communities/:id/sources/:sourceId/fetch

Fetch tracks from a source. Requires admin permissions.

### Request Body

```json
{
  "pages": 10
}
```

!!! note "Stream Restart"
    After successfully fetching tracks, the stream automatically restarts to include new tracks.

## POST /api/communities/:id/sources/deezer/import

Import tracks from a Deezer playlist URL. Requires admin permissions.

### Request Body

```json
{
  "playlist_url": "https://www.deezer.com/us/playlist/123456789"
}
```

## GET /api/sources

List all sources across all communities. Requires platform admin permissions.