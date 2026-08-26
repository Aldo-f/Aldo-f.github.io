---
title: Communities API
description: Communities API endpoints reference
---

# Communities API

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/communities` | No | List all communities |
| GET | `/api/communities/:name` | No | Get community by name |
| POST | `/api/communities` | Yes | Create new community |
| PUT | `/api/communities/:id` | Yes | Update community |
| DELETE | `/api/communities/:id` | Yes | Delete community |

## GET /api/communities

List all communities. Public endpoint, no authentication required.

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Kanjers",
      "slug": "kanjers",
      "description": "Best Belgian hits",
      "active": true,
      "created_at": "2026-01-01T00:00:00Z"
    }
  ]
}
```

## GET /api/communities/:name

Get community by name (slug). Public endpoint, no authentication required.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| `name` | string | Community slug/name |

### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Kanjers",
    "slug": "kanjers",
    "description": "Best Belgian hits",
    "owner_user_id": "user123",
    "active": true,
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

## POST /api/communities

Create a new community. Requires authentication.

!!! note "Stream Creation"
    This endpoint only creates the community. Stream is auto-created after tracks are added via sources.

### Request Body

```json
{
  "name": "My Radio",
  "description": "Community description"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "My Radio",
    "slug": "my-radio",
    "description": "Community description",
    "owner_user_id": "user123",
    "active": true,
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

## PUT /api/communities/:id

Update community details. Requires authentication and owner/admin permissions.

### Request Body

```json
{
  "name": "Updated Name",
  "description": "Updated description"
}
```

## DELETE /api/communities/:id

Delete a community. Requires owner or platform admin permissions.

!!! warning "Data Loss"
    Deleting a community will remove all associated sources, tracks, members, and play history.