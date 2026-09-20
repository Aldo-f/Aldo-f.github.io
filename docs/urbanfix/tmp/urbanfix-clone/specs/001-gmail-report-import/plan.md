# Implementation Plan – Gmail Report Import  

**Feature**: gmail-report-import  
**Spec**: specs/001-gmail-report-import/spec.md  
**Plan**: specs/001-gmail-report-import/plan.md  

## 📋 Technical Context  

### Knowns  
- IMAP host: `imap.gmail.com` (port 993, TLS).  
- Credentials available via `GMAIL_IMAP_USER` and `GMAIL_IMAP_PASSWORD` in `.env`.  
- Date filter: `SINCE "10-Oct-2025"` (IMAP format).  
- AWV code pattern: `[A-Z]{2}-\d{2,4}-\d{4}` (matches `KM-2025-29314`, `MB-26-09439`).  
- City‑specific code patterns: configurable; initial set includes the same AWV pattern and optional bracketed pattern `[A-Z]-\d{6}` (e.g., `[A-700739]`).  
- Existing AI defect‑analysis pipeline (`analyzeDefect`, `generateFullReport`) is functional and can be reused.  
- Current storage layer uses a `reports` table with auto‑increment `id`.  
- Frontend built with React/Vite, Tailwind, TypeScript.  

### Unknowns (NEEDS CLARIFICATION)  
- **Ghent‑specific code patterns**: Aldo indicated that Ghent uses multiple formats (e.g., `MB-26-09439`, `[A-700739]`). We will treat the city‑pattern list as fully configurable via admin UI; no further clarification needed.  
- **Raw e‑mail retention**: Aldo confirmed to keep full raw e‑mail for audit (optional column `rawEmail`).  
- **Code normalisation**: Aldo confirmed codes should be stored **exact as found** (no uppercase/trimming).  

> All open questions have been resolved; no remaining NEEDS CLARIFICATION items.

## 📜 Constitution Check  
No project constitution (`.specify/memory/constitution.md`) is present. Therefore, no governance constraints to validate.

## 📚 Phase 0: Research  
All technical unknowns have been resolved in the spec clarification step. No further research is required.  
*(If any arise during implementation, they will be logged and addressed in subsequent iterations.)*

## 🏗️ Phase 1: Design & Contracts  

### 1. Data Model (`data-model.md`)  
See `specs/001-gmail-report-import/data-model.md` (to be created).  
**Changes**  
- Add column `externalEmailId TEXT UNIQUE` to `reports`.  
- Add optional column `rawEmail TEXT` (to store full MIME source for audit).  
- Create join table `report_incident_codes`:  
  ```sql
  CREATE TABLE report_incident_codes (
      report_id   INTEGER NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
      code        TEXT    NOT NULL,
      PRIMARY KEY (report_id, code)
  );
  ```  
- Indexes:  
  - `CREATE INDEX idx_reports_external_email ON reports(externalEmailId);`  
  - `CREATE INDEX idx_report_incident_codes_code ON report_incident_codes(code);`  

### 2. Interface Contracts (`contracts/`)  
We expose the following backend contracts:  

#### GET /api/reports  
- Returns array of report objects, each containing:  
  - `id`, `description`, `location`, `severity`, `photoBase64`, `source`, `receivedAt`, `status`, `timeline`, `incidentCodes` (array of strings).  
- Query parameters:  
  - `code` (string): filter reports that contain the given code (exact match).  
  - `source` (string): filter by source (e.g., `"email"`).  
  - `since`, `before` (ISO date strings): date range on `receivedAt`.  

#### GET /api/reports/:id  
- Same structure as above for a single report.  

#### POST /api/reports/:id/codes  
- Body: `{ "code": string, "action": "add" | "remove" }`  
- Updates the `report_incident_codes` join table accordingly.  
- Returns `{ success: true }` or error.  

#### Internal: IMAP Poller (not public)  
- Invoked every `IMAP_POLL_INTERVAL_MS` (default 5 minutes).  
- Steps:  
  1. Connect to Gmail IMAP using credentials from environment.  
  2. Search: `SINCE "10-Oct-2025" UNSEEN`.  
  3. For each unseen message:  
     - Extract `Message-ID`, `Date`, `Subject`, `From`.  
     - Decode `text/plain` part (strip HTML to plain text for regex).  
     - Extract AWV and city codes using configured regexes.  
     - Fetch any image attachments (base64).  
     - Run AI defect‑analysis on attachments → `description`, `location`, `severity`, `photoBase64`.  
     - Check `reports` table for existing `externalEmailId`.  
       - If exists: update record, merge new codes into join table (insert missing, do not delete existing unless removed by user).  
       - If not exists: insert new report with `source="email"`, `receivedAt` from header, AI fields, and insert rows into `report_incident_codes` for each code.  
     - Optionally store raw MIME in `rawEmail` column if feature flag enabled.  
     - Mark message as `\Seen` (or move to processed folder).  
  4. Close IMAP connection.  

### 3. Quickstart Validation Guide (`quickstart.md`)  
See `specs/001-gmail-report-import/quickstart.md` (to be created).  
**Validation Scenarios**  
1. **Import a single test e‑mail**  
   - Prerequisites: A test mailbox with one message containing an AWV code and an image.  
   - Steps:  
     - Set `GMAIL_IMAP_USER` and `GMAIL_IMAP_PASSWORD` to test credentials.  
     - Run the IMAP poller manually (or wait for next interval).  
   - Expected:  
     - A new report appears in `/api/reports`.  
     - Report fields match AI‑extracted description, location, severity.  
     - `incidentCodes` contains the AWV code and any city code present.  
     - `externalEmailId` set to the message’s `Message-ID`.  
     - Raw e‑mail stored in `rawEmail` column (if enabled).  
2. **Deduplication on re‑run**  
   - Prerequisites: Same test mailbox as above, message still marked unseen (or reset).  
   - Steps:  
     - Run poller twice.  
   - Expected:  
     - Only one report exists in the database (no duplicate `externalEmailId`).  
     - No duplicate rows in `report_incident_codes`.  
3. **Code‑based filtering**  
   - Prerequisites: At least two reports with different codes.  
   - Steps:  
     - Call `/api/reports?code=<code-from-first-report>`.  
   - Expected:  
     - Only reports containing that code are returned.  
4. **Manual code edit persists**  
   - Prerequisites: A report imported from e‑mail.  
   - Steps:  
     - Call `POST /api/reports/:id/codes` with `{code: "NEWTEST-001", action: "add"}`.  
     - Run poller again (should not affect the added code).  
   - Expected:  
     - The code appears in the report’s `incidentCodes`.  
     - Subsequent poller runs do not remove it.  

## 📎 Generated Artifacts (to be created) 
- `specs/001-gmail-report-import/data-model.md` 
- `specs/001-gmail-report-import/contracts/api.md` (or separate files per endpoint) 
- `specs/001-gmail-report-import/quickstart.md` 

## 🛠️ Remaining Implementation Steps (outside spec‑kit) 
The following tasks are required to turn the design into a working feature but are not covered by the spec‑kit artefacts: 
- Apply the database migrations defined in `data-model.md` (`externalEmailId`, `rawEmail`, and the `report_incident_codes` join table). 
- Add the new API routes (`GET /api/reports?code=…`, `GET /api/reports/:id`, `GET /api/reports/codes`, `POST /api/reports/:id/codes`) to the Express server (`server.ts`) and connect them to the storage layer (update `storage.ts` or create a new service). 
- Implement the IMAP poller service (`src/services/imapService.ts`) that uses `GMAIL_IMAP_USER`/`GMAIL_IMAP_PASSWORD`, extracts codes, runs the existing AI pipeline, and performs deduplication/storage logic. 
- Wire the poller into the existing `IMAP_POLL_INTERVAL_MS` scheduling mechanism (or expose a manual `/api/emails/poll-now` endpoint). 
- Update the frontend: 
  - Report card component to render `incidentCodes` as badges. 
  - Add a filter dropdown for incident codes (populated via `GET /api/reports/codes`). 
  - Add an “Edit Codes” modal that calls `POST /api/reports/:id/codes` to add/remove codes. 
- Run the validation scenarios from `quickstart.md` (import a test e‑mail, verify deduplication, code‑based filtering, manual edit persistence). 
- Ensure linting and type‑checking pass (`npm run lint`, `npm run build`). 
- Update documentation (README) with any new environment variables and usage instructions. 

---
**Goal:** When all of the above steps are completed, the feature will be ready for production use, allowing Aldo to import his historic Gmail incident reports, store multiple incident codes per report, and interact with them via the API and UI.

**Next Step**: Run `/speckit-tasks` to generate the ordered implementation task list (`tasks.md`).