# Master Data + Session Matching (High-Level)

This view separates:
- long-lived **master data** (ABN/government-centered truth), and
- per-run **session matching** (user-specific top companies/contacts).

```mermaid
flowchart TD
    subgraph Ingestion["Master Data Ingestion (Continuous)"]
      A1[ABR / ASIC Sources]
      A2[VC / Jobs / News Sources]
      A3[Normalize + Merge by ABN]
      A4[Company Intelligence Scoring]
      A5[(companies)]
      A6[(signals)]
      A1 --> A3
      A2 --> A3
      A3 --> A4 --> A5
      A4 --> A6
    end

    subgraph Session["User Session Matching (On Demand)"]
      B1[UI User Input]
      B2[Normalize user_input]
      B3[(sessions)]
      B4[Filter + Match from companies]
      B5[Session Ranking]
      B6[Create Contact Stubs / Match Contacts]
      B7[(session_company_matches)]
      B8[(session_contact_matches)]
      B1 --> B2 --> B3
      B3 --> B4 --> B5 --> B6
      B5 --> B7
      B6 --> B8
    end

    A5 --> B4
    A6 --> B4

    subgraph Activation["Activation Layer"]
      C1[Top 10 Companies]
      C2[Top 10 Contacts]
      C3[Alerts / Outreach]
    end

    B7 --> C1
    B8 --> C2
    C1 --> C3
    C2 --> C3
```

## Why this shape works

1. `companies` and `signals` stay as canonical truth keyed by ABN.
2. Each user run creates its own `sessions` + match tables without corrupting master data.
3. You can re-rank quickly from existing master records instead of re-ingesting everything each session.
4. The UI can show personalized results while keeping provenance and audit trail.
