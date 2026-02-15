# Maya Review Agent — Presentation Deck

> Slide-by-slide content for presenting the Maya Review Agent project. Each section below maps to one slide or slide group.

---

## Slide 1: Title

# Maya Review Agent
### AI-Powered UX Intelligence for Fintech

**Manpreet Bhattee** | Product Designer & AI Engineer
February 2026

---

## Slide 2: The Problem

### Maya is losing trust — and the data proves it.

- **12,345 reviews** analyzed (Aug 2025 – Feb 2026)
- Overall sentiment: **mixed-negative**
- **4 of the top 5 issues** have severity 5/5
- Users are actively switching to GCash

> "I've tried several times today, but I can't get in."

> "My phone was stolen and the hacker was able to access this app and took my savings."

**This isn't about features. It's a trust crisis.**

---

## Slide 3: The Insight

### Negative reviews are the best UX research you're not reading.

|  |  |
| --- | --- |
| 12,000+ reviews | More specific than user interviews |
| Screen-level detail | "The login OTP never arrives" |
| Emotional context | "I'm scared to use this app" |
| Competitor intelligence | "I switched to GCash because..." |

**The problem:** No team can manually read, tag, and prioritize 12K reviews fast enough to inform design sprints.

---

## Slide 4: The Solution

### We built an AI agent to do it in minutes.

**Maya Review Agent** — an 8-step Python pipeline powered by Gemini 2.0 Flash

```
python main.py --months 12 --stars 1,2
```

**One command. Full analysis. Actionable output.**

| Input | Output |
| --- | --- |
| 10,000+ Maya reviews | 9 ranked UX opportunities |
| 10,000+ GCash reviews | Funnel drop-off map |
| 6 months of data | Version spike analysis |
| | 9 auto-generated charts |
| | Competitive benchmark |
| | Design brief with user quotes |

---

## Slide 5: How It Works

### 8-step pipeline

| # | Step | What happens |
| --- | --- | --- |
| 1 | **Scrape** | Pull 20,000+ reviews from Google Play & iOS |
| 2 | **Temporal** | Track issues month-over-month |
| 3 | **Comprehensive** | Categorize every review by issue, journey, severity |
| 4 | **Funnel** | Map drop-offs to specific screens |
| 5 | **Accessibility** | Find edge-case users (elderly, OFWs, budget phones) |
| 6 | **Competitor** | Benchmark Maya vs. GCash |
| 7 | **Screenshots** | Download current app visuals |
| 8 | **Insights** | Generate ranked report + charts |

**Built with:** Python, Gemini 2.0 Flash, pandas, matplotlib, Rich CLI

---

## Slide 6: Top Findings

### The 5 issues killing Maya's ratings

| # | Issue | Severity | What users say |
| --- | --- | --- | --- |
| 1 | **Login failures** | 5/5 | "I can't access my money" |
| 2 | **Support unreachable** | 5/5 | "No one answers" |
| 3 | **Unauthorized transactions** | 5/5 | "PHP 9,000 stolen, months to resolve" |
| 4 | **Security concerns** | 5/5 | "Stolen phone = instant account drain" |
| 5 | **Cash-in delays** | 4/5 | "Success screen but money never arrived" |

---

## Slide 7: Funnel Drop-offs

### Where users abandon the app

| Screen | Severity | Evidence |
| --- | --- | --- |
| **Login > OTP Entry** | 5/5 | 45 reviews mentioning this exact screen |
| **Cash In > Bank Integration** | 4/5 | 30 reviews |
| **KYC > Selfie Capture** | 4/5 | 25 reviews (crashes, retries) |
| **Crypto > Buy Token** | 3/5 | 12 reviews |
| **Send Money > Contact Selection** | 2/5 | 8 reviews |

**Key takeaway:** The highest drop-off is at the very first screen — login. Users never even get to use the app.

---

## Slide 8: Version Spike

### One bad release caused measurable trust erosion

**v2.148.3** — November 2025 to February 2026

|  |  |
| --- | --- |
| 1-star rate | **45.2%** (vs. 34.6% baseline) |
| Reviews affected | 188 |
| Root causes | Login regressions, payment failures, chatbot-only support |

**+10.6 percentage points** of 1-star reviews from a single version.

The agent automatically flags these spikes so teams can respond to regressions before they become trends.

---

## Slide 9: Temporal Trends

### What's getting better vs. worse

| Getting better | Getting worse |
| --- | --- |
| Login issues (improving) | Customer service (declining) |
| Cash-in delays (improving) | Unauthorized transactions (rising) |

| Persistent (6-7 months) | Emerging (Jan-Feb 2026) |
| --- | --- |
| Payment issues | OTP failures |
| KYC/onboarding | Transfer delays |
| Loan/credit | Savings problems |

---

## Slide 10: Competitive Intelligence

### Maya vs. GCash — what users say

**Users switch to GCash for:**
- Stronger security measures
- Better data privacy
- Faster transactions
- Functioning customer support

**Maya wins on:**
- Interface design ("cleaner UI")
- Feature breadth
- Savings interest rates
- Crypto access

> "I had money stolen from my account, and the customer support was unhelpful. Switching to GCash."

---

## Slide 11: Design Recommendations

### 4 flows redesigned based on agent findings

| Flow | Addresses | Key Design Move |
| --- | --- | --- |
| **A. Frictionless Login** | Login failures (#1) | Biometric-first auth, fallback chain |
| **B. Transparent Transactions** | Cash-in delays (#5) | Real-time timeline tracker |
| **C. Accessible Support** | Unreachable support (#2) | Ticket dashboard, human escalation |
| **D. Security Center** | Unauthorized access (#3-4) | Kill Switch, Safety Score, session management |

Each flow was designed to directly address a top-ranked agent finding — not based on assumptions, but on 12,000+ data points.

---

## Slide 12: Design Direction (Wireframes)

### High-fidelity wireframes for the 4 critical flows

> Wireframes created as design direction based on agent findings. Each screen maps to a specific pain point identified in the analysis.

**Flow A — Login:** Biometric-first, simplified input, clear error states
**Flow B — Transactions:** Timeline view, pending dashboard, status tracking
**Flow C — Support:** Ticket cards, status pills, chat with escalation
**Flow D — Security:** Shield icon, Safety Score, Kill Switch toggle

*Wireframes available in design_assets/ folder*

---

## Slide 13: What I Learned

### 3 takeaways from building an AI design research agent

**1. Reviews > surveys for screen-level UX feedback**
Users describe exact screens, exact errors, exact moments of frustration. At 12K reviews, the patterns are statistically significant.

**2. Temporal analysis is the killer feature**
Knowing an issue exists is useful. Knowing it's been getting worse for 7 months is urgent. The agent tracks trends that dashboards miss.

**3. Competitor scraping turns feedback into market intelligence**
When users say "I switched to GCash because..." — that's not just a review. It's a competitive gap with a dollar value.

---

## Slide 14: Impact

### Metrics to track post-redesign

| Metric | Baseline | Target |
| --- | --- | --- |
| Login success rate | 5+ failed attempts reported | >90% first-attempt |
| Cash-in reflection | 24+ hours | Under 5 minutes |
| Support resolution | "Months" per users | Under 48 hours |
| 1-star rate per version | 35% | Under 25% |

---

## Slide 15: Thank You

# Maya Review Agent

**AI-Powered UX Intelligence for Fintech**

Built with Python, Gemini 2.0 Flash, and 12,345 real user voices.

Manpreet Bhattee
February 2026

---

## Appendix: Agent Output Samples

### Charts generated by the agent

1. Rating Trend Over Time
2. Sentiment Distribution
3. Business Impact Distribution
4. Priority Scores (bar chart)
5. Severity vs. Frequency (scatter plot)
6. Pain Point Frequency
7. Version Ratings (flagging v2.148.3)
8. Issue Lifecycle (trends over time)
9. Funnel Drop-off

### Reports generated

- Full UX Insights Report (346 lines, markdown)
- Executive Brief (2-page summary)
- Journey Friction Map (screen-level)
- Competitor Comparison (Maya vs. GCash)

### Tech details

| Component | Technology |
| --- | --- |
| Language | Python 3.11+ |
| LLM | Gemini 2.0 Flash |
| Scraping | google-play-scraper, app-store-scraper |
| Data | pandas |
| Charts | matplotlib |
| CLI | Rich |
| Alt backend | Ollama (local/free) |
