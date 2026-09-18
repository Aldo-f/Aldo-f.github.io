# Nocturna Troubleshooting Guide

Quick reference for common issues.

---

## Quick Diagnostics

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| "Engine unreachable" | Hermes binary not found / gateway down | Check `hermes version`, verify gateway URL/password |
| 401 Unauthorized | Session expired / token invalid | Log out, clear localStorage, log in again |
| 409 forbidden_move | Tried to drag card to wrong column | Use action buttons (Complete, Block, etc.) |
| 502 cli_error | Hermes CLI returned non-JSON | Check Hermes logs, `hermes version` works? |
| 503 engine_unreachable | Gateway not reachable | Check network, Traefik, tunnel, firewall |
| Blank board | No tasks or wrong board slug | Check board slug in Instance Manager |
| LAN discovery empty | Hermes gateway not running on LAN | Start `hermes gateway run` on target machine |

---

## Docker Issues

### Container exits immediately
```bash
docker logs nocturna --tail 50
# Common: hermes binary not found, DB permission, port in use
```

### "database is locked"
```bash
docker compose down
docker run --rm -v nocturna_data:/data alpine \
  rm -f /data/nocturna.db-wal /data/nocturna.db-shm
docker compose up -d
```

### Hermes CLI not working in container
```bash
docker exec nocturna hermes version
# Should print version. If not:
docker exec nocturna ls -la /home/nocturna/.hermes/hermes-agent/hermes
```

### Port 3000 already in use
```bash
lsof -i :3000
# Kill existing process or change PORT env var
```

---

## Gateway Connection Issues

### "Connection refused" / timeout
1. Verify gateway is running: `curl -sk https://your-gateway/api/health`
2. Check Traefik dashboard: router `nocturna` exists and healthy
3. Verify DNS resolves to correct IP
4. Check firewall allows port 443 (Traefik) and 8787 (Hermes gateway)

### Authentication failures
```bash
# Test from Nocturna container
docker exec nocturna curl -sk -H "X-Hermes-Password: your-password" \
  https://your-gateway/api/health
```

### TLS / certificate issues
```bash
# Test with curl -v
curl -v https://nocturna.yourdomain.com/api/health
# Check: cert valid? chain complete? hostname matches?
```

---

## Local CLI Issues

### "hermes: command not found"
```bash
# Inside container
docker exec nocturna which hermes
# Or check bind mount
docker exec nocturna ls -la /home/nocturna/.hermes/hermes-agent/hermes
```

### "ModuleNotFoundError" when running hermes
```bash
# PYTHONPATH must point to engine source
docker exec nocturna env | grep PYTHONPATH
# Should be /home/nocturna/.hermes/hermes-agent
```

### Permission denied on ~/.hermes
```bash
# Host side: ensure docker user can read
ls -la ~/.hermes
# Fix if needed:
chmod -R a+rX ~/.hermes
```

---

## LAN Discovery Issues

### No instances found
- Hermes gateway must be running on target: `hermes gateway run`
- Both devices on same subnet
- UDP broadcast allowed (port 8787)
- Nocturna container network mode must allow broadcast (use `host` or `bridge` with correct config)

### Found instance but can't connect
- Target machine firewall blocks 8787
- Wrong URL (use `http://<lan-ip>:8787`, not `localhost`)
- Hermes gateway bind address: `hermes config set web.host 0.0.0.0`

---

## Authentication Issues

### "Session expired" but just logged in
- Clear `localStorage` for the domain in DevTools
- Check cookie/session storage not blocked by browser
- Verify server time is correct (NTP sync)

### Can't register first user
- Database file permissions: `data/nocturna.db` must be writable by container user
- Check SQLite schema: `docker exec nocturna sqlite3 /app/data/nocturna.db .schema`

### Forgot admin password
```bash
# Reset via SQLite
docker exec -it nocturna sqlite3 /app/data/nocturna.db
sqlite> DELETE FROM sessions WHERE user_id = (SELECT id FROM users WHERE username = 'admin');
sqlite> UPDATE users SET password_hash = '...' WHERE username = 'admin';
# Or just delete and re-register (if no other users)
sqlite> DELETE FROM users WHERE username = 'admin';
```

---

## Frontend Issues

### White screen / React error boundary
```bash
# Check browser console
# Common: Vite HMR socket connection failed in prod
# Fix: DISABLE_HMR=true in production
```

### "Unexpected token" on build
```bash
npm run build
# Check: Node version 22+ required
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Styles not applying (Tailwind v4)
```bash
# Ensure CSS import is in main.tsx, not in components
# Check: src/index.css has @import "tailwindcss";
```

---

## SSH Remote Issues

### "Permission denied (publickey)"
- SSH key must be in container at `/home/nocturna/.ssh/id_ed25519` (or configured path)
- Key must be added to remote `~/.ssh/authorized_keys`
- Container needs `.ssh` directory with correct permissions (700)

### "Host key verification failed"
```bash
# Pre-add host key to known_hosts
docker exec nocturna ssh-keyscan -H remote-host >> /home/nocturna/.ssh/known_hosts
```

### Connection timeout
- Check firewall allows outbound port 22
- Verify SSH server running on remote
- Test from host: `ssh user@remote-host hermes version`

---

## Performance Issues

### Board loads slowly
- Check `api/health` response time
- Large task counts: consider archiving old tasks
- Polling interval: 3s default (configurable in `useBoard.ts`)

### High memory usage
```bash
docker stats nocturna
# Node.js default heap: ~1.4GB. Limit if needed:
# docker run --memory=512m ...
```

---

## Log Locations

| Component | Location |
|-----------|----------|
| Nocturna server | `docker logs nocturna` |
| Hermes (local CLI) | `docker exec nocturna hermes version` + task output in task drawer |
| Hermes (gateway) | `journalctl -u hermes-gateway -f` (systemd) or container logs |
| Traefik | `docker logs traefik` |
| SQLite DB | `data/nocturna.db` (volume) |

---

## Reset Everything (Nuclear Option)

```bash
# Stop and remove everything
docker compose down -v
rm -rf data/

# Recreate
docker compose up -d --build

# Re-register admin user via UI
```

---

## Getting Help

1. Check [GitHub Issues](https://github.com/Aldo-f/Nocturna/issues)
2. Run diagnostics:
   ```bash
   curl -sk https://your-domain/api/health
   curl -sk https://your-domain/api/gateway/status
   ```
3. Include in issue:
   - `docker logs nocturna --tail 100`
   - `docker exec nocturna hermes version`
   - Browser console errors
   - Steps to reproduce