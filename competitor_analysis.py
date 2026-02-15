"""
Competitor analysis module.
Compares Maya and GCash app reviews to identify relative strengths,
weaknesses, and feature gaps between the two apps.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pandas as pd

import config
import llm

logger = logging.getLogger(__name__)


COMPARISON_PROMPT = """\
You are a senior UX strategist comparing two competing fintech apps in the \
Philippines: **Maya** and **GCash**.

Below are real user reviews from both apps collected over the same time period.

## MAYA REVIEWS ({maya_count} sampled)
{maya_reviews}

## GCASH REVIEWS ({gcash_count} sampled)
{gcash_reviews}

Analyze both sets of reviews and produce a competitive comparison as JSON:
{{
  "summary": "2-3 sentence executive overview of how the two apps compare from users' perspective",
  "gcash_strengths": [
    {{
      "area": "short label, e.g. 'Cash-in network'",
      "description": "what GCash does better according to its users",
      "user_evidence": ["direct quote or close paraphrase from GCash reviews"],
      "maya_gap": "what Maya lacks or does worse in this area based on Maya reviews"
    }}
  ],
  "maya_strengths": [
    {{
      "area": "short label",
      "description": "what Maya does better according to its users",
      "user_evidence": ["direct quote or close paraphrase from Maya reviews"],
      "gcash_gap": "what GCash lacks or does worse in this area based on GCash reviews"
    }}
  ],
  "feature_gaps": [
    {{
      "feature": "feature or capability name",
      "available_in": "Maya|GCash|Both (but better in one)",
      "user_demand": "high|medium|low",
      "description": "what the gap is and why users care",
      "quotes": ["relevant user quote from either app"]
    }}
  ],
  "shared_pain_points": [
    {{
      "issue": "pain point both apps share",
      "description": "brief explanation"
    }}
  ],
  "rating_comparison": {{
    "maya_avg": <float>,
    "gcash_avg": <float>,
    "interpretation": "brief note on what the rating gap means"
  }}
}}

Guidelines:
- Base every finding on actual review evidence, not assumptions.
- Include 5-8 items per strengths list and 5-10 feature gaps.
- Feature gaps should be concrete features or capabilities, not vague sentiments.
- shared_pain_points: issues users of BOTH apps complain about.
- For rating_comparison, calculate averages from the reviews provided.
- Return ONLY valid JSON, no markdown fences or commentary."""


def _sample_reviews(df: pd.DataFrame, n: int | None = None) -> pd.DataFrame:
    """
    Sample up to n reviews, stratified across star ratings so the LLM sees
    a representative spread instead of mostly 1-star or 5-star.
    """
    if n is None:
        n = config.get("competitor", "sample_per_app", 150)
    if len(df) <= n:
        return df

    # Stratified sample: proportional to rating distribution, min 1 per group.
    grouped = df.groupby("rating", group_keys=False)
    return grouped.apply(
        lambda g: g.sample(n=max(1, int(len(g) / len(df) * n)), random_state=42)
    ).reset_index(drop=True)


def _format_reviews(df: pd.DataFrame) -> str:
    """Format a DataFrame of reviews into a compact text block for the prompt."""
    lines = []
    for _, row in df.iterrows():
        stars = "*" * int(row["rating"]) if pd.notna(row.get("rating")) else "?"
        date_str = ""
        if pd.notna(row.get("date")):
            date_str = f" ({str(row['date'])[:10]})"
        text = str(row.get("text", "")).strip()
        if text:
            lines.append(f"[{stars}]{date_str} {text}")
    return "\n".join(lines)


def run(
    maya_df: pd.DataFrame,
    gcash_df: pd.DataFrame,
    suffix: str = "",
) -> dict:
    """
    Run competitive comparison. Returns structured comparison dict.
    Caches to data/competitor_comparison{suffix}.json.
    """
    json_output = config.output_dir() / f"competitor_comparison{suffix}.json"

    if json_output.exists():
        logger.info(f"Loading cached competitor comparison from {json_output}")
        with open(json_output) as f:
            return json.load(f)

    logger.info(
        f"Comparing Maya ({len(maya_df)} reviews) vs "
        f"GCash ({len(gcash_df)} reviews)..."
    )

    maya_sample = _sample_reviews(maya_df)
    gcash_sample = _sample_reviews(gcash_df)

    prompt = COMPARISON_PROMPT.format(
        maya_count=len(maya_sample),
        gcash_count=len(gcash_sample),
        maya_reviews=_format_reviews(maya_sample),
        gcash_reviews=_format_reviews(gcash_sample),
    )

    model = llm.get_model()
    try:
        comparison = llm.call(model, prompt)
    except Exception as e:
        logger.error(f"Competitor comparison failed: {e}")
        return {"error": str(e)}

    json_output.parent.mkdir(parents=True, exist_ok=True)
    with open(json_output, "w") as f:
        json.dump(comparison, f, indent=2, default=str)
    logger.info(f"Saved competitor comparison to {json_output}")

    return comparison
