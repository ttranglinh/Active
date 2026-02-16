# Active Repo Structure (Modular Monolith)

This repository uses a **modular monolith** design: one codebase and one deployable app, but separated into business-capability modules.

## Why This Design

1. **Architecture-aligned boundaries**
   Your modules map directly to `docs/visual-architecture.md` layers (Input, Ingestion, Intelligence, Storage, Activation), so design and code stay consistent.

2. **Faster iteration with lower ops overhead**
   You get microservice-like separation without distributed-system complexity (service discovery, network retries, cross-service auth).

3. **Safer refactors**
   Each module exposes a public API; internals can change without breaking the rest of the app.

4. **Clear data ownership**
   Raw ingestion data, processed intelligence outputs, and canonical lead records have explicit owners, reducing schema drift and coupling.

5. **Incremental path to microservices (if needed later)**
   If scale requires it, a module can be extracted because contracts already exist.

## Target Structure

```txt
active/
+-- .github/                         # CI/CD pipelines (GitHub Actions)
+-- docs/                            # Architecture, ADRs, operating playbooks
+-- data/                            # Local/dev data artifacts
¦   +-- raw/                         # Immutable ingestion payloads
¦   ¦   +-- linkedin/
¦   ¦       +-- profiles/
¦   +-- processed/                   # Enriched/normalized/scored outputs
+-- scripts/                         # One-off jobs and local runners
+-- src/
¦   +-- app/                         # App bootstrap and wiring
¦   ¦   +-- main.py
¦   ¦   +-- config.py
¦   ¦   +-- container.py
¦   +-- modules/
¦   ¦   +-- input_capture/           # Offer/Firmographic/Persona/Signal intake
¦   ¦   ¦   +-- domain/
¦   ¦   ¦   +-- application/
¦   ¦   ¦   +-- infrastructure/
¦   ¦   ¦   +-- api/
¦   ¦   +-- ingestion/               # Serper, Bright Data, manual triggers
¦   ¦   ¦   +-- domain/
¦   ¦   ¦   +-- application/
¦   ¦   ¦   +-- infrastructure/
¦   ¦   ¦   +-- api/
¦   ¦   +-- intelligence/            # Orchestration, scoring, recommendations
¦   ¦   ¦   +-- domain/
¦   ¦   ¦   +-- application/
¦   ¦   ¦   +-- infrastructure/
¦   ¦   ¦   +-- api/
¦   ¦   +-- lead_store/              # Canonical lead model + persistence
¦   ¦   ¦   +-- domain/
¦   ¦   ¦   +-- application/
¦   ¦   ¦   +-- infrastructure/
¦   ¦   ¦   +-- api/
¦   ¦   +-- activation/              # Alerts, outreach, reporting outputs
¦   ¦       +-- domain/
¦   ¦       +-- application/
¦   ¦       +-- infrastructure/
¦   ¦       +-- api/
¦   +-- shared/                      # Minimal shared kernel only
¦       +-- events/
¦       +-- logging/
¦       +-- utils/
+-- tests/
¦   +-- unit/
¦   +-- integration/
¦   +-- contract/
+-- pyproject.toml
+-- README.md
```

## Module Responsibilities and Reasons

### `modules/input_capture`
- Owns validation of user inputs: services, firmographic filters, ICP, and signals.
- Reason: input rules evolve frequently and should not be mixed with scraping or scoring logic.

### `modules/ingestion`
- Owns external source collection (Serper search, LinkedIn URL extraction, Bright Data profile scraping, manual URL intake).
- Writes only to `data/raw/...`.
- Reason: keeps external API volatility isolated to one module and preserves immutable source data.

### `modules/intelligence`
- Owns orchestration from raw data to scored candidates.
- Writes processed/scoring artifacts to `data/processed/...`.
- Reason: recommendation logic and ranking experiments can move fast without touching ingestion adapters.

### `modules/lead_store`
- Owns canonical lead schema and repository interfaces.
- Reason: one source of truth prevents every module from defining its own lead format.

### `modules/activation`
- Owns outbound use cases: alerting, CRM sync payloads, reporting views.
- Reason: delivery channels change often and should not impact upstream ingestion/intelligence.

## Contract Rules (Critical for Modular Monolith)

1. A module can import another module only through its `api/` package.
2. Direct imports into another module's `domain/`, `application/`, or `infrastructure/` are not allowed.
3. `shared/` must stay small and generic (events, logging primitives, cross-cutting helpers only).
4. Raw data is append-only and never edited in place.

Reason: these rules preserve module boundaries so the monolith does not collapse into a tightly coupled codebase.

## Event-Driven Flow Inside the Monolith

Use internal domain events for cross-module coordination:
- `ProfilesCollected`
- `CandidatesScored`
- `LeadsReadyForActivation`

Reason: events reduce hard dependencies while keeping everything in one runtime.

## Mapping From Current Structure

- `src/ingestion` -> `src/modules/ingestion`
- `src/brain` -> `src/modules/intelligence`
- `src/core` -> `src/modules/input_capture`
- `src/activation` -> `src/modules/activation`
- Add new `src/modules/lead_store`
- Add new `src/app` and `src/shared`

Reason: this keeps your current work recognizable while introducing stronger boundaries.

## Practical Benefits for Active (Now)

1. You can ship ingestion quickly while intelligence is still evolving.
2. Bright Data or Serper API changes stay localized in `modules/ingestion`.
3. Scoring experiments can be versioned in `modules/intelligence` without breaking collection.
4. Activation channels (email, CRM, dashboards) can be added independently.

## Practical Benefits for Active (Later)

1. Easier onboarding: new contributors can own one module.
2. Cleaner testing: unit tests by module + contract tests for module APIs.
3. Easier scale decisions: extract only bottleneck modules if needed.
