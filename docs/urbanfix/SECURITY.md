# Security Specifications

## Overview
This document outlines the security model for the UrbanFix application, covering authentication, authorization, CORS policy, and general security best‑practices applied across the backend API and frontend.

## Authentication
- **Provider**: Google Gemini API key is used for AI services; user authentication for the app is based on **JWT** issued by the server.
- **Login flow**:
  1. User provides credentials (email/password) via `/api/auth/login`.
  2. Server validates credentials against stored hashes (bcrypt).
  3. On success, a signed JWT (HS256) containing `userId`, `email`, and `role` is returned.
- **Token expiry**: 1 hour, with refresh token endpoint `/api/auth/refresh` to obtain a new JWT.
- **HTTPS only**: All endpoints must be accessed over HTTPS in production; the development server runs locally over HTTP but should be behind a proxy for secure transport.

## Authorization (Role‑Based Access Control)
- **Roles**: `admin`, `moderator`, `user`.
- **Permissions**:
  - `admin`: Full access to all API routes, including user management, report deletion, and system settings.
  - `moderator`: Can view and update reports, but cannot delete users or change system settings.
  - `user`: Can create new defect reports and view their own reports only.
- **Implementation**: Middleware `checkRole` in `server/middleware/auth.ts` checks `req.user.role` against required role for the route. Unauthorized attempts return **403 Forbidden**.

## CORS Policy
- **Allowed origins**: In production, only the domain `https://urbanfix.be` (and sub‑domains) are allowed.
- **Development**: `http://localhost:3000` is permitted.
- **Headers**:
  - `Access-Control-Allow-Origin`: Set dynamically based on whitelist.
  - `Access-Control-Allow-Methods`: `GET,POST,PUT,DELETE,OPTIONS`.
  - `Access-Control-Allow-Headers`: `Content-Type, Authorization`.
- **Implementation**: Configured via Express `cors` middleware in `server.ts`.

## Input Sanitisation & Validation (Reference)
- All validation rules are documented in **docs/VALIDATION.md** and enforced via `express‑validator`.
- Sanitisation of string inputs using `sanitize-html` to strip scripts and HTML.

## Secure Headers
- Use `helmet` middleware to set security‑related HTTP headers:
  - `Content‑Security‑Policy`
  - `X‑Content‑Type‑Options`
  - `X‑Frame‑Options`
  - `Referrer‑Policy`

## Rate Limiting & Brute‑Force Protection
- Apply `express‑rate‑limit` on authentication endpoints: max 5 attempts per minute per IP.
- Log failed login attempts and lock accounts after 10 consecutive failures for 15 minutes.

## Data Protection
- Sensitive data such as passwords are stored hashed with bcrypt (cost factor 12).
- No plain‑text secrets are committed to the repository; environment variables (e.g., `GEMINI_API_KEY`, `JWT_SECRET`) are loaded from `.env`.
- Uploaded images are stored base64‑encoded with a maximum size of 25 MiB; files are scanned for malicious payloads before processing.

## Auditing & Logging
- All security‑relevant actions (login, logout, failed auth, role changes) are logged using `winston` with log level `info`.
- Logs are written to `logs/` and rotated daily.

---
*Generated on $(date)*
