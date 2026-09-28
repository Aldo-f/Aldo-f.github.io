---
title: "Agent Orchestration in Practice: How Nocturna Uses Hermes for Kanban Automation"
date: 2026-09-14
categories:
  - AI Agents
  - Home Lab
tags:
  - hermes
  - agent-workflow
  - delegation
  - nocturna
  - kanban
  - cron
  - skills
  - ai-orchestration
  - raspberry-pi
projects:
  - nocturna
---
Most AI agent demos stop at a chat window. Nocturna goes further — it's a full kanban control center that spawns Hermes subagents, runs scheduled tasks via cron, delegates work to peer agents, and manages it all through a real-time board UI. This post walks through the actual integration architecture, with code from the Nocturna repo.

<!-- more -->

## Why Orchestration Matters

Running a single LLM call is easy. Running *reliable, scheduled, multi-agent workflows* — where tasks have lifecycles, failures are surfaced, and humans can intervene — that's the hard part. Nocturna solves this by wrapping the Hermes Agent CLI and Gateway API in a structured kanban board that treats AI tasks as first-class citizens with states, priorities, and lifecycle transitions.

The core insight: **an AI agent is not a chatbot. It's a worker process.** And worker processes need queues, supervisors, and dashboards.

## The Three Integration Points

Nocturna talks to Hermes through three distinct channels, each with its own code path:

### 1. Local CLI — Spawning the `hermes` Binary

When Hermes runs on the same machine, Nocturna spawns the `hermes` CLI binary directly via `execFile`:

```typescript
// server/kanbanCli.ts
export async function runCliRaw(args: string[], options: ExecCliOptions = {}): Promise<string> {
  const bin = options.binPath || getHermesBin();
  const timeout = options.timeoutMs ?? 10000;

  return new Promise((resolve, reject) => {
    const child = execFile(bin, args, {
      timeout,
      cwd: options.cwd || process.cwd(),
      env: { ...process.env, ...options.env },
      maxBuffer: 10 * 1024 * 1024,
    }, (error, stdout, stderr) => {
      if (error) {
        if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
          return reject(new CliError(
            'engine_unreachable',
            `Hermes CLI binary not found at '${bin}'.`,
            error.message
          ));
        }
        if ((error as { killed?: boolean }).killed) {
          return reject(new CliError(
            'engine_unreachable',
            `Hermes CLI timed out after ${timeout}ms.`,
            stderr || error.message
          ));
        }
        return reject(new CliError(
          'cli_error',
          `Hermes CLI exited with code ${error.code ?? 1}`,
          stderr || stdout || error.message
        ));
      }
      resolve(stdout.toString());
    });
  });
}
```

The binary detection logic searches multiple candidate paths:

```typescript
export function getHermesBin(): string {
  if (process.env.NOCTURNA_HERMES_BIN) return process.env.NOCTURNA_HERMES_BIN;

  const candidatePaths = [
    '/usr/local/bin/hermes',
    '/usr/bin/hermes',
    path.join(process.env.HOME || '', '.local', 'bin', 'hermes'),
    path.join(process.env.HOME || '', '.hermes', 'hermes-agent', 'hermes'),
    path.join(process.cwd(), 'tests', 'fake-hermes'),
  ];

  for (const candidate of candidatePaths) {
    if (candidate && fs.existsSync(candidate)) {
      try {
        fs.accessSync(candidate, fs.constants.X_OK);
        return candidate;
      } catch {}
    }
  }
  return 'hermes';
}
```

Every CLI call goes through `runCliJson`, which parses the output as JSON and wraps parse failures in a typed `CliError`:

```typescript
export async function runCliJson<T = unknown>(args: string[], options: ExecCliOptions = {}): Promise<T> {
  const raw = await runCliRaw(args, options);
  try {
    return JSON.parse(raw.trim()) as T;
  } catch (err) {
    throw new CliError(
      'cli_error',
      'Failed to parse JSON output from Hermes CLI',
      `Raw output: ${raw.slice(0, 500)}. Error: ${(err as Error).message}`
    );
  }
}
```

### 2. Gateway Mode — HTTP API to a Remote Hermes Instance

When Hermes is running elsewhere (another Pi on the LAN, or a remote server), Nocturna switches to Gateway mode — an HTTP client with authentication, timeout handling, and fallback auth strategies:

```typescript
// server/gatewayClient.ts
export async function gatewayFetch<T = unknown>(
  endpoint: string,
  options: GatewayFetchOptions = {}
): Promise<T> {
  const config = options.config || getGatewayConfig();
  if (!config || !config.baseUrl) {
    throw new CliError('engine_unreachable', 'Hermes Gateway URL is not configured.');
  }

  const fullUrl = `${config.baseUrl}${endpoint}`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), options.timeoutMs ?? 5000);

  const headers = new Headers(options.headers || {});
  if (config.password) {
    headers.set('Authorization', `Bearer ${config.password}`);
    headers.set('X-Hermes-Password', config.password);
  }

  let res = await fetch(fullUrl, { ...options, headers, signal: controller.signal });

  // Fallback: If 401 with Bearer token, attempt Basic Auth
  if (res.status === 401 && config.password) {
    const basicAuth = Buffer.from(`admin:${config.password}`).toString('base64');
    const retryHeaders = new Headers(headers);
    retryHeaders.set('Authorization', `Basic ${basicAuth}`);
    res = await fetch(fullUrl, { ...options, headers: retryHeaders, signal: controller.signal });
  }
  // ...
}
```

The branching logic is visible in every route. Here's the task listing endpoint:

```typescript
// server/routes/tasks.ts
tasksRouter.get('/', async (req, res, next) => {
  const config = configFromInstance(req.activeInstance);
  if (isGatewayActive(req.activeInstance)) {
    const gatewayRes = await gatewayFetch<unknown>(`/api/tasks${gatewayQuery}`, { config });
    // ... transform gateway response
    return res.json({ tasks });
  }
  // CLI fallback
  const args = appendBoardArg(['kanban', 'list', '--json'], board);
  const rawTasks = await runCliJson<TaskDto[]>(args);
  // ...
});
```

### 3. SSH Remote — Running Hermes on a Distant Host

For instances accessible via SSH, Nocturna uses the `ssh2` library to execute Hermes commands remotely:

```typescript
// server/instanceRunner.ts
export async function executeSshCommand(
  instance: InstanceRecord,
  command: string,
  timeoutMs = 10000
): Promise<{ stdout: string; stderr: string; code: number }> {
  return new Promise((resolve, reject) => {
    const conn = new SshClient();
    const timer = setTimeout(() => {
      conn.end();
      reject(new Error(`SSH connection timed out after ${timeoutMs}ms`));
    }, timeoutMs);

    conn.on('ready', () => {
      conn.exec(command, (err, stream) => {
        if (err) { clearTimeout(timer); conn.end(); return reject(err); }
        let stdout = '', stderr = '';
        stream.on('close', (code: number) => {
          clearTimeout(timer); conn.end();
          resolve({ stdout, stderr, code: code ?? 0 });
        });
        stream.on('data', (data: Buffer) => { stdout += data.toString(); });
        stream.stderr.on('data', (data: Buffer) => { stderr += data.toString(); });
      });
    });
    // ...
  });
}
```

## Subagent Delegation

One of Nocturna's most powerful features is **delegation** — the ability to spawn subagent processes for specific tasks. This is a Gateway-only feature (the CLI doesn't support it), which means the route returns a clear 501 when running in CLI mode:

```typescript
// server/routes/delegate.ts
delegateRouter.post('/', async (req, res, next) => {
  if (!isGatewayActive(req.activeInstance)) {
    return res.status(501).json({
      error: {
        code: 'not_found',
        message: 'Delegation requires Gateway connection',
        detail: 'Subagent delegation is a Gateway tool, not available via CLI',
      },
    });
  }
  const config = configFromInstance(req.activeInstance);
  const result = await gatewayFetch('/api/delegate', {
    method: 'POST',
    body: JSON.stringify(req.body),
    config,
  });
  return res.json(result);
});
```

The delegation API supports three operations beyond the initial spawn:

- **Status check** — `GET /api/delegate/status/:id` polls the subagent's progress
- **Steer** — `POST /api/delegate/:id/steer` injects a mid-run course correction
- **Stop** — `POST /api/delegate/:id/stop` terminates the subagent

This mirrors the Hermes Agent's own A2A (agent-to-agent) protocol. Nocturna acts as the control plane, while the actual agent work happens in spawned processes.

## Cron: Scheduled Agent Work

Not every task needs to be triggered manually. Nocturna exposes Hermes's cron system through a full REST API. Here's how a cron job is created:

```typescript
// server/routes/cron.ts
cronRouter.post('/', async (req, res, next) => {
  if (isGatewayActive(req.activeInstance)) {
    const result = await gatewayFetch('/api/cron', {
      method: 'POST',
      body: JSON.stringify(req.body || {}),
      config,
    });
    return res.status(201).json(result);
  }
  // CLI mode: build args from request body
  const body = req.body || {};
  const args: string[] = ['cron', 'create', body.schedule, body.prompt];
  if (body.name) args.push('--name', body.name);
  if (body.skill && body.skill.length > 0) {
    for (const s of body.skill) args.push('--skill', s);
  }
  if (body.workdir) args.push('--workdir', body.workdir);
  if (body.model) args.push('--model', body.model);
  args.push('--json');
  const result = await runCliJson(args, { env: buildBoardEnv(board) });
  return res.status(201).json(result);
});
```

The `--skill` flag is particularly important — it lets you attach Hermes skills to a cron job, so the scheduled agent has the right tools loaded. For example, a nightly backup verification cron might use `--skill hermes-agent --skill disk-space-management`.

The cron API supports the full lifecycle: `list`, `create`, `pause`, `resume`, `run` (manual trigger), `remove`, and `runs` (execution history).

## Loops: Session-Scoped Recurring Tasks

Beyond cron (which persists across sessions), Nocturna also exposes **loops** — interval-based recurring tasks that exist within a Hermes Gateway session. These are Gateway-only:

```typescript
// server/routes/loops.ts
loopsRouter.post('/', async (req, res, next) => {
  const { interval, prompt } = req.body || {};
  if (!interval || !prompt) {
    return res.status(422).json({
      error: { code: 'validation', message: 'interval and prompt are required' },
    });
  }
  if (isGatewayActive(req.activeInstance)) {
    const body: Record<string, unknown> = { interval, prompt };
    if (req.body.times !== undefined) body.times = req.body.times;
    if (req.body.until !== undefined) body.until = req.body.until;
    const result = await gatewayFetch('/api/loops', {
      method: 'POST',
      body: JSON.stringify(body),
      config,
    });
    return res.status(201).json(result);
  }
  return res.status(501).json({
    error: {
      code: 'not_found',
      message: 'Loop management requires Gateway connection',
    },
  });
});
```

The difference: cron jobs survive restarts; loops don't. Loops are ideal for "check every 5 minutes while I'm watching the board" scenarios.

## The Honest State Model

Nocturna doesn't fake success. When a task fails, it stays failed on the board. Direct status moves are explicitly rejected:

```typescript
// server/routes/tasks.ts
tasksRouter.patch('/:id/status', (req, res) => {
  return res.status(409).json({
    error: {
      code: 'forbidden_move',
      message: 'Direct status moves are forbidden by Hermes state machine',
      detail: 'Use specific lifecycle action endpoints (e.g. /complete, /block, /unblock, /promote, /archive).',
    },
  });
});
```

Instead, tasks move through lifecycle actions: `complete`, `block`, `unblock`, `promote`, `archive`. Each emits a hook event:

```typescript
// server/routes/actions.ts
actionsRouter.post('/:id/complete', async (req, res, next) => {
  const id = req.params.id;
  const { summary } = req.body || {};
  const args = ['kanban', 'complete', id];
  if (summary) args.push('--summary', summary);
  await runCliJson(args);
  await emitHook('kanban_task_completed', {
    task_id: id, status: 'done', timestamp: Math.floor(Date.now() / 1000)
  });
  return res.json({ ok: true, id, status: 'done' });
});
```

The hook system allows side effects — for example, desktop notifications when a task is blocked:

```typescript
// server/hooks.ts
if (process.env.HERMES_HOOK_NOTIFY === '1') {
  registerHook('kanban_task_blocked', async (data) => {
    try {
      await execFileAsync('notify-send', [
        'Hermes Task Blocked',
        `Task ${data.task_id} was blocked at ${new Date(data.timestamp * 1000).toLocaleString()}`,
      ]);
    } catch { /* notify-send not available */ }
  });
}
```

## Board Scope: Multi-Board Isolation

Nocturna supports multiple kanban boards through the `HERMES_KANBAN_BOARD` environment variable. The board scope is resolved per-request:

```typescript
// server/boardScope.ts
export function resolveBoardSlug(slug?: string | null): string {
  if (slug && slug.trim()) {
    const cleaned = slug.trim();
    if (!SLUG_REGEX.test(cleaned)) {
      throw new CliError('validation', `Invalid board slug format: '${cleaned}'.`);
    }
    return cleaned;
  }
  return process.env.HERMES_KANBAN_BOARD || 'default';
}

export function buildBoardEnv(slug?: string): Record<string, string> {
  return slug ? { HERMES_KANBAN_BOARD: slug } : {};
}
```

This means every CLI invocation carries the board context as an env var, while Gateway requests pass it as a query parameter. The board abstraction lets you run separate boards for different projects — `nocturna` for agent tasks, `thuis` for media automation, etc.

## LAN Discovery: Finding Hermes on Your Network

One of Nocturna's standout features is automatic LAN discovery. It scans your local network for running Hermes instances:

```typescript
// server/instanceRunner.ts
export async function scanLanForHermes(
  targetIp?: string,
  targetPorts: number[] = [8080, 8000, 3000, 5000, 8088, 9090]
): Promise<DiscoveredLanInstance[]> {
  // Build IP list from network interfaces
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name] || []) {
      if (iface.family === 'IPv4' && !iface.internal) {
        const parts = iface.address.split('.');
        const subnetPrefix = `${parts[0]}.${parts[1]}.${parts[2]}`;
        const commonOffsets = [1, 2, 5, 10, 20, 50, 64, 100, 105, 150];
        for (const offset of commonOffsets) {
          ipsToProbe.push(`${subnetPrefix}.${offset}`);
        }
      }
    }
  }

  // Probe candidates in parallel with 1.2s timeout
  for (const ip of ipsToProbe) {
    for (const port of targetPorts) {
      probeTasks.push(
        (async () => {
          const res = await fetch(`http://${ip}:${port}/api/tasks?limit=1`, {
            signal: controller.signal,
            headers: { Accept: 'application/json' },
          });
          if ([200, 401, 403, 404].includes(res.status)) {
            discovered.push({ ip, port, url: `http://${ip}:${port}`, ... });
          }
        })()
      );
    }
  }
  await Promise.allSettled(probeTasks);
  return discovered;
}
```

This is how Nocturna finds a Hermes instance running on another Raspberry Pi at `192.168.0.5:8787` without any manual configuration.

## Data Flow: SQLite + Hermes kanban.db

Nocturna stores its own state (users, sessions, instances) in a local SQLite database at `data/nocturna.db`, using Node 22's built-in `node:sqlite` module — no external database server needed. The actual task data lives in Hermes's `kanban.db`.

The data flow is:

```
Browser → Nocturna API → { gatewayFetch or runCliJson } → Hermes
                ↓
        data/nocturna.db (auth, sessions, instances)
```

Nocturna never duplicates task state. Every board view is a live read from Hermes. This means the board always reflects the true state of the agent workforce — no stale caches, no sync issues.

## Error Handling: What Happens When Agents Fail

Every error in Nocturna follows a structured shape: `{ error: { code, message, detail } }`. The error codes are:

- `engine_unreachable` — Hermes is down or the binary is missing
- `cli_error` — Hermes ran but returned a non-zero exit code
- `not_found` — Resource doesn't exist
- `validation` — Bad request input
- `forbidden_move` — Attempted direct status change (409)

When the engine is unreachable, Nocturna marks the instance as offline:

```typescript
if (err instanceof CliError && err.code === 'engine_unreachable') {
  updateInstance(req.activeInstance.id, req.user.id, {
    status: 'unreachable',
    last_error: err.message,
    last_checked: Date.now(),
  });
}
```

The board UI then shows the instance as disconnected, and the user can switch to another instance or fix the connection — rather than seeing opaque errors.

## Extending the Pattern

The architecture Nocturna demonstrates is applicable beyond kanban:

1. **Wrap, don't replace** — Nocturna doesn't reimplement Hermes; it wraps the existing CLI and API with a structured UI.
2. **Dual-mode by default** — Every route supports both CLI and Gateway. This means the app works locally (zero network config) and remotely (zero local install).
3. **Honest state** — Don't hide failures. Blocked tasks stay blocked. The UI shows reality, not aspiration.
4. **Hookable lifecycle** — Every state transition emits an event. This lets you add notifications, logging, or integrations without modifying core logic.
5. **Board isolation** — Multiple boards via environment variable, not config files. One Hermes instance, many projects.

## Running It Yourself

Nocturna deploys with a single Docker command on a Raspberry Pi 5:

```bash
git clone https://github.com/Aldo-f/Nocturna.git
cd nocturna
docker compose up -d --build
```

The `docker-compose.yml` mounts `~/.hermes` read-only (so the in-container CLI works), persists the SQLite database in a named volume, and integrates with Traefik for automatic TLS.

If Hermes is already installed, Nocturna auto-detects it. If not, the Setup Wizard walks you through connecting via Gateway URL, LAN discovery, or SSH.

## Next Steps

- [ ] Board templates (scrum, kanban, custom columns)
- [ ] Webhook receiver for external triggers
- [ ] Mobile-responsive board view
- [ ] Export/import board JSON
