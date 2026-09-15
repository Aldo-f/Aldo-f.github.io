# WordPress Test Environment

Test WordPress instance at `https://wp.aldof.duckdns.org`

## Deployment

```bash
docker compose up -d --build
```

## Login Credentials

- **URL**: https://wp.aldof.duckdns.org
- **Username**: Aldo
- **Password**: Password654321!

## Email (SMTP Relay)

WordPress sends mail through the internal `mailrelay` service at `~/dev/06-apps-mailrelay`.

### How it works

- `msmtp` is installed in the WordPress image and symlinked to `/usr/sbin/sendmail`
- `/etc/msmtprc` points to the relay (`host mailrelay`, port `25`)
- WordPress's PHP `sendmail_path` is configured to use the wrapper
- The relay forwards to Gmail SMTP (auth + TLS)

### Testing

```bash
# From inside WordPress container
docker exec 06-apps-wordpress-wordpress-1 bash -c \
  "echo -e 'To: aldo.fieuw@gmail.com\nSubject: Test\n\nBody' | /usr/sbin/sendmail -t"

# Check relay logs
docker logs mailrelay | tail -20
```

## Verification

```bash
# Run pytest suite
uv run pytest -v tests/test_wordpress.py

# Or verify manually
curl -I https://wp.aldof.duckdns.org --insecure
```

## Architecture

- **WordPress**: 6.4-php8.2-apache (with WP-CLI + msmtp)
- **Database**: MariaDB 10.11
- **DNS**: DuckDNS (linuxserver/duckdns)
- **Mail Relay**: `crazymax/msmtpd` at `~/dev/06-apps-mailrelay`
- **Proxy**: Traefik (configured in `01-core-infra`)

## Notes

- Traefik route and backend added in `01-core-infra/ansible/roles/containers/defaults/main.yml`
- Container network bridged: `mailrelay` ↔ `06-apps-wordpress_default` ↔ `traefik_net`
