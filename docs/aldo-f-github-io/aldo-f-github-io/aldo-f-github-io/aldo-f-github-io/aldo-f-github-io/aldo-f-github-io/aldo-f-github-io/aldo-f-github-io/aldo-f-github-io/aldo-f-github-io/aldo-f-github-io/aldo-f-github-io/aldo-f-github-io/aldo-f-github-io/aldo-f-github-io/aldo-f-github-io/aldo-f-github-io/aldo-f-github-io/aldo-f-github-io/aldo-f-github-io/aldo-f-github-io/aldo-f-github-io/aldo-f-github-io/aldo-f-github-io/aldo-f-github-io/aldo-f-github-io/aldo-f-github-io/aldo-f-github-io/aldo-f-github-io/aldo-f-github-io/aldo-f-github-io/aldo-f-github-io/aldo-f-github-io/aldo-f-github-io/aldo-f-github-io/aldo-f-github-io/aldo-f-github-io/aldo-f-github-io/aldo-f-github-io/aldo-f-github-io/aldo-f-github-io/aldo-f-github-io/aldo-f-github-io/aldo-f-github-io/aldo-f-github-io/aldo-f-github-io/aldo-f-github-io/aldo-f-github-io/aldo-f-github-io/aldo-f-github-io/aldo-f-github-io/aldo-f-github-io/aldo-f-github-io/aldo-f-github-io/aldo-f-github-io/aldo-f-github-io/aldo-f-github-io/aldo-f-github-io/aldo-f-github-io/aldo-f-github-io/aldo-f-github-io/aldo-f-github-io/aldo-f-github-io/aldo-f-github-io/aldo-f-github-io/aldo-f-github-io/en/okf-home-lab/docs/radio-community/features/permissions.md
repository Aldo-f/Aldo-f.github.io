---
title: Permissions
description: Radio Community role-based permissions
---

# Permissions

## Roles

| Role | Description |
|------|-------------|
| **Owner** | User who created the community. Can delete community, add/remove admins |
| **Community Admin** | Member with role='admin' in community_members. Can manage most operations |
| **Community Member** | Member with role='member' in community_members. Can listen and vote |
| **Platform Admin** | Global platform administrator. Can do EVERYTHING on ALL communities |
| **Non-member** | Logged-in user who is NOT a member of this community |

## Platform Admin

The platform admin is defined by the `ADMIN_EMAIL` environment variable (default: `aldo@test.be`).

Platform admins have elevated permissions across ALL communities - they can manage any community even without being a member.

## Permission Matrix

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

## Implementation

Admin access is checked via `isAdmin(req.user)` function in `utils/auth.js`:

```javascript
const ADMIN_EMAIL = 'aldo@test.be';

function isPlatformAdmin(user) {
    return user && user.email === ADMIN_EMAIL;
}
```

## Helper Functions

For DRY permission handling, use the helper functions in `utils/auth.js`:

```javascript
const { PERMISSIONS, requirePermission } = require('./utils/auth');

app.delete('/api/communities/:id', authenticateToken, async (req, res) => {
    const denied = await requirePermission(req.user, communityId, PERMISSIONS.DELETE_COMMUNITY, dbGet, res);
    if (denied) return denied;
    // ... rest of handler
});
```

### Available Helpers

| Function | Description |
|----------|-------------|
| `isPlatformAdmin(user)` | Check if user is platform admin |
| `getUserRole(user, communityId, db)` | Get user's role in community |
| `hasPermission(user, communityId, permission, db)` | Check specific permission |
| `requirePermission(user, communityId, permission, db, res)` | Express middleware helper |

### Enums

- `ROLES`: OWNER, COMMUNITY_ADMIN, MEMBER, NON_MEMBER, PLATFORM_ADMIN
- `PERMISSIONS`: 24 permission constants
- `ROLE_PERMISSIONS`: Role-to-permission mapping