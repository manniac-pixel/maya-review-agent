# How the Maya Review Agent Works

> A behind-the-scenes look at the AI-powered pipeline that turns 20,000+ app reviews into actionable UX insights.

---

## Overview

| Field | Value |
|---|---|
| **Agent** | Maya Review Agent |
| **Language** | Python 3.11+ |
| **LLM** | Gemini 2.0 Flash (Google AI) |
| **Reviews Processed** | 12,345 Maya + 10,000+ GCash |
| **Pipeline Steps** | 8 |
| **Total Runtime** | ~15 minutes (full run) |
| **Output** | Ranked report, 9 charts, journey map, competitor benchmark |

---

## The Pipeline at a Glance

```
python main.py --months 12 --stars 1,2
```

| Step | Module | What Happens | LLM? | Output |
|---|---|---|---|---|
| 1 | `scraper.py` | Scrape 20,000+ reviews from Google Play & iOS | No | `raw_reviews.csv`, `gcash_reviews.csv` |
| 2 | `temporal_analyzer.py` | Analyze reviews month-by-month, detect version spikes | Yes | `temporal_analysis.json` |
| 3 | `comprehensive_analyzer.py` | Deep categorization of every review | Yes | `comprehensive_analysis.json` |
| 4 | `funnel_analyzer.py` | Find retry behavior, abandonment, drop-off points | Yes | `funnel_analysis.json` |
| 5 | `accessibility_analyzer.py` | Flag device, connectivity, and edge-case issues | Yes | `accessibility_analysis.json` |
| 6 | `competitor_analysis.py` | Compare Maya vs. GCash | Yes | `competitor_comparison.json` |
| 7 | `screenshot_scraper.py` | Download current app store screenshots | No | `screenshots/` folder |
| 8 | `insights_generator.py` | Synthesize everything into final report | Yes | `maya_insights_report.md` + 9 charts |

Every step caches its output to a JSON or CSV file. If the pipeline is interrupted, re-running the same command **resumes from the last completed step** — no wasted API calls.

---

## Step 1: Scraping Reviews

### What it does

Collects real user reviews from two sources, for two apps:

| Source | Maya | GCash |
|---|---|---|
| Google Play | `com.paymaya` | `com.globe.gcash.android` |
| iOS App Store | Maya (ID from config) | GCash (ID from config) |

### How it works

1. **Google Play scraping** — Uses the `google-play-scraper` library
   - Pulls reviews in batches of 200 (up to 50 batches = 10,000 max)
   - 1.5-second sleep between batches to avoid rate limiting
   - Filters by date cutoff (e.g., last 12 months)

2. **iOS App Store scraping** — Uses the `app-store-scraper` library
   - Tries Philippines store first, then falls back to US/GB
   - Extracts up to 5,000 reviews per country

3. **Combine & clean** — Merges both platforms into a single DataFrame
   - Removes reviews with empty text
   - Sorts by date (newest first)
   - Saves to `raw_reviews.csv`

4. **Repeat for GCash** — Same process, saves to `gcash_reviews.csv`

### What each review looks like

| Field | Example |
|---|---|
| `date` | 2026-01-15 |
| `rating` | 1 |
| `text` | "I can't log in after the update. Tried 5 times." |
| `app_version` | v2.148.3 |
| `platform` | android |

### Caching

If `raw_reviews.csv` already exists, this step is skipped entirely. Use `--fresh` to force a re-scrape.

---

## Step 1.5: Data Quality Checks

### What it does

Before any analysis begins, the agent validates the scraped data to catch problems early.

### Checks performed

| Check | What it verifies | Fail condition |
|---|---|---|
| **Reviews exist** | DataFrame is not empty | 0 reviews = hard fail |
| **Required columns** | date, rating, text, platform all present | Missing column = hard fail |
| **Date range** | How many months of data we have | Most recent review > 60 days old = warning |
| **Monthly gaps** | Identifies months with zero reviews | Gap months = warning |
| **Sample size** | Minimum reviews per platform | < 30 total or < 10 per platform = warning |

### Why this matters

Bad data in = bad insights out. If the scraper only captured 50 reviews from 1 month, the trend analysis would be meaningless. This step catches that before spending API credits.

---

## Step 2: Temporal Analysis

### What it does

Analyzes reviews **month by month** to understand how issues change over time. Also detects **version-specific regressions**.

### How it works

**Part A — Monthly Analysis:**

1. Groups reviews by calendar month
2. For each month, samples up to **150 reviews** (stratified by rating, favoring longer reviews)
3. Sends each month's sample to Gemini with this prompt structure:

> "Analyze these [N] reviews from [Month Year]. Extract: pain_points (with severity 1-5, frequency, business_impact), feature_requests, positive_mentions, competitive_comparisons."

4. Waits **10 seconds** between API calls (rate limiting)

**Part B — Trend Classification:**

5. Once all months are analyzed, sends the monthly summaries to Gemini:

> "Given these monthly analyses, classify each issue as: resolved, persistent, or emerging."

**Part C — Version Spike Detection:**

6. Calculates 1-star rate per app version (pure math, no LLM)
7. Flags versions where 1-star rate exceeds baseline by **+10 percentage points**
8. For flagged versions, sends up to **80 negative reviews** to Gemini:

> "This version has 45% 1-star rate vs 35% baseline. Analyze these reviews to determine root cause."

### What it found for Maya

| Finding | Detail |
|---|---|
| **Persistent (7 months)** | Payment issues, KYC, customer support |
| **Emerging (Feb 2026)** | OTP failures, transfer delays |
| **Improving** | Login issues, cash-in delays |
| **Version spike** | v2.148.3 — 45.2% 1-star (login regressions + chatbot-only support) |

### Output

`temporal_analysis.json` — Contains monthly results, trend classifications, and version spike analyses.

---

## Step 3: Comprehensive Analysis

### What it does

The deepest analysis step. Reads **all reviews** (not just monthly slices) and extracts detailed UX insights with screen-level specificity.

### How it works

1. Takes the full review dataset and creates a **stratified sample** ensuring rating and platform diversity
2. Splits into **up to 5 chunks** of 200 reviews each
3. Each chunk is sent to Gemini with a detailed prompt asking for:

| Category | What it extracts |
|---|---|
| **Critical pain points** | Issue, severity, frequency, affected journey, trigger action, UI element, expected vs actual behavior, screen location, error messages |
| **Competitive insights** | Where users mention competitors and why |
| **Trust & security concerns** | Specific fears and incidents |
| **Feature requests** | What users explicitly ask for |
| **Positive signals** | What's working well (to preserve) |
| **User segments** | Who's complaining and what they need |

4. After all chunks are analyzed, a **synthesis step** merges results:
   - Deduplicates similar findings across chunks
   - Adjusts severity/frequency based on recurrence
   - Preserves the most specific user quotes

### Why chunking matters

Gemini 2.0 Flash has context limits. Sending 1,000 reviews in one call would exceed the window or produce shallow analysis. By chunking into 200-review batches, each chunk gets deep attention, then synthesis creates the unified view.

### Output

`comprehensive_analysis.json` — The richest data file. Contains every pain point with screen-level detail, user quotes, and business impact classification.

---

## Step 4: Funnel Analysis

### What it does

Detects **where users get stuck, retry, and give up** — the behavioral signals that indicate specific screens are broken.

### How it works

This step uses a **two-pass approach**: regex first (free), then LLM (targeted).

**Pass 1 — Regex Signal Extraction (no LLM cost):**

Scans every review for three types of behavioral language:

| Signal Type | Regex Examples | What it means |
|---|---|---|
| **Retry** | "tried 5 times", "keeps failing", "every time I try" | User is stuck in a loop |
| **Abandonment** | "gave up", "switched to GCash", "uninstalled" | User left permanently |
| **Multi-step failure** | "entered my number, then... but it crashed" | A specific flow is broken at a specific step |

Each review gets tagged: `has_retry`, `has_abandonment`, `has_multi_step`.

**Pass 2 — LLM Deep Analysis:**

Only the tagged reviews (up to 300) are sent to Gemini:

> "These reviews contain funnel signals [RETRY], [ABANDON], [MULTI-STEP]. Analyze for: retry patterns (how many attempts, what outcome), abandonment drivers, multi-step failures, and drop-off hotspots (which screen, which step)."

### What it found

| Drop-off Screen | Severity | Evidence |
|---|---|---|
| Login > OTP Entry | 5/5 | 45 reviews |
| Cash In > Bank Integration | 4/5 | 30 reviews |
| KYC > Selfie Capture | 4/5 | 25 reviews |
| Crypto > Buy Token | 3/5 | 12 reviews |
| Send Money > Contact Selection | 2/5 | 8 reviews |

### Output

`funnel_analysis.json` — Signal breakdown counts + LLM analysis of retry patterns, abandonment drivers, and screen-level drop-off hotspots.

---

## Step 5: Accessibility Analysis

### What it does

Identifies issues specific to the **Philippines market context** — budget devices, slow connectivity, elderly users, OFWs (overseas Filipino workers), and other edge cases.

### How it works

Same two-pass approach as funnel analysis:

**Pass 1 — Regex Signal Extraction:**

| Signal Type | What it catches |
|---|---|
| **Device mentions** | Samsung, Xiaomi, Oppo, iPhone, "old phone", "budget phone" |
| **Connectivity** | "slow internet", "no signal", "province", "mobile data", "timeout" |
| **Accessibility** | "text too small", "can't read", "Tagalog", "senior", "lola" (grandmother) |
| **Edge cases** | "phone stolen", "SIM change", "OFW", "dual SIM", "expired ID", "minor" |

Brand names are normalized (e.g., "Galaxy" → "Samsung") and counted.

**Pass 2 — LLM Analysis:**

Up to 250 tagged reviews sent to Gemini for structured analysis of connectivity issues, device compatibility gaps, accessibility needs, and edge-case user flows.

### Why this matters

Maya's user base includes:
- **Budget Android users** (Samsung, Xiaomi, Oppo) on slow connections
- **OFWs abroad** sending money home with different SIM/network conditions
- **Elderly users** ("lola") who need larger text and simpler flows
- **Users with stolen phones** who need emergency account recovery without the original SIM

Generic UX analysis misses these. This step surfaces them specifically.

### Output

`accessibility_analysis.json` — Device distribution, connectivity issues, accessibility gaps, and edge-case flows with recommendations.

---

## Step 6: Competitor Comparison

### What it does

Benchmarks Maya against GCash by analyzing **both apps' reviews side by side**.

### How it works

1. Samples **150 reviews from each app** (stratified by rating for fair comparison)
2. Formats them with ratings and dates
3. Sends both sets to Gemini in a single prompt:

> "Compare these Maya and GCash reviews. Identify: GCash strengths (with user evidence), Maya strengths (with user evidence), feature gaps, shared pain points, and rating comparison."

### What it found

| Dimension | Maya | GCash |
|---|---|---|
| **Security** | Weak (stolen phone = instant drain) | Multi-factor auth |
| **Transaction Speed** | Cash-in delays (24h+) | Fast processing |
| **Support** | Dead hotlines | More responsive |
| **UI Design** | Users prefer Maya | Functional but less polished |
| **Features** | Broader (crypto, savings) | More payment integrations |

### Why scrape the competitor?

Without GCash data, findings like "users are concerned about security" lack context. With GCash data, we can say: "Users are **switching** to GCash **specifically because** of security — here are their exact words." That's a fundamentally different conversation with stakeholders.

### Output

`competitor_comparison.json` — Structured comparison with user evidence, feature gaps, and shared pain points.

---

## Step 7: Screenshot Scraping

### What it does

Downloads the current app store screenshots for visual reference. No LLM involved.

### How it works

1. Fetches Maya's Google Play listing metadata
2. Downloads all promotional screenshots to `data/screenshots/google_play/`
3. Fetches iOS screenshots via iTunes Lookup API
4. Saves to `data/screenshots/ios/`

### What we learned

The 7 screenshots from Google Play are all **marketing images** showing happy-path flows (wallet, credit card, savings). **None of them show the friction screens** identified in the analysis — login, KYC, cash-in confirmation, support form.

This gap itself is an insight: the app store presence doesn't reflect the actual user experience.

### Output

`screenshots/` folder + `screenshots_manifest.json` metadata.

---

## Step 8: Insights Generation

### What it does

The final synthesis. Combines **all previous analyses** into a single ranked report with charts.

### How it works

1. **Condenses** temporal and comprehensive data (strips raw reviews to save context)
2. Sends condensed data to Gemini:

> "Synthesize these analyses into: executive_summary, ranked_ux_opportunities (with priority scores), quick_wins, strategic_bets, competitive_gaps, user_segments, trend_summary."

3. **Generates 9 charts** using matplotlib:

| Chart | What it shows |
|---|---|
| `rating_trend.png` | Monthly average ratings |
| `sentiment_distribution.png` | Positive / negative / neutral split |
| `business_impact.png` | Which issues affect which metrics |
| `priority_scores.png` | Bar chart of all ranked issues |
| `severity_frequency.png` | Scatter plot (critical & common quadrant) |
| `pain_point_frequency.png` | Issue frequency counts |
| `version_ratings.png` | 1-star rate per version |
| `issue_lifecycle.png` | Issue trends over time |
| `funnel_dropoff.png` | Drop-off points in user journeys |

4. **Builds journey friction map** — Maps pain points to specific screens and flows
5. **Renders Markdown report** — Combines everything into `maya_insights_report.md`

### The priority scoring formula

Each issue is scored by: **Severity (1-5) x Frequency weight x Business Impact count**

| Issue | Severity | Frequency | Impacts | Score |
|---|---|---|---|---|
| Login failures | 5 | High (x1.0) | 4 areas | **18** |
| Customer service | 5 | High (x1.0) | 2 areas | **15** |
| Cash-in delays | 4 | High (x1.0) | 2 areas | **14** |

This ensures issues that are both severe AND frequent AND business-critical rise to the top.

### Output

- `final_insights.json` — Structured insights data
- `maya_insights_report.md` — The human-readable report (346 lines)
- `data/charts/` — 9 PNG visualization files
- `journey_map.json` — Screen-level friction mapping

---

## Technical Architecture

### LLM Layer (`llm.py`)

The agent supports two backends:

| Backend | Model | Cost | Speed | When to use |
|---|---|---|---|---|
| **Gemini** | gemini-2.0-flash | ~$0.10/run | Fast | Production runs, full analysis |
| **Ollama** | llama3.1:8b | Free | Slower | Testing, development, no API key needed |

**Rate limit handling:**
- Catches HTTP 429 errors from Gemini
- Parses `retry-after` headers
- Base retry delay: 60 seconds
- Exponential backoff with jitter (up to 4 retries)
- Temperature: 0.2 (low — we want consistent categorization, not creativity)

### Configuration (`config.py`)

All parameters are configurable via `config.yaml` or environment variables:

```
MAYA_SCRAPER__GPLAY_BATCH_SIZE=200
MAYA_TEMPORAL__MAX_REVIEWS_PER_MONTH=150
MAYA_LLM__GEMINI_MODEL=gemini-2.0-flash
```

### Caching & Resume

Every step saves its output to a JSON file. The pipeline checks for existing files before running each step:

```
if temporal_analysis.json exists → skip step 2
if comprehensive_analysis.json exists → skip step 3
...
```

This means:
- **Interrupted runs resume automatically**
- **Re-analysis of specific steps** is possible by deleting that step's JSON file
- **`--fresh` flag** clears all cached files and runs from scratch

### CLI Experience

The agent uses **Rich** for terminal output:

- Color-coded progress bar showing current step
- Percentage completion and elapsed time
- Completion banner with all output file paths
- Table formatting for quick review of results

---

## What Makes This Agent Different

### vs. Manual review tagging

| Manual | Agent |
|---|---|
| Read 12,000 reviews one by one | Processes all 12,000 in minutes |
| Subjective severity ratings | Consistent scoring across all reviews |
| One-time snapshot | Re-runnable monthly to track trends |
| No competitor context | Built-in GCash benchmarking |

### vs. App Store Connect / Google Play Console analytics

| Store analytics | Agent |
|---|---|
| Rating counts and averages | Issue categorization by type, journey, screen |
| No text analysis | Full NLP on every review |
| No version spike root cause | Automatic version regression detection |
| No competitor data | Side-by-side competitor comparison |

### vs. Generic sentiment analysis tools

| Generic tools | Agent |
|---|---|
| "Positive / Negative / Neutral" | 9 ranked issues with severity, frequency, business impact |
| No domain awareness | Philippines-market context (OFWs, budget devices, Tagalog) |
| No screen-level mapping | Maps issues to specific screens and user journeys |
| Static output | Temporal trending — what's getting better vs worse |

---

## Running the Agent

### Quick start

```bash
# Full run (scrape + analyze)
python main.py --months 12

# Analyze only 1-star reviews (strongest signal)
python main.py --skip-scrape --stars 1

# Use free local LLM (no API key needed)
python main.py --backend ollama --skip-scrape

# Fresh start (delete all cached data)
python main.py --fresh --months 6

# Verbose mode (debug logging)
python main.py --skip-scrape -v
```

### Requirements

```
python 3.11+
google-play-scraper
app-store-scraper
google-generativeai
pandas
matplotlib
rich
python-dotenv
pyyaml
textblob (fallback)
```

### Environment

```
GOOGLE_API_KEY=your-gemini-api-key
```

---

## Output File Map

```
data/
├── raw_reviews.csv              ← 10,000+ Maya reviews
├── gcash_reviews.csv            ← 10,000+ GCash reviews
├── temporal_analysis.json       ← Monthly trends + version spikes
├── comprehensive_analysis.json  ← Deep UX categorization
├── funnel_analysis.json         ← Drop-off hotspots
├── accessibility_analysis.json  ← Device/connectivity/edge cases
├── competitor_comparison.json   ← Maya vs GCash
├── journey_map.json             ← Screen-level friction map
├── final_insights.json          ← Ranked opportunities
├── maya_insights_report.md      ← Human-readable report (346 lines)
├── screenshots_manifest.json    ← Screenshot metadata
├── screenshots/
│   ├── google_play/             ← 7 Google Play screenshots
│   └── ios/                     ← iOS screenshots
└── charts/
    ├── rating_trend.png
    ├── sentiment_distribution.png
    ├── business_impact.png
    ├── priority_scores.png
    ├── severity_frequency.png
    ├── pain_point_frequency.png
    ├── version_ratings.png
    ├── issue_lifecycle.png
    └── funnel_dropoff.png
```

---

*Maya Review Agent | Built by Manpreet Bhattee | February 2026*
