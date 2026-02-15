# Maya Review Agent — AI-Powered UX Intelligence

> An AI agent that scrapes 20,000+ app reviews and turns them into ranked, screen-level UX insights for fintech product teams.

---

## Page Structure

> This is the **master page** for the Maya Review Agent project. It follows a narrative arc: why we built it, how it works, what it found, and what to do next. Each section below maps to a **sub-page in Notion** — link them as nested pages under this master page.

| # | Sub-Page | What It Covers |
|---|---|---|
| 1 | **The Problem** | Why Maya is losing users — context and motivation |
| 2 | **How the Agent Works** | The 8-step pipeline, architecture, technical process |
| 3 | **Findings: All Reviews** | Full analysis of 12,345 reviews (mixed ratings) |
| 4 | **Findings: 1-Star Deep Dive** | Focused analysis of 2,703 1-star reviews only |
| 5 | **The Full Research Hub** | Complete data — every issue, journey, screen, segment, month |
| 6 | **What to Do Next** | Design recommendations, metrics, validation plan |

---

---

# 1. The Problem

> **Why we built this.** Maya is a top Philippine digital bank — but users are leaving. The app store reviews explain exactly why, if you can read 12,000 of them.

---

## Context

Maya (formerly PayMaya) serves millions of Filipinos for payments, transfers, savings, loans, and crypto. Despite strong product fundamentals, the app's ratings have been declining steadily.

| Metric | Value |
|---|---|
| **Reviews analyzed** | 12,345 |
| **Period** | August 2025 — February 2026 |
| **Overall sentiment** | Mixed-negative |
| **Average rating** | ~3.4 / 5 |
| **1-star review baseline** | 35% of all reviews |

## The Core Insight

Negative reviews are the most specific, actionable UX research most teams never read. Users describe **exact screens**, **exact errors**, and **exact moments** of frustration — at a scale no human team can process manually.

> "I've tried several times today, but I can't get in."

> "My phone was stolen and the hacker was able to access this app and took my savings and made loan in a snap of a finger."

> "I tried calling your toll-free hotline, but no one answered."

> "The screen showed that it was successful, but the money never reflected on my balance until more than a day later."

These aren't edge cases. **4 of the top 5 issues** carry severity 5/5 with high frequency. Maya doesn't have a feature problem — it has a **trust crisis**.

## The Challenge

| Manual approach | Time |
|---|---|
| Read 12,345 reviews | ~200 hours |
| Categorize and tag each review | ~100 hours |
| Cross-reference with competitor data | ~40 hours |
| Track trends month-over-month | Ongoing |
| **Total** | **~340+ hours** |

**What if an AI agent could do this in 15 minutes?**

---

---

# 2. How the Agent Works

> **The technical process.** An 8-step Python pipeline powered by Gemini 2.0 Flash that scrapes, analyzes, maps, benchmarks, and reports — in a single command.

---

## One Command

```
python main.py --months 12 --stars 1,2
```

**Input:** App store review data (Google Play + iOS, Maya + GCash)
**Output:** Ranked UX report, 9 charts, journey friction map, competitor benchmark

## The 8-Step Pipeline

| Step | Module | What Happens | Uses LLM? | Output File |
|---|---|---|---|---|
| 1 | **Scraper** | Pulls 20,000+ reviews from Google Play & iOS App Store | No | `raw_reviews.csv`, `gcash_reviews.csv` |
| 1.5 | **Data Quality** | Validates data before analysis (empty reviews, date gaps, sample size) | No | Pass/fail gate |
| 2 | **Temporal Analyzer** | Analyzes reviews month-by-month, classifies trends, detects version spikes | Yes | `temporal_analysis.json` |
| 3 | **Comprehensive Analyzer** | Deep categorization — issue type, journey, severity, screen, UI element | Yes | `comprehensive_analysis.json` |
| 4 | **Funnel Analyzer** | Detects retry behavior, abandonment signals, screen-level drop-offs | Yes | `funnel_analysis.json` |
| 5 | **Accessibility Analyzer** | Flags device, connectivity, and edge-case issues (Philippines market) | Yes | `accessibility_analysis.json` |
| 6 | **Competitor Analyzer** | Benchmarks Maya vs. GCash using both apps' reviews | Yes | `competitor_comparison.json` |
| 7 | **Screenshot Scraper** | Downloads current app store screenshots for visual reference | No | `screenshots/` |
| 8 | **Insights Generator** | Synthesizes everything into ranked report + 9 auto-generated charts | Yes | `maya_insights_report.md` |

## Step-by-Step Breakdown

### Step 1 — Scraping Reviews

Collects reviews from both platforms for both apps:

- **Google Play:** Batches of 200, up to 10,000 reviews per app, 1.5s delay between batches
- **iOS App Store:** Tries Philippines store first, then US/GB fallback, up to 5,000 reviews
- **Output:** CSV files with date, rating, text, app_version, platform

If cached CSVs exist, scraping is skipped automatically. Use `--fresh` to force re-scrape.

### Step 2 — Temporal Analysis

Tracks how issues evolve over time:

1. Groups reviews by calendar month
2. Samples up to **150 reviews per month** (stratified by rating)
3. Sends each month to Gemini: "Extract pain points with severity, frequency, business impact"
4. Classifies trends across months: **resolved**, **persistent**, or **emerging**
5. Calculates 1-star rate per app version
6. Flags versions with 1-star rate **+10 points above baseline**
7. Deep-dives flagged versions with up to 80 negative reviews

### Step 3 — Comprehensive Analysis

The deepest analysis layer:

1. Creates **stratified sample** ensuring rating + platform diversity
2. Splits into **5 chunks of 200 reviews** each
3. Each chunk analyzed for:
   - Critical pain points (with trigger action, UI element, expected vs actual behavior, screen location)
   - Competitive insights
   - Trust & security concerns
   - Feature requests
   - Positive signals (what to preserve)
   - User segments
4. **Synthesis step** merges chunks — deduplicates, adjusts severity based on recurrence

### Step 4 — Funnel Analysis

Two-pass approach (regex first, then LLM):

**Pass 1 — Free regex scan** tags every review:

| Signal | Pattern examples |
|---|---|
| **Retry** | "tried 5 times", "keeps failing", "every time" |
| **Abandonment** | "gave up", "switched to GCash", "uninstalled" |
| **Multi-step failure** | "entered my number, then... but it crashed" |

**Pass 2 — LLM deep analysis** on tagged reviews only (up to 300), mapping drop-offs to specific screens.

### Step 5 — Accessibility Analysis

Same two-pass approach, targeting Philippines-market signals:

| Signal | What it catches |
|---|---|
| **Devices** | Samsung, Xiaomi, Oppo, "old phone", "budget phone" |
| **Connectivity** | "slow internet", "no signal", "province" |
| **Accessibility** | "text too small", "lola" (grandmother), "Tagalog" |
| **Edge cases** | "phone stolen", "OFW", "dual SIM", "expired ID" |

### Step 6 — Competitor Comparison

Samples 150 reviews from each app (Maya + GCash), sends both to Gemini in a single call:

> "Compare these reviews. Identify each app's strengths, feature gaps, shared pain points."

Without GCash data, "users are concerned about security" is feedback. With it, "users are switching to GCash specifically because of security" is market intelligence.

### Step 7 — Screenshot Scraping

Downloads app store screenshots for visual reference. No LLM. Key finding: all 7 Google Play screenshots show happy-path marketing flows — **none show the friction screens** identified in the analysis.

### Step 8 — Insights Generation

Final synthesis:

1. Condenses all prior analyses
2. Sends to Gemini for ranking by **priority score** (severity x frequency x business impact)
3. Generates **9 charts** via matplotlib
4. Builds **journey friction map** (screen-level)
5. Renders full **Markdown report**

## Architecture Decisions

| Decision | Rationale |
|---|---|
| **Gemini 2.0 Flash** over GPT-4 | Faster and cheaper for high-volume classification |
| **Dual-platform scraping** | Google Play + iOS surfaces different issue profiles |
| **Competitor scraping** | GCash reviews provide benchmark context |
| **Regex pre-filtering** (Steps 4-5) | Reduces LLM calls by 80% — only send signal-rich reviews |
| **Chunked analysis** (Step 3) | 200-review chunks get deeper attention than 1,000 in one call |
| **JSON checkpoints** | Every step caches output — interrupted runs resume automatically |
| **Ollama fallback** | Free local alternative for testing without API key |

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| LLM | Gemini 2.0 Flash (cloud) / Ollama llama3.1:8b (local) |
| Scraping | google-play-scraper, app-store-scraper |
| Data | pandas, JSON checkpoints |
| Visualization | matplotlib (9 auto-generated charts) |
| CLI | Rich (progress bars, colored tables, panels) |
| Config | YAML + dotenv + environment variable overrides |

---

---

# 3. Findings: All Reviews (12,345)

> **The full picture.** What the agent found across all ratings — 1-star through 5-star — over 7 months.

---

## Executive Summary

| Metric | Value |
|---|---|
| **Reviews analyzed** | 12,345 |
| **Period** | August 2025 — February 2026 |
| **Overall sentiment** | Mixed-negative |
| **Top persistent issues** | Payment issues (7 months), KYC/onboarding (7 months), Loan/credit (6 months) |
| **Emerging issues** | OTP failures (Feb 2026), Transfer delays (Feb 2026), Savings problems (Jan 2026) |
| **Resolved / improving** | Security issues severity addressed, UI/UX frequency dropping |

## 9 Ranked UX Opportunities

| Rank | Issue | Severity | Frequency | Priority Score | Business Impact |
|---|---|---|---|---|---|
| 1 | **Login & Authentication Failures** | 5/5 | High | **18** | Activation, retention, trust, revenue |
| 2 | **Customer Service Unreachable** | 5/5 | High | **15** | Trust, revenue |
| 3 | **Unauthorized Transactions** | 5/5 | High | **15** | Trust, revenue |
| 4 | **Security Concerns** | 5/5 | High | **15** | Trust, revenue |
| 5 | **Cash-in Delays** | 4/5 | High | **14** | Transaction volume, trust |
| 6 | **Cash-in Transaction Failures** | 4/5 | High | **12** | Transaction volume, trust, revenue |
| 7 | **Customer Service Quality** | 4/5 | High | **12** | Trust, revenue |
| 8 | **Duplicate Account Issues** | 4/5 | Medium | **10** | Activation, retention, trust |
| 9 | **Data Privacy Concerns** | 3/5 | Low | **6** | Trust, revenue |

### Issue Details

**#1 — Login & Authentication Failures** (Score: 18)
> "I've tried several times today, but I can't get in."
> "It's like you don't even know when you'd be able to login to your account."

Affects every journey: onboarding, payments, transfers, savings, credit, crypto, support. Users report infinite loops, failed biometrics, OTP never arriving.

**#2 — Customer Service Unreachable** (Score: 15)
> "I tried calling your toll-free hotline, but no one answered."
> "My email messages get rejected when sent to your Maya support services."

Hotlines don't work. Emails bounce. Chatbot gives automated responses. Tickets vanish.

**#3 — Unauthorized Transactions** (Score: 15)
> "I had an unauthorized transaction of PHP 9,000 and it took them a month to resolve."
> "They kept saying my case is still ongoing, but I've been waiting for months."

Users report stolen funds with no recourse. Resolution takes months when it happens at all.

**#4 — Security Concerns** (Score: 15)
> "My phone was stolen and the hacker was able to access this app and took my savings and made loan in a snap of a finger."

Stolen phone = instant account drain + fraudulent loans. No emergency freeze mechanism.

**#5 — Cash-in Delays** (Score: 14)
> "The screen showed that it was successful, but the money never reflected on my balance until more than a day later."

"Success" screen doesn't mean success. Funds take 24+ hours to reflect.

## Funnel Drop-Off Hotspots

| Screen | Journey | Evidence | Severity |
|---|---|---|---|
| **Login > OTP Entry** | Onboarding | 45 reviews | 5/5 |
| **Cash In > Bank Integration** | Payments | 30 reviews | 4/5 |
| **KYC > Selfie Capture** | Onboarding | 25 reviews | 4/5 |
| **Crypto > Buy Token** | Crypto | 12 reviews | 3/5 |
| **Send Money > Contact Selection** | Transfers | 8 reviews | 2/5 |

The #1 drop-off is at the very first screen. Users never get past login.

## Version Spike: v2.148.3

| Metric | Value |
|---|---|
| **1-star rate** | 45.2% (vs. 34.6% baseline) |
| **Reviews** | 188 |
| **Period** | November 2025 — February 2026 |
| **Root causes** | Login regressions, payment failures, chatbot-only support |

A single release caused a **+10.6 percentage point** spike in 1-star reviews.

### All Versions by 1-Star Rate

| Version | Reviews | Avg Rating | 1-Star Rate | Status |
|---|---|---|---|---|
| v2.148.3 | 188 | 2.95 | 45.2% | SPIKE |
| v2.151.0 | 258 | 3.13 | 42.2% | |
| v2.147.1 | 679 | 3.30 | 36.8% | |
| v2.151.1 | 1,430 | 3.37 | 35.6% | |
| v2.145.0 | 582 | 3.34 | 35.1% | |
| v2.152.0 | 429 | 3.40 | 33.6% | |
| v2.146.0 | 665 | 3.40 | 33.2% | |
| v2.141.1 | 86 | 4.24 | 16.3% | Best |

## Temporal Trends

| Getting better | Getting worse |
|---|---|
| Login issues | Customer service |
| Cash-in delays | Unauthorized transactions |

| Persistent (6-7 months) | Emerging (Jan-Feb 2026) |
|---|---|
| Payment issues | OTP failures |
| KYC/onboarding | Transfer delays |
| Loan/credit | Savings problems |
| Customer support | |

## Competitive Position vs. GCash

| Dimension | Maya | GCash |
|---|---|---|
| **Security** | Weak (stolen phone = instant drain) | Multi-factor auth |
| **Data Privacy** | Low transparency | Better practices |
| **Transaction Speed** | Cash-in delays (24h+) | Fast processing |
| **Customer Support** | Dead hotlines, rejected emails | More responsive |
| **UI Design** | Users prefer Maya's design | Functional but less polished |
| **Features** | Broader (crypto, savings, loans) | More payment integrations |

Users actively switch to GCash citing reliability and security.

## Quick Wins (High Impact, Low Effort)

1. **Improve error messages** — Make them concise, actionable ("What went wrong + why + what to do")
2. **Simplify login screen** — Remove unnecessary fields, reduce friction
3. **Fix customer service channels** — Ensure hotlines actually connect

## Strategic Bets (High Impact, High Effort)

1. **Multi-factor authentication overhaul** — Biometric primary, fallback chain, stolen-phone recovery
2. **Backend cash-in optimization** — Real-time processing instead of 24h+ delays
3. **24/7 customer support with human escalation** — Replace chatbot-first with visible human paths

## Charts

The agent auto-generates 9 visualizations:

1. **Rating Trend Over Time** — Monthly average showing decline
2. **Sentiment Distribution** — Positive/negative/neutral split
3. **Business Impact** — Which issues affect which metrics
4. **Priority Scores** — Bar chart of all 9 ranked issues
5. **Severity vs. Frequency** — Scatter plot (upper-right = critical & common)
6. **Pain Point Frequency** — Which issues appear most
7. **Version Ratings** — 1-star rate per version (v2.148.3 spike)
8. **Issue Lifecycle** — How each issue trends over time
9. **Funnel Drop-off** — Where users abandon journeys

---

---

# 4. Findings: 1-Star Deep Dive (2,703 reviews)

> **The angriest users tell you the most.** Filtering to 1-star reviews only amplifies the signal — these users had the worst experiences and describe them in the most detail.

---

## Why a Separate 1-Star Analysis?

Mixed-rating analysis (Section 3) gives the balanced picture. But 1-star reviews are where users describe:
- The **exact screen** that broke
- The **exact error message** they saw
- The **exact moment** they decided to uninstall
- The **exact competitor** they switched to

Running the agent with `--stars 1` isolates this signal.

```
python main.py --skip-scrape --stars 1
```

## Executive Summary

| Metric | Value |
|---|---|
| **Reviews analyzed** | 2,703 (1-star only) |
| **Period** | August 2025 — February 2026 |
| **Overall sentiment** | Negative (by definition) |
| **Top persistent issues** | Customer support (7 months), UI/UX (7 months) |
| **Emerging issues** | Loans/credit (Sep 2025), Crypto (Sep 2025) |
| **Resolved** | Payment/transfer severity decreased significantly |

## Ranked Issues (1-Star Only)

| Rank | Issue | Severity | Frequency | Priority Score | Category |
|---|---|---|---|---|---|
| 1 | **Login Experience** | 5/5 | High | **19** | Strategic bet |
| 2 | **Customer Support** | 5/5 | High | **19** | Strategic bet |
| 3 | **UI/UX Issues** | 4/5 | Medium | **16** | Strategic bet |

### Key difference from the all-reviews analysis

In the full dataset, login scores 18. In 1-star only, it scores **19** — and ties with customer support. This confirms that login failures aren't just annoying — they're the **#1 reason users leave a 1-star review**.

Customer support also jumps to a tie for #1. When things break, users turn to support. When support fails too, that's when they leave 1-star reviews.

## User Voices (1-Star)

### Login
> "I've been trying to log in for days and it's still not working."
> "I'm frustrated with the constant login errors."

### Customer Support
> "I've been on hold for over an hour and still haven't spoken to a human."
> "The customer support is terrible, they just keep sending me automated responses."

### UI/UX
> "I tried to get it back through their chat support, but they couldn't help me."
> "It just keeps on taking my money..."

## Quick Wins from 1-Star Analysis

1. **Error message improvements** — The fastest way to reduce 1-star reviews. Users repeatedly mention confusing, unhelpful error messages.
2. **UI/UX fixes** — Specific screens mentioned in 1-star reviews are the highest-leverage targets.

## Competitive Signal from 1-Star Reviews

> "I tried calling their hotline but no one is entertaining us."
> "GCash has a more efficient customer support system."

1-star reviewers are the most likely to name competitors. They've already decided to leave — and they tell you where they're going.

## Trend from 1-Star Reviews

| Improving | Stable |
|---|---|
| Payment/transfer issues (severity decreasing) | Security concerns (unchanged) |

Payment issues improving in 1-star reviews is a positive signal — Maya's backend fixes are working for the most frustrated users. Security remains unchanged — no visible progress.

---

---

# 5. The Full Research Hub

> **Every data point, every journey, every screen, every month.** This is the comprehensive reference — the complete output of the Maya Review Agent.

---

## Journey Friction Map

> Friction scores are cumulative weighted values. Higher = more friction. They aggregate pain point count multiplied by severity.

| Journey | Friction Score | Pain Points | Priority | Top Issues |
|---|---|---|---|---|
| **General** | 110.4 | 12 | High | Security, Payments, KYC, Loans, Support |
| **Payments** | 24.0 | 2 | High | Cash-in Delays, Cash-In Failures |
| **Onboarding** | 23.0 | 2 | Critical | Login Failures, Duplicate Account Lockouts |
| **Transfers** | 15.0 | 1 | Critical | Unauthorized Transactions |
| **Support** | 15.0 | 1 | Critical | Unreachable Customer Service |

## Screen-Level Friction

### Critical Screens (Severity 5/5)

| Screen | Journey | Issue | Recommendation |
|---|---|---|---|
| **Login Screen** | Onboarding | Auth failures, biometric not prompting, OTP delays | Robust login with multiple auth methods |
| **Transfer — Recipient Selection** | Transfers | Unauthorized transactions occurring | Improve verification, add biometric confirmation |
| **Support — Contact Us Form** | Support | Form doesn't work, tickets vanish | Fix form + provide effective channels |
| **Security Settings** | General | Can't access or manage security settings | Improve settings UI and protection |

### High Priority Screens (Severity 4/5)

| Screen | Journey | Issue | Recommendation |
|---|---|---|---|
| **Account Creation / Verification** | Onboarding | Duplicate accounts, verification failures | Prevent duplicates, improve verification |
| **Cash In — Bank Account Selection** | Payments | Problems linking bank accounts | Simplify bank linking, better errors |
| **Transaction Confirmation** | Payments | Delays in confirmation, "success" lie | Improve processing, clearer status |
| **Payment History** | General | Problems viewing/managing history | Simplify history view |

## Flow Sequences

### Onboarding Flow

| Step | Screen | Known Issues | Drop-off Risk |
|---|---|---|---|
| 1 | Login Screen | Auth failures, biometric not prompting, OTP delays | HIGH |
| 2 | Account Creation / Verification | Duplicate accounts, KYC scanner fails, missing locations | HIGH |

### Payments Flow

| Step | Screen | Known Issues | Drop-off Risk |
|---|---|---|---|
| 1 | Cash In — Bank Account Selection | Bank linking errors | MEDIUM |
| 2 | Transaction Confirmation | Funds not reflecting for 24h+ | HIGH |

### Transfers Flow

| Step | Screen | Known Issues | Drop-off Risk |
|---|---|---|---|
| 1 | Transfer — Recipient Selection | Unauthorized transactions | CRITICAL |

### Support Flow

| Step | Screen | Known Issues | Drop-off Risk |
|---|---|---|---|
| 1 | Support — Contact Us Form | Form doesn't work, tickets vanish | CRITICAL |

## Competitive Analysis: Maya vs. GCash

| Dimension | Maya | GCash | Gap |
|---|---|---|---|
| **Security** | Stolen phone = instant drain | Multi-factor auth | Maya needs MFA |
| **Data Privacy** | Low transparency | Better practices | Maya needs clear policy |
| **Transaction Speed** | Cash-in delays (24h+) | Fast processing | Maya needs backend optimization |
| **Customer Support** | Dead hotlines, rejected emails | More responsive | Maya needs 24/7 support |
| **UI Design** | Users prefer Maya's design | Functional but less polished | Maya advantage — preserve |
| **Features** | Broader (crypto, savings, loans) | More payment integrations | Mixed |

**Key risk:** Users actively switching to GCash citing reliability and security.

## User Segments

| Segment | Presence | Needs | Frustrations | Opportunity |
|---|---|---|---|---|
| **First-time users** | High | Ease of use, convenience | Login failures, security concerns | Improve onboarding, reduce friction |
| **Power users** | Medium | Enhanced security, advanced features | Limited customization, inconsistent support | Robust security, advanced features |
| **Credit users** | Low | Easy features, competitive rates | Difficulty accessing credit, high fees | Simplify credit UX, reduce fees |

## Positive Signals (Preserve These)

| Signal | Frequency | Context |
|---|---|---|
| **User-friendly interface** | High | Consistently praised, preferred over GCash |
| **Easy onboarding** (when working) | High | Quick registration and verification |
| **Convenient payment options** | Medium | Broad bill pay and transfer coverage |
| **Savings feature** | Medium | Interest rates and goal-based saving |
| **Crypto access** | Medium | Small-amount crypto buying valued |

## Feature Requests (User-Driven)

### High Priority
- Tap To Pay (GCash parity)
- Watch Pay (GCash parity)
- Biometric approval for QR payments
- Fingerprint login as primary
- Email OTP / 2FA via authenticator app
- Photo upload alternative for KYC
- Improved customer support (human agents)

### Medium Priority
- Higher credit limits
- Personal loan expansion
- Enhanced crypto trading
- Simplified KYC process

## Monthly Breakdown

### August 2025
**Pain Points:** Login (4/5), Payments (4/5), Customer Support (4/5), KYC (4/5), Loans (3/5), Security (3/5), Performance (3/5)
**Feature Requests:** Email OTP/2FA (high), Improved Support (high)
**Positive:** Convenience (high), Security perception (medium)

### September 2025
**Pain Points:** Payments (4/5), Loans (4/5), KYC (3/5), Support (3/5), Security (2/5)
**Feature Requests:** Crypto Support (high), Personal Loan (medium)
**Positive:** Convenience/Ease of Use (high)

### October 2025
**Pain Points:** Login (4/5), Loans (4/5), Support (4/5), Security (5/5), KYC (3/5), UI/UX (3/5)
**Feature Requests:** Night Mode (low), QR Code Payment (low)
**Positive:** Convenience (high)

### November 2025
**Pain Points:** Payments (4/5), Loans (4/5), KYC (3/5), Support (3/5), Security (3/5)
**Feature Requests:** Photo ID Upload (high), Improved Loan Process (high)
**Positive:** Convenience (high)

### December 2025
**Pain Points:** Payments (4/5), Loans (4/5), Support (4/5), KYC (3/5), Crypto (3/5)
**Feature Requests:** Higher Credit Limits (high), Better Support (high)
**Positive:** Convenience/Ease of Use (high)

### January 2026
**Pain Points:** Support (4/5), Payments (4/5), KYC (3/5), Loans (3/5), Savings (2/5)
**Feature Requests:** Improved Support (high), Enhanced Payments (high)
**Positive:** User-Friendly Interface (high), Convenience (high)

### February 2026
**Pain Points:** Login (4/5), OTP (4/5), Transfers (4/5), Loans (4/5), Crypto (4/5), Support (4/5), Security (4/5)
**Feature Requests:** Tap To Pay (high), Watch Pay (high), Biometric Approval (high), Fingerprint Login (high)
**Positive:** Easy to Use (high), Convenient (high)

## App Store Screenshots

7 screenshots captured from Google Play — all marketing images showing happy-path flows:

| # | Screen | Covers Friction? |
|---|---|---|
| 01 | Wallet / Home Dashboard | Partially (Cash In entry) |
| 02 | Maya Black Credit Card promo | No |
| 03 | Credit Card Management | No |
| 04 | Credit Card Approval | No |
| 05 | Credit Card Freeze/Unfreeze | Partially (security) |
| 06 | Savings Screen | No |
| 07 | Personal Loan Screen | No |

**None of the critical friction screens** (login, KYC, cash-in confirmation, support form) appear in the app store listing.

---

---

# 6. What to Do Next

> **From insights to action.** Design recommendations mapped directly to agent findings, with timelines, metrics, and validation plan.

---

## 4 Design Flows (Mapped to Top Issues)

### Flow A: Frictionless Login
**Addresses:** Login failures (#1, Priority 18)

| Element | Design |
|---|---|
| **Primary auth** | Biometric (Face ID / fingerprint) — one tap to enter |
| **Fallback chain** | Biometric → password → email OTP → support escalation |
| **Error states** | Clear messaging: what went wrong + why + what to do next |
| **Login screen** | Simplified — remove unnecessary fields |

### Flow B: Transparent Transactions
**Addresses:** Cash-in delays (#5, Priority 14)

| Element | Design |
|---|---|
| **Timeline view** | Request Sent → Processing → Received (real-time updates) |
| **Pending dashboard** | Track all in-transit funds in one place |
| **Push notifications** | Alert at each state change |
| **Retry/cancel** | Flows for stuck transactions |

### Flow C: Accessible Support
**Addresses:** Customer service unreachable (#2, Priority 15)

| Element | Design |
|---|---|
| **Ticket dashboard** | "My Tickets" on Help Center home with status pills |
| **Human escalation** | Visible paths — not buried behind chatbot |
| **Contextual help** | Help buttons at high-friction screens (login, KYC, transfer) |
| **Status tracking** | Investigating → In Progress → Resolved with timestamps |

### Flow D: Security Center
**Addresses:** Unauthorized transactions + security (#3-4, Priority 15)

| Element | Design |
|---|---|
| **Kill Switch** | One-tap freeze all cards and accounts |
| **Safety Score** | Visual shield with percentage indicator |
| **Active sessions** | See all logged-in devices, remote logout |
| **Stolen phone flow** | Remote lock, freeze, recovery without SIM |

## Implementation Timeline

### Phase 1: Immediate (Week 1-2)
- [ ] Login & auth redesign — audit full flow, map every error, design fallback chain
- [ ] Security & trust sprint — stolen-phone emergency flow, biometric transaction approval

### Phase 2: Short-Term (Week 3-6)
- [ ] Payment flow fixes — real-time status, pending dashboard, retry/cancel
- [ ] Customer support overhaul — human escalation, ticket tracker, contextual help
- [ ] Error messaging system — rewrite all error messages with actionable copy

### Phase 3: Medium-Term (Month 2-3)
- [ ] KYC/onboarding redesign — photo upload, fix address dropdowns, progress save-state
- [ ] Accessibility & inclusion — font size controls, Tagalog, low-bandwidth, budget devices
- [ ] Competitive parity — Tap To Pay, Watch Pay, biometric QR approval

### Phase 4: Validation
- [ ] Usability testing — 3 segments (first-time, power users, OFWs)
- [ ] Budget device testing — Samsung, Xiaomi, Oppo on slow connectivity
- [ ] Elderly user testing — font size, navigation clarity

## Success Metrics

| Metric | Current State | Target |
|---|---|---|
| **Login success rate** | Users report 5+ failed attempts | >90% first-attempt success |
| **Cash-in reflection time** | 24+ hours | Under 5 minutes |
| **Support ticket resolution** | "Months" per user reports | Under 48 hours |
| **1-star review rate per version** | 35% baseline | Under 25% |
| **"Switched to GCash" mentions** | Active trend in reviews | Declining quarter-over-quarter |

## Running the Agent Monthly

The agent is designed to run monthly to track improvement:

```
python main.py --months 1 --skip-scrape
```

Compare monthly outputs to measure:
- Are priority scores decreasing?
- Are persistent issues becoming resolved?
- Are new emerging issues appearing?
- Is the 1-star baseline dropping?

---

---

## How to Set This Up in Notion

### Page hierarchy

```
Maya Review Agent (this master page)
├── 1. The Problem
├── 2. How the Agent Works
├── 3. Findings: All Reviews (12,345)
├── 4. Findings: 1-Star Deep Dive (2,703)
├── 5. The Full Research Hub
└── 6. What to Do Next
```

### Setup instructions

1. Create a new Notion page titled **"Maya Review Agent"**
2. Paste the top-level overview and page structure table
3. Create **6 sub-pages** (one for each section)
4. Copy each section's content into its sub-page
5. Upload the 9 chart PNGs from `data/charts/` as image blocks in Sections 3 and 5
6. Upload app screenshots from `data/screenshots/` in Section 5
7. Add a **cover image** — use `data/charts/priority_scores.png` or `data/charts/rating_trend.png`
8. Add an **icon** — use a bar chart or robot emoji

### Callout blocks

In Notion, convert these blockquotes to **callout blocks** for visual impact:
- User quotes → Yellow callout with speech bubble icon
- Key insights → Blue callout with lightbulb icon
- Warnings/risks → Red callout with warning icon

---

*Maya Review Agent | Built by Manpreet Bhattee | February 2026*
