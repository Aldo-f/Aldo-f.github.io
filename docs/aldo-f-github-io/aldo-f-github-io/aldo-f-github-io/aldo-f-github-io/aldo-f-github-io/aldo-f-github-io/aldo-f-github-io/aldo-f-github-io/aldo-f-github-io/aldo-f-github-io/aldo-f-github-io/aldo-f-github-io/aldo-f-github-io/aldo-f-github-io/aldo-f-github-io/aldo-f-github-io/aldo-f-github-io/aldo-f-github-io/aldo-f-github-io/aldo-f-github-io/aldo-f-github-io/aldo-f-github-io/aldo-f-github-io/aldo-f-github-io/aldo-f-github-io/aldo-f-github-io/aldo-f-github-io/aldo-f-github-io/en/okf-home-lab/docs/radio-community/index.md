---
title: Home
description: Radio Community - Democratic internet radio platform
---

# Radio Community

**Radio Community** is a democratic internet radio platform where community members can:

- Create and manage radio communities
- Add music from various sources (Joe.be, Deezer, manual uploads)
- Vote on tracks (swipe left/right)
- Listen to community streams

## Quick Links

- [Getting Started](getting-started.md)
- [Architecture Overview](architecture/structure.md)
- [API Reference](api/communities.md)
- [Features](features/voting.md)
- [Development Guide](dev/workflow.md)

## Key Features

### Multiple Communities
Create and manage separate radio communities with unique identities and music collections.

### Music Sources
- **Joe.be API**: Automated fetching from Belgian radio stations
- **Deezer**: Import playlists from Deezer
- **Manual Uploads**: Add your own music files

### Voting System
Community members vote on tracks (swipe left/right). The playlist algorithm balances votes, freshness, and variety to ensure fair rotation.

### Stream Control
Admins can start, stop, and restart streams from the admin UI.

### Role-based Access
- **Owner**: Community creator (can delete community, manage admins)
- **Community Admin**: Manage community operations
- **Community Member**: Listen and vote
- **Platform Admin**: Global access to all communities

## Tech Stack

- **Backend**: Node.js + Express
- **Database**: PostgreSQL (via node-postgres/pg)
- **Frontend**: React 18 + TypeScript + Tailwind CSS + DaisyUI
- **Streaming**: Icecast + Liquidsoap
- **Auth**: OAuth 2.0 (external auth-service)