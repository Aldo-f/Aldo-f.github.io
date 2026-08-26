# Doc Freshness Gaps — Minimal-Method Fix Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Make the documentation chain fully automatic and current (app repo edit → watcher syncs → RAG invalidates → site deploys), using ONE method only — extend the existing `documentation_watcher/watcher.py` + a single post-sync script. No new daemons, no new frameworks, no webhooks.

**Architecture:** The watcher daemon is already running as `okf-watcher.service` and scans every `~/dev/06-apps-*` repo on a 5-minute loop. We fix it in place: complete its repo→destination mapping, make it also mirror into the OKF bundle, and after any change run one existing script (`scripts/post_sync.sh`, new but plain bash calling tools that already exist) that invalidates the RAG hash marker, commits+pushes the site repo (which triggers the existing GitHub Pages deploy), and runs the existing test suite. Separately: **remove the raw OKF bundle from the public website** — agents fetch knowledge locally via `rag_query.py`; humans only need a short usage page.

**Tech Stack:** Python 3.13 (existing watcher), bash, git, mkdocs (already installed in site venv), systemd user service (already running).

---

## User's two design decisions (confirmed good)

1. **One method:** everything hangs off the existing watcher loop. No GitHub webhooks, no extra cron jobs, no new services. Fewer moving parts = fewer breakage points.
2. **Split agent-visible vs public-visible:** YES, this is correct.
   - The OKF bundle is *machine* knowledge (YAML front-matter, receipts, hashes) — noise for human readers, and it exposes internal paths/hostnames publicly today.
   - Agents don't need it published; they call `rag_query.py` locally against `~/dev/okf-home-lab/`.
   - The public site keeps only a human "How to use" page describing the home-lab docs structure. This also removes sensitive detail (IPs, health-check endpoints, credentials layout) from the public internet.

---

## Current context / assumptions

- Watcher: `~/dev/okf-home-lab/documentation_watcher/watcher.py`, systemd unit `~/.config/systemd/user/okf-watcher.service` (active).
- Site repo: `~/dev/06-apps-aldo-f-github-io` (deploys to Pages on push to main).
- Bundle: `~/dev/okf-home-lab` with `.mem0_index_hash` staleness marker consumed by `rag/rag_query.py`.
- Test suite: `~/dev/okf-home-lab/okf_test_suite.py` (all green as of last run).
- Site venv python: `~/dev/06-apps-aldo-f-github-io/venv/bin/python`.
- Current public exposure to REMOVE: `mkdocs.en.yml` nav section "OKF Home Lab" (lines ~108–115) and the copied tree at `docs/en/okf-home-lab/`.
- Unmapped repos found by audit: letspeppol, neo-brutalist-home, nextcloud, passive-income(-sync), thuis-v4/v5 (thuis-v4/v5 DO have mapping branches but fall into the generic else — verify each).

## Proposed approach (single method)

Extend `watcher.py`:

1. Replace the hardcoded if/elif destination map with ONE data-driven dict `REPO_DEST_MAP` (repo name → list of destinations). Destinations can be both the site `docs/<name>/` mirror AND/OR the OKF bundle path.
2. After any successful integration cycle where files changed: write a small state flag, then invoke `scripts/post_sync.sh` (subprocess, blocking, logged).
3. `post_sync.sh` does exactly four things, in order:
   a. remove stale RAG hash marker (`rm -f ~/dev/okf-home-lab/.mem0_index_hash`)
   b. commit+push the site repo (if anything staged)
   c. wait for deploy, curl the live URL until 200 (max 10 tries × 15 s)
   d. run `okf_test_suite.py` and log result
4. Remove OKF bundle from the public site: delete nav entries + copied tree; add a single human page `docs/en/home-lab-docs.md` ("Home-lab documentation — how to use") explaining what exists and pointing to the project sections. Dutch mirror `docs/nl/home-lab-docs.md`.

No other mechanisms introduced. Everything reuses git, bash, existing venv, existing test suite.

---

## Step-by-step plan

### Task 1: Data-driven repo→destination map in watcher

**Objective:** Every `06-apps-*` repo resolves to explicit destination(s); no silent generic fallback.

**Files:**
- Modify: `~/dev/okf-home-lab/documentation_watcher/watcher.py:205-235` (the integrate_changes if/elif block)

**Step 1: Write failing test**

Create `~/dev/okf-home-lab/tests/test_watcher_map.py`:

```python
"""Every known app repo must have an explicit destination mapping."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "documentation_watcher"))
import watcher  # noqa: E402


def test_all_dev_app_repos_are_mapped():
    dev = Path.home() / "dev"
    repos = {p.name for p in dev.iterdir()
             if p.is_dir() and p.name.startswith("06-apps-")
             and "-legacy" not in p.name}
    mapped = set(watcher.REPO_DEST_MAP)
    missing = repos - mapped
    assert not missing, f"Repos without destination mapping: {sorted(missing)}"


def test_every_destination_is_absolute():
    for repo, dests in watcher.REPO_DEST_MAP.items():
        assert dests, f"{repo} maps to empty destination list"
        for d in dests:
            assert Path(d).is_absolute(), f"{repo} -> {d} not absolute"
```

**Step 2: Run test to verify failure**

Run: `source ~/dev/okf-home-lab/.venv/bin/activate && pytest ~/dev/okf-home-lab/tests/test_watcher_map.py -v`
Expected: FAIL — `AttributeError: module 'watcher' has no attribute 'REPO_DEST_MAP'`

**Step 3: Implement**

In `watcher.py`, above `integrate_changes()`:

```python
# Explicit repo -> destination directories. One source of truth;
# the generic else-branch is gone on purpose: unknown repos must fail
# the mapping test above instead of silently landing somewhere odd.
DOCS_SITE_DOCS = str(DOCS_SITE / "docs")
OKF_BUNDLE = str(Path(__file__).resolve().parent.parent)

REPO_DEST_MAP = {
    "06-apps-clock":              [f"{DOCS_SITE_DOCS}/clock"],
    "06-apps-radio-community":    [f"{DOCS_SITE_DOCS}/radio-community"],
    "06-apps-wordpress-stantonius": [f"{DOCS_SITE_DOCS}/wordpress-stantonius"],
    "06-apps-passive-income":     [f"{DOCS_SITE_DOCS}/passive-income",
                                   f"{OKF_BUNDLE}/docs/passive-income"],
    "06-apps-passive-income-sync": [f"{DOCS_SITE_DOCS}/passive-income-sync"],
    "06-apps-thuis-v4":           [f"{DOCS_SITE_DOCS}/thuis-v4"],
    "06-apps-thuis-v5":           [f"{DOCS_SITE_DOCS}/thuis-v5"],
    # Aldo's own app: docs published on the site AND kept in the bundle
    "06-apps-neo-brutalist-home": [f"{DOCS_SITE_DOCS}/neo-brutalist-home",
                                   f"{OKF_BUNDLE}/docs/neo-brutalist-home"],
    # NOT Aldo's own application: knowledge for agents only, never published
    "06-apps-letspeppol":         [f"{OKF_BUNDLE}/docs/letspeppol"],
}
```

Rewrite `integrate_changes()` to look up `REPO_DEST_MAP[repo_name]` and copy into **each** destination; skip repos absent from the map with a logged warning (test above guards that this never happens silently).

**Step 4: Run test to verify pass**

Run: `pytest ~/dev/okf-home-lab/tests/test_watcher_map.py -v`
Expected: 2 passed

**Step 5: Commit**

```bash
cd ~/dev/okf-home-lab && git add documentation_watcher/watcher.py tests/test_watcher_map.py
git commit -m "feat(watcher): data-driven repo->destination map, all apps covered"
```

---

### Task 2: Mirror changed app docs into the OKF bundle too

**Objective:** RAG knowledge base receives the same updates the site gets.

**Files:**
- Modify: `~/dev/okf-home-lab/documentation_watcher/watcher.py` (destinations from Task 1 already include bundle paths where wanted)

**Step 1: Write failing test**

Append to `tests/test_watcher_map.py`:

```python
def test_bundle_receives_passive_income_docs(tmp_path):
    """Integration: a doc change lands in BOTH site mirror and bundle."""
    # Uses REPO_DEST_MAP directly; full end-to-end covered by post_sync gate.
    dests = watcher.REPO_DEST_MAP["06-apps-passive-income"]
    bundle_dest = [d for d in dests if "okf-home-lab" in d]
    assert bundle_dest, "passive-income must mirror into OKF bundle"
```

**Step 2: Run** — expected PASS after Task 1 (this is a guard, keep it).

**Step 3: Manual verification**

Touch a file in `~/dev/06-apps-passive-income/docs/` (add trailing newline), restart watcher, wait one cycle:

Run: `systemctl --user restart okf-watcher && sleep 310 && ls -la ~/dev/okf-home-lab/docs/passive-income/ | head -5`
Expected: mirrored files present with fresh mtimes.

**Step 4: Commit**

```bash
cd ~/dev/okf-home-lab && git add tests/test_watcher_map.py documentation_watcher/watcher.py
git commit -m "feat(watcher): mirror app docs into OKF bundle"
```

---

### Task 3: post_sync.sh — invalidate → push → verify → test

**Objective:** After any synced change, the whole chain fires automatically.

**Files:**
- Create: `~/dev/okf-home-lab/scripts/post_sync.sh`

**Step 1: Write the script (complete)**

```bash
#!/usr/bin/env bash
# Runs after the watcher integrates doc changes.
# Chain: invalidate RAG cache -> push site (triggers Pages deploy) ->
#        verify live -> run test suite. Single method, no new services.
set -euo pipefail

SITE_REPO="$HOME/dev/06-apps-aldo-f-github-io"
BUNDLE="$HOME/dev/okf-home-lab"
LOG="$BUNDLE/logs/post_sync.log"
mkdir -p "$(dirname "$LOG")"

log() { echo "$(date -Is) $*" >> "$LOG"; }

log "--- post_sync start ---"

# 1. Invalidate RAG content hash so next query rebuilds the index
rm -f "$BUNDLE/.mem0_index_hash"
log "RAG hash marker invalidated"

# 2. Commit & push site repo (Pages deploy triggers on main push)
cd "$SITE_REPO"
git add docs/
if ! git diff --cached --quiet; then
  git commit -m "docs: auto-sync from watcher $(date +%Y-%m-%dT%H:%M)"
  git push origin main
  log "site repo pushed"
else
  log "nothing to push"
fi

# 3. Verify live site responds (deploy takes ~60-90 s)
for i in $(seq 1 10); do
  code=$(curl -fsS -o /dev/null -w '%{http_code}' https://aldo-f.github.io/ || echo 000)
  [ "$code" = "200" ] && break
  sleep 15
done
log "live check final HTTP code: $code"

# 4. Run test suite (non-fatal: log only, so watcher loop never dies)
if "$BUNDLE/.venv/bin/python" "$BUNDLE/okf_test_suite.py" >> "$LOG" 2>&1; then
  log "test suite PASSED"
else
  log "WARNING: test suite FAILED - inspect $LOG"
fi

log "--- post_sync done ---"
```

**Step 2: Make executable and dry-run**

Run: `chmod +x ~/dev/okf-home-lab/scripts/post_sync.sh && bash ~/dev/okf-home-lab/scripts/post_sync.sh && tail -8 ~/dev/okf-home-lab/logs/post_sync.log`
Expected: log lines ending with `--- post_sync done ---`, HTTP code 200.

**Step 3: Commit**

```bash
cd ~/dev/okf-home-lab && git add scripts/post_sync.sh
git commit -m "feat(sync): post_sync chain - invalidate RAG, push, verify live, test"
```

---

### Task 4: Hook post_sync into the watcher

**Objective:** Watcher invokes the chain only when files actually changed.

**Files:**
- Modify: `~/dev/okf-home-lab/documentation_watcher/watcher.py` (`run_once()`, near line 250)

**Step 1: Implementation**

At the end of `run_once()`:

```python
if changes and self.integrate_changes(changes):
    post_sync = Path(__file__).resolve().parent.parent / "scripts" / "post_sync.sh"
    if post_sync.exists():
        subprocess.run(["bash", str(post_sync)], timeout=900)
    else:
        print("post_sync.sh missing - skipping publish chain")
```

(`subprocess` is already imported in watcher.py.)

**Step 2: Verify**

Restart watcher, touch a doc in a mapped repo, wait one cycle + post_sync duration (~3 min):

Run: `systemctl --user restart okf-watcher && sleep 600 && tail -10 ~/dev/okf-home-lab/logs/post_sync.log && systemctl --user is-active okf-watcher`
Expected: fresh log entries; service still `active`.

**Step 3: Commit**

```bash
cd ~/dev/okf-home-lab && git add documentation_watcher/watcher.py
git commit -m "feat(watcher): trigger post_sync publish chain after integration"
```

---

### Task 5: Remove OKF internals from the public site (agent/public split)

**Objective:** Public site shows only human "how to use" docs; agents fetch OKF/RAG locally.

**Files:**
- Modify: `~/dev/06-apps-aldo-f-github-io/mkdocs.en.yml` (delete nav lines ~108–115 "OKF Home Lab" block)
- Delete: `~/dev/06-apps-aldo-f-github-io/docs/en/okf-home-lab/` (entire copied tree)
- Create: `~/dev/06-apps-aldo-f-github-io/docs/en/home-lab-docs.md`
- Create: `~/dev/06-apps-aldo-f-github-io/docs/nl/home-lab-docs.md` (Dutch mirror)
- Add nav entry in both `mkdocs.en.yml` and `mkdocs.nl.yml`

**Step 1: Create EN page**

```markdown
# Home-lab Documentation

This hub documents Aldo's home-lab: infrastructure, media services and
self-hosted applications.

## What you'll find here

| Section | Content |
|---------|---------|
| Thuis (v3/v4/v5/main) | VRT MAX video downloader — install, usage, troubleshooting |
| Clocky | React clock studio — features and development |
| Blanky | Project docs, main and v1 |
| Radio Community | Democratic internet radio — architecture, API, streaming |
| Passive Income (PINO) | Orchestrator for passive-income providers |

Documentation for each project lives in its own section (see the navigation)
and is pulled straight from that project's repository, so it always matches
the code.

## For AI agents

Agent-readable structured knowledge (OKF format) and a local
retrieval pipeline are maintained separately and queried locally — they are
intentionally not published on this site.
```

**Step 2: Create NL mirror** (`docs/nl/home-lab-docs.md`) — same table, Dutch prose.

**Step 3: Update nav**

In `mkdocs.en.yml`: replace the whole `OKF Home Lab:` block with:

```yaml
      - Home-lab Docs: home-lab-docs.md
```

In `mkdocs.nl.yml`, add under nav:

```yaml
  - Home-lab Docs: home-lab-docs.md
```

**Step 4: Delete the exposed tree**

```bash
rm -rf ~/dev/06-apps-aldo-f-github-io/docs/en/okf-home-lab
```

**Step 5: Build & verify locally before pushing**

Run: `cd ~/dev/06-apps-aldo-f-github-io && ./venv/bin/python -m mkdocs build --strict -f mkdocs.en.yml -d site && ./venv/bin/python -m mkdocs build --strict -f mkdocs.nl.yml -d site/nl`
Expected: both builds succeed, zero warnings about missing okf-home-lab pages.

Also confirm nothing references the removed path:
Run: `grep -rn "okf-home-lab" ~/dev/06-apps-aldo-f-github-io/docs/en/*.md ~/dev/06-apps-aldo-f-github-io/mkdocs.*.yml`
Expected: no matches.

**Step 6: Commit & push**

```bash
cd ~/dev/06-apps-aldo-f-github-io
git add -A
git commit -m "fix(security): unpublish OKF internals; add human how-to-use page (EN/NL)"
git push origin main
```

Then verify live: `curl -fsS https://aldo-f.github.io/home-lab-docs/` → contains "Home-lab Documentation"; `curl -o /dev/null -w '%{http_code}' https://aldo-f.github.io/okf-home-lab/rag/rag_query/` → 404 once Pages redeploy finishes.

---

### Task 6: End-to-end freshness proof

**Objective:** Demonstrate the full automatic chain works, no manual steps.

**Steps:**
1. Pick a mapped repo, e.g. edit `~/dev/06-apps-radio-community/docs/getting-started.md` (append a harmless comment line).
2. Wait ≤ 6 min (watcher cycle + post_sync).
3. Verify all three surfaces updated:
   ```bash
   grep -c "freshness-proof" ~/dev/06-apps-aldo-f-github-io/docs/radio-community/getting-started.md   # ≥1
   tail -5 ~/dev/okf-home-lab/logs/post_sync.log                                                      # pushed + passed
   curl -fsS https://aldo-f.github.io/radio-community/getting-started/ | grep -c "freshness-proof"     # ≥1
   ```
4. Revert the probe line, let the watcher sync the revert back.
5. Final: rerun `~/dev/okf-home-lab/okf_test_suite.py` → expect EXIT=0.

---

## Files likely to change (summary)

| File | Action |
|---|---|
| `~/dev/okf-home-lab/documentation_watcher/watcher.py` | modify (map, bundle mirroring, post_sync hook) |
| `~/dev/okf-home-lab/scripts/post_sync.sh` | create |
| `~/dev/okf-home-lab/tests/test_watcher_map.py` | create |
| `~/dev/06-apps-aldo-f-github-io/mkdocs.en.yml` / `mkdocs.nl.yml` | modify (nav swap) |
| `~/dev/06-apps-aldo-f-github-io/docs/en/okf-home-lab/` | delete |
| `~/dev/06-apps-aldo-f-github-io/docs/{en,nl}/home-lab-docs.md` | create |

## Tests / validation

- Unit: `tests/test_watcher_map.py` (mapping completeness, absolute paths, bundle mirror guard).
- Integration: Task 4 manual cycle; Task 6 end-to-end proof.
- Regression: existing `okf_test_suite.py` must stay green (runs inside post_sync too).

## Risks, tradeoffs, open questions

- **Auto-push risk:** post_sync pushes whatever the watcher synced. Mitigation: watcher only copies from your own app repos; worst case a bad doc goes public — revert via one commit. Acceptable for a personal docs site.
- **Deploy race:** concurrent pushes could race with post_sync's push. Low likelihood (single writer); `git pull --rebase` retry could be added later — YAGNI now.
- **post_sync blocks the watcher loop** up to ~15 min during deploy waits. Fine: docs sync frequency is low; loop simply pauses.
- **Test-suite failure must not kill the watcher** — handled (log-only warning).
- **Open question (RESOLVED):** `neo-brutalist-home` publishes to the site mirror AND the bundle (Aldo's own app). `letspeppol` is bundle-only — it's not Aldo's application, so its docs are agent knowledge, never published. `06-apps-nextcloud` is runtime host state (not project code), intentionally unmapped from doc publishing.
- **Open question (RESOLVED):** NL translations of newly mirrored app docs stay English-only for now (autotranslate covers site pages, not mirrors); revisit if it bothers readers.
