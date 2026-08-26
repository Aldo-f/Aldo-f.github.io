---
title: Playlist Algorithm
description: Radio Community playlist scoring algorithm
---

# Playlist Algorithm

## Overview

The playlist algorithm ensures fair rotation so that every community member's music gets played. It combines votes, freshness, source priority, and play history to calculate a score for each track.

## Score Calculation

```
voteScore = (positive_votes - negative_votes) × 10
freshnessBonus = min(days_since_added × 0.5, 10)
sourceWeight = manual (3) | deezer (2) | joe_easy (1)
playPenalty = play_count × 2

Score = voteScore + freshnessBonus + sourceWeight - playPenalty
```

### Score Components

| Component | Calculation | Max Value |
|-----------|-------------|-----------|
| voteScore | (positive - negative) × 10 | Unlimited |
| freshnessBonus | days × 0.5 | 10 |
| sourceWeight | manual: 3, deezer: 2, joe_easy: 1 | 3 |
| playPenalty | plays × 2 | Unlimited (reduces score) |

### Minimum Score Threshold

Tracks with score >= -20 are included in the playlist. Tracks below this threshold are excluded.

## Stream Playlist Generation

The stream uses weighted random selection with variety filters:

### 1. Categorization (after scoring)

| Category | Tracks |
|----------|--------|
| HOT | Top 10 tracks by score |
| REGULAR | Tracks 11-50 by score |
| COLD | Tracks 50+ by score |

### 2. Weighted Random Selection

| Category | Selection Chance |
|----------|-------------------|
| HOT | 40% |
| REGULAR | 40% |
| COLD | 20% |

### 3. Variety Filters (excluded from selection)

- Tracks played in last 60 minutes
- Same artist as last 2 played tracks
- Same album as last 1 played track

### 4. Fallback Strategy

If a category is empty or all tracks are filtered out, the algorithm tries other categories. Maximum 10 attempts per track.

## Design Goals

### Fair Rotation
No single user dominates; everyone's contributions get played.

### Vote-Based
Upvotes increase play frequency, downvotes decrease it.

### Freshness Boost
New tracks get promoted to encourage variety.

### Source Priority
Manual uploads are prioritized to encourage user contributions.

### Repetition Avoidance
Recently played tracks are penalized to maintain variety.

## Source Weights Rationale

| Source | Weight | Rationale |
|--------|--------|-----------|
| **joe_easy** | 1 | Lowest weight - fully automated API additions requiring no user effort |
| **deezer** | 2 | Medium weight - imported content requiring user initiation but minimal effort |
| **manual** | 3 | Highest weight - user-uploaded content recognizing personal effort in sourcing and adding tracks |

## Research Inspiration

- **TeamPlayer**: Democratic internet radio with member-created playlists
- **Vote Radio**: Song selection based on voting results
- **AzuraCast**: Playlist weights and request control systems

!!! note "Track Appending"
    Tracks are NOT replaced when new ones are fetched - they are ADDED to the playlist. The frontend shows the first 10 tracks from the sorted list.