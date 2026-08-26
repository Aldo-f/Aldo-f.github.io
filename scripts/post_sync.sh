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

# 1. Invalidate RAG content hash so the next query rebuilds the index
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
code="000"
for i in $(seq 1 10); do
  code=$(curl -fsS -o /dev/null -w '%{http_code}' https://aldo-f.github.io/ 2>/dev/null || echo 000)
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
