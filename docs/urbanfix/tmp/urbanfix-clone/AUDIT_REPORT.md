# UrbanFix Spec Audit Report

**Date:** 2026-09-12
**Repository:** `/home/aldo/dev/06-apps-urbanfix`
**Audited Specs:** 001-gmail-report-import, 001-meldpunt-browser-automation, 002-incident-creation-workflow, 003-email-sync-tracking, 004-reminders-automation

---

## Executive Summary

| Spec | Status | Coverage | Key Gap |
|------|--------|----------|---------|
| 001-gmail-report-import | ✅ Partial | ~85% | UI code-filtering exists but no dedicated `POST /api/reports/:id/codes` endpoint |
| 001-meldpunt-browser-automation | ⚠️ Stub | ~40% | Browser agent coded but reCAPTCHA solving is simulated; no real form submission |
| 002-incident-creation-workflow | ✅ Implemented | ~90% | Only gap is real Meldpunt submission (covered by spec 001) |
| 003-email-sync-tracking | ✅ Partial | ~70% | IMAP polling implemented; real automatic polling on email arrival missing |
| 004-reminders-automation | ✅ Partial | ~75% | Cron job implemented; UI trigger and threshold config in settings need wiring |

---

## Spec 001: Gmail Report Import

### What's Implemented

| Requirement | File | Lines | Status |
|-------------|------|-------|--------|
| IMAP credentials via env | `server/services/imapService.ts` | 448-469 | ✅ |
| SINCE "10-Oct-2025" filter | `server/services/imapService.ts` | 484-486 | ✅ |
| AWV code regex `[A-Z]{2}-\d{2,4}-\d{4}` | `server/services/imapService.ts` | 510-511 | ✅ |
| Code extraction from subject+body | `server/services/imapService.ts` | 37-43 | ✅ |
| AI analysis on attachments | `server/services/imapService.ts` | 99-150 | ✅ |
| Deduplication by `externalEmailId` | `server/services/imapService.ts` | 60-66, 152-158 | ✅ |
| Multiple incident codes on report | `src/types.ts` | 110 | ✅ |
| Report creation from email | `server/services/imapService.ts` | 152-395 | ✅ |
| UI: Edit Codes modal | `src/components/EditCodesModal.tsx` | 1-172 | ✅ |
| UI: Incident code badges in cards | `src/components/ReportCard.tsx` | 48-58 | ✅ |
| UI: Code filter dropdown | `src/components/ReportFilter.tsx` | 1-73 | ✅ |

### What's Missing

| Gap | Detail | Recommendation |
|-----|--------|----------------|
| **No `POST /api/reports/:id/codes` endpoint** | Spec SC8 requires an API endpoint for adding/removing codes. The `EditCodesModal` calls `onSave(codes)` but this updates client-side only — no backend persists changes to `incidentCodes`. | Add endpoint to `server.ts`; update `EditCodesModal` to POST to it. |
| **No multi-code filter on `/api/reports`** | Spec SC7 says filter by one or more codes. `ReportFilter` supports single-code select only. | Extend filter to multi-select; add `?codes=KM-...,MB-...` query param support in GET `/api/reports`. |
| **No join table (`report_incident_codes`)** | Spec says codes should use a join table, not stored in a delimited list. Current implementation stores codes as `string[]` on `ReportItem.incidentCodes`. | Acceptable deviation for JSON storage; no database migration needed. Flag as technical debt if SQL migration occurs. |

---

## Spec 001: Meldpunt Browser Automation

### What's Implemented

| Requirement | File | Lines | Status |
|-------------|------|-------|--------|
| Playwright + Chromium | `server/services/meldpuntBrowser.ts` | 1 | ✅ |
| Browser launch with Buster extension | `server/services/meldpuntBrowser.ts` | 28-53 | ✅ |
| reCAPTCHA v2 detection | `server/services/meldpuntBrowser.ts` | 194-266 | ⚠️ Partial |
| Location step with GPS click | `server/services/meldpuntBrowser.ts` | 520-603 | ⚠️ Partial |
| FAQ skip detection | `server/services/meldpuntBrowser.ts` | 486-518 | ✅ |
| Impact group selection | `server/services/meldpuntBrowser.ts` | 422-484 | ✅ |
| Contact info pre-fill | `server/services/meldpuntBrowser.ts` | 359-420 | ✅ |
| Submission & tracking code capture | `server/services/meldpuntBrowser.ts` | 293-357 | ⚠️ Partial |
| Mode switch (`MELDPUNT_MODE=real`) | `server/services/meldpuntBot.ts` | 28-36 | ✅ |

### What's Missing

| Gap | Detail | Recommendation |
|-----|--------|----------------|
| **reCAPTCHA solving is simulated** | `meldpuntBrowser.ts` lines 226-237: code explicitly states "simulate solving with Whisper" and returns a mock token. The `solveRecaptcha()` method clicks UI elements but doesn't actually solve. | Integrate real Buster extension audio challenge flow; use local Whisper model via `BUSTER_WHISPER_MODEL` env var. |
| **Location click is placeholder** | `meldpuntBrowser.ts` lines 541-569: clicks map center as placeholder, not actual GPS coordinate. | Implement Leaflet `latLngToLayerPoint()` conversion or use browser `page.evaluate()` with Leaflet API. |
| **Photo upload not wired** | `fillForm()` validates size but doesn't actually upload files via `page.setInputFiles()`. | Add `page.locator('input[type="file"]').setInputFiles()` for each photo. |
| **No integration tests** | Spec mentions "Add integration tests with mock pages". | Create `test/e2e/meldpunt.spec.ts` with Playwright mock server. |
| **Buster extension path hardcoded fallback** | `meldpuntBrowser.ts` line 22 uses `.bundler/buster-extension/` — must verify this path exists and contains a valid manifest. | Verify extension integrity; add health check on startup. |

---

## Spec 002: Incident Creation Workflow

### What's Implemented

| Requirement | File | Lines | Status |
|-------------|------|-------|--------|
| Photo upload with drag & drop | `src/components/NewReportWorkflow.tsx` | 59-87 | ✅ |
| EXIF GPS extraction | `src/utils/exifParser.ts` | (exists) | ✅ |
| Map preview with GPS pin | `src/components/LocationPickerMap.tsx` | (exists) | ✅ |
| AI defect analysis | `server/services/ai.ts` | (exists) | ✅ |
| AI report generation | `server/services/ai.ts` | (exists) | ✅ |
| Form preview & editing | `src/components/NewReportWorkflow.tsx` | 97-100 | ✅ |
| Impact group selection | `src/components/NewReportWorkflow.tsx` | 44-49 | ✅ |
| Location confirmation with map | `src/components/NewReportWorkflow.tsx` | 100+ | ✅ |
| Contact info pre-fill | `src/components/NewReportWorkflow.tsx` | settings-based | ✅ |
| Submission flow (mock) | `server/services/meldpuntBot.ts` | 42-218 | ⚠️ Mock only |
| Timeline view | `src/components/TimelineView.tsx` | (exists) | ✅ |
| SSE real-time updates | `server.ts` | 92-106 | ✅ |

### What's Missing

| Gap | Detail | Recommendation |
|-----|--------|----------------|
| **Real Meldpunt submission** | `executeMeldpuntSubmission()` uses mock by default (`MELDPUNT_MODE=real` required). | Complete browser automation gaps in Spec 001 first, then enable by default. |
| **Photo compression on client** | Spec says "compress if needed" for >2.5MB. Validation exists but no client-side canvas compression. | Add `src/utils/imageCompress.ts` using canvas `toBlob()`. |

---

## Spec 003: Email Sync & Tracking

### What's Implemented

| Requirement | File | Lines | Status |
|-------------|------|-------|--------|
| Email storage in JSON | `server/services/storage.ts` | (exists) | ✅ |
| Fuzzy text matching | `server/services/emailSync.ts` | 6-41 | ✅ |
| Tracking code extraction | `server/services/emailSync.ts` | 63-83 | ✅ |
| Status keyword detection | `src/utils/statusDeduction.ts` | (exists) | ✅ |
| Simulated email generation | `server/services/emailSync.ts` | 171-245 | ✅ |
| Manual email processing | `server.ts` line 306 `POST /api/emails/process-incoming` | ✅ |
| IMAP polling service | `server/services/imapService.ts` | 400-430, 444-563 | ✅ |
| Poll interval configurable | `server/services/imapService.ts` | 405 | ✅ |

### What's Missing

| Gap | Detail | Recommendation |
|-----|--------|----------------|
| **Automatic email processing on arrival** | Spec says "process and match automatically." Current polling is manual (`/api/emails/poll-now`) or scheduled via `startImapPolling()`. No real-time webhook/listener. | Acceptable for IMAP (polling model); document as limitation. Consider WebSocket push on new email detected. |
| **Match score threshold not enforced** | Spec says "> 0.8 = auto-link." `emailSync.ts` line 92 uses `>= 0.4`. SettingsModal already exposes `reminderThresholdDays` (line 674) and `reminderCronSchedule` (line 694), but **no `autoSendReminders` toggle** exists in the UI. | Raise fuzzy-match threshold to 0.8 (or make configurable); add `autoSendReminders` toggle to SettingsModal. |

---

## Spec 004: Reminders Automation

### What's Implemented

| Requirement | File | Lines | Status |
|-------------|------|-------|--------|
| AI-generated reminder text | `server/services/ai.ts` `generateReminderEmail()` | (exists) | ✅ |
| Manual "send reminder" button | `src/components/ReportDetailModal.tsx` | (exists) | ✅ |
| Cron job for stale incidents | `server/services/reminderCron.ts` | 1-166 | ✅ |
| Configurable threshold (days) | `server/services/reminderCron.ts` | 97-99 | ✅ |
| `lastReminderSentDate` tracking | `src/types.ts` line 106 | ✅ |
| SMTP sending | `server/services/smtpSend.ts` | (exists) | ✅ |

### What's Missing

| Gap | Detail | Recommendation |
|-----|--------|----------------|
| **Reminder threshold not exposed in settings UI** | `emailSync.reminderThresholdDays` exists in type but SettingsModal doesn't render it. | Add field to `SettingsModal.tsx`. |
| **Auto-send reminders toggle not wired** | `settings.emailSync.autoSendReminders` checked in cron but no UI toggle. | Add toggle to SettingsModal. |
| **No UI indicator of pending reminders** | Users can't see which reports will trigger reminders. | Add badge/indicator on report cards for "reminder due in X days". |

---

## Recommended Next Actions (Priority Order)

### P0: API Endpoint Gap (Spec 001)
**File:** `server.ts`  
**Action:** Add `POST /api/reports/:id/codes` endpoint to persist code edits from `EditCodesModal`.  
**Impact:** Without this, manual code edits are lost on page reload.

### P1: Match Score Threshold (Spec 003)
**File:** `server/services/emailSync.ts` line 92  
**Action:** Change `>= 0.4` to `>= 0.8` or add `matchScoreThreshold` to settings.  
**Impact:** Prevents false-positive email-to-report linkages.

### P2: Reminder Settings UI (Spec 004) — **Already Partially Done**
**File:** `src/components/SettingsModal.tsx` lines 674-700  
**Status:** `reminderThresholdDays` and `reminderCronSchedule` are already wired. Only the `autoSendReminders` toggle is missing from the UI.  
**Action:** Add the `autoSendReminders` checkbox to SettingsModal.  
**Impact:** Makes reminder auto-send discoverable and toggleable.

### P3: Real Browser Automation (Spec 001)
**Files:** `server/services/meldpuntBrowser.ts`  
**Action:** Fix reCAPTCHA solver to use real Buster extension, implement actual Leaflet GPS click, wire photo upload.  
**Impact:** Enables production submission to MeldpuntWegen.be.

### P4: Multi-Code Filter + autoSendReminders Toggle (Spec 001 + 004)
**Files:** `src/components/ReportFilter.tsx`, `server.ts` GET `/api/reports`, `src/components/SettingsModal.tsx`  
**Action:** Extend filter to support multiple codes; add `autoSendReminders` checkbox to SettingsModal.  
**Impact:** Better UX for multi-code filtering; complete reminder config parity.

---

## Files Referenced

| File | Purpose |
|------|---------|
| `server/services/imapService.ts` | IMAP polling, email import, code extraction |
| `server/services/meldpuntBot.ts` | Submission orchestration (mock/real switch) |
| `server/services/meldpuntBrowser.ts` | Playwright browser automation agent |
| `server/services/emailSync.ts` | Fuzzy matching, simulated emails |
| `server/services/reminderCron.ts` | Scheduled reminder checks |
| `server.ts` | Express routes |
| `src/types.ts` | Data models (ReportItem, EmailCorrespondence) |
| `src/components/EditCodesModal.tsx` | Manual code editing UI |
| `src/components/ReportFilter.tsx` | Code-based filtering UI |
| `src/components/ReportCard.tsx` | Code badge display |
| `src/components/EmailInbox.tsx` | Email correspondence view |
| `src/components/NewReportWorkflow.tsx` | Incident creation wizard |
| `src/components/ReportDetailModal.tsx` | Incident detail with reminders |
