# API Response Schemas

Below are response body definitions for the public API endpoints.

## /api/reports (GET)
```json
[
  {
    "id": "string",
    "title": "string",
    "rawDefectHint": "string",
    "fullReportText": "string",
    "photos": [],
    "location": {},
    "contactInfo": {},
    "submissionStatus": "concept|verzenden|ingediend|bevestigd|in_behandeling|doorgestuurd|opgelost|afgewezen",
    "lastUpdatedDate": "ISO8601 string"
  }
]
```

## /api/reports/:id (GET)
```json
{
  "id": "string",
  "title": "string",
  "rawDefectHint": "string",
  "fullReportText": "string",
  "photos": [],
  "location": {},
  "contactInfo": {},
  "submissionStatus": "concept|verzenden|ingediend|bevestigd|in_behandeling|doorgestuurd|opgelost|afgewezen",
  "timeline": [],
  "emails": [],
  "automationLogs": [],
  "lastUpdatedDate": "ISO8601 string"
}
```

## /api/ai/analyze-defect (POST)
```json
{
  "analysis": "string",
  "confidence": 0.0,
  "extractedData": {}
}
```

(Additional endpoints omitted for brevity.)