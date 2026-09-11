# SDD Specificaties (Specification-Driven Development)

## 1. Datamodellen (Types & Schema's)

### `ReportItem`
```typescript
interface ReportItem {
  id: string;                      // unieke uuid
  title: string;                   // Korte titel / samenvatting
  rawDefectHint: string;           // Korte beschrijving door gebruiker
  fullReportText: string;          // Gegenereerde tekst (max 2000 chars)
  impactedGroups: ('voetgangers' | 'fietsers' | 'openbaar_vervoer' | 'gemotoriseerd')[];
  photos: {
    filename: string;
    sizeBytes: number;
    base64Data?: string;
    url?: string;
    originalSize: number;
    compressedSize: number;
    gps?: {
      latitude: number;
      longitude: number;
      accuracy?: number;
    };
    timestamp?: string;
  }[];
  location: {
    latitude: number;
    longitude: number;
    address?: string;
    municipality?: string;
    hasGps: boolean;
  };
  contactInfo: {
    firstName: string;             // 'Aldo'
    lastName: string;              // 'Fieuw'
    email: string;                 // 'aldo.fieuw@gmail.com'
    wantsResponse: boolean;        // true
  };
  submissionStatus: 'concept' | 'verzenden' | 'ingediend' | 'bevestigd' | 'in_behandeling' | 'doorgestuurd' | 'opgelost' | 'afgewezen';
  trackingCode?: string;           // Dossiernummer / behandelingscode van AWV (bv. MWV-2026-84920)
  submissionDate?: string;
  lastUpdatedDate: string;
  lastReminderSentDate?: string;
  assignedAuthority?: string;      // e.g. 'AWV District', 'Gemeentelijke Dienst'
  emails: EmailCorrespondence[];
  automationLogs: {
    timestamp: string;
    step: string;
    message: string;
    success: boolean;
  }[];
}

interface EmailCorrespondence {
  id: string;
  messageId?: string;
  date: string;
  from: string;
  to: string;
  subject: string;
  body: string;
  matchedReportId?: string;
  matchScore: number;              // 0 to 1
  isReply: boolean;
  statusUpdate?: 'in_behandeling' | 'doorgestuurd' | 'opgelost' | 'afgewezen';
  extractedTrackingCode?: string;
}
```

## 2. MeldpuntWegen.be Stappen & Protocol

1. **reCAPTCHA Solver**:
   - Gebruik Buster / Speech-to-Text audio challenge solver fallback specs.
2. **Coördinaten Mapping**:
   - Conversie van WGS84 GPS (Lat/Lng) naar Vlaamse Lambert 72 / Kaartpin coördinaten.
   - Reverse geocoding via OpenStreetMap Nominatim / Geopunt Vlaanderen API.
3. **FAQ Skipper**:
   - Detectie van 'Veelgestelde vragen' tussenstap; automatisch doorsturen indien aanwezig.
4. **Beelden & 2.5MB Limiet**:
   - Client & Server canvas resize / JPEG quality reduceer indien `filesize > 2.5MB`.
5. **Formulierpayload**:
   - Validatie van verplichte contactgegevens (Aldo Fieuw, email, vinkje).
   - Validatie van tekstlengte (`<= 2000` tekens).

## 3. Fuzzy E-mail Matching Algoritme
- Inkomende e-mails van AWV herhalen vaak de gemelde tekst, soms met afwijkende witregels of linebreaks.
- Algoritme:
  1. Verwijder alle regeleinden (`\r\n`, `\n`), dubbele spaties, leestekens.
  2. Normaliseer naar kleine letters (lowercase).
  3. Bepaal de langste gemeenschappelijke substring of N-gram overlap ratio.
  4. Extraheer eventueel dossiernummer (`MWV-\d+` of `Dossier:\s*([A-Z0-9-]+)`).
  5. Koppel automatisch aan het juiste dossier en markeer als geverifieerd.
