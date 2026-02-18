**ACTIVE**

Product Requirements Document

AU Tech Startup Intelligence Platform for Solo Founders & Micro Teams

|                 |                                                                      |
|-----------------|----------------------------------------------------------------------|
| **Version**     | 1.0 --- Initial Release                                              |
| **Date**        | February 2026                                                        |
| **Status**      | Active --- In Development                                            |
| **Author**      | Linh --- Founder                                                     |
| **Target**      | Solo founders · Tech freelancers · Micro teams (≤5)                  |
| **Positioning** | AU tech startup prospecting database with growth signal intelligence |

# 1. Product Overview {#product-overview}

## 1.1 Vision {#vision}

Active is the B2B contact intelligence platform built specifically for the Australian tech startup ecosystem. Unlike broad-market tools like Firmable or Apollo, Active is designed from the ground up for solo founders, tech freelancers, and micro teams who need to find and reach the right people fast --- without enterprise pricing, complex setup, or tools built for SDR teams they don\'t have.

Active doesn\'t just give you data. It shows you **who is growing, who just got funded, who is hiring right now** --- and surfaces those signals as actionable prospect intelligence, not raw records.

## 1.2 Problem Statement {#problem-statement}

|                            |                                                           |                                                                        |
|----------------------------|-----------------------------------------------------------|------------------------------------------------------------------------|
| **Problem**                | **Current Reality**                                       | **Active\'s Answer**                                                   |
| Global tools underserve AU | Apollo/ZoomInfo have thin, stale AU startup data          | ABN/ASIC + ACMA DNC + AHPRA backbone with AU-first data freshness    |
| Firmable priced out solos  | \$100+/mo minimum locks out freelancers and solo founders | Free tier + \$19/mo solo plan --- no user minimums                     |
| Data without signal        | Firmable shows headcount. That\'s it.                     | Growth rate, hiring velocity, funding recency, tech stack --- sortable |
| Data goes stale fast       | No mechanism for community correction                     | Gamified contributor system --- users earn credits to improve data     |

## 1.3 Target Customer {#target-customer}

### Primary: Solo Founders

Australian tech founders running their own outbound with no SDR. They have 20 minutes between product work to prospect, not 90 minutes. They need ICP-to-contact in under 2 minutes, mobile-friendly, and a pricing model that doesn\'t assume a team.

### Secondary: Tech Freelancers

Developers, designers, and consultants who do their own BD. They prospect infrequently but intensely --- they need credits that don\'t expire, not a monthly subscription that charges them during slow months.

### Tertiary: Micro Teams (2--5 people)

Early-stage startups where one person wears the sales hat part-time. They need shared credit pools, basic list management, and CSV export to feed their CRM --- not Salesforce integrations.

## 1.4 Success Metrics --- 12 Months {#success-metrics-12-months}

|                        |             |             |              |
|------------------------|-------------|-------------|--------------|
| **Metric**             | **Month 3** | **Month 6** | **Month 12** |
| Registered users       | 100         | 500         | 2,000        |
| Paying users           | 20          | 120         | 500          |
| MRR (AUD)              | \$500       | \$4,000     | \$18,000     |
| Active contributors    | 10          | 80          | 300          |
| Data corrections/month | 50          | 400         | 2,000        |
| NPS                    | \> 40       | \> 45       | \> 50        |
| Avg session (mins)     | 8           | 12          | 15           |

# 2. User Journey & UX Flow {#user-journey-ux-flow}

Active is designed around a single core truth: a solo founder has **20 minutes**, not 90. Every UX decision flows from this constraint.

## 2.1 Primary User Journey --- Solo Founder Prospecting {#primary-user-journey-solo-founder-prospecting}

**STEP 1 --- ARRIVE & ORIENT (\< 30 SECONDS)**

User lands on dashboard. They see: Today\'s 5 (5 AI-curated high-signal prospects matching their saved ICP), a credit balance badge, and a single prominent search bar. No configuration required on repeat visits --- the system remembers their ICP.

**STEP 2 --- QUICK HIT OR FULL SEARCH (\< 60 SECONDS)**

Two entry points side by side:

- Quick Hit: Type a sentence describing ideal customer (e.g. \'Series A SaaS companies in Melbourne hiring engineers\'). Claude API parses this into filters and returns a pre-qualified list in one step. No filter configuration.

- Full Search: Traditional filter panel --- industry, state, funding stage, headcount, tech stack, hiring activity, signal score. For power users who want precision.

**STEP 3 --- SCAN RESULTS WITH SIGNAL SCORES (\< 60 SECONDS)**

Results list shows: company name, location, headcount, funding stage, and a **Signal Score (0--100)** --- a composite of recent hiring velocity, funding recency, tech stack relevance, and growth rate. Users sort by Signal Score, not alphabetically.

Each result card shows 3 signal badges: e.g. \'↑ Hiring 5 roles\', \'Funded 4mo ago\', \'Uses HubSpot\'. Scannable in under 3 seconds.

**STEP 4 --- COMPANY PROFILE (\< 90 SECONDS)**

Click → company profile page. Sections: Core firmographics, Signal timeline (chronological feed of growth events), Key contacts preview (blurred), Tech stack chips, Related companies (same investors / same founding team). One-click \'Save to list\' or \'Unlock contacts\'.

**STEP 5 --- UNLOCK CONTACT (1 CREDIT)**

User clicks Unlock. 1 credit deducted. Contact card reveals: verified work email, mobile (if available), LinkedIn URL, title, seniority, and a **\'Why contact now\' AI note** --- a one-sentence context blurb generated from recent signals (e.g. \'New VP Sales hired 6 weeks ago --- likely building out tech stack\').

**STEP 6 --- SAVE, EXPORT, OR ACT**

User chooses:

- Save to a named list (e.g. \'Melbourne Series A --- Oct campaign\')

- Export list to CSV/XLSX for CRM upload

**STEP 7 --- CONTRIBUTE (EARN CREDITS BACK)**

If an email bounces or a contact has left the company, a toast notification appears: \'Did this email bounce? Report it and earn 2 credits.\' One click. This is the passive entry point to the contributor flywheel.

## 2.2 UX Flow Diagram (Screen-by-Screen) {#ux-flow-diagram-screen-by-screen}

The following describes the complete screen flow for the MVP web application.

|                      |                                    |                                                                         |
|----------------------|------------------------------------|-------------------------------------------------------------------------|
| **Screen**           | **Primary Action**                 | **Key UX Decision**                                                     |
| Landing / Sign-up    | Email signup or Google OAuth       | Social proof: \'500+ AU founders use Active\'. Free tier CTA prominent. |
| Onboarding (3 steps) | Set ICP, pick vertical (optional)  | Skip-friendly. Saved ICP unlocks \'Today\'s 5\' feature.                |
| Dashboard            | See Today\'s 5 + credit balance    | Desktop: 2-column. Mobile: single column, same data.                    |
| Search / Filters     | Type ICP sentence or set filters   | Quick Hit bar above filter panel. Filters collapse on mobile.           |
| Results List         | Scan Signal Scores, save companies | Signal Score column sortable. Signal badges on each card.               |
| Company Profile      | View signals, unlock contacts      | Signal timeline is chronological. Contacts blurred until unlock.        |
| Contact Unlock Modal | Confirm 1 credit spend             | Shows \'Why contact now\' AI note before confirming spend.              |
| My Lists             | Manage saved lists, export CSV     | List sharing within team (Growth plan). Export button prominent.        |
| Contribute / Verify  | Report bad data, verify contacts   | Credit reward shown before action. Weekly verification task.            |
| Credits & Billing    | Buy credit packs, upgrade plan     | Credit balance in nav always visible. Top-up in 2 clicks.               |
| Settings             | Team management, ICP defaults      | Solo: minimal. Growth: team seats + shared pool.                        |

## 2.3 Mobile-First Considerations {#mobile-first-considerations}

Firmable is desktop-only. Active treats mobile as a first-class surface --- solo founders prospect from phones between meetings.

- Today\'s 5 is the mobile home screen --- one swipeable card stack, one tap to unlock

- Quick Hit search works on mobile keyboard --- no filter configuration required

- Contact unlock is a bottom sheet, not a modal --- thumb-reachable on phones

- CSV export emails the file rather than downloading --- works on iOS/Android

- All tables scroll horizontally on mobile --- no data hidden

# 3. Signal Intelligence for AU Tech Startups {#signal-intelligence-for-au-tech-startups}

This is Active\'s core differentiation over Firmable. Static firmographics (headcount, location, industry) are table stakes. **Growth signals** are what tell a solo founder who to contact today, not just who exists.

## 3.1 The Signal Score {#the-signal-score}

Every company in Active has a Signal Score from 0--100, recalculated weekly. It is the primary sort column in all search results and the basis for Today\'s 5 recommendations.

Score is a weighted composite of five signal categories:

|                       |            |           |                                                 |
|-----------------------|------------|-----------|-------------------------------------------------|
| **Signal Category**   | **Weight** | **Decay** | **Why It Matters**                              |
| Hiring velocity       | 30%        | Weekly    | Hiring = budget approved, headcount growing     |
| Funding recency       | 25%        | Monthly   | Fresh capital = active vendor evaluation period |
| Headcount growth rate | 20%        | Monthly   | Trajectory matters more than current size       |
| Tech stack signals    | 15%        | Quarterly | Stack reveals spend patterns and tool gaps      |
| News & web activity   | 10%        | Weekly    | New product launch, press = company is active   |

## 3.2 The 8 Signals Active Tracks {#the-8-signals-active-tracks}

### Signal 1: Hiring Velocity (Highest Weight)

Source: Seek, LinkedIn Jobs, Indeed AU --- scraped weekly per company domain.

- Current open roles count

- Roles opened in last 30 days

- Role categories (Engineering / Sales / Marketing / Operations)

- Senior vs. junior ratio (Senior hires = strategic, not backfill)

Insight logic: Company posting 3+ engineering roles AND 1 sales role in 30 days = scaling product AND building revenue team. Flag as high-signal for SaaS tools sellers.

### Signal 2: Funding Round Recency

Source: AU VC portfolio pages (AirTree, Antler, Blackbird, Square Peg, Folklore, Airtree, Sequoia AU scraped quarterly).

- Last funding round amount, stage, date

- Lead investor name(s)

- Months since last raise (score decays linearly over 18 months)

Insight logic: Companies in months 3--12 post-raise are in active vendor evaluation. Month 0--2 = too early (hiring). Month 13+ = budget committed or Series B prep.

### Signal 3: Headcount Growth Rate

Source: LinkedIn headcount over time (scraped via People Data Labs API), cross-referenced with job posting history.

- Current headcount range

- Headcount 6 months ago (inferred from PDL historical data)

- Growth % calculated: (current - previous) / previous × 100

- Bands: Shrinking (\<-5%), Flat (-5% to +10%), Growing (10--50%), Scaling (50%+)

Insight logic: A 15-person company that was 8 people 6 months ago (+88% growth) is a better prospect than a 50-person company that\'s been flat for a year.

### Signal 4: Tech Stack

Source: Wappalyzer open-source for MVP (use only for top 50 companies).

- CRM in use (HubSpot / Salesforce / Pipedrive / None detected)

- Marketing automation (ActiveCampaign / Mailchimp / Klaviyo)

- Infrastructure (AWS / GCP / Azure / Vercel)

- Analytics (Mixpanel / Amplitude / GA4)

- Support (Intercom / Zendesk / Freshdesk)

Insight logic: Company using HubSpot Free = not yet on paid Sales Hub = opportunity for HubSpot partner selling. Company on AWS but no observability tool = opportunity for DataDog/Sentry alternatives.

### Signal 5: Leadership Changes

Source: LinkedIn scrape (via PDL), press releases, company blog.

- New C-suite or VP hire in last 90 days

- Founder departure / new CEO

- CRO/VP Sales hire (= building revenue team from scratch)

Insight logic: New CRO hired 6 weeks ago = evaluating entire sales stack. New CFO = vendor spend review imminent. These are the highest-value outreach windows in B2B sales.

### Signal 6: News & Press Activity {#signal-6-news-press-activity}

Source: Google News RSS per company name, company blog RSS if available.

- Product launch announcement

- Partnership announcement

- Award or recognition

- Expansion announcement (new market, new office)

Insight logic: Product launch = they\'re selling, they need tools to support the GTM. Expansion = new headcount incoming, new budget cycle.

### Signal 7: Investor Portfolio Tags

Source: Quarterly scrape of AU VC portfolio pages. One-time setup, high value.

- VC-backed flag (yes/no)

- Investor name(s) (AirTree / Blackbird / Square Peg / Folklore / Sequoia AU / Apex / Others)

- Portfolio stage filter (Seed / Series A / Series B+)

Insight logic: AirTree portfolio companies are high-growth, well-networked, and pre-validated as serious businesses. Filtering by investor is a quality proxy when other signals are weak.

### Signal 8: ABN/ASIC Health

Source: ABR bulk extract (free, quarterly update), ASIC company registry.

- ABN status (Active / Cancelled / Deregistered)

- Entity type (Pty Ltd / Trust / Sole Trader / Partnership)

- Registered state

- Years since incorporation

Insight logic: A 2-year-old Pty Ltd with an active ABN and 15 employees is far more creditworthy than a 6-month-old sole trader. This is the hygiene filter that removes noise from results.

## 3.3 \'Why Contact Now\' AI Note {#why-contact-now-ai-note}

Every unlocked contact includes a one-sentence AI-generated note based on the most recent signal. This is generated via OpenAI at unlock time.

Examples:

- \'Acme hired a VP Sales 6 weeks ago --- likely evaluating CRM and outreach tooling right now.\'

- \'TechCo raised \$3M Series A 4 months ago --- in active vendor selection window.\'

- \'BuildX posted 6 engineering roles this month --- growing fast, likely needs dev tooling.\'

Prompt template: \'Given these signals about \[company\], write a single sentence explaining why this is a good company to contact this week. Be specific and actionable. Max 25 words.\'

# 4. Gamified Contributor System {#gamified-contributor-system}

Active\'s data quality improves the more it\'s used --- not despite being used by many people, but **because** of it. Every user who corrects bad data makes the platform better for everyone. Credits are the currency that makes this happen.

## 4.1 Why Gamification Is the Moat {#why-gamification-is-the-moat}

Firmable maintains their database top-down: scraping + ASIC + third-party APIs. When data goes stale, their team has to fix it. This doesn\'t scale. Apollo\'s breakthrough was making their 2M+ users passively improve data quality. Active builds this flywheel from day one.

After 12 months of active users, Active\'s data accuracy for AU tech startups will exceed Firmable\'s --- not because we spend more on data collection, but because our users collectively verify thousands of records per week.

## 4.2 Credit Economy {#credit-economy}

Credits are the central unit of both consumption and contribution. The same currency used to unlock contacts can be earned back by improving the database.

|                                               |                            |                   |
|-----------------------------------------------|----------------------------|-------------------|
| **Action**                                    | **Credits**                | **Frequency Cap** |
| Unlock a contact (email + mobile)             | −1 credit                  | No cap            |
| Export a list to CSV/XLSX                     | −5 credits per 100 records | No cap            |
| Report a bounced email (verified)             | +2 credits                 | 50/month          |
| Confirm contact still at company              | +1 credit                  | 100/month         |
| Report wrong title/department                 | +1 credit                  | 50/month          |
| Complete weekly verification task (3 records) | +5 credits                 | Once/week         |
| Refer a user who activates                    | +30 credits one-time       | No cap            |
| Complete onboarding ICP setup                 | +10 credits one-time       | Once              |

## 4.3 Contributor Tiers & Badges {#contributor-tiers-badges}

Users build a Contributor Score separate from credits --- a reputation metric that unlocks perks and social status within the Active community.

|           |               |                                          |              |
|-----------|---------------|------------------------------------------|--------------|
| **Tier**  | **Threshold** | **Perks**                                | **Badge**    |
| Scout     | 0--49 pts     | Standard access                          | 🔍 Scout     |
| Mapper    | 50--199 pts   | +10% monthly credit bonus                | 🗺 Mapper     |
| Validator | 200--499 pts  | Priority support + early features        | ✅ Validator |
| Architect | 500+ pts      | Free Growth plan + founding member badge | 🏛 Architect  |

## 4.4 Verification Mechanisms {#verification-mechanisms}

### Passive (Zero Friction)

- Bounced email toast: \'This email may have bounced based on your activity. Confirm to earn 2 credits.\' --- appears if SendGrid (Phase 2) detects bounce

- CRM sync: when HubSpot/Salesforce shows job change for a contact in Active\'s DB, that signal auto-updates the shared record and credits the syncing user -> Not now in MVP

- \'Report bad data\' micro-button on every contact card --- one click, fills in a reason modal, submits correction

### Active (Slight Effort, Higher Reward)

- Weekly Verification Task: every Sunday, user receives 3 records to verify (\'Is this person still at this company?\'). Complete all 3 = 5 credits. Takes under 2 minutes.

- Data Enrichment Challenge: monthly campaign targeting a specific data gap (e.g. \'Help us verify 500 Melbourne Series A contacts this month\'). Top 10 contributors earn 100 bonus credits.

- Title Correction Queue: system flags records where job title format is inconsistent (\'VP of sales\' vs \'VP Sales\'). Users normalise, earn 1 credit per correction.

### Community (High Effort, Highest Reward)

- Industry Expert Review: users in a specific vertical (e.g. recruited from Fishburners Slack) can apply to be an \'Industry Reviewer\' --- they review 20 records/month for their sector and earn Architect status faster

- Data Source Submissions: users can submit a new data source (e.g. a niche AU startup directory they know about) --- if accepted and ingested, they earn 200 credits

## 4.5 Data Quality Pipeline Triggered by Contributions {#data-quality-pipeline-triggered-by-contributions}

Every contribution doesn\'t just update one record --- it triggers a downstream quality pipeline:

1.  User reports email bounce → email_status field set to \'bounced\' → record flagged for re-verification queue

2.  Re-verification job runs (Hunter.io re-check + PDL refresh) → if confirmed, record updated globally

3.  If 3 independent users report same issue → record auto-updates without manual review

4.  Contributor score incremented for all 3 users, credit reward distributed

5.  Data quality score for that company record updated (used in Signal Score calculation --- high-quality records get slight Signal Score boost)

# 5. Reverse Pricing Model {#reverse-pricing-model}

Firmable\'s pricing assumes a sales team. Active\'s pricing assumes a founder doing everything themselves. This isn\'t a discount --- it\'s a **structural repositioning** of who the product is for.

## 5.1 Pricing Philosophy {#pricing-philosophy}

- Free forever tier --- not a time-limited trial. Enough value to be genuinely useful, not just a teaser.

- Solo plan at \$19/mo --- no user minimums, no \'per seat × 2\' floors. One person, full product.

- Pay-as-you-go credits --- freelancers don\'t want subscriptions. Buy when you need them.

- Transparent credit costs --- 1 unlock = 1 credit everywhere. No surprise charges for mobile numbers.

- Annual solo at \$149/yr --- one transaction, full year, \$79 saving. Reduces churn for core users.

## 5.2 Plan Comparison {#plan-comparison}

|                              |                   |                      |                        |                              |
|------------------------------|-------------------|----------------------|------------------------|------------------------------|
| **Feature**                  | **Free**          | **Solo --- \$19/mo** | **Growth --- \$49/mo** | **Team --- \$99/mo**         |
| **Credits / month**          | 25                | 300                  | 1,000                  | 3,000 shared                 |
| **Credit card required**     | No                | Yes                  | Yes                    | Yes                          |
| **Users included**           | 1                 | 1                    | 1                      | Up to 5                      |
| **Credit expiry**            | No expiry         | No expiry            | No expiry              | No expiry                    |
| **Signal Score access**      | Basic (3 signals) | Full (8 signals)     | Full                   | Full                         |
| **Quick Hit ICP search**     | Limited (3/day)   | Unlimited            | Unlimited              | Unlimited                    |
| **Today\'s 5**               | Yes               | Yes                  | Yes                    | Yes                          |
| **List save**                | 1 list            | 10 lists             | Unlimited              | Unlimited + shared           |
| **CSV export**               | 50 records        | 500 records          | Unlimited              | Unlimited                    |
| **Mobile app**               | Yes               | Yes                  | Yes                    | Yes                          |
| **CRM sync (HubSpot)**       | No                | No                   | Yes                    | Yes                          |
| **Contributor tier**         | Scout eligible    | All tiers            | All tiers              | All tiers + team leaderboard |
| **Annual option (save 20%)** | N/A               | \$149/yr             | \$469/yr               | \$949/yr                     |

## 5.3 Credit Packs (Add-On) {#credit-packs-add-on}

For freelancers or solo users who hit their monthly credit limit mid-campaign without wanting to upgrade plans permanently.

|                   |                                                                |
|-------------------|----------------------------------------------------------------|
| **Starter Pack**  | 100 credits --- \$12 AUD. One-time purchase, no subscription.  |
| **Campaign Pack** | 500 credits --- \$49 AUD. For one intensive outbound campaign. |
| **Power Pack**    | 1,500 credits --- \$119 AUD. Stacks on any plan, no expiry.    |

## 5.4 Firmable Comparison {#firmable-comparison}

|                               |                                                       |
|-------------------------------|-------------------------------------------------------|
| **Firmable minimum spend**    | \$100 AUD/month (2-user minimum at \$50/user)         |
| **Active minimum spend**      | \$0 (free tier, no credit card)                       |
| **Firmable solo use case**    | Not supported --- minimum 2 seats                     |
| **Active solo use case**      | \$19/month, full product access, 300 credits          |
| **Firmable freelancer model** | No --- monthly subscription only, 14-day trial        |
| **Active freelancer model**   | Free tier + credit packs --- no subscription required |
| **Firmable trial**            | 14 days with credit card                              |
| **Active free tier**          | Forever, no credit card, 25 credits/month             |

# 6. Feature Specifications {#feature-specifications}

## 6.1 MVP Feature Set (Phase 1) {#mvp-feature-set-phase-1}

|                                 |                                                                                                                         |              |            |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------------|--------------|------------|
| **Feature**                     | **Description**                                                                                                         | **Priority** | **Effort** |
| **Company search + filters**    | 10+ filters: industry, state, funding stage, headcount, tech stack, hiring activity, signal score range, VC-backed flag | **P0**       | Medium     |
| **Quick Hit ICP search**        | Natural language to filters via OpenAI API. One sentence → pre-qualified list.                                          | **P0**       | Low        |
| **Signal Score display**        | Composite score on every company card. Sortable. 3 signal badges visible.                                               | **P0**       | Medium     |
| **Company profile page**        | Full firmographics + signal timeline + blurred contacts + tech stack chips                                              | **P0**       | Medium     |
| **Contact unlock**              | 1 credit → reveals email, mobile, LinkedIn, title + \'Why contact now\' AI note                                         | **P0**       | Medium     |
| **Today\'s 5**                  | Daily digest of 5 high-signal prospects matching saved ICP. Dashboard landing.                                          | **P0**       | Low        |
| **List save + management**      | Save named lists, add/remove companies, view saved lists                                                                | **P0**       | Low        |
| **CSV / XLSX export**           | Export list up to plan limits. Email delivery on mobile.                                                                | **P0**       | Low        |
| **Free tier + Solo plan**       | Stripe billing: free (25 cr/mo), solo \$19/mo, growth \$49/mo                                                           | **P0**       | Low        |
| **Credit packs**                | One-time Stripe payment for credit top-ups                                                                              | **P0**       | Low        |
| **Contributor: bounce report**  | \'Report bounced email\' button + credit reward                                                                         | P1           | Low        |
| **Contributor: verify contact** | Weekly verification task (3 records, 5 credits)                                                                         | P1           | Low        |
| **Contributor score + badges**  | Scout → Mapper → Validator → Architect tiers                                                                            | P1           | Low        |
| **Google OAuth + email signup** | Supabase Auth. No password friction.                                                                                    | **P0**       | Low        |
| **Team accounts (Growth+)**     | Shared credit pool, invite members, basic roles                                                                         | P1           | Medium     |
| **Mobile-responsive UI**        | All screens usable on iOS/Android browser                                                                               | **P0**       | Medium     |
| **DNC flag display**            | Red badge on contacts in ACMA DNC register                                                                              | **P0**       | Low        |

## 6.2 Phase 2 Features (Months 4--6) {#phase-2-features-months-46}

- AI draft email: unlock → one-click → OpenAI-generated personalised first email using signal context

- Basic sequence sender: 3-step email sequence with unsubscribe footer (Privacy Act compliant)

- Reply tracking: open/click webhooks displayed per contact in list view

- Salesforce integration: push contacts, pull enrichment back

- Data Enrichment Challenge: monthly gamified community data event

## 6.3 Phase 3 Features (Months 7--12) {#phase-3-features-months-712}

- Chrome extension: overlay Active data on LinkedIn and company websites

- Intent data layer: companies actively researching your category (Enterprise add-on)

- Buying signal agents: automated alerts when tracked companies hit key signal thresholds

- API access: raw data API for technical users (developers building on top of Active)

- White-label / reseller: vertical-specific resellers (e.g. a recruitment firm reselling Active to their clients)

# 7. High-Level Architecture {#high-level-architecture}

Architecture decisions are made to minimise cost and build time while preserving the ability to scale. Every component has a **zero-cost or near-zero starting point** with a clear upgrade path as usage grows.

## 7.1 Architecture Overview {#architecture-overview}

|                                            |                                                                                                                                                                                                               |
|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Philosophy**                             | Buy infrastructure, build product. Use managed services for every undifferentiated concern (auth, storage, payments, email). Build only what users pay for: search, signal scoring, and the contributor loop. |
| **Stack principle**                        | Supabase as the operational core. Typesense for search. Vercel for frontend. Make.com for enrichment pipelines. OpenAI API for AI features. Stripe for billing.                                               |
| **Scaling ceiling before re-architecture** | \~5,000 MAU / 2M company records / 20M contact records. Re-architecture (sharding, Elasticsearch upgrade, custom enrichment pipelines) needed only if traction justifies it.                                  |

## 7.2 Component Breakdown {#component-breakdown}

|                     |                                         |                                    |                             |
|---------------------|-----------------------------------------|------------------------------------|-----------------------------|
| **Layer**           | **Component**                           | **Tool / Service**                 | **Monthly Cost (MVP)**      |
| Frontend            | Web app (React SPA)                     | Next.js 15 + Tailwind → Vercel     | Free (Hobby) → \$20         |
| Auth                | User auth + team management             | Supabase Auth (OAuth + email)      | Free → \$25 (Pro)           |
| Database            | Primary data store                      | Supabase PostgreSQL                | Free → \$25 (Pro)           |
| Search              | Company + contact search                | Typesense Cloud                    | \$30/mo (3 nodes)           |
| AI --- Search       | Quick Hit ICP parsing                   | OpenAI API (o4 model --- cheapest) | \~\$5--15/mo at MVP scale   |
| AI --- Notes        | \'Why contact now\' at unlock           | OpenAI API (o4 model)              | \~\$10--30/mo at MVP scale  |
| People data         | On-demand contact enrichment            | Hunter.io/ People Data Labs API (refered to active_data_pipeline)               | Usage-based \~\$0.05/record |
| Email verify        | Email verification at unlock            | Hunter.io API                      | Free 25/mo → \$49/mo        |
| Data pipeline       | ABN/ASIC bulk import + refresh          | Python script on Railway or Render | Free--\$5/mo                |
| Enrichment flow     | Unlock → PDL → Supabase → credit deduct | Make.com    | Free → \$9/mo               |
| Billing             | Subscriptions + credit packs            | Stripe                             | 2.7% + \$0.30/txn           |
| Transactional email | Auth emails, exports, alerts            | Resend                             | Free 3K/mo → \$20/mo        |
| Analytics           | Usage, funnels, session replay          | PostHog Cloud                      | Free to 1M events/mo        |
| Error tracking      | Frontend + backend errors               | Sentry                             | Free tier                   |
| DNC data            | ACMA DNC register import                | Python script (free public data)   | \$0                         |

## 7.3 Data Architecture {#data-architecture}

### Core Tables (PostgreSQL via Supabase)

companies --- ABN (PK), entity name, trading name, entity type, status, state, suburb, postcode, industry (ANZSIC), sub-industry, employee range, revenue range, website, LinkedIn URL, founded year, VC-backed flag, investor names (JSON), funding stage, last funding date, funding amount, tech stack (JSON), signal_score (0--100), signal_updated_at, dnc_flag, data_quality_score, created_at, updated_at.

contacts --- contact_id (PK), company_id (FK → companies.abn), first_name, last_name, title, department, seniority (C-Suite/VP/Director/Manager/IC), email_work, email_status (verified/bounced/catch-all/unknown), mobile, mobile_status, linkedin_url, state, city, data_source (PDL/Hunter/manual), last_verified_at, contributor_corrections (int), created_at, updated_at.

signals --- signal_id (PK), company_abn (FK), signal_type (hiring/funding/leadership/news/techstack/headcount/investor), signal_value (JSON), signal_date, source_url, created_at. One row per signal event.

users, teams, credit_transactions, saved_lists, contributor_actions --- standard SaaS operational tables. See Section 5 for credit logic.

### Search Index (Typesense)

Typesense collection mirrors company table with denormalised fields for fast faceted search. Synced from Supabase via a lightweight webhook or polling job on every company record update. Supports: full-text name search, numeric range filters (headcount, signal score, funding amount), multi-select facets (state, industry, tech stack, funding stage), geo-filter by state/suburb, sort by signal_score DESC (default).

### Enrichment Pipeline (Make.com) {#enrichment-pipeline-make.com}

Trigger: user clicks Unlock contact → Supabase edge function fires → Make.com webhook receives company_id + contact_id → waterfall: (1) check if contact already enriched in last 30 days → return cached if yes → (2) call PDL API for contact → (3) call Hunter.io for email verification → (4) write enriched contact to Supabase → (5) deduct 1 credit from team pool → (6) return enriched contact to frontend. Latency target: \< 3 seconds.

## 7.4 Data Ingestion Pipeline {#data-ingestion-pipeline}

|                               |                                                                                |                                       |
|-------------------------------|--------------------------------------------------------------------------------|---------------------------------------|
| **Data Source**               | **Method**                                                                     | **Frequency**                         |
| ABR Bulk Extract (ABN data)   | Python script downloads bulk file, parses, upserts to Supabase companies table | Quarterly (auto-scheduled on Railway) |
| ASIC company registry         | Python scraper for company type, directors, incorporation date                 | Monthly for active companies          |
| ACMA DNC register             | Python script downloads register, sets dnc_flag on matching ABNs               | Monthly                               |
| AU VC portfolio pages         | Python scraper for AirTree, Blackbird, Square Peg, Folklore, Apex pages        | Quarterly                             |
| Job postings (hiring signals) | Seek/LinkedIn/Indeed AU domain-based scrape --- count open roles per company   | Weekly                                |
| BuiltWith / Wappalyzer        | BuiltWith API (paid, Phase 2) or Wappalyzer open-source for tech stack         | Quarterly per company                 |
| Google News RSS               | Per-company RSS query for news signals                                         | Weekly for Signal Score companies     |
| PDL (people data)             | On-demand at unlock --- not pre-scraped. Pay per use.                          | Real-time                             |

# 8. Delivery Timeline {#delivery-timeline}

Deploy Forward approach: ship a working product in 10 weeks. Learn from real users. Add features based on what they actually use, not what sounds good in a PRD.

## 8.1 Phase 0 --- Foundation (Week 1--2) {#phase-0-foundation-week-12}

Goal: database seeded, search running, auth working. Nothing user-facing yet.

- Set up Supabase project --- create companies, contacts, signals, users, teams, credit_transactions tables

- Download and ingest ABR bulk extract --- \~3M AU business records imported

- Run ASIC scraper for company type enrichment on top 100K active Pty Ltd companies

- Import ACMA DNC register, set dnc_flag on matching records

- Stand up Typesense Cloud, sync company records, validate search and filters

- Set up Next.js app on Vercel with Supabase Auth (Google OAuth + email)

- Scrape AU VC portfolio pages (AirTree, Blackbird, Square Peg, Folklore) --- tag VC-backed companies

**Exit criteria: can run a search query against 3M companies and get filtered results in \< 1 second.**

## 8.2 Phase 1 --- Core Product (Week 3--6) {#phase-1-core-product-week-36}

Goal: searchable database with Signal Scores, contact unlock, and basic billing. First users can get value.

- Company search UI: filter panel + results list with Signal Score column and 3 signal badges

- Quick Hit ICP search: OpenAI API parses natural language to Typesense filters

- Company profile page: firmographics + signal timeline + blurred contacts + tech stack chips

- Contact unlock flow: Make.com webhook → PDL → Hunter verify → credit deduct → reveal

- \'Why contact now\' AI note: OpenAI generates at unlock from signal context

- Signal Score calculation: weekly cron job computes composite score for all companies

- Job posting scraper: Seek/LinkedIn weekly scrape for hiring velocity per domain

- Stripe integration: Free tier, Solo \$19, Growth \$49, Team \$99 + credit packs

- Today\'s 5: daily digest algorithm matching saved ICP against highest Signal Score companies

- DNC flag badge: red warning displayed on contacts in DNC register

**Exit criteria: a solo founder can find 5 high-signal AU tech startups, unlock contacts, and export to CSV in under 10 minutes.**

## 8.3 Phase 2 --- Retention & Contribution (Week 7--9) {#phase-2-retention-contribution-week-79}

Goal: users come back. Contributor flywheel starts spinning. Data quality improves.

- List management: save named lists, add/remove companies, manage multiple lists

- CSV/XLSX export with credit deduction and email delivery on mobile

- Contributor system: bounce report button, credit reward, contributor score tracking

- Weekly verification task: Sunday push notification (email + in-app) with 3 records + 5 credit reward

- Contributor badge display: Scout/Mapper/Validator/Architect on user profile

- Team accounts: shared credit pool, member invite, basic admin/member roles (Growth plan)

- Onboarding ICP setup: 3-step flow, +10 credits on completion

- Referral system: unique referral link, +30 credits on referred user activation

**Exit criteria: at least 20% of weekly active users complete a contributor action.**

## 8.4 Phase 3 --- Launch & Growth (Week 10--12) {#phase-3-launch-growth-week-1012}

Goal: public launch. First paying users. Content-driven acquisition starts.

- Mobile UI polish pass: test on iOS Safari and Android Chrome, fix touch targets, bottom sheet unlocks

- Onboarding email sequence: Day 0 (welcome + 10 credits), Day 3 (first unlock guide), Day 7 (contributor prompt)

- Landing page: positioning for AU solo founders + section for \'expanding to Australia\'

- Public launch post: Startmate Slack, Fishburners, YC\'s Work at a Startup, LinkedIn

- Founding Member cohort: 50 free Growth plan accounts for early users, in exchange for feedback + referrals

- PostHog funnel setup: track signup → first search → first unlock → first export → paid conversion

- Stripe webhook → PostHog: revenue events tracked alongside product events

**Exit criteria: 100 registered users, 20 paying users, first MRR \> \$500 AUD.**

## 8.5 Phase 4 --- Outreach Loop (Month 4--5) {#phase-4-outreach-loop-month-45}

Goal: collapse the workflow. Data → outreach in one place. This is the retention multiplier.

- HubSpot two-way sync: push unlocked contacts, pull job change signals back to Active

- AI draft email: Claude Sonnet generates personalised first email from contact + signal context

- Basic sequence: 3-step email sequence with Resend, unsubscribe footer, open/click tracking

- Reply inbox: basic reply management within Active (not a full email client --- just replies to Active sequences)

- Salesforce connector: push contacts, pull enrichment

## 8.6 Timeline Summary {#timeline-summary}

|             |              |                                                |                                       |
|-------------|--------------|------------------------------------------------|---------------------------------------|
| **Phase**   | **Timeline** | **Key Deliverable**                            | **Exit Criteria**                     |
| **Phase 0** | Week 1--2    | Database + search foundation                   | 3M companies searchable \< 1s         |
| **Phase 1** | Week 3--6    | Core product: search, signals, unlock, billing | Solo founder gets value in \< 10 min  |
| **Phase 2** | Week 7--9    | Retention: lists, export, contributor system   | 20% WAU complete contributor action   |
| **Phase 3** | Week 10--12  | Public launch + growth                         | 100 users, 20 paying, \$500 MRR       |
| **Phase 4** | Month 4--5   | Outreach loop (email + sequences)              | Avg session \> 15 min, churn \< 5%/mo |
| **Phase 5** | Month 6--9   | HubSpot/Salesforce + Chrome extension          | 30% users integrate CRM               |
| **Phase 6** | Month 10--12 | Intent data + buying signal agents             | \$10K MRR                             |

# 9. Cost Model {#cost-model}

## 9.1 Infrastructure Cost at MVP Scale (\< 200 MAU) {#infrastructure-cost-at-mvp-scale-200-mau}

|                        |                                                                 |
|------------------------|-----------------------------------------------------------------|
| **Supabase Pro**       | \$25/mo --- needed once DB exceeds free tier limits             |
| **Typesense Cloud**    | \$30/mo --- 3-node cluster, handles millions of search queries  |
| **Vercel**             | \$0 (Hobby) → \$20/mo (Pro) --- frontend hosting                |
| **Railway / Render**   | \$5/mo --- Python pipeline jobs (ABN/ASIC/DNC refresh)          |
| **Make.com**           | \$9/mo (Core) --- enrichment automation workflows               |
| **Claude API (Haiku)** | \~\$15--40/mo --- Quick Hit + Why Contact Now at 200 MAU        |
| **PDL API**            | \~\$0.05--0.15/unlock × usage --- only pay when users unlock    |
| **Hunter.io**          | \$49/mo (Starter, 500 verifications) --- or \$0 free tier early |
| **Resend**             | \$0 (free 3K/mo) → \$20/mo                                      |
| **PostHog**            | \$0 (free to 1M events/mo)                                      |
| **Sentry**             | \$0 (free tier)                                                 |
| **Stripe fees**        | 2.7% + \$0.30 per transaction                                   |
| **Total (MVP launch)** | \~\$130--175 AUD/mo fixed + variable PDL/Claude usage           |

## 9.2 Unit Economics {#unit-economics}

|                              |                                                                                                                                                                                                                          |                                                                                                       |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **Solo plan revenue**        |                                                                                                                                                                                                                          | \$19/mo per user                                                                                      |
| **PDL cost per unlock**      |                                                                                                                                                                                                                          | \~\$0.10 average                                                                                      |
| **300 credits/mo Solo plan** |                                                                                                                                                                                                                          | If user unlocks all 300: \~\$30 PDL cost \> \$19 revenue --- cap heavy users or add waterfall caching |
| **Realistic unlock rate**    |                                                                                                                                                                                                                          | Average solo user unlocks 40--80 contacts/month. Cost: \~\$4--8. Margin: \~\$11--15/user.             |
| **Break-even (fixed costs)** |                                                                                                                                                                                                                          | 9 paying Solo users covers \$175/mo fixed infra                                                       |
| **Cash flow positive**       |                                                                                                                                                                                                                          | \~15 paying users covers all fixed + variable costs at realistic unlock rates                         |
| **💡**                       | Credit caching is critical: if a contact has been enriched in the last 30 days, serve cached data --- no new PDL call. This reduces variable cost dramatically as the database fills up with recently-verified contacts. |                                                                                                       |

# 10. Risks & Mitigations {#risks-mitigations}

|                                                 |              |                |                                                                                                                              |
|-------------------------------------------------|--------------|----------------|------------------------------------------------------------------------------------------------------------------------------|
| **Risk**                                        | **Severity** | **Likelihood** | **Mitigation**                                                                                                               |
| AU contact data thin via PDL API                | High         | Medium         | Waterfall: PDL → Hunter → LinkedIn. Add manual import for key contacts. Honest about coverage in onboarding.                 |
| Privacy Act compliance breach                   | High         | Low            | Only B2B professional data. DNC flag mandatory. Legal review before launch. No home addresses ever stored.                   |
| Signal Score not valued by users                | Medium       | Low            | Validate in founding member cohort. If unused, simplify to 3 core signals. PostHog tracks column sort events.                |
| Gamification feels forced                       | Medium       | Medium         | Make credits feel like money, not points. Tie every action to a tangible credit reward. Test with 10 founding members first. |
| LinkedIn blocks scraping                        | Medium       | Medium         | Use PDL API (ToS-compliant) not direct scrape. People data is API-sourced only.                                              |
| Firmable price-cuts to compete                  | Low          | Low            | Their cost structure (team size, data ops) prevents sub-\$50 solo plan. Our moat is structural.                              |
| ABR/ASIC data staleness                         | Low          | Low            | ABR bulk export updates quarterly. Automate refresh. ASIC company changes trigger re-scrape.                                 |
| Stripe payment friction on free plan conversion | Medium       | Medium         | No credit card for free tier. Stripe Checkout for first payment. Credit pack as low-friction first transaction.              |
