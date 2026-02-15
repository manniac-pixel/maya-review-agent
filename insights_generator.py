"""
Insights Generator module.
Combines temporal + comprehensive analysis into a final ranked report
with executive summary, scored UX opportunities, and actionable recommendations.
Exports to JSON and Markdown.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

import llm
import journey_mapping
import visualizations

logger = logging.getLogger(__name__)

DEFAULT_JSON_OUTPUT = Path("data/final_insights.json")
DEFAULT_MD_OUTPUT = Path("data/maya_insights_report.md")


INSIGHTS_PROMPT = """\
You are a senior UX strategist preparing a UX audit report for Maya, \
a leading fintech app in the Philippines.

You have two data sources:

## TEMPORAL ANALYSIS (trends over time)
{temporal_json}

## COMPREHENSIVE ANALYSIS (deep dive across all reviews)
{comprehensive_json}

Combine both analyses and produce a final strategic insights report as JSON:
{{
  "executive_summary": {{
    "total_reviews_analyzed": <number>,
    "date_range": "YYYY-MM to YYYY-MM",
    "overall_sentiment": "brief assessment",
    "top_persistent_issues": [
      {{"theme": "...", "description": "...", "months_active": <number>}}
    ],
    "top_emerging_issues": [
      {{"theme": "...", "description": "...", "first_seen": "YYYY-MM"}}
    ],
    "top_resolved_issues": [
      {{"theme": "...", "description": "...", "evidence": "..."}}
    ]
  }},
  "ranked_ux_opportunities": [
    {{
      "rank": 1,
      "theme": "...",
      "description": "detailed description",
      "severity": 1-5,
      "frequency": "high|medium|low",
      "business_impact": "activation|retention|transaction_volume|trust|revenue",
      "priority_score": <number>,
      "affected_journey": "...",
      "user_quotes": ["quote1", "quote2"],
      "recommendation": "specific actionable recommendation",
      "category": "quick_win|strategic_bet|maintenance"
    }}
  ],
  "quick_wins": [
    {{
      "issue": "...",
      "recommendation": "...",
      "effort": "low",
      "impact": "high|medium",
      "rationale": "why this is a quick win"
    }}
  ],
  "strategic_bets": [
    {{
      "initiative": "...",
      "description": "...",
      "effort": "high",
      "impact": "high",
      "user_need": "the core user need this addresses",
      "competitive_context": "how competitors handle this"
    }}
  ],
  "competitive_gaps": [
    {{
      "area": "...",
      "competitor": "GCash or other",
      "gap_description": "what Maya lacks",
      "user_quotes": ["quote"],
      "recommendation": "..."
    }}
  ],
  "user_segment_insights": [
    {{
      "segment": "...",
      "size_signal": "how prominent in reviews",
      "top_needs": ["..."],
      "top_frustrations": ["..."],
      "opportunity": "..."
    }}
  ],
  "positive_flow_benchmarks": [
    {{
      "flow": "specific flow that works well (e.g. 'Send Money to bank')",
      "journey": "which user journey this belongs to",
      "what_works": "why users praise this flow",
      "success_factors": ["specific reasons it works (e.g. 'fast processing', 'clear feedback')"],
      "competitive_advantage": "how this compares to competitors (if mentioned)",
      "preservation_priority": "critical|high|medium — how important to preserve in redesign",
      "quotes": ["exact positive quote from users"]
    }}
  ],
  "trend_summary": {{
    "improving_areas": ["..."],
    "declining_areas": ["..."],
    "stable_pain_points": ["..."]
  }}
}}

PRIORITY SCORING FORMULA:
score = (severity * 2) + frequency_score + business_impact_score
Where: frequency: high=3, medium=2, low=1
       business_impact: activation=3, retention=2, transaction_volume=1, trust=2, revenue=2

Rank opportunities by priority_score descending.
Quick wins = high impact + low effort (UI/copy fixes, error message improvements, etc.)
Strategic bets = high impact + high effort (new features, major redesigns)

Be specific and actionable. Every recommendation should be something a product/design team can act on.
Return ONLY valid JSON, no markdown fences or commentary."""


def _generate_markdown(
    insights: dict,
    chart_paths: dict[str, str] | None = None,
    comparison: dict | None = None,
    journey_map: dict | None = None,
) -> str:
    """Convert structured insights into a formatted Markdown report."""
    charts = chart_paths or {}
    lines = []

    lines.append("# Maya App UX Review Analysis Report")
    lines.append(f"\n*Generated: {datetime.now().strftime('%B %d, %Y')}*\n")

    # Executive Summary
    es = insights.get("executive_summary", {})
    lines.append("## Executive Summary\n")
    lines.append(
        f"**Reviews analyzed:** {es.get('total_reviews_analyzed', 'N/A')} | "
        f"**Period:** {es.get('date_range', 'N/A')}"
    )
    lines.append(f"\n**Overall sentiment:** {es.get('overall_sentiment', 'N/A')}\n")

    if "rating_trend" in charts:
        lines.append(f"![Rating Trend Over Time]({charts['rating_trend']})\n")
    if "sentiment_distribution" in charts:
        lines.append(f"![Sentiment Distribution]({charts['sentiment_distribution']})\n")
    if "business_impact" in charts:
        lines.append(f"![Business Impact Distribution]({charts['business_impact']})\n")

    lines.append("### Top Persistent Issues (Not Resolved)")
    for item in es.get("top_persistent_issues", []):
        lines.append(
            f"- **{item['theme']}**: {item['description']} "
            f"*(active {item.get('months_active', '?')} months)*"
        )

    lines.append("\n### Emerging Issues (New Problems)")
    for item in es.get("top_emerging_issues", []):
        lines.append(
            f"- **{item['theme']}**: {item['description']} "
            f"*(first seen {item.get('first_seen', '?')})*"
        )

    lines.append("\n### Resolved Issues (Improvements by Maya)")
    for item in es.get("top_resolved_issues", []):
        lines.append(
            f"- **{item['theme']}**: {item['description']} "
            f"-- *{item.get('evidence', '')}*"
        )

    # Ranked UX Opportunities
    lines.append("\n---\n## Ranked UX Opportunities\n")
    lines.append(
        "| Rank | Issue | Severity | Frequency | Impact | Score | Category |"
    )
    lines.append("|------|-------|----------|-----------|--------|-------|----------|")
    for opp in insights.get("ranked_ux_opportunities", []):
        lines.append(
            f"| {opp.get('rank', '-')} | {opp['theme']} | "
            f"{opp.get('severity', '-')}/5 | {opp.get('frequency', '-')} | "
            f"{opp.get('business_impact', '-')} | "
            f"**{opp.get('priority_score', '-')}** | "
            f"{opp.get('category', '-')} |"
        )

    if "priority_bar" in charts:
        lines.append(f"\n![Priority Score Bar Chart]({charts['priority_bar']})\n")
    if "severity_frequency" in charts:
        lines.append(f"![Severity vs Frequency]({charts['severity_frequency']})\n")
    if "pain_point_frequency" in charts:
        lines.append(f"![Pain Point Frequency]({charts['pain_point_frequency']})\n")

    lines.append("\n### Detailed Recommendations\n")
    for opp in insights.get("ranked_ux_opportunities", []):
        lines.append(f"#### #{opp.get('rank', '-')}: {opp['theme']}\n")
        lines.append(f"**Journey:** {opp.get('affected_journey', 'N/A')}\n")
        lines.append(f"{opp.get('description', '')}\n")
        lines.append(f"**Recommendation:** {opp.get('recommendation', '')}\n")
        quotes = opp.get("user_quotes", [])
        if quotes:
            lines.append("**User voices:**")
            for q in quotes[:3]:
                lines.append(f'> "{q}"')
            lines.append("")

    if "severity_heatmap" in charts:
        lines.append(f"![Monthly Severity Heatmap]({charts['severity_heatmap']})\n")

    # Journey Friction Map
    if journey_map and journey_map.get("journey_scores"):
        lines.append("---\n## Journey Friction Map\n")

        # Friction score table
        lines.append("| Journey | Pain Points | Friction Score | Top Issues |")
        lines.append("|---------|-------------|----------------|------------|")
        for j in journey_map["journey_scores"]:
            top = ", ".join(j.get("top_themes", [])[:3])
            lines.append(
                f"| **{j['journey'].replace('_', ' ').title()}** | "
                f"{j['pain_point_count']} | "
                f"**{j['friction_score']}** | "
                f"{top} |"
            )
        lines.append("")

        # Screen-level detail per journey
        screen_data = journey_map.get("screen_mapping", {})
        journeys_detail = screen_data.get("journeys", [])
        if journeys_detail:
            lines.append("### Screen-Level Breakdown\n")
            for jd in journeys_detail:
                name = jd.get("journey", "?").replace("_", " ").title()
                priority = jd.get("improvement_priority", "?")
                lines.append(f"#### {name} (priority: {priority})\n")

                summary = jd.get("friction_summary", "")
                if summary:
                    lines.append(f"{summary}\n")

                flow = jd.get("flow_sequence", [])
                if flow:
                    lines.append(
                        "**Flow:** " + " → ".join(f"`{s}`" for s in flow) + "\n"
                    )

                hotspot = jd.get("highest_friction_screen", "")
                if hotspot:
                    lines.append(f"**Highest-friction screen:** `{hotspot}`\n")

                for screen in jd.get("screens", []):
                    sname = screen.get("screen", "?")
                    sev = screen.get("severity", "?")
                    lines.append(f"- **{sname}** (severity {sev}/5)")
                    desc = screen.get("description", "")
                    if desc:
                        lines.append(f"  {desc}")
                    rec = screen.get("recommendation", "")
                    if rec:
                        lines.append(f"  *Recommendation:* {rec}")
                lines.append("")

    # Positive Flow Benchmarks
    benchmarks = insights.get("positive_flow_benchmarks", [])
    if benchmarks:
        lines.append("---\n## Positive Flow Benchmarks (What Works Well)\n")
        lines.append(
            "| Flow | Journey | What Works | Preservation Priority |"
        )
        lines.append("|------|---------|------------|----------------------|")
        for bench in benchmarks:
            lines.append(
                f"| {bench.get('flow', '-')} | {bench.get('journey', '-')} | "
                f"{bench.get('what_works', '-')} | "
                f"**{bench.get('preservation_priority', '-')}** |"
            )
        lines.append("")

        lines.append("### Detailed Benchmarks\n")
        for bench in benchmarks:
            lines.append(f"#### {bench.get('flow', '?')}\n")
            lines.append(f"**Journey:** {bench.get('journey', 'N/A')}\n")
            lines.append(f"{bench.get('what_works', '')}\n")
            factors = bench.get("success_factors", [])
            if factors:
                lines.append("**Success factors:** " + ", ".join(factors))
            comp_adv = bench.get("competitive_advantage", "")
            if comp_adv:
                lines.append(f"\n**Competitive advantage:** {comp_adv}")
            for q in bench.get("quotes", [])[:2]:
                lines.append(f'> "{q}"')
            lines.append("")

    # Funnel Highlights (if funnel data was injected)
    funnel_highlights = insights.get("_funnel_highlights", {})
    hotspots = funnel_highlights.get("drop_off_hotspots", [])
    if hotspots:
        lines.append("---\n## Funnel Drop-Off Hotspots\n")
        lines.append("| Screen/Step | Journey | Evidence | Severity | Signals |")
        lines.append("|-------------|---------|----------|----------|---------|")
        for h in hotspots:
            signals = ", ".join(h.get("signals", []))
            lines.append(
                f"| {h.get('screen_or_step', '-')} | {h.get('journey', '-')} | "
                f"{h.get('evidence_count', '-')} | {h.get('severity', '-')}/5 | "
                f"{signals} |"
            )
        lines.append("")

    # Quick Wins
    lines.append("---\n## Quick Wins (High Impact, Low Effort)\n")
    for qw in insights.get("quick_wins", []):
        lines.append(f"### {qw['issue']}\n")
        lines.append(f"- **Recommendation:** {qw['recommendation']}")
        lines.append(f"- **Impact:** {qw.get('impact', 'N/A')}")
        lines.append(f"- **Rationale:** {qw.get('rationale', '')}\n")

    # Strategic Bets
    lines.append("---\n## Strategic Bets (High Impact, High Effort)\n")
    for sb in insights.get("strategic_bets", []):
        lines.append(f"### {sb['initiative']}\n")
        lines.append(f"{sb.get('description', '')}\n")
        lines.append(f"- **User need:** {sb.get('user_need', 'N/A')}")
        lines.append(
            f"- **Competitive context:** {sb.get('competitive_context', 'N/A')}\n"
        )

    # Competitive Gaps
    lines.append("---\n## Competitive Gaps\n")
    for cg in insights.get("competitive_gaps", []):
        lines.append(
            f"### {cg['area']} (vs {cg.get('competitor', 'competitors')})\n"
        )
        lines.append(f"{cg.get('gap_description', '')}\n")
        lines.append(f"**Recommendation:** {cg.get('recommendation', '')}\n")
        for q in cg.get("user_quotes", [])[:2]:
            lines.append(f'> "{q}"')
        lines.append("")

    # User Segments
    lines.append("---\n## User Segments\n")
    for seg in insights.get("user_segment_insights", []):
        lines.append(f"### {seg['segment']}\n")
        lines.append(f"*Presence in reviews:* {seg.get('size_signal', 'N/A')}\n")
        needs = seg.get("top_needs", [])
        if needs:
            lines.append("**Needs:** " + ", ".join(needs))
        frustrations = seg.get("top_frustrations", [])
        if frustrations:
            lines.append("**Frustrations:** " + ", ".join(frustrations))
        lines.append(f"\n**Opportunity:** {seg.get('opportunity', '')}\n")

    # Version Spikes (injected from temporal data, not from LLM insights)
    version_analysis = insights.get("_version_analysis", {})
    spike_analyses = version_analysis.get("spike_analyses", {})
    if spike_analyses:
        baseline = version_analysis.get("baseline", {})
        lines.append(
            f"---\n## Version Spike Analysis\n"
        )
        if "version_ratings" in charts:
            lines.append(f"![Version 1-Star Rate]({charts['version_ratings']})\n")
        lines.append(
            f"*Baseline: {baseline.get('one_star_pct', '?')}% 1-star rate, "
            f"avg rating {baseline.get('avg_rating', '?')}/5 "
            f"across {baseline.get('total_versioned_reviews', '?')} versioned reviews*\n"
        )
        version_stats = {
            v["version"]: v
            for v in version_analysis.get("version_stats", [])
        }
        for ver, analysis in spike_analyses.items():
            if "error" in analysis:
                continue
            stats = version_stats.get(ver, {})
            lines.append(
                f"### v{ver} — {stats.get('one_star_pct', '?')}% 1-star "
                f"({stats.get('review_count', '?')} reviews, "
                f"{stats.get('date_first', '?')} to {stats.get('date_last', '?')})\n"
            )
            root = analysis.get("likely_root_cause_summary", "")
            if root:
                lines.append(f"**Root cause:** {root}\n")
            for issue in analysis.get("primary_issues", []):
                lines.append(
                    f"- **{issue.get('theme', '?')}** "
                    f"({issue.get('affected_area', '?')}, "
                    f"likely: {issue.get('likely_cause', '?')}, "
                    f"severity {issue.get('severity', '?')}/5)"
                )
                lines.append(f"  {issue.get('description', '')}")
                for q in issue.get("quotes", [])[:2]:
                    lines.append(f'  > "{q}"')
            vs_previous = analysis.get("comparison_to_previous", "")
            if vs_previous:
                lines.append(f"\n*{vs_previous}*\n")

    # Competitor Comparison (Maya vs GCash)
    if comparison and "error" not in comparison:
        lines.append("---\n## Competitor Comparison: Maya vs GCash\n")
        summary = comparison.get("summary", "")
        if summary:
            lines.append(f"{summary}\n")

        rating_cmp = comparison.get("rating_comparison", {})
        if rating_cmp:
            lines.append(
                f"**Average ratings:** Maya {rating_cmp.get('maya_avg', '?')}/5 | "
                f"GCash {rating_cmp.get('gcash_avg', '?')}/5 — "
                f"*{rating_cmp.get('interpretation', '')}*\n"
            )

        gcash_strengths = comparison.get("gcash_strengths", [])
        if gcash_strengths:
            lines.append("### Where GCash Leads\n")
            for item in gcash_strengths:
                lines.append(f"**{item.get('area', '?')}** — {item.get('description', '')}\n")
                maya_gap = item.get("maya_gap", "")
                if maya_gap:
                    lines.append(f"*Maya gap:* {maya_gap}\n")
                for q in item.get("user_evidence", [])[:2]:
                    lines.append(f'> "{q}"')
                lines.append("")

        maya_strengths = comparison.get("maya_strengths", [])
        if maya_strengths:
            lines.append("### Where Maya Leads\n")
            for item in maya_strengths:
                lines.append(f"**{item.get('area', '?')}** — {item.get('description', '')}\n")
                gcash_gap = item.get("gcash_gap", "")
                if gcash_gap:
                    lines.append(f"*GCash gap:* {gcash_gap}\n")
                for q in item.get("user_evidence", [])[:2]:
                    lines.append(f'> "{q}"')
                lines.append("")

        feature_gaps = comparison.get("feature_gaps", [])
        if feature_gaps:
            lines.append("### Feature Gaps\n")
            lines.append("| Feature | Available In | User Demand | Description |")
            lines.append("|---------|-------------|-------------|-------------|")
            for fg in feature_gaps:
                lines.append(
                    f"| {fg.get('feature', '?')} | {fg.get('available_in', '?')} | "
                    f"{fg.get('user_demand', '?')} | {fg.get('description', '')} |"
                )
            lines.append("")

        shared = comparison.get("shared_pain_points", [])
        if shared:
            lines.append("### Shared Pain Points (Both Apps)\n")
            for item in shared:
                lines.append(f"- **{item.get('issue', '?')}**: {item.get('description', '')}")
            lines.append("")

    # Trend Summary
    ts = insights.get("trend_summary", {})
    lines.append("---\n## Trend Summary\n")
    if "trend_classification" in charts:
        lines.append(f"![Trend Classification]({charts['trend_classification']})\n")
    if "issue_lifecycle" in charts:
        lines.append(f"![Issue Lifecycle]({charts['issue_lifecycle']})\n")
    improving = ts.get("improving_areas", [])
    if improving:
        lines.append("**Getting better:** " + ", ".join(improving))
    declining = ts.get("declining_areas", [])
    if declining:
        lines.append("\n**Getting worse:** " + ", ".join(declining))
    stable = ts.get("stable_pain_points", [])
    if stable:
        lines.append("\n**Unchanged pain points:** " + ", ".join(stable))

    lines.append(
        "\n---\n*Report generated by Maya Review Analysis Agent using Gemini API.*"
    )

    return "\n".join(lines)


def run(
    temporal_data: dict,
    comprehensive_data: dict,
    suffix: str = "",
    comparison: dict | None = None,
    reviews_df=None,
    funnel_data: dict | None = None,
    accessibility_data: dict | None = None,
) -> dict:
    """
    Generate final insights. If output files exist, load cached results.
    suffix: e.g. '_1star' for filtered runs, '' for full analysis.
    comparison: optional competitor comparison dict (Maya vs GCash).
    reviews_df: optional raw DataFrame for chart generation.
    funnel_data: optional funnel analysis results.
    accessibility_data: optional accessibility analysis results.
    """
    json_output = Path(f"data/final_insights{suffix}.json")
    md_output = Path(f"data/maya_insights_report{suffix}.md")

    if json_output.exists():
        logger.info(f"Loading cached insights from {json_output}")
        with open(json_output) as f:
            insights = json.load(f)

        # Run journey mapping even when insights are cached (it has its own cache)
        journey_map_path = Path(f"data/journey_map{suffix}.json")
        if not journey_map_path.exists():
            logger.info("Journey map not found — generating from cached insights...")
            journey_mapping.run(
                insights, comprehensive_data, temporal_data, suffix=suffix,
                funnel_data=funnel_data, accessibility_data=accessibility_data,
            )

        return insights

    model = llm.get_model()

    temporal_condensed = {
        "months_analyzed": temporal_data.get("months_analyzed", []),
        "trends": temporal_data.get("trends", {}),
        "version_analysis": temporal_data.get("version_analysis", {}),
    }

    comprehensive_condensed = comprehensive_data.get("analysis", {})

    prompt = INSIGHTS_PROMPT.format(
        temporal_json=json.dumps(temporal_condensed, indent=1, default=str),
        comprehensive_json=json.dumps(comprehensive_condensed, indent=1, default=str),
    )

    logger.info("Generating final insights with Gemini...")
    try:
        insights = llm.call(model, prompt)
    except Exception as e:
        logger.error(f"Insights generation failed: {e}")
        return {"error": str(e)}

    if "executive_summary" in insights:
        insights["executive_summary"].setdefault(
            "total_reviews_analyzed", comprehensive_data.get("total_reviews", 0)
        )

    # Attach version spike data for the markdown renderer
    version_analysis = temporal_data.get("version_analysis", {})
    if version_analysis.get("spike_analyses"):
        insights["_version_analysis"] = version_analysis

    # Attach funnel highlights for the markdown renderer
    if funnel_data and funnel_data.get("drop_off_hotspots"):
        insights["_funnel_highlights"] = {
            "drop_off_hotspots": funnel_data["drop_off_hotspots"],
        }

    json_output.parent.mkdir(parents=True, exist_ok=True)
    with open(json_output, "w") as f:
        json.dump(insights, f, indent=2, default=str)
    logger.info(f"Saved final insights to {json_output}")

    logger.info("Building journey friction map...")
    journey_map = journey_mapping.run(
        insights, comprehensive_data, temporal_data, suffix=suffix,
        funnel_data=funnel_data, accessibility_data=accessibility_data,
    )

    chart_paths = visualizations.generate_all_charts(
        insights, temporal_data, comprehensive_data, suffix=suffix,
        reviews_df=reviews_df, funnel_data=funnel_data,
    )

    md_report = _generate_markdown(
        insights, chart_paths=chart_paths, comparison=comparison,
        journey_map=journey_map,
    )
    with open(md_output, "w") as f:
        f.write(md_report)
    logger.info(f"Saved Markdown report to {md_output}")

    return insights
