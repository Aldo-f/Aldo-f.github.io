# Radio Community - Project Documentation

## Overview

**Radio Community** is a democratic internet radio platform where community members can:
- Create and manage radio communities
- Add music from various sources (Joe.be, Deezer, manual uploads)
- Vote on tracks (swipe left/right)
- Listen to community streams

## Architecture

```
radio-community/
├── server.js          # Main Express server (3197 lines, 80+ routes)
├── db/
│   └── init.postgres.sql  # PostgreSQL database schema
├── utils/
│   ├── auth.js       # Permission system (ROLES, PERMISSIONS, isAdmin)
│   ├── slugify.js    # URL slug generation
│   └── fileUtils.js  # File operations (setOwnership)
├── streams/
│   ├── deezerDownloader.js  # Deezer API integration
│   ├── joeBeDownloader.js    # Joe.be API integration
│   └── streamManager.js      # Liquidsoap stream management
├── frontend/
│   └── src/
│       ├── components/ # 17 React components
│       ├── pages/      # 6 route pages
│       ├── types/      # Shared TypeScript interfaces
│       └── lib/        # Context providers
└── docker-compose.yml  # Service orchestration
```

## Technology Stack

- **Backend**: Node.js + Express
- **Database**: PostgreSQL (via node-postgres/pg)
- **Frontend**: React 18 + TypeScript + Tailwind CSS + DaisyUI
- **Streaming**: Icecast + Liquidsoap
- **APIs**: Joe.be, Deezer
- **Auth**: OAuth 2.0 via external auth-service

## Stream Creation Flow

### Current Flow (Fixed 2026-03-28)
1. **Create Community** - User creates community with name + description
2. **Select Source** - User selects music source (joe_easy/deezer/manual) during creation
3. **Fetch Tracks** - System fetches tracks from source
4. **Auto-create Stream** - Stream is automatically created/started after tracks exist

### Key Behavior
- **Stream NOT created during community creation** - prevents empty playlist issues
- **Stream auto-restarts** when new tracks are added via fetch or sync
- **Stream controls** available in admin UI (start/stop/restart)

### Previous Issue (Fixed)
Previously, streams were created immediately during community creation (before sources existed), resulting in empty playlists and non-functional streams.

## API Endpoints

### Communities
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/communities | No | List all communities |
| GET | /api/communities/:id | Yes | Get community details |
| POST | /api/communities | Yes | Create community (no stream creation) |
| PUT | /api/communities/:id | Yes | Update community |
| DELETE | /api/communities/:id | Yes | Delete community |

### Sources
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/communities/:id/sources | Yes | List sources |
| POST | /api/communities/:id/sources | Yes | Create source |
| PUT | /api/communities/:id/sources/:sourceId | Yes | Update source |
| DELETE | /api/communities/:id/sources/:sourceId | Yes | Delete source |
| POST | /api/communities/:id/sources/:sourceId/fetch | Yes | Fetch tracks from source |
| POST | /api/communities/:id/sync | Yes | Sync tracks with filesystem |

### Tracks
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/communities/:id/tracks | Yes | Get tracks with scores |
| POST | /api/communities/:id/votes | Yes | Vote on track |
| GET | /api/communities/:id/playlist.m3u | Yes | Get M3U playlist |

### Members
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/communities/:id/members | Yes | List members |
| POST | /api/communities/:id/members | Yes | Add member |
| DELETE | /api/communities/:id/members/:userId | Yes | Remove member |

### Stream Management
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/communities/:id/stream | Yes | Get stream status |
| POST | /api/communities/:id/stream/start | Yes | Start stream |
| POST | /api/communities/:id/stream/stop | Yes | Stop stream |
| POST | /api/communities/:id/stream/restart | Yes | Restart stream |
| GET | /api/stream | No | Redirect to Icecast |
| GET | /stream/:communityId | Yes | Proxy to Icecast |

## Permissions

### Roles
- **Owner**: User who created the community (can delete community, add/remove admins)
- **Community Admin**: Member with role='admin' in community_members (everything except delete/add-remove admins)
- **Community Member**: Member with role='member' in community_members (listen, vote)
- **Platform Admin**: Global platform administrator (aldo@test.be, can do EVERYTHING on ALL communities)
- **Non-member**: Logged-in user who is NOT a member of this community

### Global Admin
The platform admin is defined by the `ADMIN_EMAIL` environment variable (default: `aldo@test.be`). Platform admins have elevated permissions across ALL communities - they can manage any community even without being a member.

### Permission Matrix

| Action | Owner | Community Admin | Platform Admin | Community Member | Non-member |
|--------|-------|-----------------|----------------|------------------|------------|
| **Community** |
| View community | ✅ | ✅ | ✅ | ✅ | ✅ |
| Update community | ✅ | ✅ | ✅ | ❌ | ❌ |
| Delete community | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Stream** |
| View stream status | ✅ | ✅ | ✅ | ✅ | ❌ |
| Start stream | ✅ | ✅ | ✅ | ❌ | ❌ |
| Stop stream | ✅ | ✅ | ✅ | ❌ | ❌ |
| Restart stream | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Sources** |
| List sources | ✅ | ✅ | ✅ | ✅ | ❌ |
| Create source | ✅ | ✅ | ✅ | ❌ | ❌ |
| Update source | ✅ | ✅ | ✅ | ❌ | ❌ |
| Delete source | ✅ | ✅ | ✅ | ❌ | ❌ |
| Fetch tracks | ✅ | ✅ | ✅ | ❌ | ❌ |
| Activate source | ✅ | ✅ | ✅ | ❌ | ❌ |
| Sync tracks | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Members** |
| List members | ✅ | ✅ | ✅ | ✅ | ❌ |
| Add member (as admin) | ✅ | ❌ | ✅ | ❌ | ❌ |
| Add member (as member) | ✅ | ✅ | ✅ | ❌ | ❌ |
| Remove member (who is admin) | ✅ | ❌ | ✅ | ❌ | ❌ |
| Remove member (who is member) | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Tracks** |
| View tracks | ✅ | ✅ | ✅ | ✅ | ❌ |
| Vote on tracks | ✅ | ✅ | ✅ | ✅ | ❌ |
| Update track | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Global (any community)** |
| Scan sources | - | - | ✅ | - | ❌ |
| Manage affiliates | - | - | ✅ | - | ❌ |

### Implementation
Admin access is checked via `isAdmin(req.user)` function in `utils/auth.js`:
```javascript
const ADMIN_EMAIL = 'aldo@test.be';

function isPlatformAdmin(user) {
    return user && user.email === ADMIN_EMAIL;
}
```

For DRY permission handling, use the helper functions:
```javascript
const { PERMISSIONS, requirePermission } = require('./utils/auth');

app.delete('/api/communities/:id', authenticateToken, async (req, res) => {
    const denied = await requirePermission(req.user, communityId, PERMISSIONS.DELETE_COMMUNITY, dbGet, res);
    if (denied) return denied;
    // ... rest of handler
});
```

Available helpers in `utils/auth.js`:
- `isPlatformAdmin(user)` - Check if user is platform admin
- `getUserRole(user, communityId, db)` - Get user's role in community
- `hasPermission(user, communityId, permission, db)` - Check specific permission
- `requirePermission(user, communityId, permission, db, res)` - Express middleware helper

## Database Schema

### Tables

**communities**
- id, name, slug, description, owner_user_id, active, created_at

**sources**
- id, community_id, type (joe_easy/deezer/manual), name, config_json, enabled

**tracks**
- id, source_id, title, artist, album, duration, bpm, deezer_id, file_path

**community_members**
- id, community_id, user_id, role (admin/member), stream_key

**votes**
- id, played_instance_id, user_id, value (-1/0/1), created_at

## 2-Step Community Creation

### User Flow
1. **Step 1 - Community Info**
   - Enter community name (required)
   - Add description (optional)

2. **Step 2 - Source Selection**
   - Select source type: joe_easy, deezer, or manual
   - Configure source:
     - **joe_easy**: Select station (6 options: all hits, 70s, 80s, 90s, 00s, hot)
     - **deezer**: Enter playlist URL
     - **manual**: No config needed
   - Click "Create" to complete

### Backend Flow
1. POST /api/communities → create community
2. POST /api/communities/:id/sources → create source
3. POST /api/communities/:id/sources/:sourceId/fetch → fetch tracks (skip for manual)
4. Stream auto-created after tracks exist

## Voting System

- Users swipe left (-1) or right (+1) on tracks
- One vote allowed per track play instance
- Score = positive_votes - negative_votes
- Higher score = more frequent playback

## Playlist Algorithm

### Score Calculation
```
voteScore = (positive_votes - negative_votes) × 10
freshnessBonus = min(days_since_added × 0.5, 10)
sourceWeight = manual (3) | deezer (2) | joe_easy (1)
playPenalty = play_count × 2

Score = voteScore + freshnessBonus + sourceWeight - playPenalty
```

Tracks with score >= -20 are included.

### Stream Playlist Generation

The stream uses weighted random selection with variety filters:

1. **Categorization** (after scoring):
   - HOT: Top 10 tracks by score
   - REGULAR: Tracks 11-50 by score
   - COLD: Tracks 50+ by score

2. **Weighted Random Selection**:
   - 40% chance: Select from HOT
   - 40% chance: Select from REGULAR
   - 20% chance: Select from COLD

3. **Variety Filters** (excluded from selection):
   - Tracks played in last 60 minutes
   - Same artist as last 2 played tracks
   - Same album as last 1 played track

4. **Fallback**: If category is empty or filtered out, try other categories. Max 10 attempts per track.

**Note:** Tracks are NOT replaced when new ones are fetched - they are ADDED to the playlist. The frontend shows the first 10 tracks from the sorted list.

## Stream Management (Admin)

### Status Display
The ManageCommunityPage shows stream status:
- Stream Exists: Yes/No
- Running: Yes/No/N/A
- Container Name

### Manual Controls
- **Start**: Create and start stream if not exists
- **Stop**: Stop running stream (with confirmation)
- **Restart**: Restart stream to pick up new tracks

### Automatic Stream Restart
Stream automatically restarts when new tracks are added (so Liquidsoap picks up the updated playlist):
1. New tracks fetched via joe_easy source
2. New tracks fetched via deezer source
3. Tracks synced via /sync endpoint

**Important:** New tracks are APPENDED to the playlist, not replacing existing ones. The listening experience is not disrupted.

## Development Workflow

### Frontend Changes
1. Make changes in `frontend/src/`
2. Build: `cd frontend && npm run build`
3. **No container restart needed** - frontend/dist is mounted as volume

### Backend Changes
1. Changes to server.js require rebuild: `docker compose up -d --build`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 3000 | Server port |
| DATABASE_URL | - | PostgreSQL connection string (required) |
| AUTH_SERVICE_URL | http://auth-service:3008 | Auth service |
| MUSIC_PATH | /music | Music storage |
| DEEZER_ARL | - | Deezer download token |
| SOURCE_JOE | https://api.joe.be/2.0 | Joe.be API URL |
| JOE_STATION_ID | joe_easy | Default Joe.be station |
| DEEZER_API_BASE | https://api.deezer.com | Deezer API |
| ICECAST_HOST | icecast | Icecast server |
| ICECAST_PORT | 8000 | Icecast port |
| ADMIN_EMAIL | aldo@test.be | Platform admin email |

## Recent Changes (2026-03-29)

### Permission System Refactor
1. **Created `utils/auth.js`**: DRY permission system with:
   - `ROLES` enum: OWNER, COMMUNITY_ADMIN, MEMBER, NON_MEMBER, PLATFORM_ADMIN
   - `PERMISSIONS` enum: 24 permission constants
   - `ROLE_PERMISSIONS` matrix: Role-to-permission mapping
   - Helper functions: `isPlatformAdmin()`, `getUserRole()`, `hasPermission()`, `requirePermission()`
2. **Fixed isAdmin export**: Added backward-compatible `isAdmin` alias for existing code
3. **Fixed isAdmin call signatures**: Changed `isAdmin(req.user.email)` to `isAdmin(req.user)` in 4 places

### Test Infrastructure Fix
1. **Fixed missing imports**: Added `@playwright/test` imports to:
   - `tests/api/02-seed-flow.spec.js`
   - `tests/api/03-seed-source-create.spec.js`
2. **Excluded unit tests**: Added `testIgnore` to `playwright.config.js`

### Files Changed (Permission System)
- `utils/auth.js` (new - 260 lines)
- `server.js` - Updated permission checks

### Files Changed (Tests)
- `tests/api/02-seed-flow.spec.js` - Added Playwright import
- `tests/api/03-seed-source-create.spec.js` - Added Playwright import
- `playwright.config.js` - Added testIgnore for unit tests

---

## Recent Changes (2026-03-28)

### Stream Fix & 2-Step Creation
1. **Fixed stream creation timing**: Removed stream creation from community creation (was causing empty playlists)
2. **Auto-restart after track fetch**: Added streamManager.restartCommunityStream() after successful fetches
3. **2-step CreateCommunityPage**: Community info → source selection → auto-create
4. **Stream status in UI**: Added "Stream" tab in ManageCommunityPage
5. **Stream controls**: Start/Stop/Restart buttons with loading states

### Files Changed (Stream Fix)
- `server.js` - Removed line 828-833, added restart calls at lines 1522-1529, 2087-2090, 2140-2143
- `frontend/src/pages/CreateCommunityPage.tsx` - Complete rewrite with 2-step form
- `frontend/src/pages/ManageCommunityPage.tsx` - Added stream status & controls

## Previous Refactoring (2026-03-27)

### Completed
1. **Dead code removal**: Removed server.js.backup, debug-test.js, duplicate directory
2. **DRY - Backend**: Extracted setOwnership to utils/fileUtils.js
3. **DRY - Frontend**: Created shared types in frontend/src/types/index.ts
   - Track, Community, Member, Vote, Source interfaces
   - Updated 11 components to use shared types
4. **Middleware**: Created server/middleware/auth.js, membership.js

### Files Changed (Refactoring)
- `utils/fileUtils.js` (new)
- `streams/deezerDownloader.js` (refactored)
- `streams/joeBeDownloader.js` (refactored)
- `frontend/src/types/index.ts` (new)
- `frontend/src/components/*.tsx` (11 files updated)
- `server/middleware/auth.js` (new)
- `server/middleware/membership.js` (new)

## Future Improvements (Not Implemented)

1. **MVC Separation**: Full refactor of server.js into routes/controllers/models
2. **Centralized API Client**: Create frontend/src/lib/api.ts
3. **Rate Limiting**: Add express-rate-limit to protect endpoints
4. **Caching**: Add Redis for frequently accessed data
5. **Testing**: Add Jest unit tests and Playwright E2E tests
