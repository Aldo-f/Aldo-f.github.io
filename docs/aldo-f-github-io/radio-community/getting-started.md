---
title: Getting Started
description: Quick start guide for Radio Community
---

# Getting Started

This guide will help you get up and running with Radio Community.

## Prerequisites

- Docker and Docker Compose
- PostgreSQL database
- External auth service (OAuth 2.0)

## Quick Start

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f radio-community
```

The application will be available at the configured domain.

## Creating Your First Community

### Step 1: Community Info

1. Navigate to the application
2. Click "Create Community"
3. Enter a community name (required)
4. Add a description (optional)

### Step 2: Source Selection

Choose a music source type:

| Source Type | Configuration | Description |
|-------------|---------------|-------------|
| **Joe.be** | Select station (all hits, 70s, 80s, 90s, 00s, hot) | Automated Belgian radio |
| **Deezer** | Enter playlist URL | Import from Deezer |
| **Manual** | No config needed | Upload your own files |

### Step 3: Create

Click "Create" to complete the process. The system will:
1. Create the community
2. Set up the selected source
3. Fetch tracks (if using Joe.be or Deezer)
4. Auto-create the stream once tracks exist

## Stream URL Format

Once a community has a stream, members can listen at:

```
https://your-domain.com/stream?key=YOUR_STREAM_KEY
```

Each member gets a unique stream key from the admin.

## Adding Members

Community admins can add members who will receive their own stream keys for listening.

## Next Steps

- [Architecture Overview](architecture/structure.md)
- [API Reference](api/communities.md)
- [Voting System](features/voting.md)
- [Development Guide](dev/workflow.md)<!-- freshness-proof 1787726577 -->
