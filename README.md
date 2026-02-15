# Maya Review Agent

An AI-powered pipeline that scrapes 20,000+ fintech app reviews and turns them into ranked, screen-level UX insights — in 15 minutes.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Gemini](https://img.shields.io/badge/LLM-Gemini%202.0%20Flash-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## What It Does

Maya is one of the Philippines' largest digital banks. This agent analyzes its app store reviews to surface exactly where users get frustrated, why they leave 1-star reviews, and what to fix first.

**Input:** 12,345+ reviews from Google Play & iOS App Store (Maya + GCash competitor)

**Output:**
- 9 ranked UX opportunities with severity, frequency, and business impact scores
- Screen-level funnel drop-off map (which exact screen users abandon)
- Version spike detection (which releases caused rating drops)
- Temporal trends (what's getting better vs. worse over 7 months)
- Competitive benchmark (Maya vs. GCash — strengths, gaps, switching reasons)
- 9 auto-generated charts
- Accessibility analysis (budget devices, slow connectivity, elderly users, OFWs)

### Sample Finding

> **Login & Authentication Failures** — Severity 5/5, Priority Score 18
>
> "I've tried several times today, but I can't get in."
>
> 45 reviews mention the Login > OTP Entry screen specifically. Version v2.148.3 spiked 1-star rate from 35% to 45%.

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/maya-review-agent.git
cd maya-review-agent

# Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set API key
echo "GOOGLE_API_KEY=your-key-here" > .env

# Run
python main.py --months 12
```

## Usage

```bash
# Full run (scrape + analyze)
python main.py --months 12

# Analyze only 1-star reviews (strongest signal)
python main.py --skip-scrape --stars 1

# Analyze 1 and 2-star reviews
python main.py --skip-scrape --stars 1,2

# Use free local LLM (no API key needed)
python main.py --backend ollama --skip-scrape

# Fresh start (clear cache)
python main.py --fresh --months 6

# Verbose logging
python main.py --skip-scrape -v
```

## The 8-Step Pipeline

```
┌─────────────┐    ┌──────────────┐    ┌───────────────────┐
│  1. Scrape   │───▶│ 2. Temporal  │───▶│ 3. Comprehensive  │
│  20K reviews │    │  month-by-   │    │  deep UX analysis │
│  (Play+iOS)  │    │  month trends│    │  (chunked+merged) │
└─────────────┘    └──────────────┘    └───────────────────┘
                                                │
┌─────────────┐    ┌──────────────┐    ┌───────┴───────────┐
│ 6. Compete  │◀───│ 5. Access-   │◀───│ 4. Funnel         │
│ Maya vs     │    │  ibility     │    │  drop-offs &      │
│ GCash       │    │  & edge cases│    │  retry detection   │
└─────────────┘    └──────────────┘    └───────────────────┘
       │
┌──────┴──────┐    ┌──────────────┐
│ 7. Screen-  │───▶│ 8. Insights  │──▶ Report + 9 Charts
│  shots      │    │  synthesis   │
└─────────────┘    └──────────────┘
```

| Step | Module | LLM? | What it does |
|------|--------|------|--------------|
| 1 | `scraper.py` | No | Scrapes Google Play + iOS for Maya & GCash reviews |
| 2 | `temporal_analyzer.py` | Yes | Monthly analysis, trend classification, version spike detection |
| 3 | `comprehensive_analyzer.py` | Yes | Deep categorization by issue, journey, screen, severity |
| 4 | `funnel_analyzer.py` | Yes | Regex pre-filter + LLM analysis of retry/abandonment signals |
| 5 | `accessibility_analyzer.py` | Yes | Device, connectivity, and Philippines-market edge cases |
| 6 | `competitor_analysis.py` | Yes | Side-by-side Maya vs. GCash comparison |
| 7 | `screenshot_scraper.py` | No | Downloads app store screenshots |
| 8 | `insights_generator.py` | Yes | Ranked report + charts + journey friction map |

Every step caches to JSON. Interrupted runs resume automatically.

## Output

```
data/
├── raw_reviews.csv              # 10,000+ Maya reviews
├── gcash_reviews.csv            # 10,000+ GCash reviews
├── temporal_analysis.json       # Monthly trends + version spikes
├── comprehensive_analysis.json  # Deep UX categorization
├── funnel_analysis.json         # Drop-off hotspots
├── accessibility_analysis.json  # Device/connectivity/edge cases
├── competitor_comparison.json   # Maya vs GCash
├── journey_map.json             # Screen-level friction map
├── final_insights.json          # Ranked opportunities
├── maya_insights_report.md      # Human-readable report
├── screenshots/                 # App store screenshots
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

## Key Findings (Maya, Feb 2026)

| # | Issue | Severity | Score |
|---|-------|----------|-------|
| 1 | Login & Authentication Failures | 5/5 | 18 |
| 2 | Customer Service Unreachable | 5/5 | 15 |
| 3 | Unauthorized Transactions | 5/5 | 15 |
| 4 | Security Concerns | 5/5 | 15 |
| 5 | Cash-in Delays | 4/5 | 14 |

4 of the top 5 issues are severity 5/5 and trust-related. Maya has a trust crisis, not a feature problem.

## Interactive Dashboard

A Streamlit web app is included for exploring the findings interactively:

```bash
pip install streamlit
streamlit run streamlit_app.py
```

## Architecture

- **LLM:** Gemini 2.0 Flash (fast, cheap classification) or Ollama (free, local)
- **Regex pre-filtering:** Steps 4-5 use regex to tag signal-rich reviews before sending to LLM — reduces API calls by ~80%
- **Chunked analysis:** Step 3 splits reviews into 200-review chunks for deeper attention, then synthesizes
- **Checkpoint caching:** Every step saves to JSON — resume from any point
- **Rate limiting:** Exponential backoff with jitter for Gemini 429 errors
- **Data quality gate:** Validates review data before spending API credits

## Configuration

Edit `config.yaml` or use environment variables:

```bash
MAYA_SCRAPER__GPLAY_BATCH_SIZE=200
MAYA_TEMPORAL__MAX_REVIEWS_PER_MONTH=150
MAYA_LLM__GEMINI_MODEL=gemini-2.0-flash
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| LLM | Gemini 2.0 Flash / Ollama |
| Scraping | google-play-scraper, app-store-scraper |
| Data | pandas |
| Charts | matplotlib |
| CLI | Rich |
| Web UI | Streamlit |
| Config | YAML + dotenv |

## License

MIT

---

Built by Manpreet Bhattee | February 2026
