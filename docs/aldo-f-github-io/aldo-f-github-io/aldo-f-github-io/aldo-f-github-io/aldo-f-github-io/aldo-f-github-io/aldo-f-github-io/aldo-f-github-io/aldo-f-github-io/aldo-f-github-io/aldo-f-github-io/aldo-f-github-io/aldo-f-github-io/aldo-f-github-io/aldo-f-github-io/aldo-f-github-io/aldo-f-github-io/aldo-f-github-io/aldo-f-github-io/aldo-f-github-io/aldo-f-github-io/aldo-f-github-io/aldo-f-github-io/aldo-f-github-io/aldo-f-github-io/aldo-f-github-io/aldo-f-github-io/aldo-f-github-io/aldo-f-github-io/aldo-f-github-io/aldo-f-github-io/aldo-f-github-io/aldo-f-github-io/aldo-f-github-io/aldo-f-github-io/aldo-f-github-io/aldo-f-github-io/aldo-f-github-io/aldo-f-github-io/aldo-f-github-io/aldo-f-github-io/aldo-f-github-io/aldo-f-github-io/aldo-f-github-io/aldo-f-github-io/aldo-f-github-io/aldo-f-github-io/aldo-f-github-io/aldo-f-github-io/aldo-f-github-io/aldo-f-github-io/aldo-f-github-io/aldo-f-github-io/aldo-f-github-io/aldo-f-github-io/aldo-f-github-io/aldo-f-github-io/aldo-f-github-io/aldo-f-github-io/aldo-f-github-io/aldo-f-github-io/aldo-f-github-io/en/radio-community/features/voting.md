---
title: Voting System
description: Radio Community voting system documentation
---

# Voting System

## Overview

The voting system allows community members to influence which tracks get played more frequently by voting up or down tracks as they listen.

## How It Works

### Voting Actions

| Action | Value | UI |
|--------|-------|-----|
| Upvote | `+1` | Swipe right |
| Downvote | `-1` | Swipe left |

### Voting Rules

1. **One vote per play instance** - A user can vote once per track play. If the same track plays again later, they can vote again.
2. **Score calculation** - Score = positive_votes - negative_votes
3. **Higher score = more plays** - Tracks with higher scores appear more frequently in the playlist

## API Endpoints

### Vote on Track

```
POST /api/communities/:id/votes
```

**Request Body:**

```json
{
  "played_instance_id": 123,
  "value": 1
}
```

**Values:**
- `1` - Upvote (swipe right)
- `-1` - Downvote (swipe left)

### Get Votes for Track

```
GET /api/communities/:id/tracks/:track_id/votes
```

Returns all votes for a specific track, showing who voted and what value.

## Score Display

Tracks are displayed with their current score in the frontend:

```json
{
  "id": 1,
  "title": "Summer of 69",
  "artist": "Bryan Adams",
  "score": 15
}
```

## Integration with Playlist

The voting score directly influences the playlist algorithm. See [Playlist Algorithm](playlist-algorithm.md) for details on how votes affect track selection.

!!! note "Vote Weight"
    Each vote carries significant weight in the algorithm. A score of 15 means 15 more net positive votes than negative votes for this track.