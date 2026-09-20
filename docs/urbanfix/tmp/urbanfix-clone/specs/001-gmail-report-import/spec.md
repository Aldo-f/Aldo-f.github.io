# Email‑to‑Report Import with Multiple Incident Codes  

**Short name**: gmail-report-import  
**Feature ID**: 001  
**Status**: Draft  

## 🎯 Goal  
As Aldo, I want the system to automatically import my historic incident‑report e‑mails from my Gmail account (`aldo.fieuw@gmail.com`) dating from 10 Oct 2025 onward, so that each e‑mail becomes a defect report linked to its **AWV code** and any additional **city‑specific codes** (e.g., Ghent, MoBiliteit). A single report must be able to carry **multiple** incident codes, enabling traceability to all relevant identifiers.  

## 👥 Actors  
- **System** – performs the automated IMAP pull, code extraction, report creation, deduplication, and storage.  
- **Aldo (user)** – views imported reports, verifies or adds codes, filters/searches by code.  

## 📖 User Scenarios  

| Scenario | Description |
|----------|-------------|
| **SC1 – Periodic Import** | The system connects to Aldo’s Gmail via IMAP, selects only unseen messages with `SINCE "10-Oct-2025"`, and processes each message exactly once. |
| **SC2 – Code Extraction** | For each message, the system scans the subject, body (plain/text‑stripped HTML), and relevant headers for:<br>• AWV code pattern (e.g., `KM-2025-29314`, `MB-26-09439`)<br>• Any additional city‑code patterns (configurable list). All distinct matches are collected as the report’s `incidentCodes`. |
| **SC3 – Report Creation** | Using the existing AI defect‑analysis pipeline, the system extracts description, location, severity, and any attached images from the e‑mail. A new `ReportItem` is created with:<br>• AI‑generated fields<br>• `source = "email"`<br>• `receivedAt` = e‑mail Date header<br>• `incidentCodes` = array of extracted codes (AWV + others). |
| **SC4 – Deduplication** | Before creating a report, the system checks whether a report already exists for the same e‑mail `Message‑ID` (stored as `externalEmailId`). If found, the report is **updated** (e.g., add newly discovered codes) rather than duplicated. |
| **SC5 – Storage of Multiple Codes** | The system persists the many‑to‑many relationship between reports and incident codes in a dedicated join table (`report_incident_codes`). Each code appears as a separate row linked to the report ID. |
| **SC6 – UI Presentation** | In the reports list and detail view, all codes associated with a report are displayed as badges or a comma‑separated list. |
| **SC7 – Code‑Based Filtering** | Aldo can filter the reports list by one or more codes (e.g., show all reports containing code `KM-2025-29314`). The backend returns reports whose join table contains the requested code(s). |
| **SC8 – Manual Code Adjustment** | Aldo may add or remove codes for a given report via an “Edit Codes” action, which updates the join table accordingly. |

## ✅ Functional Requirements  

1. **Mail Ingestion**  
   - The system shall provide a configurable IMAP client (host, port, TLS, credentials) using the environment variables `GMAIL_IMAP_USER` and `GMAIL_IMAP_PASSWORD`.  
   - It shall fetch only messages with date ≥ 10‑Oct‑2025 and that are not yet marked as processed (e.g., `\Seen` flag or a custom folder).  

2. **Code Detection**  
   - The system shall apply a set of regular‑expression patterns (AWV + city‑specific) to subject, body, and relevant headers.  
   - AWV pattern: `[A-Z]{2}-\d{2,4}-\d{4}` (matches examples `KM-2025-29314` and `MB-26-09439`).  
   - City‑specific patterns are configurable; initially we will use a generic pattern that captures common formats observed: `[A-Z]{2}-\d{2,4}-\d{4}` (same as AWV) and optionally `[A-Z]-\d{6}` possibly surrounded by square brackets (e.g., `[A-700739]`).  
   - All unique matches shall be collected as the report’s `incidentCodes`.  

3. **Report Creation**  
   - For each processed e‑mail, the system shall invoke the existing AI image‑analysis pipeline on any image attachments to populate description, location, severity, and photo (base64).  
   - The created report shall store: `source = "email"`, `receivedAt` (from e‑mail Date), and the array of `incidentCodes`.  

4. **Deduplication**  
   - The system shall store the e‑mail’s `Message‑ID` (or a hash thereof) in a new column `externalEmailId` on the `reports` table (UNIQUE).  
   - On ingest, if a report with the same `externalEmailId` exists, the system shall update that record (merge new codes) instead of inserting a duplicate.  

5. **Data Model – Multiple Codes**  
   - A new table `report_incident_codes` shall be created:  
     ```sql
     CREATE TABLE report_incident_codes (
         report_id   INTEGER NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
         code        TEXT    NOT NULL,
         PRIMARY KEY (report_id, code)
     );
     ```  
   - The `reports` table shall **not** store a delimited list; all code look‑ups shall use the join table.  

6. **API Adjustments**  
   - `GET /api/reports` and `GET /api/reports/:id` shall include the `incidentCodes` array (derived from the join table).  
   - Optional endpoint `POST /api/reports/:id/codes` shall allow adding/removing codes (body: `{code: string, action: "add"|"remove"}`).  

7. **UI Adjustments**  
   - Report cards shall render each code as a badge (or a comma‑separated list if space‑constrained).  
   - A filter control shall let Aldo select one or more codes; the filtered list updates accordingly.  

8. **Processing Idempotency**  
   - Re‑running the import job shall not create duplicate reports; it shall only update codes or leave existing reports unchanged.  

## 🎯 Success Criteria  

- **Import Completeness** – ≥ 95 % of Aldo’s e‑mails from 10‑Oct‑2025 to present are imported as reports with correct `incidentCodes`.  
- **No Duplicates** – Zero reports share the same `externalEmailId` after any number of import runs.  
- **Code Accuracy** – For a random sample of 50 imported reports, the set of codes stored matches the set manually extracted from the source e‑mail (≥ 98 % accuracy).  
- **UI Reflects Codes** – In the reports list, every report displays *all* its associated codes; filtering by any single code returns exactly the reports that contain that code.  
- **Manual Edit Persists** – After Aldo adds or removes a code via the UI, the change survives subsequent import runs (i.e., the join table is not overwritten by the automated process).  

## 📝 Assumptions  

- Gmail IMAP credentials are available via `GMAIL_IMAP_USER` and `GMAIL_IMAP_PASSWORD` in `.env`.  
- E‑mail bodies are UTF‑8 encoded; attachments are image/* MIME types compatible with the existing AI pipeline.  
- The current AI defect‑analysis pipeline (`analyzeDefect`, `generateFullReport`) is functional and can be reused without modification.  
- The existing `reports` table has an auto‑increment `id` primary key and supports adding new columns (`externalEmailId` and optional `rawEmail`).  
- The application runs in a Node/Express environment (as per current stack) but the spec avoids referencing specific frameworks, libraries, or APIs.  

## 🔓 Open Questions / Needs Clarification  

*All open questions have been resolved during the clarification step.*  

---  

### ✅ Next Steps (Spec‑Kit Flow)  

1. **Run `/speckit-clarify`** (optional) to confirm no remaining open questions.  
2. **Run `/speckit-plan`** to derive technical design (data‑model changes, API updates, UI components, background worker).  
3. **Run `/speckit-tasks`** to generate an ordered `tasks.md` ready for implementation.  

---  

*This spec is deliberately implementation‑agnostic; it describes **what** the system must do and **why**, leaving the **how** to the planning phase.*