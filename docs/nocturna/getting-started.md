# Getting Started with Nocturna

This guide walks you through installing Nocturna, connecting it to your Hermes instance, and creating your first board.

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Node.js | 22+ | `node --version` |
| npm | 10+ | `npm --version` |
| Hermes Agent | Latest | [Install guide](https://hermes-agent.nousresearch.com/docs) |
| Python | 3.11+ | For Hermes CLI (if using Local CLI mode) |

---

## Installation

### Option 1: Local Development (Recommended for First Time)

```bash
# Clone the repo
git clone https://github.com/Aldo-f/Nocturna.git
cd Nocturna

# Install dependencies
npm install

# Start development server
npm run dev
# → Opens http://localhost:3000
```

### Option 2: Docker (Production)

```bash
docker compose up -d --build
# → Runs on port 3000
```

---

## First Launch: Setup Wizard

On first visit to `http://localhost:3000`, you'll see the **Setup Wizard**:

### Step 1: Choose Your Backend

| Backend | When to Use |
|---------|-------------|
| **Local CLI** | Hermes and Nocturna on the same machine. Nocturna spawns the `hermes` binary directly. |
| **LAN Discovery** | Hermes runs on another device on your local network. Nocturna scans and finds it. |
| **Hermes Gateway** | Hermes runs on a remote server, behind NAT, or in the cloud. Connect via HTTPS. |

### Step 2: Configure the Backend

#### Local CLI
- Nocturna auto-detects `hermes` at `~/.hermes/hermes-agent/hermes`
- If found, click **Auto-link** to create the instance
- If not found, enter the path manually (e.g., `/usr/local/bin/hermes`)

#### LAN Discovery
- Click **Scan LAN** — Nocturna broadcasts UDP and lists responding Hermes instances
- Click **Add** next to the one you want
- Enter a friendly name, optionally set as default

#### Hermes Gateway
- Enter the gateway URL (e.g., `https://gateway.example.com`)
- Enter password or API key (from `hermes config set web.basic_auth.password`)
- Click **Test Connection**, then **Save**

### Step 3: Create Admin Account

- Enter username and password
- This creates the first user (admin)
- Session token stored in browser `localStorage` (30-day expiry)

### Step 4: You're In!

You'll land on the **Board** — an empty kanban ready for tasks.

---

## Creating Your First Task

1. Press `N` or click **+ New Task**
2. Fill in:
   - **Title** — short, actionable
   - **Body** — markdown supported (acceptance criteria, context, links)
   - **Assignee** — optional (for multi-user setups)
   - **Priority** — 1–5 (higher = more important)
   - **Goal Mode** — toggle for autonomous execution with acceptance criteria
3. Click **Create**

The card appears in the **Triage** column.

---

## Lifecycle Actions

Don't drag cards between columns — use the action buttons on each card:

| Action | Transition | When to Use |
|--------|------------|-------------|
| **Complete** | `todo` → `done` | Task finished, acceptance criteria met |
| **Block** | `todo`/`doing` → `blocked` | External dependency, waiting on something |
| **Unblock** | `blocked` → `todo` | Dependency resolved |
| **Request Review** | `doing` → `review` | Want human eyes before done |
| **Request Changes** | `review` → `changes_requested` | Reviewer found issues |
| **Promote** | `todo` → `doing` / `doing` → `ready` | Move forward in workflow |
| **Archive** | any → `archived` | Remove from board (permanent) |

> **Direct status changes are forbidden** — the engine owns the state machine. Nocturna enforces this via the API (409 `forbidden_move`).

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `N` | New task |
| `F` | Focus search |
| `?` | Show shortcuts cheat sheet |
| `Esc` | Close drawer / dialog |
| `←` `→` | Navigate columns in drawer |

---

## Multi-Instance Setup

After initial setup, add more instances via the **Instance Manager** (gear icon in navbar):

- **Multiple Local CLI** — different `hermes` binaries or boards
- **Multiple Gateway** — different environments (dev/staging/prod)
- **SSH Remote** — connect to a remote host over SSH
- **Switch instantly** — no restart needed, just select from dropdown

---

## Troubleshooting

### "Engine unreachable" on Local CLI
- Ensure `hermes` is on PATH or set `NOCTURNA_HERMES_BIN`
- Run `hermes version` to verify it works
- Check `~/.hermes/config.yaml` exists

### LAN Discovery finds nothing
- Ensure both devices on same subnet
- Hermes gateway must be running on target: `hermes gateway run`
- Check firewall allows UDP broadcast (port 8787)

### Gateway connection fails
- Verify URL is HTTPS (required for remote)
- Check password/API key matches `hermes config`
- Ensure gateway is accessible from Nocturna's network

### "Session expired" / logged out unexpectedly
- Clear browser `localStorage` for the domain
- Re-login — tokens expire after 30 days of inactivity

---

## Next Steps

- Read [Architecture](architecture.md) to understand how it works
- See [Deployment](deployment.md) for production hosting
- Check [API Reference](api.md) for integration