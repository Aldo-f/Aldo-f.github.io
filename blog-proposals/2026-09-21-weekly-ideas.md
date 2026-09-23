# Weekly Blog Post Ideas - September 21, 2026

## Proposal 1: From Docker-Traefik to K3s: How I Migrated My Home-Lab API Gateway

### Angle/hook
After months of running Traefik as a Docker container, I faced a critical choice: keep debugging image corruption and disk pressure issues, or migrate to native Kubernetes with K3s. This post details how I converted Traefik routes to IngressRoutes, created Deployment+Service patterns, and solved ACME certificate conflicts—while keeping my personal LLM API running during the transition.

### Outline
- **The Breaking Point**: Docker image corruption after `docker prune` and pod evictions due to disk pressure (98% full)
- **K3s Architecture**: Why K3s over K3d/docker-compose for a single-node home lab
- **Migration Steps**: Converting `routes.yml` to IngressRoute CRDs, creating service-definitions
- **ACME Certificate Journey**: Fixing certResolver conflicts and validating certificates via `curl -v`
- **Testing Rigor**: Three-layer verification (Python health checks, Ansible assertions, real `curl` output)
- **Lessons Learned**: What worked, what went wrong, and how to migrate safely

### Target audience
Home-lab operators on Raspberry Pi managing mixed Docker/Kubernetes workloads who need a practical migration guide from container-based reverse proxies to native Kubernetes ingress.

### Estimated effort
Medium—requires compiling test outputs, commit details, and technical diagrams. Core infrastructure work is done; mostly documentation with technical details.

### Tags
k3s, traefik, kubernetes, acme, raspberry-pi, home-lab, infrastructure-migration, docker, certbot

---

## Proposal 2: UrbanFix Goes Ansible: Enforcing Infrastructure-as-Code in the Home Lab

### Angle/hook
UrbanFix was running outside the Ansible-managed deployment system—breaking the single source of truth principle. This post shows how I created the proper Ansible template, integrated it with `__HOME__` macros, and verified the deployment with our three-layer check (Python, Ansible, template validation)—demonstrating how to standardize any standalone docker-compose repo.

### Outline
- **The Problem**: UrbanFix's port conflicts, manual Traefik config, and certResolver misconfiguration
- **The Template Pattern**: Creating `templates/infra/urbanfix/` with proper `__HOME__` placeholders
- **Integrating with containers role**: Adding to `container_services` dictionary with pinned image tags
- **Verification Pipeline**: Python health check at `/health`, Ansible assertions, docker-compose validation
- **Result**: One-command deployment: `./install.sh --tags containers --limit-services '["urbanfix","04-network-traefik"]'`
- **Migration Playbook**: Step-by-step guide for moving any docker-compose service into Ansible

### Target audience
Ansible users in home-lab environments who struggle with maintaining consistency across services deployed through different methods.

### Estimated effort
Low-Medium—the work is already complete and verified. Effort is in writing up the process with before/after comparisons and explaining the anti-patterns avoided.

### Tags
ansible, docker-compose, urbanfix, infrastructure-as-code, raspberry-pi, devops, home-lab, templating

---

## Proposal 3: Verification-First: How I Validate Home-Lab Services With Real curl Output

### Angle/hook
I never claim a service is deployed until I see actual HTTP responses. This post explains my three-layer verification approach (Python tests, Ansible assertions, real `curl` checks) that caught ACME conflicts, disk pressure evictions, and missing service definitions—before they became user-facing outages.

### Outline
- **The Three-Layer Check**: Python health endpoint checks, Ansible playbook assertions, raw `curl` verification
- **Case Study: Final Verification**: Real output showing `503` (backend down), `404` (service missing), TLS validation
- **Disk Pressure Drama**: How `/dev/sdb2` at 98% capacity evicted k3s pods, and the fix
- **ACME Conflict Resolution**: Certificate validation before and after certResolver switch
- **Test Artifacts**: Linking read `tests/verify_final_three_urls.txt` with actual command outputs
- **Automation Scripts**: Reusing test cases 1-8 for repeatable verification across services

### Target audience
DevOps practitioners who want reliable infrastructure validation workflows that catch issues before they impact users.

### Estimated effort
Low—excellent test artifacts already exist in `tests/` directory. Main work is structuring the narrative with code examples and linking to verification scripts.

### Tags
verification, devops, ansible, testing, curl, http, raspberry-pi, home-lab, acme, kubernetes

---

## Additional Notes

### Recent Activity Summary (Sept 14-21)
Key commits this week focused on k3s integration:
- `9d782bd9e`: UrbanFix port fixes, certResolver, torrent+qbittorrent unification
- `e8b521131`: Headlamp IngressRoute, service-definitions, AGENTS.md updates
- `6bd758b3f`: HOMEPAGE_ALLOWED_HOSTS with all DuckDNS domains
- `c134e4a7f`: Ingress routes for urbanfix, torrent, rag, opencode, dev subdomains
- `69ba54a55`: Final verification that 3 URLs respond correctly (503/404 → eventually fixed)

### Services in Focus
- **Freellmapi**: K3s deployment manifest created, ACME certified (aledfieuw+pi5@gmail.com)
- **UrbanFix**: Migrated from standalone to Ansible-managed
- **Headlamp**: Added as IngressRoute with proper service definitions
- **Torrent/qbittorrent**: Unified configuration pattern