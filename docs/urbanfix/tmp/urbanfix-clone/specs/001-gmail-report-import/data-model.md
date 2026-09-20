# Data Model – Gmail Report Import  

**Feature**: gmail-report-import  
**Spec**: specs/001-gmail-report-import/spec.md  
**Plan**: specs/001-gmail-report-import/plan.md  

## 🗃️ Entities  

### Report (existing, extended)  
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Existing |
| `description` | TEXT | NOT NULL | AI‑generated or user‑entered |
| `location` | TEXT | | Lat/long or address string |
| `severity` | TEXT | | e.g., "low", "medium", "high" |
| `photoBase64` | TEXT | | Base64‑encoded image |
| `source` | TEXT | NOT NULL | "web" or "email" |
| `receivedAt` | TEXT | NOT NULL | ISO‑8601 timestamp |
| `status` | TEXT | NOT NULL | SubmissionStatus enum |
| `timeline` | JSON | | Array of TimelineEvent |
| `incidentCodes` | (virtual) | | Derived from join table |
| **`externalEmailId`** | **TEXT** | **UNIQUE** | **NEW** – stores e‑mail `Message-ID` for deduplication |
| **`rawEmail`** | **TEXT** | | **NEW** – optional full MIME source for audit |

### IncidentCode (new – join table entity)  
| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `report_id` | INTEGER | PRIMARY KEY, REFERENCES reports(id) ON DELETE CASCADE | Part of composite PK |
| `code` | TEXT | PRIMARY KEY | The incident code string (exact as found) |

## 🔗 Relationships  
- **Report 1 : N IncidentCode** – A report can have multiple incident codes (AWV, Ghent, MoBiliteit, etc.).  
- **IncidentCode N : 1 Report** – Each code row belongs to exactly one report.  

## ✅ Validation Rules  
1. `externalEmailId` must be unique across all reports (enforced by DB UNIQUE constraint).  
2. `code` in `report_incident_codes` must be non‑empty and stored **exactly as found** (no normalisation).  
3. `source` must be one of the allowed values ("web", "email").  
4. `receivedAt` must be a valid ISO‑8601 date‑time string.  

## 🔄 State Transitions (Report.status)  
Unchanged from existing `SubmissionStatus` type:  
`concept` → `verzenden` → `verzonden` → `in_behandeling` → `opgelost` / `geannuleerd`  

## 📋 Migration Steps (SQL)  
```sql
-- 1. Add new columns to reports table
ALTER TABLE reports ADD COLUMN externalEmailId TEXT UNIQUE;
ALTER TABLE reports ADD COLUMN rawEmail TEXT;

-- 2. Create join table for incident codes
CREATE TABLE report_incident_codes (
    report_id INTEGER NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    code TEXT NOT NULL,
    PRIMARY KEY (report_id, code)
);

-- 3. Indexes for common look‑ups
CREATE INDEX idx_reports_external_email ON reports(externalEmailId);
CREATE INDEX idx_report_incident_codes_code ON report_incident_codes(code);
```