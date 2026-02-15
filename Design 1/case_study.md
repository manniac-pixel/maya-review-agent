# Maya Review Agent: AI-Powered UX Intelligence for Fintech

---

## Overview

|  |  |
| --- | --- |
| **Project** | Maya App — UX Review Analysis Agent |
| **Role** | Product Designer & AI Engineer |
| **Duration** | February 2026 (2-week sprint) |
| **Tools** | Python, Gemini 2.0 Flash API, pandas, matplotlib, Rich CLI |
| **Scope** | 12,345 reviews analyzed across Google Play & iOS App Store |

---

## The Problem

### Maya is losing users — and the reviews tell you exactly why.

Maya (formerly PayMaya) is one of the Philippines' leading digital banks, serving millions of users for payments, transfers, savings, and crypto. Despite strong product fundamentals, Maya's app store ratings have been declining, with a **mixed-negative overall sentiment** across 12,345 reviews from August 2025 to February 2026.

The core challenge: **negative reviews contain highly specific, actionable UX feedback** — but at scale, no human team can read, categorize, and prioritize 12,000+ reviews fast enough to inform design decisions.

### The real cost of ignoring reviews

> "I've tried several times today, but I can't get in."
> — Maya user, 1-star review

> "My phone was stolen and the hacker was able to access this app and took my savings and made loan in a snap of a finger."
> — Maya user, 1-star review

These aren't edge cases. Login failures alone carry a **severity score of 5/5** with **high frequency**, impacting activation, retention, trust, and revenue simultaneously.

---

## The Hypothesis

**What if we could build an AI agent that reads every single review, maps pain points to specific screens in the user journey, and outputs a prioritized design brief — in minutes instead of weeks?**

Instead of manually tagging reviews in spreadsheets, we built an automated pipeline that:
1. Scrapes reviews at scale (both Maya and competitor GCash)
2. Analyzes sentiment and categorizes issues using LLMs
3. Maps problems to specific screens and user journeys
4. Ranks issues by severity, frequency, and business impact
5. Generates actionable design recommendations with real user quotes

---

## The Solution: Maya Review Agent

### Architecture

An 8-step Python pipeline powered by Gemini 2.0 Flash:

| Step | Module | What It Does |
| --- | --- | --- |
| 1 | `scraper` | Scrapes 10,000+ Maya reviews + 10,000+ GCash reviews from Google Play & iOS |
| 2 | `temporal_analyzer` | Tracks how issues evolve month-over-month (persistent vs. emerging vs. resolved) |
| 3 | `comprehensive_analyzer` | Deep categorization of every review by issue type, journey, and severity |
| 4 | `funnel_analyzer` | Maps drop-off points to specific screens in the user flow |
| 5 | `accessibility_analyzer` | Identifies edge-case users (elderly, OFWs, budget devices) |
| 6 | `competitor_analysis` | Benchmarks Maya against GCash across key dimensions |
| 7 | `screenshot_scraper` | Downloads current app screenshots for visual reference |
| 8 | `insights_generator` | Synthesizes everything into a ranked report with charts |

### How it works

```
python main.py --months 12 --stars 1,2
```

The agent runs end-to-end in a single command. It supports:
- **Star filtering** — analyze only 1-star reviews, or any combination
- **Backend switching** — Gemini (cloud) or Ollama (local/free)
- **Caching** — resume from any checkpoint without re-running earlier steps
- **Fresh mode** — clear cache and re-run from scratch

### Key design decisions

| Decision | Why |
| --- | --- |
| **Gemini 2.0 Flash** over GPT-4 | Faster, cheaper for high-volume text classification. 12K reviews processed in minutes |
| **Dual-platform scraping** | Google Play + iOS gives complete picture. iOS reviews often surface different issues |
| **Competitor scraping** | GCash reviews provide benchmark context — users explicitly compare the two |
| **Checkpoint caching** | Each step saves to JSON/CSV. Re-runs skip completed steps automatically |
| **Rich CLI output** | Progress bars, colored tables, and panels for clear pipeline visibility |

---

## The Findings

### 9 ranked UX opportunities

The agent identified and ranked 9 critical issues by a composite priority score (severity x frequency x business impact):

| Rank | Issue | Severity | Priority Score | Business Impact |
| --- | --- | --- | --- | --- |
| 1 | **Login & Authentication Failures** | 5/5 | **18** | Activation, retention, trust, revenue |
| 2 | **Customer Service Unreachable** | 5/5 | **15** | Trust, revenue |
| 3 | **Unauthorized Transactions** | 5/5 | **15** | Trust, revenue |
| 4 | **Security Concerns** | 5/5 | **15** | Trust, revenue |
| 5 | **Cash-in Delays** | 4/5 | **14** | Transaction volume, trust |
| 6 | **Cash-in Issues** (general) | 4/5 | **12** | Transaction volume, trust, revenue |
| 7 | **Customer Service** (follow-up) | 4/5 | **12** | Trust, revenue |
| 8 | **Duplicate Account Issues** | 4/5 | **10** | Activation, retention, trust |
| 9 | **Data Privacy Concerns** | 3/5 | **6** | Trust, revenue |

> **Key insight:** 4 of the top 5 issues have severity 5/5, and all are trust-related. Maya doesn't have a feature problem — it has a **trust crisis**.

### Funnel drop-off hotspots

The agent mapped pain points to specific screens:

| Screen | Journey | Evidence (reviews) | Severity |
| --- | --- | --- | --- |
| **Login > OTP Entry** | Onboarding | 45 reviews | 5/5 |
| **Cash In > Bank Integration** | Payments | 30 reviews | 4/5 |
| **KYC > Selfie Capture** | Onboarding | 25 reviews | 4/5 |
| **Crypto > Buy Token** | Crypto | 12 reviews | 3/5 |
| **Send Money > Contact Selection** | Transfers | 8 reviews | 2/5 |

### Version spike: v2.148.3

The temporal analysis flagged a critical version:

- **45.2% one-star rate** vs. 34.6% baseline (+10.6 percentage points)
- 188 reviews between November 2025 – February 2026
- Root causes: login regressions, payment failures, chatbot-only support
- This single release caused measurable trust erosion

### Temporal patterns

| Trend | Issues |
| --- | --- |
| **Getting better** | Login issues, cash-in delays |
| **Getting worse** | Customer service, unauthorized transactions |
| **Persistent (6-7 months)** | Payment issues, KYC/onboarding, loan/credit |
| **Emerging (Jan-Feb 2026)** | OTP failures, transfer delays, savings problems |

### Competitive position vs. GCash

Users actively switch to GCash citing:
- Stronger security measures
- Better data privacy practices
- Faster transaction processing
- Functioning customer support

**Maya's advantages:** Interface design preference, feature breadth, savings interest rates, crypto access.

---

## Journey Friction Map

The agent produced a screen-level friction map across 5 user journeys:

| Journey | Pain Points | Friction Score | Priority |
| --- | --- | --- | --- |
| General | 12 | 110.4 | High |
| Payments | 2 | 24.0 | High |
| Onboarding | 2 | 23.0 | Critical |
| Transfers | 1 | 15.0 | Critical |
| Support | 1 | 15.0 | Critical |

### 4 critical screens (severity 5/5)

1. **Login Screen** — Login failures blocking user access
2. **Transfer Recipient Selection** — Unauthorized transactions
3. **Support Contact Form** — Customer service unreachable
4. **Security Settings** — Account security vulnerabilities

---

## Design Recommendations

Based on the agent's findings, we identified 4 redesign priorities that directly address the highest-impact issues:

### Flow A: Frictionless Login
**Addresses:** Login failures (Priority #1, Score 18)

- Biometric-first authentication (Face ID / fingerprint as primary)
- Fallback chain: biometric → password → email OTP → support escalation
- Clear error messaging with actionable next steps
- Simplified input — reduce fields on login screen

### Flow B: Transparent Transactions
**Addresses:** Cash-in delays (Priority #5, Score 14)

- Real-time transaction timeline (Request Sent → Processing → Received)
- Pending transactions dashboard with live status
- Push notifications at each state change
- Retry/cancel flows for stuck transactions

### Flow C: Accessible Support
**Addresses:** Customer service unreachable (Priority #2, Score 15)

- "My Tickets" dashboard on Help Center home
- Ticket status pills (Investigating, Resolved) with timestamps
- Human escalation paths visible in UI (not buried behind chatbot)
- Contextual help buttons at high-friction screens

### Flow D: Security Center
**Addresses:** Unauthorized transactions + security concerns (Priority #3-4, Score 15)

- Emergency "Kill Switch" to instantly freeze all cards and accounts
- Safety Score with visual shield indicator
- Active sessions list with remote logout capability
- Transaction confirmation with biometric approval

---

## Visualizations

The agent auto-generates 9 charts for each run:

1. **Rating Trend Over Time** — Monthly average ratings showing decline trajectory
2. **Sentiment Distribution** — Positive/negative/neutral breakdown
3. **Business Impact Distribution** — Which issues affect which business metrics
4. **Priority Scores** — Bar chart of all 9 ranked issues
5. **Severity vs. Frequency** — Scatter plot identifying "critical & common" quadrant
6. **Pain Point Frequency** — Which issues appear most often
7. **Version Ratings** — 1-star rate per app version (flagging v2.148.3)
8. **Issue Lifecycle** — How each issue trends over time
9. **Funnel Drop-off** — Where users abandon specific journeys

---

## What I Learned

### On building AI agents for design research

1. **Reviews are underrated as a data source.** 12,000 reviews contain more specific, screen-level UX feedback than most user interviews. The signal-to-noise ratio is high for 1-star reviews.

2. **LLMs excel at categorization at scale.** What would take a research team weeks (reading, tagging, categorizing 12K reviews) takes the agent minutes. The quality of categorization is surprisingly good with Gemini 2.0 Flash.

3. **Temporal analysis reveals what dashboards miss.** Knowing that an issue is "high severity" is useful. Knowing it's been high severity for 7 months and getting worse is actionable.

4. **Competitor context changes the framing.** When users say "I switched to GCash because..." — that's not just feedback, it's market intelligence. Scraping competitor reviews in parallel was one of the best design decisions.

### On the limits of AI-generated UI

We initially attempted to generate high-fidelity mockups using AI design tools (Google Stitch). While the tool is promising for rapid wireframing, **AI-generated screens struggle to match specific brand guidelines** — particularly custom fonts (Tuka), exact color palettes, and the level of polish expected for a production fintech app. The wireframes serve well as design direction, but final screens need human designers.

---

## Impact & Next Steps

### Metrics to track post-redesign

| Metric | Current State | Target |
| --- | --- | --- |
| Login success rate | Users report 5+ failed attempts | First-attempt success > 90% |
| Cash-in reflection time | 24+ hours reported | Under 5 minutes |
| Support ticket resolution | "Months" per user reports | Under 48 hours |
| 1-star review rate per version | 35% baseline | Under 25% |
| "Switched to GCash" mentions | Active trend in reviews | Declining quarter-over-quarter |

### What's next

- [ ]  Usability testing with 3 segments: first-time users, power users, OFWs
- [ ]  Test on budget Android devices (Samsung, Xiaomi, Oppo) with slow connectivity
- [ ]  Test with elderly users (font size, navigation clarity)
- [ ]  Implement Tagalog/Filipino language support
- [ ]  Run the agent monthly to track improvement trends

---

## Tech Stack

| Component | Technology |
| --- | --- |
| Language | Python 3.11+ |
| LLM | Gemini 2.0 Flash (via Google AI API) |
| Scraping | google-play-scraper, app-store-scraper |
| Data | pandas, JSON checkpoints |
| Visualization | matplotlib |
| CLI | Rich (progress bars, tables, panels) |
| Config | YAML + dotenv |
| Alternative backend | Ollama (local, free) |

---

*Built by Manpreet Bhattee | February 2026*
