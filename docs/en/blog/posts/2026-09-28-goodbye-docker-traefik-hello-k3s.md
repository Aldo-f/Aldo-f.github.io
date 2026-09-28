---
title: "Goodbye Docker Traefik, Hello k3s: Migrating 24 DuckDNS Routes to cert-manager TLS"
date: 2026-09-28
categories:
  - Home Lab
  - Infrastructure
tags:
  - k3s
  - traefik
  - cert-manager
  - tls
  - lets-encrypt
  - duckdns
  - home-lab
  - migration
  - raspberry-pi
projects:
  - home-lab
---

When your home lab outgrows Docker Compose, the reverse proxy becomes the
first casualty. I ran Traefik as a Docker container with its own ACME
resolver — issuing per-domain TLS certificates via DuckDNS DNS challenges.
It worked for a year. Then k3s entered the picture, and everything broke.

This post documents the real, messy, iterative migration of 24 DuckDNS
domains from Docker Traefik to k3s IngressRoutes backed by a single
cert-manager Certificate with HTTP-01 challenges. Including the disk
pressure evictions, corrupted Traefik images, and ACME email
misconfigurations that happened along the way.

<!-- more -->

## Why Migrate: When Two Traefiks Fight Over Port 443

The Docker Traefik setup was simple: one container, a `traefik.yml` with
a `duckdns` certificatesResolver using DNS challenges, and a `routes.yml`
file with per-router `certResolver: duckdns` entries:

```yaml
# 04-network-traefik/traefik.yml (Docker Traefik — the old setup)
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
          permanent: true
  websecure:
    address: ":443"

providers:
  file:
    filename: /etc/traefik/routes.yml

certificatesResolvers:
  duckdns:
    acme:
      email: "aldof@duckdns.org"
      storage: /letsencrypt/acme.json
      dnsChallenge:
        provider: duckdns
        delayBeforeCheck: 30
```

Each router in `routes.yml` specified `tls: certResolver: duckdns`,
meaning Traefik requested a separate Let's Encrypt certificate per
domain. With 24 domains, that's 24 separate ACME orders, 24 TLS secrets,
and 24 chances for rate-limit failures.

When k3s installed its own Traefik via Helm (the default `traefik` chart),
both Traefik instances tried to bind port 443. The Docker container won
the race more often, but k3s Traefik kept trying to obtain its own
certificates via its own ACME resolver — configured with a different
email (`aldo+fieuw+pi5@gmail.com` vs `aldof@duckdns.org`). Let's Encrypt
saw conflicting ACME accounts trying to validate the same domains, and
started returning `403 urn:ietf:params:acme:error:unauthorized`:

```
2026-09-14T12:17:25Z ERR Unable to obtain ACME certificate for domains
  error="unable to generate a certificate for the domains [aldo-f.duckdns.org]:
  resolver: one or more domains had a problem: [aldo-f.duckdns.org:
  invalid authorization: *** error: 403 :: urn:ietf:params:acme:error:unauthorized]"
```

The ACME challenge files were being served by Docker Traefik, but k3s
Traefik was the one requesting validation. They were stepping on each
other.

## The Architecture: One Certificate, 24 SANs

The solution: **one cert-manager `Certificate` resource with all 24
DuckDNS domains as SANs, backed by a single `aldof-domains-tls` Kubernetes
secret.** cert-manager handles ACME ordering and renewal. Traefik just
references the secret — no ACME resolver of its own.

### cert-manager (Helm, jetstack)

```bash
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true
```

### ClusterIssuer with HTTP-01 challenge

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    email: aldo+fieuw+pi5@gmail.com
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    server: https://acme-v02.api.letsencrypt.org/directory
    solvers:
    - http01:
        ingress:
          class: traefik
```

cert-manager creates a temporary IngressRoute for the HTTP-01 challenge,
Traefik serves it, Let's Encrypt validates, and cert-manager stores the
certificate in the named secret. No DNS challenge provider needed.

### The Certificate resource — 24 SANs in one shot

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: aldof-domains
  namespace: default
spec:
  dnsNames:
  - digipunt.aldof.duckdns.org
  - docs.digipunt.aldof.duckdns.org
  - freellm.aldof.duckdns.org
  - cloud.aldof.duckdns.org
  - vault.aldof.duckdns.org
  - jellyfin.aldof.duckdns.org
  - wp.aldof.duckdns.org
  - stantonius.aldof.duckdns.org
  - aldof.duckdns.org
  - qbittorrent.aldof.duckdns.org
  - torrent.aldof.duckdns.org
  - rag.aldof.duckdns.org
  - gateway.hermes.aldof.duckdns.org
  - clock.dev.aldof.duckdns.org
  - web.hermes.dev.aldof.duckdns.org
  - tq.hermes.dev.aldof.duckdns.org
  - opencode.dev.aldof.duckdns.org
  - portainer.dev.aldof.duckdns.org
  - cockpit.dev.aldof.duckdns.org
  - metrics.hermes.dev.aldof.duckdns.org
  - stantonius.usful.duckdns.org
  - usful.duckdns.org
  - aldo-f.duckdns.org
  - lotte1.duckdns.org
  issuerRef:
    kind: ClusterIssuer
    name: letsencrypt-prod
  secretName: aldof-domains-tls
```

That's 24 domains in one certificate. One ACME order, one renewal cycle
(90 days), one secret to reference everywhere.

### IngressRoutes reference the shared secret

Every IngressRoute now points to the same secret:

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: jellyfin
  namespace: default
spec:
  entryPoints:
  - websecure
  routes:
  - match: Host(`jellyfin.aldof.duckdns.org`)
    kind: Rule
    services:
    - name: jellyfin
      port: 8096
  tls:
    secretName: aldof-domains-tls
```

Compare this to the old Docker Traefik `routes.yml` where each router
had `tls: certResolver: duckdns` — Traefik was the certificate authority
manager. Now it's just a router.

### k3s Traefik Helm values — stripped of ACME

The k3s Traefik Helm chart no longer needs any `certificatesResolvers`
configuration:

```yaml
# 08-infra-k3s/helm-values/traefik-values.yaml
service:
  type: LoadBalancer
  loadBalancerIP: 192.168.0.5

providers:
  kubernetesCRD:
    allowCrossNamespace: true
  kubernetesIngress:
    publishedService:
      enabled: true

deployment:
  tolerations:
    - key: node.kubernetes.io/disk-pressure
      operator: Exists
      effect: NoSchedule
```

Note the `tolerations` for `disk-pressure` — that's a hard-won lesson
from the migration. More on that below.

## Step-by-Step: Converting Docker Routes to IngressRoutes

### 1. Stop Docker Traefik's ACME resolver

```bash
helm uninstall traefik -n kube-system  # remove k3s Traefik first
docker restart traefik                  # Docker Traefik still runs
# But now only Docker Traefik handles ACME — temporarily
```

### 2. Convert each Docker route to an IngressRoute

The old `routes.yml` had entries like:

```yaml
# Docker Traefik — old format
http:
  routers:
    freellm:
      rule: "Host(`freellm.aldof.duckdns.org`)"
      entryPoints:
        - websecure
      service: freellmapi
      tls:
        certResolver: myresolver
```

The k3s equivalent:

```yaml
# k3s IngressRoute — new format
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: freellm
  namespace: default
spec:
  entryPoints:
  - websecure
  routes:
  - match: Host(`freellm.aldof.duckdns.org`)
    kind: Rule
    services:
    - name: freellmapi
      port: 3001
  tls:
    secretName: aldof-domains-tls
```

Key differences:
- `rule: "Host(...)` → `match: Host(...)`
- `service: freellmapi` → `services: [{name: freellmapi, port: 3001}]`
- `certResolver: myresolver` → `secretName: aldof-domains-tls`
- Each IngressRoute is a separate YAML document (not a nested router)

### 3. Create Service+Endpoints for external services

Services running in Docker (not k3s pods) need Kubernetes
`Service` + `Endpoints` objects so k3s Traefik can route to them:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: jellyfin
  namespace: default
spec:
  ports:
  - port: 8096
    targetPort: 8096
---
apiVersion: v1
kind: Endpoints
metadata:
  name: jellyfin
  namespace: default
subsets:
- addresses:
  - ip: 192.168.0.5
  ports:
  - port: 8096
```

### 4. Apply and verify

```bash
kubectl apply -f 08-infra-k3s/manifests/ingress-configurations/
kubectl get ingressroute -A
kubectl get certificate
```

## When Things Break: Three Real Failure Modes

### Failure 1: Disk Pressure Evicts k3s Pods

The Pi 5's storage hit 98% capacity (`/dev/sdb2: 220G/235G`). Kubernetes
applied a `disk-pressure=NoSchedule` taint, and k3s started evicting
pods — including the Traefik pod:

```
NAME                       READY   STATUS    RESTARTS   AGE
toolbox-7768c4db6f-22gzp   0/1     Evicted   0          2m34s
```

The fix was two-fold:
1. Clean up disk space (remove old Docker images, clear build caches)
2. Add a toleration to the Traefik deployment so it schedules even under
   disk pressure:

```yaml
deployment:
  tolerations:
    - key: node.kubernetes.io/disk-pressure
      operator: Exists
      effect: NoSchedule
```

This is a pragmatic choice — running Traefik under disk pressure is
risky, but losing your reverse proxy means losing access to everything,
including the tools you need to fix the disk.

### Failure 2: Docker Traefik Image Corruption

After running `docker prune` to free disk space, the Docker Traefik
image became corrupted. Pulling it again failed because the image layers
were partially present but damaged:

```
Error: failed to register layer: operation not permitted
```

The Docker Traefik was unrecoverable. This turned out to be a blessing —
it forced the complete cutover to k3s Traefik. But for a few hours, there
was no working reverse proxy at all.

### Failure 3: ACME Email Misconfiguration

The Docker Traefik used `aldof@duckdns.org` for ACME. The k3s Traefik
Helm chart was configured with `aldo+fieuw+pi5@gmail.com`. Let's Encrypt
treats different emails as different ACME accounts. When both tried to
validate the same domain, the challenges conflicted:

```
2026-09-14T16:35:08Z ERR Cannot retrieve the ACME challenge
  for freellm.aldof.duckdns.org (token "test") providerName=acme
```

The fix: standardize on one email (`aldo+fieuw+pi5@gmail.com`) across
all ACME configurations, and remove the Docker Traefik's ACME resolver
entirely once cert-manager took over.

## Verification: Real curl Output

The final verification file (`tests/verify_final_three_urls.txt`)
captures the actual curl output after migration:

```
=== EINDVERIFICATIE — 3 URL's (reële curl-output) ===

1. https://freellm.aldof.duckdns.org/
   curl -k -s -o /dev/null -w "%{http_code}\n" → 503
   (Traefik routing works, backend freellmapi-down)

2. https://aldof.duckdns.org/
   curl -k -s -o /dev/null -w "%{http_code}\n" → 404
   (Traefik routing works, homepage-service missing in k3s)

3. https://stantonius.usful.duckdns.org/
   curl -k -s -o /dev/null -w "%{http_code}\n" → 404
   (Traefik routing works, stantonius-service missing in k3s)
```

503 and 404 are the correct answers here — they prove Traefik is routing
correctly, and the backends just aren't deployed yet. The TLS
certificate is valid:

```
* SSL connection using TLSv1.3 / TLS_AES_128_GCM_SHA256
* Server certificate:
*  SSL certificate verify ok.
```

Today, the certificate is live and healthy:

```bash
$ kubectl get certificate aldof-domains
NAME              READY   SECRET              AGE
aldof-domains     True    aldof-domains-tls   39h

$ echo | openssl s_client -connect jellyfin.aldof.duckdns.org:443 \
    -servername jellyfin.aldof.duckdns.org 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
subject=CN=digipunt.aldof.duckdns.org
issuer=C=US, O=Let's Encrypt, CN=YR1
notBefore=Sep 27 07:07:52 2026 GMT
notAfter=Dec 26 07:07:51 2026 GMT
```

## The Sablier Pattern: On-Demand Services

Not every service needs to run 24/7. Some developer tools (OpenCode,
the blog ideas generator, ad-hoc dashboards) only need to be available
when someone is actually using them. The sablier proxy pattern handles
this: Traefik routes to sablier, which starts the container on first
request and proxies the traffic once it's ready. After an idle timeout,
sablier stops the container.

This keeps the cert-manager certificate valid (the IngressRoute always
exists) while saving resources on services that are rarely accessed.

## What's Left

A handful of Docker Traefik routes still exist in `04-network-traefik/routes.yml`
for services not yet migrated to k3s. These will be converted as their
services move to k3s deployments. The old `certificatesResolvers` config
in `traefik.yml` has been stripped — Docker Traefik is now purely a
file-provider router with no ACME capabilities.

Future plans:
- **DNS-01 challenges** instead of HTTP-01, to support wildcard
  certificates (`*.aldof.duckdns.org`) and reduce the SAN list
- **Automated renewal alerts** via cert-manager's `CertificateRequest`
  status conditions
- **Migrate remaining Docker services** to k3s deployments with proper
  `Service` + `Endpoints` definitions

## Lessons Learned

1. **Don't run two ACME resolvers for the same domains.** Pick one
   certificate management system and stick with it. cert-manager is
   purpose-built for this; Traefik's built-in ACME is a convenience
   feature that doesn't scale.

2. **One certificate with many SANs beats many certificates.** One ACME
   order, one renewal, one secret. cert-manager handles the ordering;
   you just reference the secret.

3. **Disk pressure is a real Kubernetes failure mode.** On a single-node
   Pi 5, disk pressure evicts pods and taints the node. Monitor disk
   usage before it hits 85%, and add tolerations for critical
   infrastructure pods.

4. **Verify with real curl output, not assumptions.** The 503/404
   responses in the verification file proved routing worked. A
   successful TLS handshake proved the certificate was valid. These
   are the checks that matter — not `kubectl get pod` showing `Running`.

5. **Migration is iterative.** The commit history shows 8 commits over
   3 days (Sep 14-17), with multiple test cases, failures, and retries.
   That's normal. Don't expect a clean one-shot migration.
