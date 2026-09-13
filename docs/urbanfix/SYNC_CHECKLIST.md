# Synchronization Checklist

When making changes that affect the public specifications or the overall project state, follow this checklist to keep everything in sync.

- [ ] **Regenerate OpenAPI spec** – Run the generation script (e.g., `npm run generate-openapi` or the appropriate command) and verify the updated JSON at `/api-docs.json`.
- [ ] **Update AGENTS.md** – Reflect any new endpoints, services, or architectural changes in `AGENTS.md`.
- [ ] **Run lint and type‑check** – Execute `npm run lint` (which runs `tsc --noEmit`) and ensure no errors remain.
- [ ] **Bump version** – Increment the version number in `package.json` (and any related lockfiles) following semantic versioning.
- [ ] **Commit changes** – Stage all modified files and create a concise commit message summarising the sync actions.
- [ ] **Update documentation** – Refresh relevant docs in `docs/` (e.g., API docs, usage guides) to match the new spec.
- [ ] **Verify Swagger UI** – Open the Swagger UI (`/docs`) and confirm the displayed API matches the regenerated spec.

> This checklist ensures that after each change the public contract, developer tooling, and release artifacts stay consistent.
