# Spec: Automated Reminders

## Feature Number
004

## Short Name
reminders-automation

## Goal
Send automated reminder emails to AWV for incidents that have been pending too long.

## Current State
- ✅ AI-generated reminder text
- ✅ Manual "send reminder" button
- ❌ Automatic scheduled reminders
- ❌ Configurable reminder thresholds

## Acceptance Criteria

### AC-1: Manual Reminder
- [ ] Button on incident detail page: "Herinnering sturen"
- [ ] Generates formal reminder email via AI
- [ ] Sends via simulated email (future: real SMTP)
- [ ] Logs reminder in automationLogs

### AC-2: Automatic Reminders
- [ ] Configurable threshold (default: 14 days)
- [ ] Cron job checks for stale incidents
- [ ] Sends reminder if no update since threshold
- [ ] Tracks lastReminderSentDate

### AC-3: Reminder Content
- [ ] Includes tracking code
- [ ] References original submission date
- [ ] Formal, polite Dutch language
- [ ] Max 500 characters

## Out of Scope
- SMS reminders
- Phone call reminders
- Multi-language support

## Related Specs
- Spec 001: Browser Automation
- Spec 002: Incident Creation Workflow
- Spec 003: Email Sync
