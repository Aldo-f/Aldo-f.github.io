# Spec: Complete Incident Creation Workflow

## Feature Number
002

## Short Name
incident-creation-workflow

## Goal
Implement the complete A-to-Z workflow for creating and submitting a road defect incident:
Photo upload → AI analysis → Report generation → Review → Submit to AWV → Track response.

## Current State
Partial implementation:
- ✅ Photo upload with EXIF GPS extraction
- ✅ AI defect analysis (analyzeDefect)
- ✅ AI report generation (generateFullReport)
- ✅ Form preview and editing
- ❌ Real submission to meldpuntwegen.be (simulated only)
- ✅ Email tracking (simulated)
- ✅ Timeline view
- ✅ SSE real-time updates

## Acceptance Criteria

### AC-1: Photo Upload & EXIF Extraction
- [ ] Drag & drop or camera input for photos
- [ ] EXIF parsing extracts GPS coordinates, timestamp, filename
- [ ] Shows preview with GPS location on map
- [ ] Validates max 2.5 MB per photo (compress if needed)

### AC-2: AI Defect Analysis
- [ ] Sends photos + user hint to AI endpoint
- [ ] Returns defect hypotheses, suggested categories, detected signs, severity
- [ ] Displays suggestions for user to confirm/modify

### AC-3: Report Text Generation
- [ ] AI generates full report text (< 2000 chars)
- [ ] Text includes: problem description, photo references, safety risk, request
- [ ] User can edit the text before submission
- [ ] Live character counter shows remaining capacity

### AC-4: Impact Group Selection
- [ ] User selects at least 1 impacted group (voetgangers, fietsers, openbaar_vervoer, gemotoriseerd)
- [ ] Default: all groups pre-selected
- [ ] Validation: at least 1 required

### AC-5: Location Confirmation
- [ ] Shows map with GPS pin from photo EXIF
- [ ] User can drag pin to adjust location
- [ ] Reverse geocoding shows address
- [ ] Option to mark "without location" (rare)

### AC-6: Contact Info Pre-fill
- [ ] Loads from user settings (Aldo Fieuw, aldo.fieuw@gmail.com)
- [ ] Checkbox for "wants response" pre-checked
- [ ] User can modify before submission

### AC-7: Submission Flow
- [ ] Click "Versturen" triggers meldpuntBot submission
- [ ] Shows step-by-step progress (6 steps)
- [ ] On success: stores tracking code, updates status to 'in_behandeling'
- [ ] On failure: shows error, allows retry

### AC-8: Post-Submission
- [ ] Navigates to incident detail page
- [ ] Shows tracking code prominently
- [ ] Enables email tracking and reminder features

## Out of Scope
- Bulk photo upload from Google Photos API (manual selection only)
- Multi-user authentication (single user system)
- Mobile app (web-only for now)

## Technical Notes
- Use `exifr` library for EXIF parsing
- Client-side canvas compression for oversized photos
- Store photos as base64 in ReportItem (as per existing pattern)

## Related Specs
- Spec 001: Browser Automation for MeldpuntWegen.be
- Spec 003: Email Synchronization
- Spec 004: SSE Real-time Updates
