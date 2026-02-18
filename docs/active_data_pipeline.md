# Active — Data Pipeline
**End to End: Raw Extraction → Normalisation → Database → Search Index → Signal Scoring → Contact Stub Pre-fetch → On-Demand Email Enrichment → Contributor Loop**

> **Company -> Contact Model: Hybrid**
> Free sources pre-populate contact stubs (name + title + LinkedIn URL) at pipeline time. Paid APIs (Apify → Hunter → PDL) only fire when a user clicks Unlock to reveal email and mobile. Zero paid contact cost until actual user demand.

---

## Full Pipeline Flow

```
── COMPANY DATA ──────────────────────────────────────────────────────────────

Gov Registries       ──  Download / Scrape  ──→  Raw Files
VC Portfolio Pages   ──  Python Scraper     ──→  Raw HTML
Job Boards           ──  Domain Scrape      ──→  Role Count
News RSS             ──  Feed Parser        ──→  Headlines
                                                    │
                                              Python Cleaner
                                                    │
                                                    ▼
                                          Normalised Records
                                                    │
                                           UPSERT on ABN
                                                    │
                                                    ▼
                                              PostgreSQL  ←──────────────────┐
                                           ┌──────┴──────┐                   │
                                   Realtime Webhook   Weekly Cron            │
                                           │               │                 │
                                           ▼               ▼                 │
                                     Typesense         Signal Score          │
                                       Index                                 │

── CONTACT STUBS (Model C — free sources, pipeline time) ─────────────────────

Startmate cohort pages   ──┐
VC portfolio team pages  ──┤
Company /about pages     ──┼──  Python Scraper  ──→  name + title + +                                                    linkedin_url          
GitHub (AU location)     ──┤
Google News bylines/
(X-Ray Search)           ──┘
                                                    │
                                         Stub Normalisation
                                   (dedup on linkedin_url / full_name + ABN)
                                                    │
                                                    ▼
                                    contacts table (is_stub_only = true)
                                    email_work = NULL  mobile = NULL         │
                                                                             │
── ON-DEMAND EMAIL ENRICHMENT (at user unlock) ───────────────────────────────

User clicks Unlock
       │
       ▼
Cache check (is_stub_only = false AND last_verified < 30d?)
       │ hit → return immediately, no API call
       │ miss ↓
Apify (linkedin_url → email attempt)  ~$0.02/call
       │ found → skip to Hunter verify
       │ miss ↓
Hunter domain search (company domain → email pattern)  ~$0.03/call
       │ found → skip to verify
       │ miss ↓
PDL full lookup (name + domain)  ~$0.05–0.15/call
       │
       ▼
Hunter verify (email_status: deliverable / risky / undeliverable / unknown)
       │
       ▼
OpenAI model → "Why contact now" note  ~$0.001/call
       │
       ▼
Write enriched contact → contacts table (is_stub_only = false) ─────────────┘
Deduct 1 credit → credit_transactions

── CONTRIBUTOR LOOP (continuous) ─────────────────────────────────────────────

User Corrections  ──  Contributor Loop  ──→  Data Quality++  ──→  PostgreSQL
```

---

## Phase 1 ⛏ — Raw Data Extraction
**Timing:** Scheduled (weekly / quarterly)

Raw data pulled from government registries, public web sources, and APIs. Nothing is stored yet — this is pure collection.

### Data Sources

#### ABR Bulk Extract
| Field | Detail |
|---|---|
| **Type** | Government |
| **Cost** | $0 |
| **How** | Download ZIP from data.gov.au → parse XML → ~3M AU business records |
| **Output** | ABN, entity name, type, status, address, GST status |
| **Frequency** | Quarterly |
| **Risk** | Low |

#### ASIC Company Registry
| Field | Detail |
|---|---|
| **Type** | Government |
| **Cost** | $0 |
| **How** | Python scraper on ASIC search — targets active Pty Ltd companies |
| **Output** | Company type, incorporation date, director names |
| **Frequency** | Monthly |
| **Risk** | Low |

#### ACMA DNC Register
| Field | Detail |
|---|---|
| **Type** | Government |
| **Cost** | $0 |
| **How** | Download CSV from acma.gov.au — wash against phone numbers |
| **Output** | Phone numbers on Do Not Call register |
| **Frequency** | Monthly |
| **Risk** | Low |

#### AU VC Portfolio Pages
| Field | Detail |
|---|---|
| **Type** | Web Scrape |
| **Cost** | $0 |
| **How** | Python scraper on Blackbird, AirTree, Square Peg, Folklore, Apex, Main Sequence portfolio pages |
| **Output** | Company name, investor, rough stage, founding year |
| **Frequency** | Quarterly |
| **Risk** | Low |

#### Seek / Indeed Job Postings
| Field | Detail |
|---|---|
| **Type** | Web Scrape |
| **Cost** | $0 |
| **How** | Domain-based scrape — count open roles per company domain |
| **Output** | Open role count, role categories, seniority, date posted |
| **Frequency** | Weekly |
| **Risk** | Medium |

#### Google News RSS
| Field | Detail |
|---|---|
| **Type** | RSS Feed |
| **Cost** | $0 |
| **How** | RSS query per company name — parse titles and dates |
| **Output** | News headline, date, source URL, category |
| **Frequency** | Weekly |
| **Risk** | Low |

#### Wappalyzer (open source)
| Field | Detail |
|---|---|
| **Type** | API / Library |
| **Cost** | $0 (Phase 1) / paid Phase 2 |
| **How** | Run against company website URLs — detect tech stack |
| **Output** | CRM, marketing tools, infrastructure, analytics stack |
| **Frequency** | Quarterly |
| **Risk** | Low |

---

### Contact Stub Sources (Prioritise free sources)

These sources populate the `contacts` table with name + title + LinkedIn URL **before any user pays a credit**. Email and mobile remain NULL until unlock.

#### Startmate Cohort Pages
| Field | Detail |
|---|---|
| **Type** | Web Scrape |
| **Cost** | $0 |
| **How** | Python scraper on all public Startmate batch pages — each lists founders with name, company, LinkedIn |
| **Output** | full_name, company, linkedin_url, cohort year |
| **Frequency** | Quarterly |
| **Risk** | Low |

#### VC Portfolio Team Pages
| Field | Detail |
|---|---|
| **Type** | Web Scrape |
| **Cost** | $0 |
| **How** | Python scraper on team/about subpages of top 200 AU startups by Signal Score (where publicly listed) |
| **Output** | full_name, title, linkedin_url, company |
| **Frequency** | Quarterly |
| **Risk** | Low |

#### Company /about and /team Pages
| Field | Detail |
|---|---|
| **Type** | Web Scrape |
| **Cost** | $0 |
| **How** | Scrape `{company_domain}/about`, `/team`, `/people` for staff listings — common pattern in AU tech startups |
| **Output** | full_name, title, linkedin_url (if linked) |
| **Frequency** | Quarterly per company |
| **Risk** | Low |

#### GitHub (AU location filter)
| Field | Detail |
|---|---|
| **Type** | API |
| **Cost** | $0 (GitHub public API, 5K req/hr authenticated) |
| **How** | GitHub API: `location:Australia` + company name filter → extract profile, bio, company field, public email |
| **Output** | full_name, github_username, public_email (if set), company, linkedin_url (if in bio) |
| **Frequency** | Quarterly |
| **Risk** | Low |

#### Google News Bylines
| Field | Detail |
|---|---|
| **Type** | RSS Feed |
| **Cost** | $0 |
| **How** | Parse bylines from news articles mentioning AU startups — extract quoted founder/exec names and titles |
| **Output** | full_name, title, company, article_source |
| **Frequency** | Weekly (alongside news signal scrape) |
| **Risk** | Low |

---

## Phase 2 ⚙ — Processing & Normalisation
**Timing:** Runs immediately after extraction

Raw data is messy, inconsistent, and duplicated. This phase cleans, deduplicates, standardises, and links records before anything touches the database.

### Steps

**1. Deduplication**
ABN is the canonical primary key. All records keyed to ABN — prevents the same company appearing twice under different names (e.g. `Canva Pty Ltd` vs `Canva`).
> Tool: Python — pandas dedupe on ABN

**2. Entity Resolution**
Link ASIC company record → ABR ABN record → VC portfolio entry → job posting domain → news RSS result. All joined on ABN or normalised company domain (`canva.com` → `Canva Pty Ltd` → ABN `80168860356`).
> Tool: Python — fuzzy domain matching + ABN lookup

**3. Field Standardisation**
State codes normalised (NSW/VIC/QLD), phone numbers E.164 format, industry codes mapped to ANZSIC standard, seniority titles normalised (`VP of Sales` → `VP`), headcount strings mapped to ranges.
> Tool: Python — regex + lookup tables

**4. DNC Flag Application**
Every phone number cross-referenced against ACMA DNC register. `dnc_flag = true` set on matching contacts. This runs after every DNC register refresh.
> Tool: Python — set intersection on phone numbers

**5. VC-Backed Flag**
Companies found in VC portfolio scrape tagged `vc_backed = true`, `investor_names[]` populated. ABN cross-reference used where possible; domain matching as fallback.
> Tool: Python — domain + name matching

**6. Data Quality Score**
Each company record gets a `data_quality_score` (0–100) based on field completeness: +20 for verified email, +15 for ABN confirmed active, +15 for website URL, +10 for LinkedIn URL, etc. Used to surface reliable records first.
> Tool: Python — weighted field completeness formula

**7. Contact Stub Deduplication**
Contact stubs collected from multiple free sources may overlap (same person appearing on Startmate page AND company /team page). Deduplicate on `linkedin_url` first (exact match), then fall back to `full_name + company_abn` fuzzy match. Winner record merges best fields from all sources.
> Tool: Python — pandas dedupe on `linkedin_url`, fuzzy match fallback

**8. Contact–Company Linking**
Each stub must be linked to a `company_abn`. Use company domain from the scrape source to look up `companies.website_url` → resolve to ABN. Stubs with no resolvable ABN are held in a staging table for manual review or discarded.
> Tool: Python — domain → ABN lookup against companies table

**9. Stub Seniority Classification**
Normalise raw titles into seniority buckets for search filtering: `CEO / CTO / CFO / COO` → C-Suite, `VP *` → VP, `Head of *` → Director, `Senior * / Lead *` → Manager, everything else → IC.
> Tool: Python — regex pattern matching against title field

---

## Phase 3 🗄 — Database Write (Supabase)
**Timing:** After processing completes

Clean, normalised records are upserted into PostgreSQL via Supabase. ABN is the primary key so re-running the pipeline never creates duplicates — it only updates changed fields.

### Tables

#### `companies`
**Primary Key:** `ABN`

**Key Fields:**
`entity_name` · `trading_name` · `entity_type` · `status` · `state` · `suburb` · `industry_anzsic` · `employee_range` · `website_url` · `linkedin_url` · `vc_backed` · `investor_names[]` · `funding_stage` · `last_funding_date` · `funding_amount` · `tech_stack[]` · `signal_score` · `dnc_flag` · `data_quality_score`

| | |
|---|---|
| **Written by** | ABR pipeline, ASIC scraper, VC portfolio scraper |
| **Update strategy** | UPSERT on ABN — only changed fields overwritten |

---

#### `signals`
**Primary Key:** `signal_id (UUID)`

**Key Fields:**
`company_abn (FK)` · `signal_type` · `signal_value (JSON)` · `signal_date` · `source_url`

| | |
|---|---|
| **Written by** | Job scraper, News RSS, Funding ingestion, Leadership change detector |
| **Update strategy** | INSERT only — new row per signal event. Never overwrite history. |

---

#### `contacts`
**Primary Key:** `contact_id (UUID)`

**Stub fields** — populated at pipeline time from free sources, always visible:
`company_abn (FK)` · `first_name` · `last_name` · `full_name` · `title` · `department` · `seniority` · `linkedin_url` · `stub_source`

**Enriched fields** — populated at unlock time from paid APIs, revealed after credit spend:
`email_work` · `email_status` · `mobile` · `mobile_status` · `enriched_source`

**State flags:**
`is_stub_only` — `true` until email is unlocked. Controls what the frontend blurs vs. shows.
`last_verified_at` — timestamp of last paid enrichment. Drives 30-day cache logic.

```sql
CREATE TABLE contacts (
  contact_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_abn       TEXT REFERENCES companies(abn),

  -- Stub fields (free sources, pipeline time)
  first_name        TEXT,
  last_name         TEXT,
  full_name         TEXT,
  title             TEXT,
  department        TEXT,
  seniority         TEXT,   -- C-Suite / VP / Director / Manager / IC
  linkedin_url      TEXT,
  stub_source       TEXT,   -- 'startmate' / 'vc_portfolio' / 'website' / 'github' / 'news'

  -- Enriched fields (paid APIs, unlock time)
  email_work        TEXT,
  email_status      TEXT,   -- verified / bounced / catch-all / unknown / NULL
  mobile            TEXT,
  mobile_status     TEXT,
  enriched_source   TEXT,   -- 'proxycurl' / 'hunter' / 'pdl' / 'contributor'

  -- State
  is_stub_only      BOOLEAN DEFAULT true,
  last_verified_at  TIMESTAMP,
  created_at        TIMESTAMP DEFAULT now(),
  updated_at        TIMESTAMP DEFAULT now()
);
```

| | |
|---|---|
| **Stub written by** | Startmate scraper, VC portfolio scraper, company website scraper, GitHub API, news byline parser, X-Ray Search |
| **Enriched written by** | Apify (at unlock), Hunter.io (at unlock), PDL (at unlock fallback), contributor corrections |
| **Stub update strategy** | UPSERT on `linkedin_url` (preferred) or `full_name + company_abn` — pipeline re-runs never duplicate |
| **Enriched update strategy** | UPDATE on `contact_id` when `is_stub_only = true`. Re-enrich if `last_verified_at` > 30 days ago. |

---

#### `contributor_actions`
**Primary Key:** `action_id (UUID)`

**Key Fields:**
`user_id (FK)` · `action_type` · `record_id` · `record_type` · `correction_field` · `old_value` · `new_value` · `credits_awarded`

| | |
|---|---|
| **Written by** | User bounce reports, verification tasks, title corrections |
| **Update strategy** | INSERT only — immutable audit log. Triggers credit award. |

---

## Phase 4 🔍 — Search Index Sync (Typesense)
**Timing:** Triggered by database writes (near real-time)

PostgreSQL is the source of truth but can't do fast faceted search. Every company write triggers a sync to Typesense — a fast, open-source search engine that powers all user-facing queries.

### Sync Steps

1. Supabase Realtime webhook fires on every INSERT or UPDATE to the `companies` table
2. Lightweight sync worker (Supabase Edge Function or Railway cron) receives the change event
3. Denormalised document written to Typesense — all searchable fields in one flat object (no joins at query time)
4. Typesense indexes: full-text on company name, facets on `state` / `industry` / `funding_stage` / `tech_stack`, numeric range on `signal_score` / `headcount` / `funding_amount`
5. User search query hits Typesense directly — sub-100ms response. PostgreSQL never touched for search.
6. Sync lag: seconds to minutes. Acceptable — search results don't need millisecond freshness.

### Typesense Document Fields (Denormalised)

`abn` · `entity_name` · `trading_name` · `state` · `suburb` · `industry_label` · `employee_range` · `signal_score` · `funding_stage` · `last_funding_date` · `funding_amount` · `vc_backed` · `investor_names[]` · `tech_stack[]` · `hiring_role_count` · `dnc_flag` · `data_quality_score` · `contact_stub_count` · `has_ceo_stub` · `has_cto_stub` · `has_vp_sales_stub`

> `contact_stub_count` and seniority flags are denormalised from the `contacts` table at sync time. Enables search filter: "only show companies where a VP Sales contact stub exists."

---

## Phase 5 📊 — Signal Score Computation
**Timing:** Weekly cron job (Sunday night)

Once all raw signals are in the database, a scoring job reads from the `signals` table and computes a composite Signal Score (0–100) for every company. This is what users sort by.

### Formula

```
signal_score = (hiring × 0.30) + (funding × 0.25) + (headcount × 0.20) + (techstack × 0.15) + (news × 0.10)
```

### Score Components

| Component | Weight | Scoring Logic |
|---|---|---|
| **Hiring velocity** | 30% | Count open roles in last 30 days. Score: 0 roles = 0, 1–2 = 20, 3–5 = 50, 6–10 = 80, 10+ = 100. Decays weekly if no new postings. |
| **Funding recency** | 25% | Months since last raise. Score: 0–3mo = 100, 4–6mo = 80, 7–12mo = 60, 13–18mo = 30, 18mo+ = 0. |
| **Headcount growth rate** | 20% | % change over 6 months. Shrinking = 0, Flat = 20, Growing 10–50% = 60, Scaling 50%+ = 100. |
| **Tech stack signals** | 15% | Static score by stack maturity. No CRM detected = 40 (opportunity), Free CRM = 60, Paid CRM = 20 (already bought). |
| **News & web activity** | 10% | News mentions in last 30 days. 0 = 0, 1–2 = 40, 3–5 = 70, 5+ = 100. |

**Output:** `signal_score` written back to `companies` table → triggers Typesense sync → users see updated sort order within minutes.

---

## Phase 6 🔓 — Contact Stub Pre-fetch + On-Demand Email Enrichment
**Timing:** Stub pre-fetch at pipeline time (weekly/quarterly) · Email enrichment real-time at unlock

Model splits contact data into two distinct operations with different cost profiles. Stubs are free and collected during the pipeline run. Emails are paid and only fetched when a user actively requests them.

---

### 6a — Contact Stub Pre-fetch (pipeline time, $0)

Runs as part of the weekly/quarterly pipeline alongside company data ingestion. Target: top 200 AU tech startups by Signal Score — the companies users actually search for (or that they are still truly operated).

**Step 1 — Identify target companies**
Select all companies where `signal_score > 40` AND `vc_backed = true` OR `employee_range >= '11-50'`. This scopes the scraping effort to companies worth prospecting, not every ABN in the database.

**Step 2 — Scrape free stub sources**
For each target company, run the stub scraper pipeline in parallel:
- Startmate cohort pages → founders + early team
- VC portfolio team subpages → named staff where listed
- Company `/about`, `/team`, `/people` pages → staff listings
- GitHub API (`location:Australia` + company field) → engineers with public profiles
- Google News bylines (alongside news signal scrape), X-Ray Search → quoted founders/execs

**Step 3 — Normalise and dedup stubs**
Deduplicate on `linkedin_url` (exact) then `full_name + company_abn` (fuzzy). Classify seniority from title. Link to `company_abn` via domain resolution.

**Step 4 — Write stubs to contacts table**
UPSERT on `linkedin_url`. Set `is_stub_only = true`. `email_work = NULL`. `mobile = NULL`.

**What users see before unlock:**
```
┌─────────────────────────────────────────────────┐
│  Sarah Chen          VP Sales         [Unlock →] │
│  linkedin.com/in/...  ●●●●●●@acme.com            │
│                       (email blurred)            │
└─────────────────────────────────────────────────┘
```
Name, title, seniority, LinkedIn URL visible. Email and mobile blurred. Contact count shown on company card: "4 contacts — 1 VP, 1 CTO, 2 AEs".

---

### 6b — On-Demand Email Enrichment (unlock time, paid)

Fires only when a user clicks Unlock on a specific contact stub.

**Step 1 — Cache check**
Query `contacts` where `contact_id = X` and `is_stub_only = false` and `last_verified_at > now() - interval '30 days'`. If hit → return cached enriched record. No API call. No credit deducted.

**Step 2 — User confirms unlock**
Frontend shows stub preview (name, title, blurred email) + "Why contact now" AI note generated from company signals. User clicks "Unlock — 1 credit". Credit deducted from team pool.

**Step 3 — Make.com webhook fires**
Supabase Edge Function POSTs to Make.com scenario with `contact_id` + `linkedin_url` + `company_domain`.

**Step 4 — Apify (first attempt, cheapest)**
Pass `linkedin_url` to Apify API → attempts to extract email from LinkedIn profile. ~$0.02/call.
- If email returned → jump to Step 6 (verify)
- If no email → continue to Step 5

**Step 5 — Hunter domain search (second attempt)**
Pass `company_domain` to Hunter.io domain search → returns known email patterns and addresses at that domain. ~$0.03/call.
- If email found → continue to Step 6
- If no email → continue to Step 5b

**Step 5b — PDL full lookup (fallback, most expensive)**
Pass `full_name + company_domain` to People Data Labs API. ~$0.05–0.15/call.
- If found → continue to Step 6
- If no result → surface partial profile (name + LinkedIn only) + "Suggest email" contributor button (earns 5 credits if submission verified)

**Step 6 — Hunter.io email verification**
Pass email from whichever source found it to Hunter.io verify endpoint. Returns `email_status`: `deliverable` / `risky` / `undeliverable` / `unknown`.

**Step 7 — OpenAI model — "Why contact now" note**
Pass company signal context + contact title to OpenAI model → one-sentence note. ~$0.001/call.
> Example: *"Acme hired a VP Sales 6 weeks ago — likely evaluating CRM and outreach tooling right now."*

**Step 8 — Write enriched contact to Supabase**
Update `contacts` record: set `email_work`, `email_status`, `mobile`, `enriched_source`, `is_stub_only = false`, `last_verified_at = now()`. Insert `credit_transactions` row.

**Step 9 — Return to frontend**
Full contact card: verified email, mobile (if available), LinkedIn URL, email_status badge, "Why contact now" note.
> Latency target: < 3 seconds end to end.

---

### 6c — Enrichment cost per unlock

| Path taken | APIs called | Approx cost |
|---|---|---|
| Cache hit (enriched < 30 days ago) | None | $0 |
| Apify finds email | Apify + Hunter verify + OpenAI | ~$0.03 |
| Hunter finds email | Apify (miss) + Hunter + verify + OpenAI | ~$0.06 |
| PDL fallback needed | Apify + Hunter + PDL + verify + OpenAI | ~$0.10–0.18 |
| No email found | Apify + Hunter + PDL (all miss) | ~$0.08–0.20 (no credit charged) |

---

## Phase 7 🔄 — Contributor Feedback Loop
**Timing:** Continuous — triggered by user actions

Every user correction improves data quality for everyone. This is the flywheel that makes Active more accurate over time without paying for re-verification.

### Flow 1: User Reports Bounced Email

1. Toast: "Confirm this email bounced?" → user clicks Yes
2. `contributor_actions` row inserted (`action_type: bounce_report`)
3. `contacts.email_status` updated to `bounced`
4. Re-verification job queued (Hunter.io re-check + PDL refresh)
5. If 3 independent users report same bounce → auto-confirms without manual review
6. 2 credits awarded to reporting user
7. `contributor_score++` for user

### Flow 2: User Connects HubSpot CRM (not for this current MVP)

1. HubSpot webhook fires when contact changes job in CRM
2. Supabase Edge Function receives update payload
3. `contacts` table updated: title, company, `last_verified_at`
4. Signal row inserted (`signal_type: leadership_change`)
5. 20 credits awarded to connecting user (one-time)
6. Signal Score recalculated for affected company

### Flow 3: Weekly Verification Task

1. Sunday cron: select 3 contacts per user flagged as `unverified_30d+`
2. Push notification + in-app prompt sent via Resend
3. User confirms / denies each record ("Is this person still at this company?")
4. Confirmations update `last_verified_at`. Denials trigger re-enrichment queue.
5. 5 credits awarded on completion of all 3

---

## Summary: Key Design Decisions

| Decision | Rationale |
|---|---|
| **ABN as primary key** | Government-issued, unique, never duplicated — best deduplication anchor in AU |
| **Signals table is insert-only** | Preserves full event history for timeline display and score decay logic |
| **Contact stubs free, email paid** | Users see who works at a company before spending credits — builds desire to unlock. Zero paid contact cost until actual demand. |
| **`is_stub_only` flag** | Single boolean controls what frontend blurs vs. shows. Clean separation between free and paid data layers. |
| **Apify first in waterfall** | Cheapest path (~$0.02) when LinkedIn URL is available. Saves PDL cost (~$0.15) for the majority of unlocks. |
| **No credit charged if no email found** | Trust signal — users only pay when they get something. Reduces friction and churn from failed unlocks. |
| **Typesense separate from PostgreSQL** | Postgres is source of truth; Typesense handles all search — sub-100ms vs seconds |
| **`contact_stub_count` in Typesense** | Enables "show only companies with a VP Sales contact" filter without querying Postgres at search time |
| **Signal Score weekly, not real-time** | Avoids constant recomputation — weekly freshness is sufficient for prospecting use case |
| **30-day enrichment cache** | Same contact unlocked by multiple users only costs 1 API call per 30 days |
| **Contributor loop closes the cycle** | User bounces + CRM syncs feed back into pipeline — data improves without paying for re-verification |
| **Stub pre-fetch scoped to top 200 by Signal Score** | Avoids scraping 3M ABN records for stubs nobody ever looks at. Focus effort on companies users actually search. |