"""
Maya Review Analysis Agent — Minimal Edition
=============================================
Run: python analyze.py
  1. Scrapes Maya + GCash reviews (6 months, ~2-3k)
  2. Analyzes via Ollama (llama3.1) in chunked passes
  3. Saves insights.json + insights_summary.md

Requires: Ollama running locally with llama3.1:8b
"""

import json
import logging
import requests
from pathlib import Path

import pandas as pd

import scrape

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data"
INSIGHTS_PATH = DATA_DIR / "insights.json"
REPORT_PATH = Path(__file__).parent / "insights_summary.md"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"


def ollama_generate(prompt: str, temperature: float = 0.3) -> str:
    """Call Ollama API and return the response text."""
    resp = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": 4096},
    }, timeout=300)
    resp.raise_for_status()
    return resp.json()["response"]


def prepare_compact_reviews(df: pd.DataFrame, app: str, max_reviews: int = 400) -> str:
    """Create a compact review summary for one app, prioritizing negative reviews."""
    app_df = df[df["app"] == app].copy()
    if app_df.empty:
        return ""

    # Prioritize 1-2 star reviews (most useful for UX), then sample rest
    negative = app_df[app_df["rating"] <= 2]
    neutral = app_df[app_df["rating"] == 3]
    positive = app_df[app_df["rating"] >= 4]

    # Allocate: 60% negative, 20% neutral, 20% positive
    n_neg = min(len(negative), int(max_reviews * 0.6))
    n_neu = min(len(neutral), int(max_reviews * 0.2))
    n_pos = min(len(positive), int(max_reviews * 0.2))

    sampled = pd.concat([
        negative.sample(n=n_neg, random_state=42) if n_neg > 0 else negative,
        neutral.sample(n=n_neu, random_state=42) if n_neu > 0 else neutral,
        positive.sample(n=n_pos, random_state=42) if n_pos > 0 else positive,
    ])

    lines = [f"{app.upper()} ({len(app_df)} total reviews, avg {app_df['rating'].mean():.1f} stars)"]
    lines.append(f"Rating breakdown: " + ", ".join(
        f"{r}star={len(app_df[app_df['rating']==r])}" for r in [1,2,3,4,5]
    ))
    lines.append("")

    for _, row in sampled.iterrows():
        text = str(row["text"])[:200].replace("\n", " ")
        lines.append(f"[{int(row['rating'])}*] {text}")

    return "\n".join(lines)


def analyze_pain_points(maya_text: str, gcash_text: str) -> list:
    """Extract top 5 pain points from Maya reviews."""
    prompt = f"""You are a UX researcher analyzing Maya app (digital bank/e-wallet in Philippines) reviews.

Here are Maya user reviews (star rating in brackets):

{maya_text}

Identify the TOP 5 most critical UX pain points. For each, provide:
- title: short name
- severity: critical, high, or medium
- frequency: rough % of negative reviews about this
- user_journey_stage: onboarding, daily_use, transactions, support, account_management
- description: 2-3 sentences
- representative_quotes: 3 exact quotes from reviews above
- design_implication: specific UI/UX change needed

Return ONLY a JSON array of 5 objects. No other text. Example format:
[{{"rank":1,"title":"...","severity":"critical","frequency":"~30%","user_journey_stage":"...","description":"...","representative_quotes":["...","...","..."],"design_implication":"..."}}]"""

    log.info("  Analyzing pain points...")
    raw = ollama_generate(prompt)
    return _parse_json_array(raw, "pain_points")


def analyze_competitive_gaps(maya_text: str, gcash_text: str) -> list:
    """Compare Maya vs GCash based on reviews."""
    prompt = f"""You are a UX researcher comparing two Philippine fintech apps based on user reviews.

MAYA REVIEWS:
{maya_text[:15000]}

GCASH REVIEWS:
{gcash_text[:15000]}

Identify the TOP 3 areas where Maya loses to GCash based on these reviews. For each:
- area: the category (e.g. "reliability", "features", "UX")
- gcash_strength: what GCash users praise
- maya_weakness: what Maya users complain about in this area
- design_opportunity: specific design improvement for Maya

Return ONLY a JSON array of 3 objects. No other text. Example:
[{{"rank":1,"area":"...","gcash_strength":"...","maya_weakness":"...","design_opportunity":"..."}}]"""

    log.info("  Analyzing competitive gaps...")
    raw = ollama_generate(prompt)
    return _parse_json_array(raw, "competitive_gaps")


def analyze_feature_requests(maya_text: str) -> list:
    """Extract top 3 feature requests from Maya reviews."""
    prompt = f"""You are a UX researcher analyzing Maya app (digital bank in Philippines) reviews for feature requests.

Here are Maya user reviews:
{maya_text[:20000]}

Identify the TOP 3 most requested features or improvements. For each:
- feature: name of the feature
- demand_signal: how often/strongly users ask for this
- user_need: the underlying need
- design_direction: brief direction for designing this

Return ONLY a JSON array of 3 objects. No other text. Example:
[{{"rank":1,"feature":"...","demand_signal":"...","user_need":"...","design_direction":"..."}}]"""

    log.info("  Analyzing feature requests...")
    raw = ollama_generate(prompt)
    return _parse_json_array(raw, "feature_requests")


def generate_summary(insights: dict) -> str:
    """Generate executive summary from the insights."""
    pain_titles = [p["title"] for p in insights.get("pain_points", [])]
    gap_areas = [g["area"] for g in insights.get("competitive_gaps", [])]
    features = [f["feature"] for f in insights.get("feature_requests", [])]

    prompt = f"""Write a 3-4 sentence executive summary for a design team about Maya app (Philippine digital bank).

Key pain points found: {', '.join(pain_titles)}
Competitive gaps vs GCash: {', '.join(gap_areas)}
Top feature requests: {', '.join(features)}

Write a concise summary focusing on design implications. Return ONLY the summary text, no JSON."""

    log.info("  Generating executive summary...")
    return ollama_generate(prompt, temperature=0.5).strip()


def _parse_json_array(raw: str, label: str) -> list:
    """Parse JSON array from LLM response, handling markdown wrapping."""
    raw = raw.strip()

    # Strip markdown code blocks
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]

    # Try to find array boundaries
    raw = raw.strip()
    start = raw.find("[")
    end = raw.rfind("]")
    if start != -1 and end != -1:
        raw = raw[start:end+1]

    try:
        result = json.loads(raw)
        if isinstance(result, list):
            return result
        log.warning(f"{label}: expected array, got {type(result)}")
        return []
    except json.JSONDecodeError as e:
        log.error(f"Failed to parse {label} JSON: {e}")
        log.error(f"Raw:\n{raw[:300]}")
        (DATA_DIR / f"raw_{label}.txt").write_text(raw)
        return []


def generate_report(insights: dict) -> str:
    """Generate a clean markdown report from the insights."""
    lines = []
    lines.append("# Maya App — UX Review Insights")
    lines.append(f"*Generated {pd.Timestamp.now().strftime('%B %d, %Y')} | Last 6 months of reviews*\n")

    lines.append("## Executive Summary")
    lines.append(insights.get("executive_summary", "N/A"))
    lines.append("")

    # Pain Points
    lines.append("---")
    lines.append("## Top 5 Critical Pain Points\n")
    for pp in insights.get("pain_points", []):
        severity_icon = {"critical": "[CRITICAL]", "high": "[HIGH]", "medium": "[MEDIUM]"}.get(pp.get("severity", ""), "")
        lines.append(f"### {pp.get('rank', '?')}. {pp.get('title', 'Untitled')} {severity_icon}")
        lines.append(f"**Journey Stage:** {pp.get('user_journey_stage', 'N/A')} | **Frequency:** {pp.get('frequency', 'N/A')}\n")
        lines.append(pp.get("description", ""))
        lines.append("")
        quotes = pp.get("representative_quotes", [])
        if quotes:
            lines.append("**User Quotes:**")
            for q in quotes:
                lines.append(f"> *\"{q}\"*")
            lines.append("")
        lines.append(f"**Design Implication:** {pp.get('design_implication', 'N/A')}\n")

    # Competitive Gaps
    lines.append("---")
    lines.append("## Top 3 Competitive Gaps vs GCash\n")
    for gap in insights.get("competitive_gaps", []):
        lines.append(f"### {gap.get('rank', '?')}. {gap.get('area', 'Untitled')}")
        lines.append(f"- **GCash Strength:** {gap.get('gcash_strength', 'N/A')}")
        lines.append(f"- **Maya Weakness:** {gap.get('maya_weakness', 'N/A')}")
        lines.append(f"- **Design Opportunity:** {gap.get('design_opportunity', 'N/A')}\n")

    # Feature Requests
    lines.append("---")
    lines.append("## Top 3 Feature Requests\n")
    for fr in insights.get("feature_requests", []):
        lines.append(f"### {fr.get('rank', '?')}. {fr.get('feature', 'Untitled')}")
        lines.append(f"- **Demand:** {fr.get('demand_signal', 'N/A')}")
        lines.append(f"- **Underlying Need:** {fr.get('user_need', 'N/A')}")
        lines.append(f"- **Design Direction:** {fr.get('design_direction', 'N/A')}\n")

    lines.append("---")
    lines.append("*Analysis powered by Ollama (llama3.1) | Reviews from Google Play & iOS App Store (PH)*")

    return "\n".join(lines)


def main():
    log.info("=" * 50)
    log.info("MAYA REVIEW ANALYSIS — MINIMAL EDITION")
    log.info("=" * 50)

    # Step 1: Scrape reviews
    log.info("\nSTEP 1: Scraping reviews...")
    df = scrape.run()
    log.info(f"Working with {len(df)} reviews")

    for app in df["app"].unique():
        sub = df[df["app"] == app]
        log.info(f"  {app}: {len(sub)} reviews | avg {sub['rating'].mean():.1f} | "
                 f"1-star: {len(sub[sub['rating']==1])} | 5-star: {len(sub[sub['rating']==5])}")

    # Step 2: Prepare compact review texts
    log.info("\nSTEP 2: Analyzing with Ollama (llama3.1)...")
    maya_text = prepare_compact_reviews(df, "maya", max_reviews=400)
    gcash_text = prepare_compact_reviews(df, "gcash", max_reviews=400)
    log.info(f"  Maya review text: {len(maya_text):,} chars")
    log.info(f"  GCash review text: {len(gcash_text):,} chars")

    # Step 3: Run analysis in focused passes
    insights = {}
    insights["pain_points"] = analyze_pain_points(maya_text, gcash_text)
    insights["competitive_gaps"] = analyze_competitive_gaps(maya_text, gcash_text)
    insights["feature_requests"] = analyze_feature_requests(maya_text)
    insights["executive_summary"] = generate_summary(insights)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(INSIGHTS_PATH, "w") as f:
        json.dump(insights, f, indent=2)
    log.info(f"Saved insights to {INSIGHTS_PATH}")

    # Step 4: Generate report
    log.info("\nSTEP 3: Generating report...")
    report = generate_report(insights)
    REPORT_PATH.write_text(report)
    log.info(f"Saved report to {REPORT_PATH}")

    # Done
    log.info("\n" + "=" * 50)
    log.info("DONE!")
    log.info(f"  Insights: {INSIGHTS_PATH}")
    log.info(f"  Report:   {REPORT_PATH}")
    log.info("=" * 50)


if __name__ == "__main__":
    main()
