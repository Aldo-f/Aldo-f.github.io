# Input Validation Specifications

## Overview
All incoming data to the API must be validated and sanitised before any processing. The validation rules are enforced in the Express request handlers located under `server/`.

## General Rules
- **Never trust client input.** Validate every field, even if optional.
- **Sanitise strings** to remove any HTML or script tags before storing or rendering.
- **Use strict typings** defined in `src/types.ts` for payload structures.

## Field‑specific Validation
| Field | Type | Constraints | Regex / Length |
|-------|------|-------------|----------------|
| `email` | string | required, must be a valid email address | `^[^@\s]+@[^@\s]+\.[^@\s]+$` |
| `phoneNumber` | string | optional, 7‑15 digits, may start with `+` | `^\+?\d{7,15}$` |
| `description` | string | optional, max 500 characters | `.{0,500}` |
| `latitude` / `longitude` | number | required, valid coordinate ranges | latitude: `-90..90`, longitude: `-180..180` |
| `imageBase64` | string | optional, base64‑encoded, max 25 MiB | size check performed before decode |

## Sanitisation
- Use the `sanitize-html` package (already a dependency) to strip any HTML tags.
- Trim whitespace from string fields.
- Encode special characters when storing text that may be rendered in the UI.

## Implementation Notes
- Validation is performed using **express‑validator** middleware in `server/routes/*.ts`.
- Errors are returned with the standard API response shape `{ success: false, error: "Validation error: <details>" }` and an HTTP **400** status.
- Add new validation rules here before updating the corresponding route file.

---
*Generated on $(date)*
