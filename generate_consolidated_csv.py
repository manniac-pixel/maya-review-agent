#!/usr/bin/env python3
"""Generate a single consolidated CSV with ALL research findings across every analysis."""

import csv
import json
from pathlib import Path

DATA_DIR = Path("data")


def load_json(name):
    p = DATA_DIR / name
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {}


def q(quotes, limit=3):
    """Join quotes into a single string."""
    if not quotes:
        return ""
    return " | ".join(f'"{q}"' for q in quotes[:limit])


def main():
    insights = load_json("final_insights.json")
    comp = load_json("comprehensive_analysis.json")
    temporal = load_json("temporal_analysis.json")
    journey = load_json("journey_map.json")
    funnel = load_json("funnel_analysis.json")
    access = load_json("accessibility_analysis.json")

    output = DATA_DIR / "maya_consolidated_research.csv"
    rows = []

    # ── Section 1: Executive Summary ────────────────────────────────────
    es = insights.get("executive_summary", {})
    rows.append({
        "Section": "Executive Summary",
        "Category": "Overview",
        "Item": "Total Reviews Analyzed",
        "Detail": str(es.get("total_reviews_analyzed", "")),
    })
    rows.append({
        "Section": "Executive Summary",
        "Category": "Overview",
        "Item": "Date Range",
        "Detail": es.get("date_range", ""),
    })
    rows.append({
        "Section": "Executive Summary",
        "Category": "Overview",
        "Item": "Overall Sentiment",
        "Detail": es.get("overall_sentiment", ""),
    })

    # Persistent issues
    for item in es.get("top_persistent_issues", []):
        rows.append({
            "Section": "Executive Summary",
            "Category": "Persistent Issue",
            "Item": item.get("theme", ""),
            "Detail": item.get("description", ""),
            "Duration / Context": f"{item.get('months_active', '')} months active",
        })

    # Emerging issues
    for item in es.get("top_emerging_issues", []):
        rows.append({
            "Section": "Executive Summary",
            "Category": "Emerging Issue",
            "Item": item.get("theme", ""),
            "Detail": item.get("description", ""),
            "Duration / Context": f"First seen {item.get('first_seen', '')}",
        })

    # Resolved issues
    for item in es.get("top_resolved_issues", []):
        rows.append({
            "Section": "Executive Summary",
            "Category": "Resolved Issue",
            "Item": item.get("theme", ""),
            "Detail": item.get("description", ""),
            "Duration / Context": item.get("evidence", ""),
        })

    # ── Section 2: Ranked UX Opportunities ──────────────────────────────
    for opp in insights.get("ranked_ux_opportunities", []):
        rows.append({
            "Section": "Ranked UX Opportunities",
            "Category": opp.get("category", ""),
            "Item": opp.get("theme", ""),
            "Rank": opp.get("rank", ""),
            "Severity": opp.get("severity", ""),
            "Frequency": opp.get("frequency", ""),
            "Priority Score": opp.get("priority_score", ""),
            "Business Impact": opp.get("business_impact", ""),
            "Affected Journey": opp.get("affected_journey", ""),
            "Detail": opp.get("description", ""),
            "Recommendation": opp.get("recommendation", ""),
            "User Quotes": q(opp.get("user_quotes", [])),
        })

    # ── Section 3: Critical Pain Points (Comprehensive) ─────────────────
    analysis = comp.get("analysis", {})
    for pp in analysis.get("critical_pain_points", []):
        idet = pp.get("interaction_details", {}) or {}
        rows.append({
            "Section": "Critical Pain Points",
            "Category": pp.get("affected_journey", ""),
            "Item": pp.get("theme", ""),
            "Severity": pp.get("severity", ""),
            "Frequency": pp.get("frequency", ""),
            "Business Impact": pp.get("business_impact", ""),
            "Detail": pp.get("description", ""),
            "Screen Location": idet.get("screen_location", ""),
            "Trigger Action": idet.get("trigger_action", ""),
            "UI Element": idet.get("ui_element", ""),
            "Expected Behavior": idet.get("expected_behavior", ""),
            "Actual Behavior": idet.get("actual_behavior", ""),
            "Error Messages": " | ".join(idet.get("error_messages_seen", [])) if idet.get("error_messages_seen") else "",
            "User Quotes": q(pp.get("user_quotes", [])),
        })

    # ── Section 4: Competitive Insights ─────────────────────────────────
    for ci in analysis.get("competitive_insights", []):
        rows.append({
            "Section": "Competitive Insights",
            "Category": ci.get("competitor", ""),
            "Item": ci.get("area", ""),
            "Detail": ci.get("detail", ""),
            "Duration / Context": ci.get("user_preference", ""),
            "User Quotes": q(ci.get("quotes", [])),
        })

    # ── Section 5: Competitive Gaps ─────────────────────────────────────
    for gap in insights.get("competitive_gaps", []):
        rows.append({
            "Section": "Competitive Gaps",
            "Category": gap.get("competitor", ""),
            "Item": gap.get("area", ""),
            "Detail": gap.get("gap_description", ""),
            "Recommendation": gap.get("recommendation", ""),
            "User Quotes": q(gap.get("user_quotes", [])),
        })

    # ── Section 6: Trust & Security Concerns ────────────────────────────
    for tc in analysis.get("trust_security_concerns", []):
        rows.append({
            "Section": "Trust & Security Concerns",
            "Category": tc.get("category", ""),
            "Item": tc.get("concern", ""),
            "Severity": tc.get("severity", ""),
            "User Quotes": q(tc.get("quotes", [])),
        })

    # ── Section 7: Feature Requests ─────────────────────────────────────
    for fr in analysis.get("feature_requests", []):
        rows.append({
            "Section": "Feature Requests",
            "Category": fr.get("impact_area", ""),
            "Item": fr.get("feature", ""),
            "Frequency": fr.get("frequency", ""),
            "Detail": fr.get("user_need", ""),
            "User Quotes": q(fr.get("quotes", [])),
        })

    # ── Section 8: Positive Signals ─────────────────────────────────────
    for ps in analysis.get("positive_signals", []):
        rows.append({
            "Section": "Positive Signals",
            "Category": ps.get("user_journey", ""),
            "Item": ps.get("theme", ""),
            "Frequency": ps.get("frequency", ""),
            "Detail": ps.get("description", ""),
            "Duration / Context": ps.get("specific_flow", "") if ps.get("specific_flow") else "",
            "User Quotes": q(ps.get("quotes", [])),
        })

    # ── Section 9: Positive Flow Benchmarks ─────────────────────────────
    for bench in insights.get("positive_flow_benchmarks", []):
        rows.append({
            "Section": "Positive Flow Benchmarks",
            "Category": bench.get("journey", ""),
            "Item": bench.get("flow", ""),
            "Detail": bench.get("what_works", ""),
            "Duration / Context": bench.get("preservation_priority", ""),
            "Recommendation": bench.get("competitive_advantage", ""),
            "User Quotes": q(bench.get("quotes", [])),
        })

    # ── Section 10: Quick Wins ──────────────────────────────────────────
    for qw in insights.get("quick_wins", []):
        rows.append({
            "Section": "Quick Wins",
            "Category": f"Effort: {qw.get('effort', '')} | Impact: {qw.get('impact', '')}",
            "Item": qw.get("issue", ""),
            "Recommendation": qw.get("recommendation", ""),
            "Detail": qw.get("rationale", ""),
        })

    # ── Section 11: Strategic Bets ──────────────────────────────────────
    for sb in insights.get("strategic_bets", []):
        rows.append({
            "Section": "Strategic Bets",
            "Category": f"Effort: {sb.get('effort', '')} | Impact: {sb.get('impact', '')}",
            "Item": sb.get("initiative", ""),
            "Detail": sb.get("description", ""),
            "Duration / Context": sb.get("user_need", ""),
            "Recommendation": sb.get("competitive_context", ""),
        })

    # ── Section 12: User Segments ───────────────────────────────────────
    for seg in insights.get("user_segment_insights", []):
        rows.append({
            "Section": "User Segments",
            "Category": seg.get("size_signal", ""),
            "Item": seg.get("segment", ""),
            "Detail": f"Needs: {', '.join(seg.get('top_needs', []))} | Frustrations: {', '.join(seg.get('top_frustrations', []))}",
            "Recommendation": seg.get("opportunity", ""),
        })

    # ── Section 13: Journey Friction Scores ─────────────────────────────
    for js in journey.get("journey_scores", []):
        rows.append({
            "Section": "Journey Friction Scores",
            "Category": js.get("journey", "").upper(),
            "Item": f"{js.get('pain_point_count', 0)} pain points",
            "Priority Score": js.get("friction_score", ""),
            "Detail": ", ".join(js.get("top_themes", [])),
        })

    # ── Section 14: Screen-Level Friction Mapping ───────────────────────
    for j in journey.get("screen_mapping", {}).get("journeys", []):
        journey_name = j.get("journey", "?")
        priority = j.get("improvement_priority", "")
        for screen in j.get("screens", []):
            rows.append({
                "Section": "Screen-Level Friction Map",
                "Category": journey_name,
                "Item": screen.get("screen", ""),
                "Severity": screen.get("severity", ""),
                "Detail": screen.get("description", ""),
                "Recommendation": screen.get("recommendation", ""),
                "Duration / Context": f"Priority: {priority} | Hotspot: {j.get('highest_friction_screen', '')}",
                "Affected Journey": ", ".join(screen.get("pain_points", [])),
            })

    # ── Section 15: Flow Sequences ──────────────────────────────────────
    for j in journey.get("screen_mapping", {}).get("journeys", []):
        journey_name = j.get("journey", "?")
        flow_seq = j.get("flow_sequence", [])
        for i, step in enumerate(flow_seq):
            if isinstance(step, dict):
                rows.append({
                    "Section": "Flow Sequences",
                    "Category": journey_name,
                    "Rank": step.get("step_number", i + 1),
                    "Item": step.get("screen_name", ""),
                    "Detail": step.get("user_action", ""),
                    "Duration / Context": f"Drop-off risk: {step.get('drop_off_risk', 'unknown')}",
                    "Affected Journey": ", ".join(step.get("known_issues", [])),
                })
            elif isinstance(step, str):
                rows.append({
                    "Section": "Flow Sequences",
                    "Category": journey_name,
                    "Rank": i + 1,
                    "Item": step,
                })

    # ── Section 16: Funnel Analysis — Drop-Off Hotspots ─────────────────
    for h in funnel.get("drop_off_hotspots", []):
        rows.append({
            "Section": "Funnel: Drop-Off Hotspots",
            "Category": h.get("journey", ""),
            "Item": h.get("screen_or_step", ""),
            "Severity": h.get("severity", ""),
            "Frequency": f"{h.get('evidence_count', '')} reviews",
            "Detail": ", ".join(h.get("signals", [])),
            "Recommendation": h.get("recommendation", ""),
        })

    # ── Section 17: Funnel — Abandonment Analysis ───────────────────────
    for a in funnel.get("abandonment_analysis", []):
        rows.append({
            "Section": "Funnel: Abandonment",
            "Category": a.get("journey", ""),
            "Item": a.get("abandonment_point", ""),
            "Detail": a.get("trigger", ""),
            "Duration / Context": f"Destination: {a.get('destination', '')}",
            "Frequency": f"{a.get('evidence_count', '')} reviews",
            "User Quotes": q(a.get("quotes", [])),
        })

    # ── Section 18: Funnel — Retry Patterns ─────────────────────────────
    for r in funnel.get("retry_analysis", []):
        rows.append({
            "Section": "Funnel: Retry Patterns",
            "Category": r.get("journey", ""),
            "Item": r.get("step", ""),
            "Detail": f"Retries: {r.get('retry_count_range', '')} | Outcome: {r.get('eventual_outcome', '')}",
            "Frequency": f"{r.get('evidence_count', '')} reviews",
            "User Quotes": q(r.get("quotes", [])),
        })

    # ── Section 19: Funnel — Multi-Step Failures ────────────────────────
    for msf in funnel.get("multi_step_failures", []):
        steps_desc = " -> ".join(
            f"[{s.get('step_number', '?')}] {s.get('action', '')} ({s.get('outcome', '')})"
            for s in msf.get("steps", [])
        )
        rows.append({
            "Section": "Funnel: Multi-Step Failures",
            "Category": msf.get("journey", ""),
            "Item": msf.get("failure_point", ""),
            "Detail": steps_desc,
            "User Quotes": q(msf.get("quotes", [])),
        })

    # ── Section 20: Accessibility — Connectivity Issues ─────────────────
    for ci in access.get("connectivity_issues", []):
        rows.append({
            "Section": "Accessibility: Connectivity",
            "Category": "Connectivity",
            "Item": ci.get("condition", ""),
            "Detail": ", ".join(ci.get("affected_features", [])),
            "Frequency": f"{ci.get('evidence_count', '')} reviews",
            "Recommendation": ci.get("recommendation", ""),
        })

    # ── Section 21: Accessibility — Device Compatibility ────────────────
    for dc in access.get("device_compatibility", []):
        rows.append({
            "Section": "Accessibility: Device Compatibility",
            "Category": "Device",
            "Item": dc.get("device_segment", ""),
            "Detail": ", ".join(dc.get("issues", [])),
            "Frequency": f"{dc.get('evidence_count', '')} reviews",
            "Recommendation": dc.get("recommendation", ""),
        })

    # ── Section 22: Accessibility — Accessibility Gaps ──────────────────
    for ag in access.get("accessibility_gaps", []):
        rows.append({
            "Section": "Accessibility: Gaps",
            "Category": "Accessibility",
            "Item": ag.get("issue", ""),
            "Detail": f"Affected: {ag.get('affected_users', '')}",
            "Frequency": f"{ag.get('evidence_count', '')} reviews",
            "Recommendation": ag.get("recommendation", ""),
        })

    # ── Section 23: Accessibility — Edge Cases ──────────────────────────
    for ec in access.get("edge_cases", []):
        rows.append({
            "Section": "Accessibility: Edge Cases",
            "Category": "Edge Case",
            "Item": ec.get("scenario", ""),
            "Detail": ec.get("current_handling", ""),
            "Frequency": f"{ec.get('evidence_count', '')} reviews",
            "Recommendation": ec.get("recommendation", ""),
        })

    # ── Section 24: Device Distribution ─────────────────────────────────
    device_dist = access.get("device_distribution", {})
    brands = device_dist.get("regex_brand_mentions", device_dist.get("top_mentioned_brands", []))
    for b in brands:
        rows.append({
            "Section": "Device Distribution",
            "Category": "Brand Mentions",
            "Item": b.get("brand", ""),
            "Frequency": f"{b.get('mention_count', '')} mentions",
        })

    # ── Section 25: Version Spike Analysis ──────────────────────────────
    va = insights.get("_version_analysis", {})
    for ver, spike in va.get("spike_analyses", {}).items():
        for issue in spike.get("primary_issues", []):
            rows.append({
                "Section": "Version Spike Analysis",
                "Category": f"v{ver}",
                "Item": issue.get("theme", ""),
                "Severity": issue.get("severity", ""),
                "Detail": issue.get("description", ""),
                "Affected Journey": issue.get("affected_area", ""),
                "Duration / Context": issue.get("likely_cause", ""),
                "User Quotes": q(issue.get("quotes", [])),
            })
        if spike.get("likely_root_cause_summary"):
            rows.append({
                "Section": "Version Spike Analysis",
                "Category": f"v{ver}",
                "Item": "ROOT CAUSE SUMMARY",
                "Detail": spike["likely_root_cause_summary"],
                "Duration / Context": spike.get("comparison_to_previous", ""),
            })

    # ── Section 26: Temporal Trends ─────────────────────────────────────
    trends = temporal.get("trends", {})
    for item in trends.get("persistent_issues", []):
        if isinstance(item, dict):
            rows.append({
                "Section": "Temporal Trends",
                "Category": "PERSISTENT",
                "Item": item.get("theme", ""),
                "Severity": item.get("severity", ""),
                "Frequency": item.get("frequency", ""),
                "Detail": item.get("description", ""),
                "Duration / Context": ", ".join(item.get("months_present", [])),
            })
    for item in trends.get("emerging_issues", []):
        if isinstance(item, dict):
            rows.append({
                "Section": "Temporal Trends",
                "Category": "EMERGING",
                "Item": item.get("theme", ""),
                "Severity": item.get("severity", ""),
                "Detail": item.get("description", ""),
                "Duration / Context": f"First seen: {item.get('first_seen', '')}",
            })
    for item in trends.get("resolved_issues", []):
        if isinstance(item, dict):
            rows.append({
                "Section": "Temporal Trends",
                "Category": "RESOLVED",
                "Item": item.get("theme", ""),
                "Detail": item.get("description", ""),
                "Duration / Context": "Peak: " + ", ".join(item.get("peak_months", [])),
            })

    # ── Section 27: Trend Summary ───────────────────────────────────────
    ts = insights.get("trend_summary", {})
    for area in ts.get("improving_areas", []):
        rows.append({"Section": "Trend Summary", "Category": "IMPROVING", "Item": area})
    for area in ts.get("declining_areas", []):
        rows.append({"Section": "Trend Summary", "Category": "DECLINING", "Item": area})
    for area in ts.get("stable_pain_points", []):
        rows.append({"Section": "Trend Summary", "Category": "STABLE", "Item": area})

    # ── Section 28: Monthly Pain Points (all months) ────────────────────
    for month in sorted(temporal.get("monthly_results", {}).keys()):
        data = temporal["monthly_results"][month]
        for pp in data.get("pain_points", []):
            rows.append({
                "Section": "Monthly Pain Points",
                "Category": month,
                "Item": pp.get("theme", ""),
                "Severity": pp.get("severity", ""),
                "Frequency": pp.get("frequency", ""),
                "Detail": pp.get("description", ""),
                "User Quotes": q(pp.get("quotes", [])),
            })
        for fr in data.get("feature_requests", []):
            rows.append({
                "Section": "Monthly Feature Requests",
                "Category": month,
                "Item": fr.get("feature", ""),
                "Frequency": fr.get("frequency", ""),
                "Detail": fr.get("description", ""),
                "User Quotes": q(fr.get("quotes", [])),
            })
        for pos in data.get("positive_mentions", []):
            rows.append({
                "Section": "Monthly Positive Signals",
                "Category": month,
                "Item": pos.get("theme", ""),
                "Frequency": pos.get("frequency", ""),
                "Detail": pos.get("description", ""),
            })

    # ── Section 29: Version Stats ───────────────────────────────────────
    for vs in va.get("version_stats", []):
        rows.append({
            "Section": "Version Stats",
            "Category": f"v{vs['version']}",
            "Item": f"Reviews: {vs['review_count']} | Avg: {vs['avg_rating']}/5 | 1-star: {vs['one_star_pct']}%",
            "Detail": f"{vs.get('date_first', '')} to {vs.get('date_last', '')}",
            "Duration / Context": "SPIKE" if str(vs.get("spike")) == "True" else "",
        })

    # ── Section 30: Signal Counts Summary ───────────────────────────────
    if funnel.get("signal_breakdown"):
        sb = funnel["signal_breakdown"]
        rows.append({
            "Section": "Analysis Metadata",
            "Category": "Funnel Signals",
            "Item": f"Scanned: {funnel.get('total_reviews_scanned', '')} | Found: {funnel.get('signal_reviews_found', '')}",
            "Detail": f"Retry: {sb.get('retry', 0)} | Abandonment: {sb.get('abandonment', 0)} | Multi-step: {sb.get('multi_step', 0)}",
        })
    if access.get("signal_breakdown"):
        sb = access["signal_breakdown"]
        rows.append({
            "Section": "Analysis Metadata",
            "Category": "Accessibility Signals",
            "Item": f"Scanned: {access.get('total_reviews_scanned', '')} | Found: {access.get('signal_reviews_found', '')}",
            "Detail": f"Device: {sb.get('device', 0)} | Connectivity: {sb.get('connectivity', 0)} | A11y: {sb.get('accessibility', 0)} | Edge: {sb.get('edge_case', 0)}",
        })

    # ── Write CSV ───────────────────────────────────────────────────────
    # Collect all unique fieldnames
    all_fields = []
    seen = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                all_fields.append(key)
                seen.add(key)

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Consolidated CSV saved to {output}")
    print(f"Total rows: {len(rows)}")

    # Count by section
    from collections import Counter
    section_counts = Counter(r.get("Section", "") for r in rows)
    print("\nRows by section:")
    for section, count in section_counts.most_common():
        print(f"  {section}: {count}")


if __name__ == "__main__":
    main()
