<!--
SYNC IMPACT REPORT
Version change: (none) → 1.0.0
Modified principles: n/a (initial ratification)
Added sections: Core Principles (I–V), Security & Secrets, Development Workflow, Governance
Removed sections: none
Follow-up TODOs: implement real browser automation for meldpuntBot, add WebSocket fallback
-->

# UrbanFix Constitution

## Core Principles

### I. Automation Over Manual Work (KISS)

The system MUST minimize human intervention from photo upload to dossier tracking.
Every step that can be automated (reCAPTCHA, form filling, email matching,
reminder sending) MUST be automated. Manual steps are defects until proven
unavoidable.

### II. Single Source of Truth (DRY)

Every fact about a report lives in exactly one place: the `ReportItem` in
`server/services/storage.ts`. The frontend reads from `/api/reports`, the backend
writes there. No duplicate stores, no stale caches. SSE broadcast keeps all
clients in sync with the canonical state.

### III. AI Generates, Human Validates

AI (Gemini) proposes report text, defect hypotheses, and email replies — but the
user MUST review and approve before anything is sent to AWV. No auto-submit
without explicit confirmation. The AI is an assistant, not an autonomous agent.

### IV. Spec-Driven Development

Features are specified under `specs/<NNN>-<name>/` before code changes. The spec
states goal, constraints, acceptance criteria, and out-of-scope items. No spec =
no implementation. This prevents feature creep and keeps the scope focused on the
actual goal: automating road defect reporting to AWV.

### V. Pinned, Minimal Dependencies

Every npm package and Docker image MUST be pinned by version. `:latest` is
forbidden. The attack surface MUST stay small — this app handles sensitive personal
data (email, GPS location, photos) and must be auditable.

## Security & Secrets

- API keys (Gemini, Buster) MUST live in `.env` or Docker secrets — never in code.
- `.env`, `.env.*`, `data/`, and `*.local.jsonc` MUST be in `.gitignore`.
- Photo dataUrls can be large; enforce the 2.5 MB limit client-side before upload.
- The SSE endpoint does NOT authenticate — it runs behind Traefik with IP allowlist
  middleware (LAN-only by design).

## Development Workflow

1. **Specify first**: create `specs/<NNN>-<feature-name>/spec.md` before writing code.
2. **Constitute**: update `.specify/memory/constitution.md` if a new principle emerges.
3. **Implement**: follow the spec; mark acceptance criteria as met.
4. **Verify**: run `npm run build && docker compose up -d --build` and test on real
   runtime (the Docker container on this host).
5. **Document**: update README.md and AGENTS.md if behavior changed.

## Governance

This constitution supersedes ad-hoc practice. Amendments require a written rationale
in the commit message, a semver bump of this document (MAJOR = principle removed,
MINOR = new principle/section, PATCH = wording), and a Sync Impact Report prepended
as an HTML comment. Compliance is checked during review of every PR.
