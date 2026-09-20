# API Contracts – Gmail Report Import  

**Feature**: gmail-report-import  
**Spec**: specs/001-gmail-report-import/spec.md  
**Plan**: specs/001-gmail-report-import/plan.md  

## 📡 Public Endpoints  

### 1. GET /api/reports  
Retrieve a paginated list of reports, optionally filtered by incident code.  

#### Query Parameters  
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | No | Filter reports that contain this incident code (exact match). |
| `source` | string | No | Filter by `source` ("web" or "email"). |
| `page` | integer | No | Page number (1‑based). Default 1. |
| `limit` | integer | No | Records per page. Default 20. |

#### Response (200 OK)  
```json
{
  "success": true,
  "data": {
    "reports": [
      {
        "id": 123,
        "description": "Pothole on Main St...",
        "location": "51.123,4.567",
        "severity": "medium",
        "photoBase64": "/9j/4AAQSkZJRgABAQ...",
        "source": "email",
        "receivedAt": "2025-10-10T08:30:00Z",
        "status": "concept",
        "timeline": [],
        "incidentCodes": ["KM-2025-29314", "MB-26-09439"]
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 20
  }
}
```

---

### 2. GET /api/reports/:id  
Retrieve a single report by its database id.  

#### Response (200 OK)  
```json
{
  "success": true,
  "data": {
    "id": 123,
    "description": "...",
    "location": "...",
    "severity": "...",
    "photoBase64": "...",
    "source": "email",
    "receivedAt": "...",
    "status": "...",
    "timeline": [],
    "incidentCodes": ["KM-2025-29314"]
  }
}
```

#### Response (404 NOT FOUND)  
```json
{
  "success": false,
  "error": "Report not found"
}
```

---

### 3. POST /api/reports/:id/codes  
Add or remove an incident code from a report’s join table.  

#### Request Body  
```json
{
  "code": "GENT-2025-001",
  "action": "add"  // "add" | "remove"
}
```

#### Response (200 OK)  
```json
{
  "success": true,
  "data": {
    "incidentCodes": ["KM-2025-29314", "GENT-2025-001"]
  }
}
```

#### Response (400 BAD REQUEST – validation error)  
```json
{
  "success": false,
  "error": "Code must be a non‑empty string"
}
```

---

### 4. DELETE /api/reports/:id/codes/:code  
Remove a specific incident code from a report. *(Alternative to POST if preferred.)*  

#### Response (200 OK)  
```json
{
  "success": true,
  "data": {
    "incidentCodes": ["KM-2025-29314"]
  }
}
```

#### Response (404 NOT FOUND)  
```json
{
  "success": false,
  "error": "Code not found for this report"
}
```

---

### 5. GET /api/reports/codes  
Return all distinct incident codes currently stored (for UI autocomplete/filter).  

#### Response (200 OK)  
```json
{
  "success": true,
  "data": ["KM-2025-29314", "MB-26-09439", "GENT-2025-001", "[A-700739]"]
}
```

---

## 🔒 Internal Contracts (not public)  

### IMAP Poller (service, not exposed)  
- Runs every `IMAP_POLL_INTERVAL_MS` milliseconds.  
- Connects to `imap.gmail.com:993` (TLS) using `GMAIL_IMAP_USER` / `GMAIL_IMAP_PASSWORD`.  
- Searches: `SINCE "10-Oct-2025" UNSEEN`.  
- For each message:  
  1. Parse headers → `Message-ID`, `Date`, `Subject`, `From`.  
  2. Extract codes via regex.  
  3. Decode attachments → run AI analysis.  
  4. Insert or update report + join table rows.  
  5. Mark message `\Seen`.  

---

All responses follow the project’s standard `{ success: boolean, data?: any, error?: string }` format.