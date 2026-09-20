# Graph Report - 06-apps-urbanfix  (2026-09-17)

## Corpus Check
- 179 files · ~210,800 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 7, .example 1, .lock 1)

## Summary
- 834 nodes · 1873 edges · 64 communities (36 shown, 28 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Test Suite - Settings Persistence
- External Dependencies - React/UI Libraries
- AI Features - Waterfall & Key Encryption
- Firebase Admin & Firestore SDK
- Package.json - Core Metadata
- Package.json - Dev Dependencies
- Specify Bash Scripts
- Frontend Components - Edit Codes Modal
- React App Entry & Key Components
- Express Server & Core Services
- Package.json - Production Dependencies
- Meldpunt Browser Automation
- Firebase Auth & Auth Modal
- AI Waterfall Settings Component
- Model Discovery Utilities
- Spec-Kit Workflow & Constitution
- Email Processing & Firestore Storage
- AI Service - Defect Analysis & Reports
- Settings Modal & User Management
- TypeScript Configuration
- E2E Tests - Deletion & Persistence
- PWA Manifest
- Report Filter Components
- Footer & Map Components
- Firestore Storage Unit Tests
- Meldpunt Bot Service
- Reminder Cron Service
- Package Scripts
- Vite & Build Tooling
- Deduplication Utilities
- Package Allow Scripts
- Public Icons & Brand Assets
- Logger Utility
- Python Sync Scripts
- Settings & Real Import Services
- ESLint Configuration
- Internationalization (i18n)
- Husky Pre-commit Hooks
- Email Integration Libraries
- Translation Keys
- Husky Pre-commit Entry
- Lint Staged Config
- Package Overrides
- Developer Documentation
- Playwright Test Report
- PWA Icon 512x512
- Specification Workflow Concept
- Gmail Import Plan Spec
- Gmail Import Quickstart Spec
- Gmail Import Main Spec
- Gmail Import Tasks Spec
- Meldpunt Browser Automation Spec
- Incident Creation Workflow Spec
- Email Sync Tracking Spec
- Reminders Automation Spec
- Specs Knowledge Base
- OpenAPI Specification
- Frontend Knowledge Base
- Components Knowledge Base
- Pages Knowledge Base
- Utils Knowledge Base
- Test Error Context Document

## God Nodes (most connected - your core abstractions)
1. `ReportItem` - 41 edges
2. `react` - 33 edges
3. `startServer()` - 32 edges
4. `lucide-react` - 30 edges
5. `MeldpuntBrowserAgent` - 25 edges
6. `UserRole` - 24 edges
7. `PageRoute` - 22 edges
8. `modelDiscovery` - 19 edges
9. `getReports()` - 16 edges
10. `executeMeldpuntSubmissionReal()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Spec Audit Report` --references--> `UrbanFix Constitution`  [INFERRED]
  AUDIT_REPORT.md → .specify/memory/constitution.md
- `Settings Persistence Bug - AI Waterfall Providers Not Saved` --conceptually_related_to--> `Firestore Storage Service`  [INFERRED]
  test-results/settings-persistence-settings-persistence-chromium/error-context.md → server/services/firestoreStorage.ts
- `sendInitialData()` --calls--> `getReports()`  [EXTRACTED]
  server.ts → server/services/firestoreStorage.ts
- `startServer()` --indirect_call--> `errorLoggerMiddleware()`  [INFERRED]
  server.ts → server/middleware/errorLogger.ts
- `startServer()` --calls--> `analyzeDefect()`  [EXTRACTED]
  server.ts → server/services/ai.ts

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Speckit Workflow Chain** — github_skills_speckit_specify_skill, github_skills_speckit_clarify_skill, github_skills_speckit_plan_skill, github_skills_speckit_tasks_skill, github_skills_speckit_implement_skill, github_skills_speckit_converge_skill, github_skills_speckit_analyze_skill, github_skills_speckit_checklist_skill, github_skills_speckit_constitution_skill, github_skills_speckit_taskstoissues_skill [EXTRACTED 1.00]
- **Core Spec Artifacts Triple** — specify_templates_spec, specify_templates_plan, specify_templates_tasks [EXTRACTED 1.00]
- **Constitution Governance Chain** — specify_memory_constitution, github_skills_speckit_constitution_skill, constitution_authority_principle, sequential_specification_principle [EXTRACTED 1.00]
- **AI Services Core** — ai_waterfall, ai_defect_analysis, ai_report_generation, gemini_ai_provider [INFERRED 0.95]
- **Core Data Models** — report_item, email_correspondence, timeline_event, submission_status [EXTRACTED 1.00]
- **UrbanFix Brand Asset Suite** — public_icons_logo, public_icons_icon_192, public_icons_icon_512, public_icons_logo_svg [INFERRED 0.90]
- **Settings Save/Get Data Flow** — src_components_settings_modal, server, server_services_storage, server_services_firestore_storage [INFERRED 0.85]
- **AI Waterfall UI Component Tree** — src_components_settings_modal, src_components_ai_waterfall_settings, src_types [EXTRACTED 1.00]
- **Test Failure Triple: Spec, Screenshot, Error** — test_e2e_settings_persistence_spec, test_results_settings_persistence_settings_persistence_chromium_test_failed_1, test_results_settings_persistence_error_context [EXTRACTED 1.00]

## Communities (64 total, 28 thin omitted)

### Community 0 - "Test Suite - Settings Persistence"
Cohesion: 0.07
Nodes (50): vitest, calculateTextSimilarity(), normalizeTextForMatching(), processIncomingEmail(), simulateIncomingEmailForReport(), ExtractedEmailData, codesFor(), run() (+42 more)

### Community 1 - "External Dependencies - React/UI Libraries"
Cohesion: 0.08
Nodes (49): exifr, leaflet, yet-another-react-lightbox, ref_yet_another_react_lightbox_plugins_captions, ref_yet_another_react_lightbox_plugins_captions_css, ref_yet_another_react_lightbox_plugins_counter, ref_yet_another_react_lightbox_plugins_counter_css, ref_yet_another_react_lightbox_plugins_download (+41 more)

### Community 2 - "AI Features - Waterfall & Key Encryption"
Cohesion: 0.05
Nodes (51): AGENTS.md Knowledge Base, AI Defect Analysis Service, AES-256 API Key Encryption, AI Report Text Generation, Multi-Provider AI Waterfall, Spec Audit Report, Buster reCAPTCHA Solver, Docker Development Override (+43 more)

### Community 3 - "Firebase Admin & Firestore SDK"
Cohesion: 0.06
Nodes (38): ref_firebase_admin_app, ref_firebase_admin_firestore, ref_firebase_app, ref_firebase_firestore, ref_fs, ref_path, playwright, ref_url (+30 more)

### Community 4 - "Package.json - Core Metadata"
Cohesion: 0.04
Nodes (45): name, private, type, version, autoprefixer, canvas, cookie-parser, csurf (+37 more)

### Community 5 - "Package.json - Dev Dependencies"
Cohesion: 0.05
Nodes (38): devDependencies, autoprefixer, canvas, dotenv, esbuild, eslint, eslint-config-prettier, @eslint/js (+30 more)

### Community 6 - "Specify Bash Scripts"
Cohesion: 0.13
Nodes (29): check-prerequisites.sh script, check_dir(), check_file(), find_specify_root(), format_speckit_command(), get_current_branch(), get_feature_paths(), get_invoke_separator() (+21 more)

### Community 7 - "Frontend Components - Edit Codes Modal"
Cohesion: 0.17
Nodes (23): lucide-react, ref_motion_react, EditCodesModal(), EditCodesModalProps, EmailInboxProps, HeaderProps, PhotoLightbox(), ReportCardProps (+15 more)

### Community 8 - "React App Entry & Key Components"
Cohesion: 0.12
Nodes (24): ref_react_dom_client, App(), EmailInbox(), ReportDetailModal(), deleteReportFromFirestore(), sanitizeForFirestore(), saveEmailToFirestore(), saveReportToFirestore() (+16 more)

### Community 9 - "Express Server & Core Services"
Cohesion: 0.17
Nodes (22): express, ref_module, broadcast(), firebaseConfig, logger, errorLoggerMiddleware(), sendInitialData(), assignEmailToReport() (+14 more)

### Community 10 - "Package.json - Production Dependencies"
Cohesion: 0.07
Nodes (27): dependencies, cookie-parser, csurf, exifr, express, firebase, firebase-admin, @google/genai (+19 more)

### Community 12 - "Firebase Auth & Auth Modal"
Cohesion: 0.14
Nodes (19): firebase_applet_config, ref_firebase_auth, AuthModal(), Header(), ADMIN_EMAILS, auth, AUTHORITY_EMAIL_DOMAINS, db (+11 more)

### Community 13 - "AI Waterfall Settings Component"
Cohesion: 0.20
Nodes (15): AIWaterfallSettings(), AIWaterfallSettingsProps, AIModelProvider, AIProviderAccount, AIProviderType, AIWaterfallConfig, decodeApiKey(), encodeApiKey() (+7 more)

### Community 14 - "Model Discovery Utilities"
Cohesion: 0.18
Nodes (5): discoverModels(), modelDiscovery, ModelDiscoveryResult, ProviderConfig, ProviderModel

### Community 15 - "Spec-Kit Workflow & Constitution"
Cohesion: 0.30
Nodes (20): Checklists as Unit Tests for Requirements, Constitution Authority Principle, Extension Hooks Pattern, speckit-analyze Skill, speckit-checklist Skill, speckit-clarify Skill, speckit-constitution Skill, speckit-converge Skill (+12 more)

### Community 16 - "Email Processing & Firestore Storage"
Cohesion: 0.17
Nodes (17): RFC-822, dotenv, mailparser, saveEmails(), saveReports(), extractCodesFromEmail(), importEmailToReport(), ImportOptions (+9 more)

### Community 17 - "AI Service - Defect Analysis & Reports"
Cohesion: 0.31
Nodes (15): analyzeDefect(), callOpenAICompatible(), generateEmailReply(), generateFullReport(), generateReminderEmail(), getGoogleClient(), resolveProvider(), sanitizeFirstPersonReportText() (+7 more)

### Community 18 - "Settings Modal & User Management"
Cohesion: 0.22
Nodes (14): AuthModalProps, SettingsModal(), UsersManagement(), UsersManagementProps, deleteUserFromFirestore(), getAllowedRoles(), saveUserToFirestore(), sendUserPasswordReset() (+6 more)

### Community 19 - "TypeScript Configuration"
Cohesion: 0.12
Nodes (15): compilerOptions, allowImportingTsExtensions, allowJs, experimentalDecorators, isolatedModules, jsx, lib, module (+7 more)

### Community 20 - "E2E Tests - Deletion & Persistence"
Cohesion: 0.16
Nodes (8): AI Waterfall Architecture Pattern, @playwright/test, Firestore Storage Service, Settings Persistence Bug - AI Waterfall Providers Not Saved, AIWaterfallSettings Component, SettingsModal Component, Settings Persistence Test Error Context, Settings Persistence Test Failed Screenshot

### Community 21 - "PWA Manifest"
Cohesion: 0.15
Nodes (12): background_color, categories, description, dir, display, icons, lang, name (+4 more)

### Community 22 - "Report Filter Components"
Cohesion: 0.17
Nodes (7): react, ReportFilterProps, DocsPage(), DocsPageProps, OpenApiEndpoint, OpenApiSpecDoc, PrivacyPage()

### Community 23 - "Footer & Map Components"
Cohesion: 0.23
Nodes (10): Footer(), FooterProps, LocationPickerMapProps, MapViewProps, NewReportWorkflowProps, PermissionModalProps, NewIncidentPage(), NewIncidentPageProps (+2 more)

### Community 24 - "Firestore Storage Unit Tests"
Cohesion: 0.17
Nodes (11): mockCollection, mockDb, mockDeleteDoc, mockDoc, mockGetDoc, mockGetDocs, mockOrderBy, mockQuery (+3 more)

### Community 25 - "Meldpunt Bot Service"
Cohesion: 0.31
Nodes (8): getReports(), BotSubmitProgressCallback, ExecuteMeldpuntOptions, ExecuteMeldpuntResult, executeMeldpuntSubmission(), executeMeldpuntSubmissionMockDryRun(), AutomationLogStep, generateId()

### Community 26 - "Reminder Cron Service"
Cohesion: 0.29
Nodes (6): node-cron, checkAndSendReminders(), checkMissedRun(), CronState, startReminderCron(), EmailSenderOptions

### Community 27 - "Package Scripts"
Cohesion: 0.22
Nodes (9): scripts, build, clean, dev, lint, prepare, seed:reports, start (+1 more)

### Community 28 - "Vite & Build Tooling"
Cohesion: 0.22
Nodes (6): @tailwindcss/vite, vite, vite-plugin-pwa, @vitejs/plugin-react, ref_vitest_config, __dirname

### Community 29 - "Deduplication Utilities"
Cohesion: 0.44
Nodes (8): deduplicateReportsList(), find(), union(), extractHumanHint(), extractLocationFromRaw(), getCodes(), mergeGroup(), scoreTitle()

### Community 30 - "Package Allow Scripts"
Cohesion: 0.29
Nodes (7): allowScripts, canvas@3.2.3, esbuild@0.25.12, esbuild@0.28.2, @firebase/util@1.15.3, @google/genai@2.19.0, protobufjs@7.6.6

### Community 31 - "Public Icons & Brand Assets"
Cohesion: 0.38
Nodes (7): UrbanFix PWA Icon 192x192, UrbanFix PWA Icon 512x512, UrbanFix Logo, Logo PNG Image, UrbanFix Logo SVG Wrapper, UrbanFix Application Logo, UrbanFix Brand Identity

### Community 32 - "Logger Utility"
Cohesion: 0.43
Nodes (5): format(), LEVELS, LogLevel, replacer(), serializeError()

### Community 33 - "Python Sync Scripts"
Cohesion: 0.33
Nodes (4): json, requests, sys, time

### Community 34 - "Settings & Real Import Services"
Cohesion: 0.53
Nodes (5): getSettings(), cleanBadReports(), isAWVReport(), main(), REPORTS_FILE

### Community 35 - "ESLint Configuration"
Cohesion: 0.40
Nodes (4): @eslint/js, ref_eslint_plugin_prettier_recommended, eslint-plugin-unused-imports, typescript-eslint

### Community 37 - "Husky Pre-commit Hooks"
Cohesion: 0.67
Nodes (3): pre-commit, husky, hooks

## Knowledge Gaps
- **259 isolated node(s):** `common.sh script`, `name`, `private`, `version`, `type` (+254 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 324 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `Report Filter Components` to `Test Suite - Settings Persistence`, `External Dependencies - React/UI Libraries`, `Package.json - Core Metadata`, `Frontend Components - Edit Codes Modal`, `React App Entry & Key Components`, `Firebase Auth & Auth Modal`, `AI Waterfall Settings Component`, `Settings Modal & User Management`, `Footer & Map Components`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `devDependencies` connect `Package.json - Dev Dependencies` to `Package.json - Core Metadata`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `lucide-react` connect `Frontend Components - Edit Codes Modal` to `External Dependencies - React/UI Libraries`, `Package.json - Core Metadata`, `React App Entry & Key Components`, `Firebase Auth & Auth Modal`, `AI Waterfall Settings Component`, `Settings Modal & User Management`, `Report Filter Components`, `Footer & Map Components`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `startServer()` (e.g. with `errorLoggerMiddleware()` and `verifyFirebaseIdToken()`) actually correct?**
  _`startServer()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `common.sh script`, `name`, `private` to the rest of the system?**
  _259 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Test Suite - Settings Persistence` be split into smaller, more focused modules?**
  _Cohesion score 0.06810035842293907 - nodes in this community are weakly interconnected._
- **Should `External Dependencies - React/UI Libraries` be split into smaller, more focused modules?**
  _Cohesion score 0.07966101694915254 - nodes in this community are weakly interconnected._