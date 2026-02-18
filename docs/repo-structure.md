# Active Repo Structure (Modular Monolith)

This repo is a **modular monolith**: one deployment, clear domain modules.

## Why This Structure

1. **Domain-first design**: module boundaries follow Active product capabilities, not technical layers.
2. **Fast iteration**: one runtime and one database keep early-stage delivery simple.
3. **Clear ownership**: each module owns its models, workflows, and integrations.
4. **Public-repo clarity**: architecture mirrors PRD and data pipeline docs, easy for reviewers to understand.
5. **Future flexibility**: modules can be extracted to services later if scale requires it.

## Current Target Layout

```txt
active/
├── apps/
│   └── web/                            # Frontend app
├── config/
│   ├── apify_linkedin_profile_search_template.json
│   └── mappings/
├── data/
│   ├── raw/                            # Raw pipeline artifacts (gitignored)
│   ├── processed/                      # Processed artifacts (gitignored)
│   └── sessions/                       # Session inputs/runs (gitignored)
├── docs/
│   ├── architecture/
│   │   ├── adr/
│   │   └── context-map.md
│   └── flows/
├── scripts/
├── src/
│   ├── app/                            # Bootstrap, config, API assembly
│   ├── modules/
│   │   ├── user_input/                 # Input capture, parsing, normalization
│   │   ├── company_intelligence/       # Company ingestion + signal logic
│   │   ├── contact_pipeline/           # Stub pipeline + unlock enrichment
│   │   ├── search_index/               # Typesense sync/query capabilities
│   │   ├── contributor_system/         # Credits, verification, reputation
│   │   ├── billing/                    # Plans, credit packs, Stripe flows
│   │   └── outreach_loop/              # Lists/export/CRM/outreach workflows
│   └── shared/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── e2e/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Module Ownership

### `src/modules/user_input`
- Owns user intent capture from UI and Quick Hit style parsing into normalized search specs.
- Reason: input schema and UX evolve quickly and should not leak into ingestion logic.

### `src/modules/company_intelligence`
- Owns company-level ingestion and signal computation (ABR/ASIC/VC/jobs/news/stack).
- Reason: this is the core ranking intelligence and changes with data-source strategy.

### `src/modules/contact_pipeline`
- Owns contact stub prefetch and unlock-time enrichment waterfall.
- Reason: provider costs and enrichment quality tuning need isolated control.

### `src/modules/search_index`
- Owns sync and query logic for Typesense.
- Reason: search performance/relevance tuning should be independent from source ingestion.

### `src/modules/contributor_system`
- Owns contributor actions, reward rules, and score updates.
- Reason: this is a distinct product flywheel with fast iteration on incentives.

### `src/modules/billing`
- Owns plans, credit transactions, and payment webhooks.
- Reason: billing/compliance has separate risk and should stay isolated from product logic.

### `src/modules/outreach_loop`
- Owns list/export and future CRM/outreach integrations.
- Reason: this capability can evolve independently and is rollout-phase dependent.

## Boundary Rules

1. Cross-module calls should go through each module's `api/` interface.
2. Avoid importing another module's `domain/`, `application/`, or `infrastructure/` directly.
3. Keep `src/shared/` small and generic (events, logging, utilities).
4. Raw/processed/session data is local artifact storage and not source control.
