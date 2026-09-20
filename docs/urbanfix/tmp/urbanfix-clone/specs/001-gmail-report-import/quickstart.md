# Quickstart Validation Guide – Gmail Report Import  

**Feature**: gmail-report-import  
**Spec**: specs/001-gmail-report-import/spec.md  
**Plan**: specs/001-gmail-report-import/plan.md  

This guide describes how to manually validate that the import feature works end‑to‑end, without requiring a full test suite.

---

## Prerequisites  

1. **Environment variables** set in `.env`:  
   ```bash
   GMAIL_IMAP_USER="aldo.fieuw@gmail.com"
   GMAIL_IMAP_PASSWORD="***"
   IMAP_POLL_INTERVAL_MS=300000
   ```
2. **Database migrations** applied:  
   - `externalEmailId TEXT UNIQUE` added to `reports` table.  
   - `rawEmail TEXT` column added to `reports` table.  
   - `report_incident_codes` join table created with indexes.  
3. **Node dependencies** installed (`npm install`).  
4. **Backend server** running (`npm start`).  
5. **Frontend dev server** running (`npm run dev`).  
6. **Test e‑mail fixture** prepared: a single message in Aldo’s Gmail containing:  
   - An AWV code in the subject (e.g., `KM-2025-29314`).  
   - An optional city code in the body (e.g., `[A-700739]`).  
   - An image attachment (any photo).  

---

## Validation Scenarios  

### Scenario 1: Import a Single Test E‑Mail  

**Steps**  

1. Ensure the test e‑mail is **unseen** (or reset the `\Seen` flag).  
2. Trigger the IMAP poller:  
   ```bash
   curl -X POST http://localhost:3000/api/emails/poll-now
   ```  
   *Or wait for the next `IMAP_POLL_INTERVAL_MS` interval.*  
3. Verify the new report appears:  
   ```bash
   curl -s http://localhost:3000/api/reports | jq '.[] | select(.source=="email")'
   ```  

**Expected Outcome**  

- A new report exists with `source = "email"`.  
- `incidentCodes` contains the AWV code **and** any city code found.  
- `externalEmailId` matches the e‑mail’s `Message‑ID`.  
- `receivedAt` equals the e‑mail’s `Date` header.  
- `description`, `location`, `severity`, and `photoBase64` are populated from the AI analysis of the image attachment.  
- `rawEmail` contains the full MIME source (if feature enabled).  

---

### Scenario 2: Deduplication on Re‑Run  

**Steps**  

1. Repeat Scenario 1 (same test e‑mail still unseen).  
2. Run the poller again.  

**Expected Outcome**  

- Only **one** report exists in the database (no duplicate `externalEmailId`).  
- No duplicate rows in `report_incident_codes`.  
- The report’s fields are updated with any new data, but existing codes are preserved.  

---

### Scenario 3: Code‑Based Filtering  

**Steps**  

1. Ensure at least two reports exist with different codes.  
2. Call:  
   ```bash
   curl -s "http://localhost:3000/api/reports?code=KM-2025-29314"
   ```  

**Expected Outcome**  

- Only reports containing `KM-2025-29314` are returned.  

---

### Scenario 4: Manual Code Edit Persists  

**Steps**  

1. Identify a report ID (e.g., `123`) imported from an e‑mail.  
2. Add a new code via the API:  
   ```bash
   curl -X POST http://localhost:3000/api/reports/123/codes \
     -H "Content-Type: application/json" \
     -d '{"code":"GENT-2025-001","action":"add"}'
   ```  
3. Run the poller again (should not affect the added code).  
4. Retrieve the report:  
   ```bash
   curl -s http://localhost:3000/api/reports/123
   ```  

**Expected Outcome**  

- `incidentCodes` now includes `GENT-2025-001`.  
- Subsequent poller runs do **not** remove this code.  

---

## End‑to‑End UI Check  

1. Open the reports list page in a browser.  
2. Verify each report card displays its codes as badges.  
3. Use the code filter dropdown; selecting a code should filter the list accordingly.  
4. Click “Edit Codes” on a report; confirm you can add/remove codes and that the changes persist.  

---

## Cleanup  

After validation:  

1. Mark the test e‑mail as **Seen** (or move to a processed folder) so it won’t be re‑imported.  
2. Remove the test report from the database if needed.  

---

## Notes  

- All API endpoints follow the standard `{ success: boolean, data?: any, error?: string }` format.  
- The IMAP poller uses `imap.gmail.com:993` with TLS.  
- If `rawEmail` storage is enabled, ensure the database column is large enough (e.g., `TEXT` type supports large blobs).  

---  

*This guide focuses on manual, end‑to‑end validation; unit tests and integration tests belong in the test suite (`test/`).*