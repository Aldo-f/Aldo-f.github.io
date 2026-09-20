# API Request Schemas

Below are request body definitions for the public API endpoints.

## /api/reports (POST)
```json
{
  "title": "string",
  "rawDefectHint": "string",
  "photos": [{
    "filename": "string",
    "gps": { "latitude": number, "longitude": number }
  }],
  "location": {
    "latitude": number,
    "longitude": number,
    "address": "string"
  },
  "contactInfo": {
    "firstName": "string",
    "lastName": "string",
    "email": "string",
    "wantsResponse": boolean
  }
}
```

## /api/reports/:id/timeline (POST)
```json
{
  "title": "string",
  "description": "string",
  "status": "concept|verzenden|ingediend|bevestigd|in_behandeling|doorgestuurd|opgelost|afgewezen"
}
```

## /api/ai/analyze-defect (POST)
```json
{
  "photos": [{ "filename": "string", "base64Data": "string" }]
}
```

(Additional endpoints omitted for brevity.)