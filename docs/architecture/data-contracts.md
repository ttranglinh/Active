# Data Contracts (Sprint 1)

This document defines the minimum data contracts required to ship Sprint 1:
`user input -> company shortlist -> contact stubs -> unlock -> export`.

## Contract Rules

1. All timestamps use ISO 8601 UTC.
2. IDs are opaque strings and must be stable once issued.
3. Producers must not silently drop required fields.
4. Consumers must ignore unknown fields for forward compatibility.

## Column Metadata Standard

Each field should be documented with:
- `Type`: scalar/list/object and nullability
- `Required`: yes/no
- `Source`: UI, parser, pipeline, API, derived
- `Owner Module`: module responsible for truth
- `PII`: none/low/high
- `Validation`: key rules
- `Description`: business meaning

---

## 1) UserInputContract

Purpose: normalize UI/session input into a deterministic backend payload.

### Required fields

- `input_id`: string
- `created_at_utc`: string (ISO datetime)
- `market`: string
- `services`: string[]
- `firmographic.industries`: string[]
- `firmographic.headcount_ranges`: string[]
- `firmographic.regions`: string[]
- `firmographic.revenue_ranges`: string[]
- `icp.company_types`: string[]
- `icp.personas`: string[]
- `icp.seniority`: string[]
- `signals`: string[]
- `notes`: string

### Field metadata

| Field | Type | Required | Source | Owner Module | PII | Validation | Description |
|---|---|---|---|---|---|---|---|
| `input_id` | string | Yes | backend/session | `user_input` | none | non-empty, stable | unique input payload id |
| `created_at_utc` | datetime string | Yes | backend | `user_input` | none | valid ISO-8601 UTC | input creation timestamp |
| `market` | string | Yes | UI | `user_input` | none | non-empty | primary country/market |
| `services` | string[] | Yes | UI | `user_input` | none | trim+dedupe | offered services/capabilities |
| `firmographic.industries` | string[] | Yes | UI | `user_input` | none | trim+dedupe | target industries |
| `firmographic.headcount_ranges` | string[] | Yes | UI | `user_input` | none | allowed enum list | company size bands |
| `firmographic.regions` | string[] | Yes | UI | `user_input` | none | trim+dedupe | target geographies |
| `firmographic.revenue_ranges` | string[] | Yes | UI | `user_input` | none | optional enum | target revenue bands |
| `icp.company_types` | string[] | Yes | UI | `user_input` | none | trim+dedupe | company type tags |
| `icp.personas` | string[] | Yes | UI | `user_input` | none | trim+dedupe | target job roles |
| `icp.seniority` | string[] | Yes | UI | `user_input` | none | allowed enum list | target seniority levels |
| `signals` | string[] | Yes | UI | `user_input` | none | trim+dedupe | activity signals to prioritize |
| `notes` | string | Yes | UI | `user_input` | low | max length enforced | free-text context/value prop |

### Validation rules

- arrays must be trimmed and deduplicated
- `icp.seniority` allowed values:
  - `Intern`, `Entry/Junior`, `Manager`, `Senior/Lead`, `Director`, `Executive`, `CXO`, `Owner/Partner`
- `firmographic.headcount_ranges` allowed values:
  - `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5001-10000`, `10001+`

### Example

```json
{
  "input_id": "session_s_20260217T040525Z_d28ded62",
  "created_at_utc": "2026-02-17T04:05:25.054928Z",
  "market": "Australia",
  "services": ["B2B Lead Generation"],
  "firmographic": {
    "industries": ["SaaS"],
    "headcount_ranges": ["1-10", "11-50"],
    "regions": ["Sydney", "Melbourne"],
    "revenue_ranges": []
  },
  "icp": {
    "company_types": [],
    "personas": ["Sales Development Representative", "Business Development Representative"],
    "seniority": ["Manager", "Director", "Executive"]
  },
  "signals": ["LinkedIn Activity", "Hiring Signal"],
  "notes": "We help find qualified leads for SaaS services."
}
```

---

## 2) CompanyRecordContract

Purpose: company intelligence output consumed by search index and result list UI.

### Required fields

- `company_id`: string
- `name`: string
- `domain`: string or null
- `location`: string
- `industry`: string
- `headcount_range`: string or null
- `signal_score`: number (0 to 100)
- `signal_summary`: string[]
- `source_refs`: string[]
- `updated_at_utc`: string (ISO datetime)

### Field metadata

| Field | Type | Required | Source | Owner Module | PII | Validation | Description |
|---|---|---|---|---|---|---|---|
| `company_id` | string | Yes | pipeline/db | `company_intelligence` | none | unique | canonical company key (ABN/domain-based) |
| `name` | string | Yes | pipeline/db | `company_intelligence` | none | non-empty | company display name |
| `domain` | string/null | Yes | pipeline | `company_intelligence` | none | valid domain when present | company website domain |
| `location` | string | Yes | pipeline | `company_intelligence` | none | normalized state/city | primary location |
| `industry` | string | Yes | pipeline | `company_intelligence` | none | normalized label | industry category |
| `headcount_range` | string/null | Yes | pipeline | `company_intelligence` | none | allowed enum if present | employee band |
| `signal_score` | number | Yes | derived | `company_intelligence` | none | 0..100 | composite growth/activity score |
| `signal_summary` | string[] | Yes | derived | `company_intelligence` | none | non-empty array preferred | top signal explanations |
| `source_refs` | string[] | Yes | pipeline | `company_intelligence` | none | traceable ids/urls | provenance pointers |
| `updated_at_utc` | datetime string | Yes | backend | `company_intelligence` | none | valid ISO-8601 UTC | last update time |

### Validation rules

- `signal_score` must be in range `[0,100]`
- `company_id` must be unique in result set

### Example

```json
{
  "company_id": "abn_80168860356",
  "name": "Acme SaaS Pty Ltd",
  "domain": "acme.io",
  "location": "Sydney",
  "industry": "SaaS",
  "headcount_range": "11-50",
  "signal_score": 78,
  "signal_summary": [
    "Hiring 4 GTM roles in last 30 days",
    "Series A raised 5 months ago"
  ],
  "source_refs": [
    "seek_jobs_snapshot_2026-02-14",
    "dealroom_snapshot_2026-02-01"
  ],
  "updated_at_utc": "2026-02-18T02:11:00Z"
}
```

---

## 3) ContactStubContract

Purpose: free pre-unlock contact visibility (name/title/LinkedIn) tied to company records.

### Required fields

- `contact_id`: string
- `company_id`: string
- `full_name`: string
- `title`: string
- `seniority`: string
- `linkedin_url`: string
- `is_stub_only`: boolean
- `stub_source`: string
- `last_verified_at_utc`: string or null

### Field metadata

| Field | Type | Required | Source | Owner Module | PII | Validation | Description |
|---|---|---|---|---|---|---|---|
| `contact_id` | string | Yes | backend/db | `contact_pipeline` | low | unique | canonical contact key |
| `company_id` | string | Yes | linkage | `contact_pipeline` | none | must reference company | parent company |
| `full_name` | string | Yes | scrape/api | `contact_pipeline` | high | non-empty | contact full name |
| `title` | string | Yes | scrape/api | `contact_pipeline` | low | normalized casing | role title |
| `seniority` | string | Yes | derived | `contact_pipeline` | none | allowed enum | normalized seniority bucket |
| `linkedin_url` | string | Yes | scrape/api | `contact_pipeline` | low | linkedin /in URL format | unique public profile URL |
| `is_stub_only` | boolean | Yes | system | `contact_pipeline` | none | must be true in stub stage | indicates pre-enrichment state |
| `stub_source` | string | Yes | pipeline | `contact_pipeline` | none | allowed enum | source system for stub |
| `last_verified_at_utc` | datetime string/null | Yes | system | `contact_pipeline` | none | ISO-8601 if present | last enrichment verification |

### Validation rules

- `is_stub_only` must be `true` for stub records
- `linkedin_url` must start with `https://www.linkedin.com/in/` or `https://linkedin.com/in/`
- dedupe key priority: `linkedin_url`, fallback `full_name + company_id`
- `stub_source` allowed values:
  - `startmate`, `vc_portfolio`, `website`, `github`, `news`, `apify`

### Example

```json
{
  "contact_id": "ct_01JABYQ9WJ8Q9P3K9T",
  "company_id": "abn_80168860356",
  "full_name": "Jane Smith",
  "title": "Head of Sales",
  "seniority": "Director",
  "linkedin_url": "https://www.linkedin.com/in/jane-smith",
  "is_stub_only": true,
  "stub_source": "apify",
  "last_verified_at_utc": null
}
```

---

## 4) UnlockResultContract

Purpose: unlock response after enrichment waterfall and credit logic.

### Required fields

- `contact_id`: string
- `company_id`: string
- `email_work`: string or null
- `email_status`: string or null
- `mobile`: string or null
- `mobile_status`: string or null
- `enriched_source`: string or null
- `is_stub_only`: boolean
- `why_contact_now`: string or null
- `credits_charged`: integer
- `latency_ms`: integer

### Field metadata

| Field | Type | Required | Source | Owner Module | PII | Validation | Description |
|---|---|---|---|---|---|---|---|
| `contact_id` | string | Yes | backend/db | `contact_pipeline` | low | must exist | unlocked contact id |
| `company_id` | string | Yes | backend/db | `contact_pipeline` | none | must reference company | parent company id |
| `email_work` | string/null | Yes | enrichment API | `contact_pipeline` | high | valid email when present | revealed work email |
| `email_status` | string/null | Yes | verifier | `contact_pipeline` | none | allowed enum | deliverability status |
| `mobile` | string/null | Yes | enrichment API | `contact_pipeline` | high | E.164 when present | revealed mobile number |
| `mobile_status` | string/null | Yes | verifier | `contact_pipeline` | none | enum/open value | mobile verification state |
| `enriched_source` | string/null | Yes | system | `contact_pipeline` | none | allowed enum | winning enrichment source |
| `is_stub_only` | boolean | Yes | system | `contact_pipeline` | none | false on successful unlock | post-unlock state flag |
| `why_contact_now` | string/null | Yes | AI/derived | `company_intelligence` | none | max length enforced | one-line action context |
| `credits_charged` | integer | Yes | billing | `billing` | none | >= 0 | credit debit amount |
| `latency_ms` | integer | Yes | system | `contact_pipeline` | none | >= 0 | end-to-end unlock latency |

### Validation rules

- if no contact method is enriched, `credits_charged = 0`
- if enriched from cache, `enriched_source = "cache"`
- `email_status` allowed values:
  - `deliverable`, `risky`, `undeliverable`, `unknown`, null
- `enriched_source` allowed values:
  - `apify`, `hunter`, `pdl`, `cache`, `contributor`, null

### Example

```json
{
  "contact_id": "ct_01JABYQ9WJ8Q9P3K9T",
  "company_id": "abn_80168860356",
  "email_work": "jane@acme.io",
  "email_status": "deliverable",
  "mobile": null,
  "mobile_status": null,
  "enriched_source": "hunter",
  "is_stub_only": false,
  "why_contact_now": "Acme has opened 4 GTM roles in 30 days and is likely evaluating outbound tooling.",
  "credits_charged": 1,
  "latency_ms": 1820
}
```

---

## Sprint 1 Contract Checklist

- [ ] `UserInputContract` validated at session save
- [ ] `CompanyRecordContract` validated before indexing
- [ ] `ContactStubContract` validated before upsert
- [ ] `UnlockResultContract` validated before API response
- [ ] Contract tests added under `tests/contract/`
