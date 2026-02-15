"""
Comprehensive Analysis module.
Analyzes all reviews together using Gemini API to extract deep UX insights,
competitive intelligence, trust concerns, user segments, and feature requests.
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


ANALYSIS_PROMPT = """\
You are a senior UX researcher analyzing user reviews of Maya, \
a leading fintech app in the Philippines (payments, transfers, savings, credit, crypto).

Below are {count} user reviews (sampled from {total} total). \
Rating distribution: {rating_dist}. Platform split: {platform_split}.

Reviews:
{reviews_text}

Perform a comprehensive UX analysis and return a JSON object with this exact structure:
{{
  "critical_pain_points": [
    {{
      "theme": "short label",
      "description": "detailed description of the issue",
      "affected_journey": "onboarding|payments|transfers|savings|credit|crypto|support|general",
      "business_impact": "activation|retention|transaction_volume|trust|revenue",
      "severity": 1-5,
      "frequency": "high|medium|low",
      "user_quotes": ["exact quote 1", "exact quote 2", "exact quote 3"],
      "interaction_details": {{
        "trigger_action": "what the user was trying to do (e.g. 'enter OTP code')",
        "ui_element": "specific UI element involved (e.g. 'OTP input field', 'Submit button', 'camera overlay')",
        "expected_behavior": "what the user expected to happen",
        "actual_behavior": "what actually happened (e.g. 'app froze', 'error displayed', 'nothing happened')",
        "screen_location": "specific screen path (e.g. 'Login > OTP entry', 'Send Money > Recipient search > Amount input')",
        "error_messages_seen": ["exact error text quoted from reviews, if any"]
      }}
    }}
  ],
  "competitive_insights": [
    {{
      "competitor": "app name",
      "area": "what's being compared",
      "user_preference": "maya|competitor|mixed",
      "detail": "what specifically users prefer and why",
      "quotes": ["exact quote"]
    }}
  ],
  "trust_security_concerns": [
    {{
      "concern": "description",
      "severity": 1-5,
      "category": "data_privacy|fraud|account_security|transparency|reliability",
      "quotes": ["exact quote"]
    }}
  ],
  "feature_requests": [
    {{
      "feature": "what users want",
      "user_need": "the underlying need this addresses",
      "frequency": "high|medium|low",
      "impact_area": "activation|retention|transaction_volume|trust|revenue",
      "quotes": ["exact quote"]
    }}
  ],
  "positive_signals": [
    {{
      "theme": "what works well",
      "description": "details",
      "frequency": "high|medium|low",
      "user_journey": "which part of the experience",
      "specific_flow": "the exact flow or feature that works well (e.g. 'Send Money to bank account')",
      "success_factors": ["specific reasons it works well (e.g. 'fast processing', 'clear confirmation')"],
      "comparative_praise": "if users compare favorably to competitors, note what and why",
      "quotes": ["exact positive quote 1", "exact positive quote 2"]
    }}
  ],
  "user_segments": [
    {{
      "segment": "segment name (e.g. first-time users, power users, credit users)",
      "characteristics": "what defines this segment based on reviews",
      "primary_needs": ["need 1", "need 2"],
      "primary_frustrations": ["frustration 1", "frustration 2"]
    }}
  ]
}}

Be thorough. Focus on actionable findings for a UX redesign.
Pay special attention to GCash comparisons since it's the main competitor.
Return ONLY valid JSON, no markdown fences or commentary."""


SYNTHESIS_PROMPT = """\
You are a senior UX researcher. Below are {n_chunks} separate analyses of Maya app reviews, \
each covering a different sample of reviews. Synthesize them into a single unified analysis.

Chunk analyses:
{chunks_json}

Merge and deduplicate findings across chunks. Keep the strongest quotes. \
Adjust severity and frequency based on how often themes recur across chunks.

When merging critical_pain_points, preserve and merge interaction_details fields: \
combine trigger_action, ui_element, screen_location from multiple chunks for the same theme. \
Pick the most specific screen_location available across chunks (e.g. prefer \
"Login > OTP entry" over just "Login Screen"). Merge error_messages_seen lists.

When merging positive_signals, preserve specific_flow, success_factors, \
comparative_praise, and quotes fields. Combine success_factors lists and keep \
the most specific quotes.

Return a single JSON object with the same structure as the individual analyses:
{{
  "critical_pain_points": [...],
  "competitive_insights": [...],
  "trust_security_concerns": [...],
  "feature_requests": [...],
  "positive_signals": [...],
  "user_segments": [...]
}}

Return ONLY valid JSON, no markdown fences or commentary."""


def _sample_diverse(df: pd.DataFrame, n: int, seed: int = 42) -> pd.DataFrame:
    """Sample ensuring diversity of ratings and platforms."""
    if len(df) <= n:
        return df

    sampled = []
    for platform in df["platform"].unique():
        for rating in sorted(df["rating"].dropna().unique()):
            subset = df[(df["platform"] == platform) & (df["rating"] == rating)]
            if len(subset) == 0:
                continue
            proportion = len(subset) / len(df)
            k = max(1, int(proportion * n))
            subset = subset.assign(
                _len=subset["text"].str.len()
            ).sort_values("_len", ascending=False)
            sampled.append(subset.head(k))

    result = pd.concat(sampled).drop(columns=["_len"], errors="ignore")
    return result.head(n).sample(frac=1, random_state=seed)


def _format_reviews(df: pd.DataFrame) -> str:
    """Format reviews for the prompt."""
    lines = []
    for _, row in df.iterrows():
        stars = "*" * int(row["rating"]) if pd.notna(row["rating"]) else "?"
        platform = row.get("platform", "?")
        date_str = ""
        if pd.notna(row.get("date")):
            date_str = f" ({str(row['date'])[:10]})"
        text = str(row["text"]).strip().replace("\n", " ")
        lines.append(f"[{stars}] [{platform}]{date_str} {text}")
    return "\n".join(lines)


def analyze_chunk(model, chunk_df: pd.DataFrame, total: int) -> dict:
    """Analyze a single chunk of reviews."""
    reviews_text = _format_reviews(chunk_df)

    rating_dist = chunk_df["rating"].value_counts().sort_index().to_dict()
    rating_str = ", ".join(f"{int(k)}*: {v}" for k, v in rating_dist.items())
    platform_split = ", ".join(
        f"{k}: {v}" for k, v in chunk_df["platform"].value_counts().to_dict().items()
    )

    prompt = ANALYSIS_PROMPT.format(
        count=len(chunk_df),
        total=total,
        rating_dist=rating_str,
        platform_split=platform_split,
        reviews_text=reviews_text,
    )

    return llm.call(model, prompt)


def synthesize(model, chunk_results: list[dict]) -> dict:
    """Synthesize multiple chunk analyses into a unified analysis."""
    if len(chunk_results) == 1:
        return chunk_results[0]

    prompt = SYNTHESIS_PROMPT.format(
        n_chunks=len(chunk_results),
        chunks_json=json.dumps(chunk_results, indent=1),
    )

    return llm.call(model, prompt)


def run(reviews_df: pd.DataFrame, suffix: str = "") -> dict:
    """
    Run comprehensive analysis. If output file exists, load cached results.
    suffix: e.g. '_1star' for filtered runs, '' for full analysis.
    """
    data_dir = config.output_dir()
    max_per_chunk = config.get("comprehensive", "max_reviews_per_chunk", 200)
    max_chunks = config.get("comprehensive", "max_chunks", 5)
    inter_delay = config.get("comprehensive", "inter_call_delay_seconds", 10)

    output_path = data_dir / f"comprehensive_analysis{suffix}.json"
    if output_path.exists():
        logger.info(f"Loading cached comprehensive analysis from {output_path}")
        with open(output_path) as f:
            return json.load(f)

    model = llm.get_model()
    total = len(reviews_df)

    n_chunks = min(max_chunks, max(1, total // max_per_chunk))
    chunk_size = max_per_chunk

    logger.info(
        f"Running comprehensive analysis: {total} reviews in {n_chunks} chunk(s)"
    )

    chunk_results = []
    for i in range(n_chunks):
        chunk_df = _sample_diverse(reviews_df, chunk_size, seed=42 + i)
        logger.info(f"  Chunk {i + 1}/{n_chunks}: analyzing {len(chunk_df)} reviews...")

        try:
            result = analyze_chunk(model, chunk_df, total)
            chunk_results.append(result)
            logger.info(f"  Chunk {i + 1} done.")
        except Exception as e:
            logger.warning(f"  Chunk {i + 1} LLM failed: {e} — using TextBlob fallback")
            try:
                result = sentiment.analyze_comprehensive_fallback(chunk_df)
                chunk_results.append(result)
                logger.info(f"  Chunk {i + 1} done (TextBlob fallback).")
            except Exception as fb_err:
                logger.error(f"  Chunk {i + 1} TextBlob fallback also failed: {fb_err}")

        if i < n_chunks - 1:
            time.sleep(inter_delay)

    if not chunk_results:
        logger.error("All chunks failed. Using full TextBlob fallback.")
        analysis = sentiment.analyze_comprehensive_fallback(reviews_df)
        output = {
            "analysis_date": datetime.now().isoformat(),
            "total_reviews": total,
            "chunks_analyzed": 0,
            "analysis": analysis,
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2, default=str)
        logger.info(f"Saved TextBlob fallback analysis to {output_path}")
        return output

    # If all chunks were fallback results, skip LLM synthesis
    all_fallback = all(r.get("_fallback") for r in chunk_results)

    logger.info("Synthesizing chunk results...")
    if all_fallback or len(chunk_results) == 1:
        if all_fallback and len(chunk_results) > 1:
            logger.info("  All chunks used TextBlob fallback; merging without LLM.")
        analysis = chunk_results[0]
    else:
        try:
            analysis = synthesize(model, chunk_results)
        except Exception as e:
            logger.error(f"Synthesis failed, using first chunk: {e}")
            analysis = chunk_results[0]

    output = {
        "analysis_date": datetime.now().isoformat(),
        "total_reviews": total,
        "chunks_analyzed": len(chunk_results),
        "analysis": analysis,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    logger.info(f"Saved comprehensive analysis to {output_path}")

    return output
