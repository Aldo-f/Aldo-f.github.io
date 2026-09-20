# Spec: Email Synchronization & Tracking

## Feature Number
003

## Short Name
email-sync-tracking

## Goal
Automatically match incoming AWV emails to reported incidents and track status updates.

## Current State
- ✅ Email storage and retrieval
- ✅ Fuzzy text matching algorithm
- ✅ Tracking code extraction
- ✅ Simulated email generation
- ❌ Real IMAP polling (not implemented)
- ❌ Automatic email processing on arrival

## Acceptance Criteria

### AC-1: Email Storage
- [ ] Store all received emails in JSON file
- [ ] Include metadata: messageId, date, from, to, subject, body
- [ ] Link to report via matchedReportId

### AC-2: Fuzzy Matching
- [ ] Normalize text (remove whitespace, punctuation, lowercase)
- [ ] Calculate token overlap similarity
- [ ] Match score > 0.8 = auto-link
- [ ] Extract tracking code from subject/body

### AC-3: Status Detection
- [ ] Detect status keywords: "in behandeling", "doorgestuurd", "opgelost", "afgewezen"
- [ ] Update ReportItem.submissionStatus automatically
- [ ] Add TimelineEvent for status change

### AC-4: IMAP Polling (Future)
- [ ] Configurable poll interval (default: 5 minutes)
- [ ] Fetch new emails from Gmail IMAP
- [ ] Process and match automatically

### AC-5: Manual Processing
- [ ] API endpoint to process email text directly
- [ ] Simulate incoming email for testing
- [ ] Show match confidence score

## Out of Scope
- Email sending (only receiving for now)
- SMTP integration
- Multiple email accounts

## Related Specs
- Spec 001: Browser Automation
- Spec 002: Incident Creation Workflow
- Spec 004: SSE Real-time Updates
