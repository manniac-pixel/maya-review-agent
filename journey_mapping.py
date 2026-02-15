"""
Journey Mapping module.
Aggregates pain points from all analysis stages, groups them by user journey,
computes per-journey friction scores, and uses the LLM to map issues to
specific screens and flows within the Maya app.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import config
import llm

logger = logging.getLogger(__name__)

# Canonical journey names used throughout the codebase.
JOURNEYS = [
    "onboarding",
    "kyc",
    "payments",
    "transfers",
    "savings",
    "credit",
    "crypto",
    "support",
    "general",
]

# Weights for friction score computation (loaded from config at call time).
_DEFAULT_FREQ_WEIGHT = {"high": 3, "medium": 2, "low": 1}
_DEFAULT_TREND_WEIGHT = {"emerging": 1.5, "persistent": 1.2, "resolved": 0.3}


JOURNEY_PROMPT = """\
You are a senior UX researcher mapping user pain points to specific screens \
and flows inside Maya, a fintech super-app in the Philippines.

Below are pain points grouped by user journey, with severity and frequency \
data derived from real user reviews.

{journey_summaries}

For EACH journey that has pain points, return a JSON object with this exact structure:
{{
  "journeys": [
    {{
      "journey": "journey name (e.g. onboarding)",
      "friction_summary": "1-2 sentence summary of the overall friction in this journey",
      "screens": [
        {{
          "screen": "specific screen or flow step (e.g. 'Phone number verification', 'OTP entry', 'Document upload camera')",
          "pain_points": ["theme 1", "theme 2"],
          "description": "what goes wrong at this screen",
          "severity": 1-5,
          "recommendation": "specific fix for this screen",
          "interaction_failures": [
            {{
              "user_action": "what the user does (e.g. 'tap Submit button')",
              "ui_element": "specific element (e.g. 'Submit button', 'OTP input field')",
              "failure_mode": "what goes wrong (e.g. 'button unresponsive', 'spinner never stops')",
              "error_message": "exact error text if known, or null"
            }}
          ]
        }}
      ],
      "flow_sequence": [
        {{
          "step_number": 1,
          "screen_name": "specific screen name",
          "user_action": "what the user does at this step",
          "known_issues": ["issues reported at this step"],
          "drop_off_risk": "high|medium|low|none"
        }}
      ],
      "highest_friction_screen": "the single screen with the worst user experience",
      "improvement_priority": "critical|high|medium|low"
    }}
  ]
}}

Guidelines:
- Screen names should be specific UI locations a designer can find (e.g. \
"Send Money — recipient search", not just "transfers").
- flow_sequence: the typical user path through this journey, as a list of screen names.
- Only include journeys that have actual pain points listed above.
- Base screen identification on the pain point descriptions and user quotes, \
not assumptions about generic fintech apps.
Return ONLY valid JSON, no markdown fences or commentary."""


# ── Data collection ──────────────────────────────────────────────────────────

def _normalize_journey(raw: str) -> str:
    """Map freeform journey strings to canonical names."""
    if not raw or not isinstance(raw, str):
        return "general"
    raw_lower = raw.lower().strip()

    aliases = {
        "onboarding": "onboarding",
        "registration": "onboarding",
        "sign_up": "onboarding",
        "signup": "onboarding",
        "kyc": "kyc",
        "identity": "kyc",
        "verification": "kyc",
        "payments": "payments",
        "pay": "payments",
        "bills": "payments",
        "merchant": "payments",
        "transfers": "transfers",
        "transfer": "transfers",
        "send": "transfers",
        "remittance": "transfers",
        "savings": "savings",
        "save": "savings",
        "credit": "credit",
        "loan": "credit",
        "loans": "credit",
        "crypto": "crypto",
        "support": "support",
        "customer_support": "support",
        "customer support": "support",
        "general": "general",
        "performance": "general",
        "ui": "general",
        "ux": "general",
        "app": "general",
    }

    for alias, canonical in aliases.items():
        if alias in raw_lower:
            return canonical
    return "general"


def _collect_pain_points(
    insights: dict,
    comprehensive_data: dict,
    temporal_data: dict,
    funnel_data: dict | None = None,
) -> list[dict]:
    """
    Gather pain points from all analysis outputs into a unified list.
    Each item has: theme, journey, severity, frequency, trend, source, quotes,
    and optionally interaction_details.
    """
    seen_themes: set[str] = set()
    points: list[dict] = []

    def _add(theme, journey, severity, frequency, trend, source,
             quotes=None, interaction_details=None):
        key = theme.lower().strip()
        if key in seen_themes:
            return
        seen_themes.add(key)
        point = {
            "theme": theme,
            "journey": _normalize_journey(journey),
            "severity": severity if isinstance(severity, (int, float)) else 3,
            "frequency": frequency if isinstance(frequency, str) else "medium",
            "trend": trend,
            "source": source,
            "quotes": (quotes or [])[:3],
        }
        if interaction_details:
            point["interaction_details"] = interaction_details
        points.append(point)

    # 1. Ranked UX opportunities (highest quality — synthesised by insights LLM)
    for opp in insights.get("ranked_ux_opportunities", []):
        _add(
            opp.get("theme", ""),
            opp.get("affected_journey", ""),
            opp.get("severity", 3),
            opp.get("frequency", "medium"),
            "unknown",
            "insights",
            opp.get("user_quotes"),
        )

    # 2. Comprehensive critical pain points (with interaction_details)
    analysis = comprehensive_data.get("analysis", {})
    for pp in analysis.get("critical_pain_points", []):
        _add(
            pp.get("theme", ""),
            pp.get("affected_journey", ""),
            pp.get("severity", 3),
            pp.get("frequency", "medium"),
            "unknown",
            "comprehensive",
            pp.get("user_quotes"),
            interaction_details=pp.get("interaction_details"),
        )

    # 3. Temporal trends — tag with lifecycle status
    trends = temporal_data.get("trends", {})
    for issue in trends.get("persistent_issues", trends.get("persistent", [])):
        if isinstance(issue, dict):
            _add(
                issue.get("theme", ""),
                "",  # temporal trends don't carry journey info
                issue.get("severity", 3),
                issue.get("frequency", "medium"),
                "persistent",
                "temporal",
            )
    for issue in trends.get("emerging_issues", trends.get("emerging", [])):
        if isinstance(issue, dict):
            _add(
                issue.get("theme", ""),
                "",
                issue.get("severity", 3),
                "medium",
                "emerging",
                "temporal",
            )
    for issue in trends.get("resolved_issues", trends.get("resolved", [])):
        if isinstance(issue, dict):
            _add(
                issue.get("theme", ""),
                "",
                issue.get("severity", 2),
                "low",
                "resolved",
                "temporal",
            )

    # 4. Funnel drop-off hotspots as additional pain point sources
    if funnel_data:
        for hotspot in funnel_data.get("drop_off_hotspots", []):
            _add(
                f"Drop-off: {hotspot.get('screen_or_step', 'unknown')}",
                hotspot.get("journey", ""),
                hotspot.get("severity", 3),
                "high" if hotspot.get("evidence_count", 0) >= 5 else "medium",
                "unknown",
                "funnel",
            )

    return points


# ── Friction scoring ─────────────────────────────────────────────────────────

def _score_journey(points: list[dict]) -> float:
    """Compute aggregate friction score for a list of pain points."""
    freq_weight = config.get("journey", "freq_weight", _DEFAULT_FREQ_WEIGHT)
    trend_weight = config.get("journey", "trend_weight", _DEFAULT_TREND_WEIGHT)

    total = 0.0
    for p in points:
        sev = p.get("severity", 3)
        freq = freq_weight.get(p.get("frequency", "medium"), 2)
        trend = trend_weight.get(p.get("trend", "unknown"), 1.0)
        total += sev * freq * trend
    return round(total, 1)


def _group_by_journey(points: list[dict]) -> dict[str, list[dict]]:
    """Group pain points by canonical journey name."""
    grouped: dict[str, list[dict]] = {}
    for p in points:
        journey = p["journey"]
        grouped.setdefault(journey, []).append(p)
    return grouped


# ── LLM screen mapping ──────────────────────────────────────────────────────

def _build_journey_summaries(grouped: dict[str, list[dict]]) -> str:
    """Format grouped pain points for the LLM prompt, including interaction details."""
    sections = []
    for journey in JOURNEYS:
        points = grouped.get(journey, [])
        if not points:
            continue
        lines = [f"## Journey: {journey.upper()} ({len(points)} pain points)"]
        for p in sorted(points, key=lambda x: -x.get("severity", 0)):
            trend_tag = f" [{p['trend']}]" if p["trend"] != "unknown" else ""
            lines.append(
                f"- {p['theme']} (severity {p['severity']}/5, "
                f"frequency: {p['frequency']}{trend_tag})"
            )
            # Include interaction details if available
            idet = p.get("interaction_details")
            if idet and isinstance(idet, dict):
                trigger = idet.get("trigger_action", "")
                actual = idet.get("actual_behavior", "")
                screen = idet.get("screen_location", "")
                if trigger:
                    lines.append(f"  Trigger: {trigger}")
                if actual:
                    lines.append(f"  Actual behavior: {actual}")
                if screen:
                    lines.append(f"  Screen: {screen}")
            for q in p.get("quotes", [])[:2]:
                lines.append(f'  > "{q}"')
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


# ── Public API ───────────────────────────────────────────────────────────────

def run(
    insights: dict,
    comprehensive_data: dict,
    temporal_data: dict,
    suffix: str = "",
    funnel_data: dict | None = None,
    accessibility_data: dict | None = None,
) -> dict:
    """
    Build a journey friction map. Caches to data/journey_map{suffix}.json.
    Returns a dict with journey_scores (sorted) and llm screen mapping.
    funnel_data: optional funnel analysis results (drop-off hotspots added as pain points).
    accessibility_data: optional accessibility data (reserved for future enrichment).
    """
    json_output = config.output_dir() / f"journey_map{suffix}.json"

    if json_output.exists():
        logger.info(f"Loading cached journey map from {json_output}")
        with open(json_output) as f:
            return json.load(f)

    # ── Collect & score ──────────────────────────────────────────────────
    all_points = _collect_pain_points(
        insights, comprehensive_data, temporal_data, funnel_data=funnel_data,
    )
    logger.info(f"Collected {len(all_points)} unique pain points for journey mapping")

    grouped = _group_by_journey(all_points)

    journey_scores = []
    for journey in JOURNEYS:
        points = grouped.get(journey, [])
        if not points:
            continue
        journey_scores.append({
            "journey": journey,
            "pain_point_count": len(points),
            "friction_score": _score_journey(points),
            "top_themes": [p["theme"] for p in sorted(
                points, key=lambda x: -x.get("severity", 0),
            )[:5]],
        })

    journey_scores.sort(key=lambda j: -j["friction_score"])

    if not journey_scores:
        logger.warning("No pain points to map — skipping journey mapping")
        return {}

    logger.info(
        f"Journey friction scores: "
        + ", ".join(f"{j['journey']}={j['friction_score']}" for j in journey_scores[:5])
    )

    # ── LLM screen-level mapping ─────────────────────────────────────────
    summaries_text = _build_journey_summaries(grouped)
    prompt = JOURNEY_PROMPT.format(journey_summaries=summaries_text)

    model = llm.get_model()
    try:
        screen_map = llm.call(model, prompt)
    except Exception as e:
        logger.error(f"Journey screen mapping LLM call failed: {e}")
        screen_map = {"journeys": []}

    # ── Assemble output ──────────────────────────────────────────────────
    result = {
        "journey_scores": journey_scores,
        "screen_mapping": screen_map,
        "total_pain_points": len(all_points),
    }

    json_output.parent.mkdir(parents=True, exist_ok=True)
    with open(json_output, "w") as f:
        json.dump(result, f, indent=2, default=str)
    logger.info(f"Saved journey map to {json_output}")

    return result
