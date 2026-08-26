---
title: Tracks API
description: Tracks API endpoints reference
---

# Tracks API

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/communities/:id/tracks` | Yes | Get tracks with scores |
| GET | `/api/communities/:id/tracks/:track_id/votes` | Yes | Get votes for track |
| GET | `/api/communities/:id/current` | Yes | Get current playing track |
| GET | `/api/communities/:id/playlist` | Yes | Get M3U playlist |
| GET | `/api/communities/:id/playlist.json` | Yes | Get JSON playlist |
| POST | `/api/communities/:id/votes` | Yes | Vote on track |
| POST | `/api/communities/:id/fetch-joe` | Yes | Fetch from Joe.be |
| POST | `/api/communities/:id/sync` | Yes | Sync with filesystem |
| POST | `/api/communities/:id/tracks/:trackId/download` | Yes | Download track |
| POST | `/api/communities/:id/tracks/download-all` | Yes | Download all missing |

## GET /api/communities/:id/tracks

Get tracks with scores. Requires authentication and membership.

Only returns tracks that have a `file_path` (downloadable tracks).

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Max tracks to return (default: 50) |
| `offset` | integer | Offset for pagination |

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Summer of 69",
      "artist": "Bryan Adams",
      "album": "Waking Up the Neighbours",
      "duration": 320,
      "score": 15,
      "file_path": "community/kanjers/1.mp3"
    }
  ]
}
```

## GET /api/communities/:id/tracks/:track_id/votes

Get all votes for a specific track. Requires authentication and membership.

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user_id": "user123",
      "value": 1,
      "created_at": "2026-01-01T00:00:00Z"
    }
  ]
}
```

## GET /api/communities/:id/current

Get the currently playing track. Requires authentication and membership.

## GET /api/communities/:id/playlist

Get the M3U playlist (sorted by score). Requires authentication and membership.

### Response

Content-Type: `audio/x-mpegurl`

## GET /api/communities/:id/playlist.json

Get the JSON playlist. Requires authentication and membership.

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Summer of 69",
      "artist": "Bryan Adams",
      "file_path": "community/kanjers/1.mp3",
      "score": 15
    }
  ]
}
```

## POST /api/communities/:id/votes

Vote on a track. Requires authentication and membership.

### Request Body

```json
{
  "played_instance_id": 123,
  "value": 1
}
```

### Values

| Value | Meaning |
|-------|---------|
| `1` | Upvote (swipe right) |
| `-1` | Downvote (swipe left) |

!!! note "One Vote Per Play"
    One vote is allowed per track play instance. Users can vote again if the same track plays again.

## POST /api/communities/:id/fetch-joe

Fetch tracks from Joe.be API. Requires admin permissions.

### Request Body

```json
{
  "pages": 10
}
```

## POST /api/communities/:id/sync

Sync tracks with filesystem. Requires admin permissions.

### Request Body

```json
{
  "download_missing": false
}
```

!!! note "File Path"
    Tracks without `file_path` can be synced with the filesystem via this endpoint.

## POST /api/communities/:id/tracks/:trackId/download

Download a single track from Deezer. Requires admin permissions.

## POST /api/communities/:id/tracks/download-all

Batch download all tracks without `file_path`. Requires admin permissions.