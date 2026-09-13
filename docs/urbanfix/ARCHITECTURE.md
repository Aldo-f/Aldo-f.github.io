# Architecture Overview

```mermaid
flowchart LR
    UI[UI (React Frontend)] --> API[API (Express)]
    API --> AI[AI Service]
    AI --> Provider[Provider (Gemini / etc.)]
    AI --> Storage[Storage (JSON/SQLite)]
    API --> Meldpunt[Meldpunt Integration]
    Meldpunt --> Email[Email Service]
    Storage --> Meldpunt
```

*Data flows from the UI to the backend API, which delegates to the AI service. The AI service talks to the external provider and stores results. The API also interacts with the Meldpunt integration, which sends notifications via the Email service.*
