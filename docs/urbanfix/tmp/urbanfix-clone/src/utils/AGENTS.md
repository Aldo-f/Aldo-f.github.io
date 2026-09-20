# Utils Knowledge Base

**Generated:** 2026-09-13 16:50:00 UTC

## OVERVIEW
Pure utility functions for the frontend application. Stateless helpers for data processing, encryption, and calculations.

## STRUCTURE
```
src/utils/
├── aiKeyEncoder.ts        # AES-256 encryption for API keys
├── aiModels.ts            # AI provider/model configuration
├── deduplication.ts       # Report deduplication algorithm
├── draftStorage.ts        # Local storage for draft reports
├── emailCleaner.ts        # Email text normalization
├── exifParser.ts          # Photo GPS/metadata extraction
├── geo.ts                 # Geolocation utilities
├── id.ts                  # ID generation
├── logger.ts              # Structured logging
└── permissions.ts         # Role-based permission checks
```

## KEY FUNCTIONS
- **aiKeyEncoder**: Encrypts/decrypts AI API keys using AES-256
- **deduplicateReportsList**: Fuzzy matching algorithm for duplicate detection
- **parseExifData**: Extracts GPS coordinates from uploaded images
- **sanitizeForMatching**: Normalizes text for email-to-report matching

## CONVENTIONS
- **Pure Functions**: No side effects (except logger)
- **TypeScript Interfaces**: All functions have strict type signatures
- **No Imports from Components**: Utils don't import React components
- **Stateless**: Functions don't maintain internal state

## SECURITY NOTES
- API keys are encrypted at rest (never stored in plaintext)
- Use `aiKeyEncoder.encrypt()` before storing keys
- Use `aiKeyEncoder.decrypt()` when passing to AI providers
- Encryption key derived from environment variable

## NOTES
- `aiModels.ts` now exports empty arrays - users configure providers via UI
- `deduplication.ts` uses N-gram overlap for fuzzy matching
- `draftStorage.ts` uses localStorage for temporary report drafts