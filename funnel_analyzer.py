"""
Funnel Analyzer module.
Extracts proxy funnel data (retry signals, abandonment, drop-off hotspots)
from user reviews using regex pre-extraction followed by LLM deep analysis.
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path

import pandas as pd

import config
import llm

logger = logging.getLogger(__name__)

# ── Regex patterns for signal pre-extraction ────────────────────────────────

RETRY_PATTERNS = [
    re.compile(r"tried?\s+(\d+)\s+times?", re.IGNORECASE),
    re.compile(r"attempt(?:ed|s)?\s+(\d+)\s+times?", re.IGNORECASE),
    re.compile(r"keeps?\s+(?:failing|crashing|freezing|loading|disconnecting)", re.IGNORECASE),
    re.compile(r"(?:always|constantly|repeatedly)\s+(?:fails?|crashes?|errors?|freezes?)", re.IGNORECASE),
    re.compile(r"(?:tried|try)\s+(?:again|multiple|many|several)", re.IGNORECASE),
    re.compile(r"(?:still|keep|kept)\s+(?:getting|having|showing)\s+(?:error|issue|problem)", re.IGNORECASE),
    re.compile(r"(?:every\s+time|each\s+time)\s+(?:I|it)\s+(?:try|open|use|login)", re.IGNORECASE),
    re.compile(r"(?:retry|retried|re-?try)", re.IGNORECASE),
]

ABANDONMENT_PATTERNS = [
    re.compile(r"(?:gave|give)\s+up", re.IGNORECASE),
    re.compile(r"switch(?:ed|ing)?\s+to\s+(\w+)", re.IGNORECASE),
    re.compile(r"uninstall(?:ed|ing)?", re.IGNORECASE),
    re.compile(r"(?:moving|moved|went)\s+(?:to|back\s+to)\s+(\w+)", re.IGNORECASE),
    re.compile(r"(?:deleted?|remov(?:ed?|ing))\s+(?:the\s+)?app", re.IGNORECASE),
    re.compile(r"(?:will|going\s+to)\s+(?:use|try)\s+(\w+)\s+instead", re.IGNORECASE),
    re.compile(r"(?:better|prefer)\s+(?:to\s+use\s+)?(?:GCash|Coins\.ph|PayPal|GoTyme)", re.IGNORECASE),
    re.compile(r"(?:no\s+(?:longer|more)\s+(?:using|use|trust))", re.IGNORECASE),
    re.compile(r"(?:waste\s+of\s+time|don'?t\s+bother)", re.IGNORECASE),
]

MULTI_STEP_PATTERNS = [
    re.compile(
        r"(?:entered?|typed?|input|submitted?)\s+.{3,40}?\s*"
        r"(?:then|but|and\s+then|after\s+that)\s+.{3,40}?\s*"
        r"(?:then|but|and\s+then|after\s+that|\.{2,})\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:step\s*\d|first\s+.{5,30}?\s+then|after\s+.{5,30}?\s+it\s+(?:froze|crashed|failed|stopped))",
        re.IGNORECASE,
    ),
    re.compile(r"(?:was\s+(?:about\s+to|in\s+the\s+middle\s+of)|during\s+(?:the\s+)?)\s*\w+", re.IGNORECASE),
]


FUNNEL_PROMPT = """\
You are a UX researcher specializing in funnel analysis for Maya, \
a fintech super-app in the Philippines.

Below are {count} user reviews that contain signals of retry behavior, \
abandonment, or multi-step failure sequences. Analyze them to extract \
structured funnel intelligence.

Reviews:
{reviews_text}

Return a JSON object with this exact structure:
{{
  "retry_analysis": [
    {{
      "journey": "onboarding|payments|transfers|savings|credit|crypto|support|general",
      "step": "specific step where retries occur (e.g. 'OTP verification', 'KYC document upload')",
      "retry_count_range": "e.g. '3-5 times' or '10+ times'",
      "eventual_outcome": "success_after_retries|still_failing|gave_up",
      "evidence_count": <number of reviews mentioning this>,
      "quotes": ["exact quote"]
    }}
  ],
  "abandonment_analysis": [
    {{
      "journey": "which user journey",
      "abandonment_point": "specific screen/step where users abandon (e.g. 'KYC selfie capture')",
      "destination": "where users go instead (e.g. 'GCash', 'uninstall', 'competitor')",
      "trigger": "what caused the abandonment",
      "evidence_count": <number>,
      "quotes": ["exact quote"]
    }}
  ],
  "multi_step_failures": [
    {{
      "journey": "which user journey",
      "steps": [
        {{"step_number": 1, "action": "what user did", "outcome": "success|partial|failure"}},
        {{"step_number": 2, "action": "what user did next", "outcome": "success|partial|failure"}}
      ],
      "failure_point": "which step failed",
      "quotes": ["exact quote describing the sequence"]
    }}
  ],
  "drop_off_hotspots": [
    {{
      "screen_or_step": "specific screen name or step (e.g. 'Login > OTP entry')",
      "journey": "which user journey",
      "evidence_count": <number of reviews indicating drop-off here>,
      "severity": 1-5,
      "signals": ["retry", "abandonment", "error", "freeze"],
      "recommendation": "specific fix for this hotspot"
    }}
  ]
}}

Focus on SPECIFIC screens and steps, not generic labels. \
Use quotes from reviews to identify exact UI locations. \
Return ONLY valid JSON, no markdown fences or commentary."""


def _extract_signals(reviews_df: pd.DataFrame) -> pd.DataFrame:
    """Tag reviews that contain funnel signals via regex matching."""
    signals = []
    for _, row in reviews_df.iterrows():
        text = str(row.get("text", ""))
        if not text.strip():
            continue

        retry_matches = any(p.search(text) for p in RETRY_PATTERNS)
        abandonment_matches = any(p.search(text) for p in ABANDONMENT_PATTERNS)
        multi_step_matches = any(p.search(text) for p in MULTI_STEP_PATTERNS)

        if retry_matches or abandonment_matches or multi_step_matches:
            signals.append({
                "date": row.get("date"),
                "rating": row.get("rating"),
                "text": text,
                "platform": row.get("platform", "?"),
                "has_retry": retry_matches,
                "has_abandonment": abandonment_matches,
                "has_multi_step": multi_step_matches,
            })

    return pd.DataFrame(signals) if signals else pd.DataFrame()


def _format_signal_reviews(df: pd.DataFrame) -> str:
    """Format signal-tagged reviews for the LLM prompt."""
    lines = []
    for _, row in df.iterrows():
        stars = "*" * int(row["rating"]) if pd.notna(row["rating"]) else "?"
        platform = row.get("platform", "?")
        tags = []
        if row.get("has_retry"):
            tags.append("RETRY")
        if row.get("has_abandonment"):
            tags.append("ABANDON")
        if row.get("has_multi_step"):
            tags.append("MULTI-STEP")
        tag_str = f" [{', '.join(tags)}]"
        text = str(row["text"]).strip().replace("\n", " ")
        lines.append(f"[{stars}] [{platform}]{tag_str} {text}")
    return "\n".join(lines)


def run(reviews_df: pd.DataFrame, suffix: str = "") -> dict:
    """
    Run funnel analysis. If output file exists, load cached results.
    Returns structured funnel data with retry, abandonment, and drop-off analysis.
    """
    data_dir = config.output_dir()
    output_path = data_dir / f"funnel_analysis{suffix}.json"
    max_signal_reviews = config.get("funnel", "max_signal_reviews", 300)
    inter_delay = config.get("funnel", "inter_call_delay_seconds", 10)

    if output_path.exists():
        logger.info(f"Loading cached funnel analysis from {output_path}")
        with open(output_path) as f:
            return json.load(f)

    logger.info("Running funnel analysis: extracting signals via regex...")
    signal_df = _extract_signals(reviews_df)

    if signal_df.empty:
        logger.warning("No funnel signals found in reviews")
        result = {
            "total_reviews_scanned": len(reviews_df),
            "signal_reviews_found": 0,
            "retry_analysis": [],
            "abandonment_analysis": [],
            "multi_step_failures": [],
            "drop_off_hotspots": [],
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2, default=str)
        return result

    # Prioritize low-rating reviews and limit count
    signal_df = signal_df.sort_values("rating", ascending=True).head(max_signal_reviews)

    logger.info(
        f"Found {len(signal_df)} signal reviews "
        f"(retry: {signal_df['has_retry'].sum()}, "
        f"abandonment: {signal_df['has_abandonment'].sum()}, "
        f"multi-step: {signal_df['has_multi_step'].sum()})"
    )

    reviews_text = _format_signal_reviews(signal_df)
    prompt = FUNNEL_PROMPT.format(
        count=len(signal_df),
        reviews_text=reviews_text,
    )

    model = llm.get_model()
    try:
        analysis = llm.call(model, prompt)
    except Exception as e:
        logger.error(f"Funnel analysis LLM call failed: {e}")
        analysis = {
            "retry_analysis": [],
            "abandonment_analysis": [],
            "multi_step_failures": [],
            "drop_off_hotspots": [],
        }

    result = {
        "total_reviews_scanned": len(reviews_df),
        "signal_reviews_found": len(signal_df),
        "signal_breakdown": {
            "retry": int(signal_df["has_retry"].sum()),
            "abandonment": int(signal_df["has_abandonment"].sum()),
            "multi_step": int(signal_df["has_multi_step"].sum()),
        },
        **analysis,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    logger.info(f"Saved funnel analysis to {output_path}")

    return result
