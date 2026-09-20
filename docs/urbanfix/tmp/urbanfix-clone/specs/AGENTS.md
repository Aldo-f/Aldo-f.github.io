# Specs Knowledge Base

**Generated:** 2026-09-13 16:50:00 UTC

## OVERVIEW
Spec-driven development specifications. Each spec directory contains the requirements, contracts, and implementation plan for a feature.

## STRUCTURE
```
specs/
├── 001-gmail-report-import/       # Email import feature
│   ├── spec.md                    # Main specification
│   ├── contracts/api.md           # API contract definitions
│   ├── data-model.md              # Data model specifications
│   ├── quickstart.md              # Getting started guide
│   └── plan.md                    # Implementation plan
├── 001-meldpunt-browser-automation/
├── 002-incident-creation-workflow/
├── 003-email-sync-tracking/
└── 004-reminders-automation/
```

## WORKFLOW
1. **Discover**: Identify feature requirement
2. **Specify**: Write spec.md with requirements
3. **Contract**: Define API/data contracts
4. **Plan**: Break into implementation tasks
5. **Implement**: Build feature following spec
6. **Verify**: Run tests, update spec if needed

## SPEC FILE PURPOSES
- `spec.md` - Main requirements and acceptance criteria
- `contracts/api.md` - Request/response schemas
- `data-model.md` - Database schemas, interfaces
- `plan.md` - Implementation steps and timeline
- `quickstart.md` - Testing and verification guide

## USAGE
- New features should start with a spec in this directory
- Specs guide implementation and ensure requirements are clear
- Update specs when requirements change
- Use specs for onboarding new developers

## NOTES
- Spec numbers indicate priority/order (001, 002, etc.)
- Each spec is self-contained with its own subdirectory
- Cross-reference specs when features interact
- OpenAPI spec in `specs/openapi.yaml` is auto-generated