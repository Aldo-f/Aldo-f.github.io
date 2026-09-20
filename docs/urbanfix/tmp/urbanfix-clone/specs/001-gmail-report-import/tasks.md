# Tasks: gmail-report-import  

**Feature**: gmail-report-import  
**Spec**: specs/001-gmail-report-import/spec.md  
**Plan**: specs/001-gmail-report-import/plan.md  
**Data Model**: specs/001-gmail-report-import/data-model.md  
**Contracts**: specs/001-gmail-report-import/contracts/api.md  

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story.

- [x] T001 [P] Add `externalEmailId` and `rawEmail` columns to reports table (migration)
- [x] T002 [P] Create `report_incident_codes` join table (migration)
- [x] T003 [P] Add indexes on `externalEmailId` and `code`
- [x] T004 [US1] Update TypeScript `ReportItem` interface to include `incidentCodes: string[]`

---

## Phase 2: User Story 1 – Email Import & Deduplicate (P1) 🎯 MVP

**Goal**: Automatically import Aldo's Gmail incident reports from 10-Oct-2025 onward, extract AWV/city codes, create/update reports, and store multiple codes per report.

**Independent Test**: Run import manually; verify new report appears with correct `incidentCodes`.

- [x] T005 [P] [US1] Implement IMAP client wrapper (`src/services/imapService.ts`) using `GMAIL_IMAP_USER` / `GMAIL_IMAP_PASSWORD`
- [x] T006 [P] [US1] Implement code extraction (`extractCodesFromEmail`) with regex patterns: `[A-Z]{2}-\d{2,4}-\d{4}` and configurable city patterns (e.g., `[A-Z]-\d{6}`)
- [x] T007 [US1] Implement AI analysis integration for e-mail attachments (`processEmailAttachments`)
- [x] T008 [US1] Implement import/deduplicate logic (`importEmailToReport`): check `externalEmailId`, insert/update report, manage `report_incident_codes` join table
- [x] T009 [US1] Wire IMAP poller to existing `IMAP_POLL_INTERVAL_MS` interval
- [ ] T010 [P] [US1] Unit test for code extraction (fixture .eml files)
- [ ] T011 [P] [US1] Unit test for deduplication logic

---

## Phase 3: User Story 2 – API Exposure (P2)

**Goal**: Expose reports with `incidentCodes`, filter by code, and allow manual code add/remove.

**Independent Test**: Call `/api/reports` and `/api/reports/:id` and verify `incidentCodes` array.

- [x] T012 [P] [US2] Extend `GET /api/reports` to include `incidentCodes` (join table query)
- [x] T013 [P] [US2] Extend `GET /api/reports/:id` to include `incidentCodes`
- [x] T014 [US2] Implement `GET /api/reports/codes` endpoint
- [x] T015 [US2] Implement `POST /api/reports/:id/codes` endpoint (add/remove)
- [x] T016 [US2] Add `code` query parameter filter to `GET /api/reports`
- [ ] T017 [P] [US2] API contract tests (SuperTest) for new endpoints

---

## Phase 4: User Story 3 – UI Presentation & Filtering (P3)

**Goal**: Show codes in report cards, allow filtering by code, and allow manual edit.

**Independent Test**: Import test e-mail, view report cards, filter by code, edit codes.

- [x] T018 [P] [US3] Update report card component (`src/components/ReportsList.tsx`) to render codes as badges
- [x] T019 [P] [US3] Add code filter dropdown (`src/components/ReportsList.tsx`) using `/api/reports/codes`
- [ ] T020 [US3] Implement "Edit Codes" modal (`src/components/EditCodesModal.tsx`) using `POST /api/reports/:id/codes`
- [ ] T021 [P] [US3] Update `GET /api/reports` consumer in frontend to handle `incidentCodes`
- [ ] T022 [P] [US3] End-to-end test (Playwright): import → verify codes → filter → edit persists

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple stories.

- [ ] T023 [P] Add logging (winston) for IMAP connection, errors, and messages processed
- [ ] T024 [P] Ensure `rawEmail` column is populated when audit feature enabled
- [ ] T025 [P] Update README/docs with import feature description and env vars
- [ ] T026 [P] Performance optimization: index usage verification for `report_incident_codes`
- [ ] T027 [P] Security hardening: sanitize code input (prevent SQL injection via parameterized queries)
- [ ] T028 [P] Run quickstart validation (`specs/001-gmail-report-import/quickstart.md`)

---

## Dependencies & Execution Order  

- **Phase 1** (Foundational): No dependencies. Must complete before any user story.  
- **Phase 2** (US1): Depends on Phase 1.  
- **Phase 3** (US2): Depends on Phase 2 (needs reports to exist with codes).  
- **Phase 4** (US3): Depends on Phase 2 and Phase 3 (needs API and data model).  
- **Phase 5** (Polish): Depends on all previous phases.  

Within each user story:  
- Tests (if included) before implementation.  
- Models/data changes before services/endpoints.  
- Services before UI.  

---

## Parallel Opportunities  

- T001, T002, T003, T004 can run in parallel (Phase 1).  
- T005, T006, T007 can run in parallel (Phase 2, once Phase 1 done).  
- T012, T013, T014 can run in parallel (Phase 3).  
- T018, T019, T020 can run in parallel (Phase 4, once Phase 2/3 done).  

---

## Implementation Strategy  

### MVP First (Phase 2 only)  
1. Complete Phase 1 (Foundational).  
2. Complete Phase 2 (US1): Import and deduplicate work.  
3. **STOP and VALIDATE**: Import test e‑mail manually; verify DB state and UI.  

### Incremental Delivery  
- Phase 1 → Foundation  
- Phase 2 → US1 (import/deduplicate)  
- Phase 3 → US2 (API exposure)  
- Phase 4 → US3 (UI)  
- Phase 5 → Polish  

---

*Codes stored exactly as found (no normalisation). Raw e‑mail retained for audit. Multiple codes per report via `report_incident_codes` join table.*
