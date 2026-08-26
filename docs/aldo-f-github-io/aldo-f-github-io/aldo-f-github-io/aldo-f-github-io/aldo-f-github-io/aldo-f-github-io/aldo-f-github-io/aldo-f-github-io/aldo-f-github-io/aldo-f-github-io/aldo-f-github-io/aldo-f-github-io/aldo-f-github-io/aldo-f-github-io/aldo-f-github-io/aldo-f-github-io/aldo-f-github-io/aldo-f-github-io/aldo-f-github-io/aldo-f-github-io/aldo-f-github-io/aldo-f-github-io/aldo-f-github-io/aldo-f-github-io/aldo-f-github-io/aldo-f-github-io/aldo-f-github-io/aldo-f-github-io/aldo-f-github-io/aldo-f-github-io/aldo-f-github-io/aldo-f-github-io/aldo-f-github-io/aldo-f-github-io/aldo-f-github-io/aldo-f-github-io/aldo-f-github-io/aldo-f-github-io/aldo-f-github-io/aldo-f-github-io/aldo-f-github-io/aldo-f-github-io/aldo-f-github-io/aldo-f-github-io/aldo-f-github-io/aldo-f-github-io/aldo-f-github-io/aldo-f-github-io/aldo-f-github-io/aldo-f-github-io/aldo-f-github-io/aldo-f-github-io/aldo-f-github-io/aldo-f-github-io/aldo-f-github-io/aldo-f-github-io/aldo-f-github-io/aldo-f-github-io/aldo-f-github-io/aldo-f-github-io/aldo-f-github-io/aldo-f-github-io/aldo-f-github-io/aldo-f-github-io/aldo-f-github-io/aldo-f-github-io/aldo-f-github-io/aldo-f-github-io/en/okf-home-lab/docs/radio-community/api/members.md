---
title: Members API
description: Members API endpoints reference
---

# Members API

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/communities/:id/members` | Yes | List members |
| POST | `/api/communities/:id/members` | Yes | Add member |
| DELETE | `/api/communities/:id/members/:userId` | Yes | Remove member |

## GET /api/communities/:id/members

List all members of a community. Requires authentication and membership.

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "community_id": 1,
      "user_id": "user123",
      "role": "owner",
      "stream_key": "abc123..."
    },
    {
      "id": 2,
      "community_id": 1,
      "user_id": "user456",
      "role": "admin",
      "stream_key": "def456..."
    },
    {
      "id": 3,
      "community_id": 1,
      "user_id": "user789",
      "role": "member",
      "stream_key": "ghi789..."
    }
  ]
}
```

## POST /api/communities/:id/members

Add a member to a community. Requires admin permissions.

### Request Body

```json
{
  "user_id": "user456",
  "role": "member"
}
```

### Roles

| Role | Description |
|------|-------------|
| `owner` | Community creator (can delete, manage admins) |
| `admin` | Community admin (manage members, sources, streams) |
| `member` | Regular member (listen, vote) |

!!! note "Adding Members"
    - Owners can add admins or members
    - Admins can only add members (not other admins)

## DELETE /api/communities/:id/members/:userId

Remove a member from a community. Requires admin permissions.

!!! warning "Removing Admins"
    Only owners and platform admins can remove admins. Regular admins cannot remove other admins.