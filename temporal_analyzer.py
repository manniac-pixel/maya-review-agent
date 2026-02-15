"""
Temporal Analysis module.
Groups reviews by month, uses LLM to extract pain points per period,
detects version-specific issue spikes, and classifies trends.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

import config
import llm
import sentiment

logger = logging.getLogger(__name__)


MONTH_ANALYSIS_PROMPT = """\
You are a UX researcher analyzing user reviews of Maya, a fintech app in the Philippines.

Below are user reviews from {month_label} ({platform_breakdown}).
Average rating this month: {avg_rating:.1f}/5 ({total_count} total reviews, showing {sample_count}).

Reviews:
{reviews_text}

Analyze these reviews and return a JSON object with this exact structure:
{{
  "pain_points": [
    {{
      "theme": "short label",
      "description": "what users are complaining about",
      "severity": 1-5,
      "frequency": "high|medium|low",
      "quotes": ["exact quote 1", "exact quote 2"]
    }}
  ],
  "feature_requests": [
    {{
      "feature": "what users want",
      "description": "details",
      "frequency": "high|medium|low",
      "quotes": ["exact quote"]
    }}
  ],
  "positive_mentions": [
    {{
      "theme": "what works well",
      "description": "details",
      "frequency": "high|medium|low"
    }}
  ],
  "competitive_comparisons": [
    {{
      "competitor": "app name (e.g. GCash)",
      "context": "what users are comparing",
      "sentiment": "maya_better|competitor_better|neutral",
      "quotes": ["exact quote"]
    }}
  ]
}}

Focus on fintech-specific issues: payments, transfers, KYC, loans/credit, savings,
crypto, customer support, UI/UX, performance, security, onboarding.
Return ONLY valid JSON, no markdown fences or commentary."""


TREND_ANALYSIS_PROMPT = """\
You are a UX researcher performing temporal trend analysis on Maya app reviews.

Below is a summary of pain points extracted from each month over the analysis period:

{monthly_summaries}

Classify each unique pain point theme into one of these categories:

1. **resolved**: Appeared in earlier months but decreased significantly or disappeared in recent months.
   The Maya team likely fixed this.
2. **persistent**: Appears consistently across most months. Not addressed.
3. **emerging**: Only appears in the last 2-3 months. A new or worsening problem.

Return a JSON object:
{{
  "resolved_issues": [
    {{
      "theme": "...",
      "description": "...",
      "peak_months": ["2024-01", "2024-02"],
      "evidence": "why you think it's resolved"
    }}
  ],
  "persistent_issues": [
    {{
      "theme": "...",
      "description": "...",
      "severity": 1-5,
      "frequency": "high|medium|low",
      "months_present": ["2024-01", "2024-02"],
      "evidence": "why you think it persists"
    }}
  ],
  "emerging_issues": [
    {{
      "theme": "...",
      "description": "...",
      "severity": 1-5,
      "first_seen": "2024-10",
      "evidence": "why you think it's emerging"
    }}
  ]
}}

Return ONLY valid JSON, no markdown fences or commentary."""


VERSION_SPIKE_PROMPT = """\
You are a UX researcher analyzing a spike in negative reviews for Maya app version {version}.

This version has a significantly higher 1-star rate than average:
- Version {version}: {one_star_pct:.0f}% 1-star reviews (avg rating {avg_rating:.2f}/5, {review_count} reviews)
- Overall baseline: {baseline_pct:.0f}% 1-star reviews (avg rating {baseline_avg:.2f}/5)
- Date range for this version: {date_range}

Below are the negative reviews (1-2 star) from this version:
{reviews_text}

Identify what went wrong in this specific version. Return a JSON object:
{{
  "version": "{version}",
  "primary_issues": [
    {{
      "theme": "short label",
      "description": "what broke or degraded in this version",
      "severity": 1-5,
      "affected_area": "login|payments|transfers|KYC|credit|savings|crypto|performance|UI|security|other",
      "likely_cause": "bug|regression|new_feature_broken|server_side|design_change|other",
      "quotes": ["exact quote 1", "exact quote 2"]
    }}
  ],
  "comparison_to_previous": "how this version compares to earlier versions based on complaints",
  "likely_root_cause_summary": "one-sentence summary of what likely went wrong in this release"
}}

Return ONLY valid JSON, no markdown fences or commentary."""


# ── Helpers ─────────────────────────────────────────────────────────────

def _sample_reviews(df: pd.DataFrame, max_n: int) -> pd.DataFrame:
    """Sample reviews intelligently: mix of ratings, prefer longer reviews."""
    if len(df) <= max_n:
        return df

    sampled = []
    for rating in sorted(df["rating"].unique()):
        rating_df = df[df["rating"] == rating]
        proportion = len(rating_df) / len(df)
        n_for_rating = max(2, int(proportion * max_n))
        rating_df = rating_df.assign(
            text_len=rating_df["text"].str.len()
        ).sort_values("text_len", ascending=False)
        sampled.append(rating_df.head(n_for_rating))

    result = pd.concat(sampled).head(max_n)
    return result.drop(columns=["text_len"], errors="ignore")


def _format_reviews(df: pd.DataFrame) -> str:
    """Format reviews into text for the prompt."""
    lines = []
    for _, row in df.iterrows():
        stars = "*" * int(row["rating"]) if pd.notna(row["rating"]) else "?"
        platform = row.get("platform", "?")
        text = str(row["text"]).strip().replace("\n", " ")
        lines.append(f"[{stars}] [{platform}] {text}")
    return "\n".join(lines)


# ── Version spike detection (data-driven, no LLM) ──────────────────────

def compute_version_stats(df: pd.DataFrame) -> dict:
    """
    Compute per-version stats and flag versions with abnormal 1-star spikes.
    A version is flagged if its 1-star rate exceeds baseline by >10 percentage
    points AND it has enough reviews to be significant.
    """
    min_reviews_per_version = config.get("temporal", "min_reviews_per_version", 20)

    versioned = df.dropna(subset=["app_version"])
    if len(versioned) == 0:
        return {"versions": [], "flagged_versions": [], "baseline": {}}

    baseline_one_star = (versioned["rating"] == 1).mean()
    baseline_avg = versioned["rating"].mean()

    version_stats = []
    for ver, group in versioned.groupby("app_version"):
        count = len(group)
        if count < min_reviews_per_version:
            continue
        one_star_rate = (group["rating"] == 1).mean()
        avg_rating = group["rating"].mean()
        date_min = group["date"].min()
        date_max = group["date"].max()
        version_stats.append({
            "version": str(ver),
            "review_count": count,
            "avg_rating": round(avg_rating, 2),
            "one_star_pct": round(one_star_rate * 100, 1),
            "one_star_count": int((group["rating"] == 1).sum()),
            "date_first": str(date_min)[:10] if pd.notna(date_min) else "",
            "date_last": str(date_max)[:10] if pd.notna(date_max) else "",
            "spike": one_star_rate > baseline_one_star + 0.10,
        })

    version_stats.sort(key=lambda v: v["one_star_pct"], reverse=True)

    flagged = [v for v in version_stats if v["spike"]]

    logger.info(
        f"Version stats: {len(version_stats)} versions with >={min_reviews_per_version} reviews, "
        f"{len(flagged)} flagged with 1-star spikes"
    )
    for v in flagged:
        logger.info(
            f"  SPIKE: v{v['version']} — {v['one_star_pct']}% 1-star "
            f"(baseline {baseline_one_star*100:.0f}%), "
            f"{v['review_count']} reviews, avg {v['avg_rating']}"
        )

    return {
        "baseline": {
            "avg_rating": round(baseline_avg, 2),
            "one_star_pct": round(baseline_one_star * 100, 1),
            "total_versioned_reviews": len(versioned),
        },
        "versions": version_stats,
        "flagged_versions": flagged,
    }


# ── Version spike LLM analysis ─────────────────────────────────────────

def analyze_version_spike(
    model, version: str, ver_df: pd.DataFrame, baseline: dict
) -> dict:
    """Send flagged version's negative reviews to LLM for root-cause analysis."""
    max_per_version = config.get("temporal", "max_reviews_per_version", 80)
    negative = ver_df[ver_df["rating"] <= 2]
    sample = _sample_reviews(negative, max_per_version)
    reviews_text = _format_reviews(sample)

    date_min = ver_df["date"].min()
    date_max = ver_df["date"].max()
    date_range = f"{str(date_min)[:10]} to {str(date_max)[:10]}"

    prompt = VERSION_SPIKE_PROMPT.format(
        version=version,
        one_star_pct=(ver_df["rating"] == 1).mean() * 100,
        avg_rating=ver_df["rating"].mean(),
        review_count=len(ver_df),
        baseline_pct=baseline["one_star_pct"],
        baseline_avg=baseline["avg_rating"],
        date_range=date_range,
        reviews_text=reviews_text,
    )

    return llm.call(model, prompt)


# ── Monthly + trend analysis (unchanged logic) ─────────────────────────

def analyze_month(model, month_label: str, month_df: pd.DataFrame) -> dict:
    """Analyze a single month's reviews."""
    max_per_month = config.get("temporal", "max_reviews_per_month", 150)
    sample = _sample_reviews(month_df, max_per_month)
    reviews_text = _format_reviews(sample)

    platform_counts = month_df["platform"].value_counts().to_dict()
    platform_breakdown = ", ".join(f"{k}: {v}" for k, v in platform_counts.items())
    avg_rating = month_df["rating"].mean() if "rating" in month_df else 0

    prompt = MONTH_ANALYSIS_PROMPT.format(
        month_label=month_label,
        platform_breakdown=platform_breakdown,
        avg_rating=avg_rating,
        total_count=len(month_df),
        sample_count=len(sample),
        reviews_text=reviews_text,
    )

    return llm.call(model, prompt)


def analyze_trends(model, monthly_results: dict) -> dict:
    """Analyze trends across all months to classify issues."""
    summaries = []
    for month, data in sorted(monthly_results.items()):
        pain_themes = [
            f"- {p['theme']} (severity: {p['severity']}, freq: {p['frequency']})"
            for p in data.get("pain_points", [])
        ]
        summaries.append(f"### {month}\n" + "\n".join(pain_themes))

    prompt = TREND_ANALYSIS_PROMPT.format(monthly_summaries="\n\n".join(summaries))
    return llm.call(model, prompt)


# ── Main entry point ───────────────────────────────────────────────────

def run(reviews_df: pd.DataFrame, suffix: str = "") -> dict:
    """
    Run temporal analysis. If output file exists, load cached results.
    suffix: e.g. '_1star' for filtered runs, '' for full analysis.
    """
    data_dir = config.output_dir()
    inter_delay = config.get("temporal", "inter_call_delay_seconds", 10)

    output_path = data_dir / f"temporal_analysis{suffix}.json"
    if output_path.exists():
        logger.info(f"Loading cached temporal analysis from {output_path}")
        with open(output_path) as f:
            return json.load(f)

    model = llm.get_model()

    reviews_df = reviews_df.copy()
    reviews_df["date"] = pd.to_datetime(reviews_df["date"])
    reviews_df["month"] = reviews_df["date"].dt.to_period("M").astype(str)

    # ── Monthly analysis ────────────────────────────────────────────────
    months = sorted(reviews_df["month"].unique())
    logger.info(f"Analyzing {len(months)} months: {months[0]} to {months[-1]}")

    monthly_results = {}
    for i, month in enumerate(months):
        month_df = reviews_df[reviews_df["month"] == month]
        if len(month_df) < 3:
            logger.info(f"  Skipping {month} (only {len(month_df)} reviews)")
            continue

        logger.info(
            f"  [{i + 1}/{len(months)}] Analyzing {month} "
            f"({len(month_df)} reviews)..."
        )
        try:
            monthly_results[month] = analyze_month(model, month, month_df)
            logger.info(f"  {month} done.")
        except Exception as e:
            logger.warning(f"  LLM failed for {month}: {e} — using TextBlob fallback")
            try:
                monthly_results[month] = sentiment.analyze_month_fallback(month, month_df)
            except Exception as fb_err:
                logger.error(f"  TextBlob fallback also failed for {month}: {fb_err}")
                monthly_results[month] = {"error": str(e)}

        time.sleep(inter_delay)

    # ── Trend classification ────────────────────────────────────────────
    valid_months = {k: v for k, v in monthly_results.items() if "error" not in v}
    logger.info(
        f"Running trend analysis across {len(valid_months)} successfully analyzed months..."
    )
    try:
        trends = analyze_trends(model, valid_months)
    except Exception as e:
        logger.error(f"Trend analysis failed: {e}")
        trends = {"error": str(e)}

    # ── Version spike detection ─────────────────────────────────────────
    logger.info("Computing per-version stats...")
    version_data = compute_version_stats(reviews_df)

    version_spike_analyses = {}
    flagged = version_data.get("flagged_versions", [])
    if flagged:
        logger.info(f"Analyzing {len(flagged)} flagged version spike(s)...")
        for i, fv in enumerate(flagged):
            ver = fv["version"]
            ver_df = reviews_df[reviews_df["app_version"] == ver]
            logger.info(
                f"  [{i + 1}/{len(flagged)}] Analyzing v{ver} "
                f"({fv['one_star_pct']}% 1-star, {fv['review_count']} reviews)..."
            )
            try:
                result = analyze_version_spike(
                    model, ver, ver_df, version_data["baseline"]
                )
                version_spike_analyses[ver] = result
                logger.info(f"  v{ver} done.")
            except Exception as e:
                logger.error(f"  Failed to analyze v{ver}: {e}")
                version_spike_analyses[ver] = {"error": str(e)}

            time.sleep(inter_delay)
    else:
        logger.info("No version spikes detected above threshold.")

    # ── Assemble output ─────────────────────────────────────────────────
    output = {
        "analysis_date": datetime.now().isoformat(),
        "months_analyzed": months,
        "monthly_results": monthly_results,
        "trends": trends,
        "version_analysis": {
            "baseline": version_data["baseline"],
            "version_stats": version_data["versions"],
            "flagged_versions": [v["version"] for v in flagged],
            "spike_analyses": version_spike_analyses,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    logger.info(f"Saved temporal analysis to {output_path}")

    return output
