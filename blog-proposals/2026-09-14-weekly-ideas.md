# Weekly Blog Post Ideas - September 14, 2026

## Proposal 1: From Repo to Runtime: Bringing UrbanFix Into the Ansible-Managed Fold

### Angle/hook
Most services in Aldo's home-lab deploy through Ansible templates, but UrbanFix was bypassing this pattern—running docker-compose directly from its repo. This created inconsistency and risked configuration drift. Fixing it reinforces the "single source of truth" principle that keeps the lab stable.

### Outline
- **The Problem**: Why UrbanFix lived outside the Ansible system (and why that mattered)
- **The Fix**: Creating the Ansible template, adding to container_services, and using `__HOME__` macros
- **Verification**: Three-layer check—Python health checks, Ansible assertions, and template validation
- **Result**: UrbanFix now deploys via `./install.sh --tags containers --limit-services '["urbanfix","04-network-traefik"]'` with Traefik routing and healthchecks
- **Anti-patterns Avoided**: No runtime edits, no hardcoded paths, no `:latest` tags
- **Lessons for Other Services**: How to migrate any standalone docker-compose repo into the Ansible fold

### Target audience
Home-lab operators using Ansible for service deployment, particularly those managing mixed deployment patterns who want to consolidate under a single source of truth.

### Estimated effort
Medium—mostly documentation and process description; the technical work is already complete and verified.

### Tags
home-lab, ansible, docker-compose, traefik, urbanfix, infrastructure-as-code, raspberry-pi

---

## Proposal 2: Agent Orchestration in Practice: How Nocturna Uses Hermes for Kanban Automation

### Angle/hook
Nocturna isn't just a standalone kanban—it's deeply integrated with Hermes Agent, spawning subagents for board synchronization, using skills for delegation, and leveraging cron jobs for background work. This shows how AI agents move beyond chat to become workflow orchestrator.

### Outline
- **The Integration Points**: Where Nocturna calls Hermes (CLI, API, skill invocations)
- **Subagent Delegation**: How Nocturna spawns Hermes agent instances for specific tasks (with examples from recent sessions)
- **Skill Usage**: Which Hermes skills Nocturna relies on (hermes-agent, delegation, etc.)
- **Cron & Automation**: The scheduled tasks that keep Nocturna-Hermes sync running
- **Data Flow**: How tasks move between Hermes kanban.db and Nocturna's SQLite database
- **Error Handling**: What happens when subagents fail or time out
- **Extending the Pattern**: How to apply this agent-orchestration model to your own tools

### Target audience
Developers building AI-powered applications who want to move beyond simple LLM calls to structured agent workflows with delegation, skills, and background processing.

### Estimated effort
High—requires explaining the integration architecture with concrete examples from code and session logs.

### Tags
hermes, agent-workflow, delegation, nocturna, kanban, cron, skills, ai-orchestration, raspberry-pi

---

## Proposal 3: Thuis V5 Development Diary: From DRM Detection to Watchlist Automation

### Angle/hook
Thuis evolved from a simple VRT MAX downloader to a sophisticated media automation system with DRM detection, intelligent watchlist handling, and V4/V5 parallel development—showing how self-hosted media tools can balance cutting-edge features with rock-solid reliability.

### Outline
- **Where We Started**: Thuis V4's core architecture (URL parsing, metadata fetching, transcoding)
- **The DRM Challenge**: How Widevine detection was reverse-engineered using public test streams
- **Watchlist Intelligence**: Scheduling logic, season expansion, and duplicate prevention
- **V4/V5 Parallel Development**: Why two versions coexist and how features migrate between them
- **Cron Integration**: The `--watchlist` flag and `thuis-watchlist` cron job that runs hourly
- **Testing Rigor**: 418 passing tests (with 9 pre-existing failures) as the safety net for refactoring
- **Future Direction**: Planned V5 features and how community feedback shapes the roadmap

### Target audience
Media enthusiasts and developers building self-hosted PVR tools who want to understand DRM handling, watchlist automation, and sustainable open-source development.

### Estimated effort
Medium—leverages detailed session logs and verified test results from recent thuis work.

### Tags
thuis, vrt-max, media-automation, drm, watchlist, raspberry-pi, home-lab, belgium, podcast-downloader