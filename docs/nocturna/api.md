# Nocturna API Reference

Nocturna exposes a REST API under `/api/`. All endpoints require authentication unless noted. The API is documented using OpenAPI 3.0 — see Swagger UI at `/api-docs` when the server is running.

---

## Authentication

### Session-Based Auth

Nocturna uses server-side sessions (no JWTs):

- **Session token**: 32-byte random hex, 30-day expiry
- **Storage**: `localStorage` key `nocturna_session_token`
- **Header**: `Authorization: Bearer <token>`

### Auth Endpoints

| Method | Path | Auth | Body | Response |
|--------|------|------|------|----------|
| POST | `/api/auth/register` | ❌ | `{ username, password }` | `{ user, token, instances, activeInstance }` |
| POST | `/api/auth/login` | ❌ | `{ username, password }` | `{ user, token, activeInstance }` |
| POST | `/api/auth/logout` | ✅ | — | `{ ok: true }` |
| GET | `/api/auth/me` | ✅ | — | `{ user, activeInstance }` |

---

## Instances

Manage Hermes backend connections. Each user has isolated instances.

### Instance Object

```typescript
interface Instance {
  id: string;
  user_id: string;
  name: string;
  type: 'gateway' | 'ssh' | 'local_cli' | 'lan';
  url?: string;              // gateway/lan URL
  password?: string;         // gateway auth (never returned in GET)
  api_key?: string;          // gateway API key (never returned in GET)
  ssh_host?: string;
  ssh_port?: number;         // default 22
  ssh_user?: string;
  ssh_password?: string;     // never returned
  ssh_key?: string;          // never returned
  ssh_path?: string;
  is_default: boolean;
  status: 'unknown' | 'healthy' | 'unhealthy';
  last_error?: string;
  last_checked: number;
  created_at: number;
}
```

### Endpoints

| Method | Path | Auth | Body | Response |
|--------|------|------|------|----------|
| GET | `/api/instances` | ✅ | — | `{ instances: Instance[], activeInstanceId: string }` |
| POST | `/api/instances` | ✅ | `{ name, type, url?, password?, api_key?, ssh_*? }` | `{ instance }` |
| PUT | `/api/instances/:id` | ✅ | Partial Instance | `{ instance }` |
| DELETE | `/api/instances/:id` | ✅ | — | `{ ok: true }` |
| POST | `/api/instances/:id/select` | ✅ | — | `{ activeInstance }` |
| POST | `/api/instances/:id/set-default` | ✅ | — | `{ instance }` |
| POST | `/api/instances/:id/test` | ✅ | — | `{ ok: boolean, error?: string }` |
| POST | `/api/instances/test-connection` | ✅ | Instance config (unsaved) | `{ ok: boolean, error?: string }` |
| POST | `/api/instances/auto-detect-local` | ✅ | `autoLink?: boolean` | `{ instance, autoCreated: boolean }` |
| POST | `/api/instances/discover-lan` | ✅ | — | `{ instances: DiscoveredInstance[] }` |

### Discovered Instance

```typescript
interface DiscoveredInstance {
  url: string;           // e.g., "http://192.168.0.5:8787"
  name: string;          // hostname or "Hermes @ 192.168.0.5"
  type: 'lan';
  version?: string;
  board?: string;
}
```

---

## Tasks / Kanban

All task/kanban endpoints proxy to the active backend (CLI or Gateway).

### Task Object

```typescript
interface Task {
  id: string;
  board: string;
  status: 'triage' | 'todo' | 'ready' | 'running' | 'blocked' | 'review' | 'done' | 'archived';
  title: string;
  body: string;
  assignee?: string;
  priority: number;        // 1-5
  goal_mode: boolean;
  acceptance_criteria?: string;
  max_runtime?: string;    // e.g., "30m"
  max_retries?: number;
  created_at: number;
  updated_at: number;
  archived: boolean;
}
```

### Task Detail (Extended)

```typescript
interface TaskDetail extends Task {
  comments: { author: string; body: string; at: number }[];
  events: { id: number; kind: string; detail: string; at: number }[];
  attachments: unknown[];
  parents: string[];
  children: string[];
  runs?: RunRow[];
  goal_max_turns?: number;
  max_retries?: number | null;
  latest_summary?: string | null;
}
```

### Endpoints

| Method | Path | Auth | Query / Body | Response |
|--------|------|------|--------------|----------|
| GET | `/api/tasks` | ✅ | `board?, status?, assignee?, archived?, limit?` | `{ tasks: Task[] }` |
| GET | `/api/tasks/:id` | ✅ | — | `{ task: TaskDetail }` |
| POST | `/api/tasks` | ✅ | `{ board, title, body, assignee?, priority?, goal_mode?, acceptance_criteria?, max_runtime?, max_retries? }` | `{ task }` |
| PATCH | `/api/tasks/:id` | ✅ | Partial Task (title, body, priority, assignee) | `{ task }` |
| DELETE | `/api/tasks/:id` | ✅ | — | `{ ok: true }` (archives) |
| GET | `/api/boards` | ✅ | — | `{ boards: { slug, name }[] }` |
| GET | `/api/kanban` | ✅ | `board?` | `{ columns: { status, tasks: Task[] }[] }` |
| POST | `/api/kanban` | ✅ | `{ board, columns: { status, taskIds }[] }` | `{ ok: true }` |

---

## Lifecycle Actions (CRITICAL)

**Direct status PATCH is forbidden** (409 `forbidden_move`). Use these action endpoints:

| Method | Path | Transition |
|--------|------|------------|
| POST | `/api/tasks/:id/complete` | → `done` |
| POST | `/api/tasks/:id/block` | → `blocked` |
| POST | `/api/tasks/:id/unblock` | → `todo` (or previous) |
| POST | `/api/tasks/:id/request-review` | → `review` |
| POST | `/api/tasks/:id/request-changes` | → `changes_requested` |
| POST | `/api/tasks/:id/promote` | Next column in workflow |
| POST | `/api/tasks/:id/archive` | `archived=true` |

**Response:** `{ task: TaskDetail }` — updated task with new status.

---

## Bulk Actions

| Method | Path | Auth | Body | Response |
|--------|------|------|------|----------|
| POST | `/api/tasks/bulk` | ✅ | `{ ids: string[], action: 'complete'|'block'|'unblock'|'archive'|'promote', arg?: string }` | `{ results: { id, ok, error? }[] }` |

---

## Runs (Gateway Mode Only)

| Method | Path | Auth | Body | Response |
|--------|------|------|------|----------|
| POST | `/api/runs` | ✅ | `{ task_id, profile?, max_turns? }` | `{ run: RunRow }` |
| POST | `/api/runs/approve/:id` | ✅ | — | `{ run: RunRow }` |

### Run Row

```typescript
interface RunRow {
  run: number;           // alias for id
  id: number;
  task_id: string;
  profile?: string;
  max_turns: number;
  status: 'pending' | 'approved' | 'rejected' | 'running' | 'completed' | 'failed';
  started_at: number | null;
  ended_at: number | null;
  outcome?: string;
  summary?: string;
}
```

---

## Events

Poll for real-time engine events (used by frontend for live updates).

| Method | Path | Auth | Query | Response |
|--------|------|------|-------|----------|
| GET | `/api/events` | ✅ | `since=<epoch_ms>&board=<slug>` | `{ events: EventRow[], last_id: number }` |

### Event Row

```typescript
interface EventRow {
  id: number;
  task_id: string;
  kind: string;            // 'started', 'completed', 'blocked', 'tool_call', etc.
  detail: string;
  at: number;
}
```

### Behavior Rules

- `since=0` → return all events (full snapshot)
- Frontend caches `last_id` and passes it on subsequent polls for deltas
- Hard cap: 500 events per request
- Events scoped to requested board only
- Composed from per-task runs (Hermes CLI has no global event feed)

---

## System

| Method | Path | Auth | Response |
|--------|------|------|----------|
| GET | `/api/health` | ✅ | `{ status, engine, stats }` |
| GET | `/api/gateway/status` | ✅ | `{ reachable, config_ok, latency_ms }` |

### Health Response

```typescript
interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  engine: 'cli' | 'gateway' | 'lan' | 'ssh';
  stats: {
    tasks: number;
    running: number;
    blocked: number;
  };
}
```

---

## Error Codes

All errors follow this envelope:

```json
{
  "error": {
    "code": "engine_unreachable|cli_error|not_found|validation|forbidden_move|unauthorized|conflict",
    "message": "Human-readable message",
    "detail": "Additional context (optional)"
  }
}
```

| Code | HTTP | Origin | When |
|------|------|--------|------|
| `engine_unreachable` | 503 | `CliError` | Hermes binary missing / timeout / gateway unreachable |
| `cli_error` | 502 | `CliError` | Non-zero exit / malformed JSON from CLI |
| `validation` | 422 | `HTTPException` | Bad board slug, missing required field |
| `not_found` | 404 | `HTTPException` | Unknown task ID, instance ID |
| `forbidden_move` | 409 | `HTTPException` | Direct status PATCH, illegal transition |
| `unauthorized` | 401 | `HTTPException` | Invalid/expired session, no active instance |
| `conflict` | 409 | `HTTPException` | Duplicate instance URL, concurrent modification |

---

## Frontend Error Handling

`src/api/client.ts` wraps every fetch:

```typescript
class ApiError extends Error {
  code: string;
  detail?: string;
  status: number;
  constructor(response: Response, body: any) {
    super(body?.error?.message ?? 'API error');
    this.code = body?.error?.code ?? 'unknown';
    this.detail = body?.error?.detail;
    this.status = response.status;
  }
}

// Usage
try {
  const task = await api.tasks.get(id);
} catch (e) {
  if (e instanceof ApiError) {
    switch (e.code) {
      case 'engine_unreachable': showSetupOverlay(); break;
      case 'forbidden_move': toast('That action isn\'t allowed here'); break;
      case 'unauthorized': redirectToLogin(); break;
      default: toast(e.message);
    }
  }
}
```

---

## OpenAPI / Swagger

- **Swagger UI**: `http://localhost:3000/api-docs` (dev) or `https://your-domain/api-docs` (prod)
- **Raw spec**: `GET /api/spec.json` or `dist/specs.json` (generated at build)
- **Validate**: `npx swagger-cli validate ./dist/specs.json`

---

## Rate Limits

Currently **no rate limiting** on auth endpoints. Tracked for v1.1.

---

## Versioning

API version is not in URL path. Breaking changes will be communicated via:
- `X-Nocturna-Version` response header
- Changelog in `CHANGELOG.md`
- GitHub releases

---

## Examples

### Create Task (CLI Backend)

```bash
curl -X POST http://localhost:3000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "board": "nocturna",
    "title": "Refactor kanban CLI",
    "body": "Move to TypeScript, add tests",
    "priority": 4,
    "goal_mode": true,
    "acceptance_criteria": "All tests pass, TypeScript strict mode clean"
  }'
```

### Complete Task

```bash
curl -X POST http://localhost:3000/api/tasks/abc123/complete \
  -H "Authorization: Bearer $TOKEN"
```

### Poll Events

```bash
# First poll (full snapshot)
curl "http://localhost:3000/api/events?since=0&board=nocturna" \
  -H "Authorization: Bearer $TOKEN"

# Subsequent polls (delta)
curl "http://localhost:3000/api/events?since=1725000000&board=nocturna" \
  -H "Authorization: Bearer $TOKEN"
```

---

## See Also

- [Architecture](architecture.md) — System design and data flow
- [Deployment](deployment.md) — Production hosting
- [Getting Started](getting-started.md) — First-time setup
- [AGENTS.md](../AGENTS.md) — Full code map and conventions