---
title: Database Schema
description: Radio Community database tables and relationships
---

# Database Schema

## Tables Overview

| Table | Purpose |
|-------|---------|
| `communities` | Community definitions |
| `sources` | Music sources (joe_easy, deezer, manual) |
| `tracks` | Track metadata |
| `community_members` | User memberships |
| `played_instances` | Play history |
| `votes` | User votes on tracks |

## Table Definitions

### communities

Stores radio community definitions.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `name` | TEXT | Community name |
| `slug` | TEXT | URL-safe identifier |
| `description` | TEXT | Community description |
| `owner_user_id` | TEXT | Owner user ID |
| `stream_mount` | TEXT | Icecast mount point |
| `active` | BOOLEAN | Is community active |
| `created_at` | TIMESTAMP | Creation timestamp |

### sources

Music sources for a community.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `community_id` | INTEGER | FK to communities |
| `type` | TEXT | joe_easy, deezer, or manual |
| `name` | TEXT | Source display name |
| `config_json` | TEXT | Source configuration |
| `enabled` | BOOLEAN | Is source active |

### tracks

Track metadata and file paths.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `source_id` | INTEGER | FK to sources |
| `title` | TEXT | Track title |
| `artist` | TEXT | Artist name |
| `album` | TEXT | Album name |
| `duration` | INTEGER | Duration in seconds |
| `bpm` | INTEGER | Beats per minute |
| `deezer_id` | TEXT | Deezer track ID |
| `file_path` | TEXT | Relative path to audio file |

### community_members

User memberships in communities.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `community_id` | INTEGER | FK to communities |
| `user_id` | TEXT | User ID from auth |
| `role` | TEXT | admin or member |
| `stream_key` | TEXT | Personal stream access key |

### played_instances

Track play history.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `community_id` | INTEGER | FK to communities |
| `track_id` | INTEGER | FK to tracks |
| `played_at` | TIMESTAMP | When track was played |

### votes

User votes on track play instances.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `played_instance_id` | INTEGER | FK to played_instances |
| `user_id` | TEXT | User who voted |
| `value` | INTEGER | -1 (downvote) or +1 (upvote) |
| `created_at` | TIMESTAMP | Vote timestamp |

## Relationships

```
communities ──┬── sources ──┬── tracks
              │             │
              ├── community_members
              │
              ├── played_instances ──┬── votes
              │
              └── (stream management)
```

## Music Storage Model

```
/music/
└── community/
    └── {community_name}/
        └── {track_id}.mp3

# Database file_path stores relative path:
# community/kanjers/42.mp3
```