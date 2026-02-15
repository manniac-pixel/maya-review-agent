#!/usr/bin/env python3
"""Generate a comprehensive, in-depth Excel report from all research findings."""

import csv
import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

DATA_DIR = Path("data")

# ── Style constants ──────────────────────────────────────────────────────────
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
HEADER_FILL = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
SECTION_FONT = Font(bold=True, color="2F5496", size=12)
SUBHEADER_FILL = PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid")
SUBHEADER_FONT = Font(bold=True, color="2F5496", size=11)
CRITICAL_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
HIGH_FILL = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
MEDIUM_FILL = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
GREEN_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
LIGHT_GRAY = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
WRAP = Alignment(wrap_text=True, vertical="top")
THIN_BORDER = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"), bottom=Side(style="thin"),
)

SEVERITY_FILLS = {5: CRITICAL_FILL, 4: HIGH_FILL, 3: MEDIUM_FILL}


def style_header(ws, row, num_cols):
    for col in range(1, num_cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = THIN_BORDER


def style_rows(ws, start_row, end_row, num_cols):
    for r in range(start_row, end_row + 1):
        for c in range(1, num_cols + 1):
            cell = ws.cell(row=r, column=c)
            cell.alignment = WRAP
            cell.border = THIN_BORDER


def auto_width(ws, num_cols, max_width=55):
    for col in range(1, num_cols + 1):
        max_len = 0
        for row in ws.iter_rows(min_col=col, max_col=col, values_only=False):
            for cell in row:
                if cell.value:
                    lines = str(cell.value).split("\n")
                    longest_line = max(len(l) for l in lines) if lines else 0
                    max_len = max(max_len, min(longest_line, max_width))
        ws.column_dimensions[get_column_letter(col)].width = max_len + 4


def set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def severity_fill(sev):
    return SEVERITY_FILLS.get(sev)


def section_title(ws, row, title, num_cols):
    ws.cell(row=row, column=1, value=title).font = SECTION_FONT
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=num_cols)
    return row + 1


def load_json(name):
    p = DATA_DIR / name
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {}


def load_csv(name):
    p = DATA_DIR / name
    rows = []
    if p.exists():
        with open(p, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)
    return rows


def join_quotes(quotes, limit=None):
    if not quotes:
        return ""
    if limit:
        quotes = quotes[:limit]
    return "\n\n".join(f'"{q}"' for q in quotes)


def pipe_to_list(s):
    if not s:
        return ""
    return ", ".join(s.split("|"))


# ── Sheet 1: Executive Summary ──────────────────────────────────────────────

def build_executive_summary(wb, insights, comp, temporal):
    ws = wb.create_sheet("Executive Summary")
    es = insights.get("executive_summary", {})
    ncols = 5

    # ── Overview section
    row = section_title(ws, 1, "OVERVIEW", ncols)
    headers = ["Metric", "Value"]
    for c, h in enumerate(headers, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, 2)
    row += 1

    overview_data = [
        ("Total Reviews Analyzed", es.get("total_reviews_analyzed", "")),
        ("Date Range", es.get("date_range", "")),
        ("Overall Sentiment", es.get("overall_sentiment", "")),
        ("Months Covered", ", ".join(temporal.get("months_analyzed", []))),
        ("Comprehensive Chunks Analyzed", comp.get("chunks_analyzed", "")),
        ("Analysis Date", comp.get("analysis_date", "")[:10]),
    ]
    for label, val in overview_data:
        ws.cell(row=row, column=1, value=label)
        ws.cell(row=row, column=2, value=val)
        row += 1
    style_rows(ws, row - len(overview_data), row - 1, 2)

    # ── Trend summary
    row = section_title(ws, row + 1, "TREND SUMMARY", ncols)
    ts = insights.get("trend_summary", {})
    headers = ["Direction", "Themes"]
    for c, h in enumerate(headers, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, 2)
    row += 1
    for direction, key, fill in [
        ("Improving", "improving_areas", GREEN_FILL),
        ("Declining", "declining_areas", CRITICAL_FILL),
        ("Stable Pain Points", "stable_pain_points", HIGH_FILL),
    ]:
        ws.cell(row=row, column=1, value=direction)
        ws.cell(row=row, column=2, value=", ".join(ts.get(key, [])))
        ws.cell(row=row, column=1).fill = fill
        row += 1
    style_rows(ws, row - 3, row - 1, 2)

    # ── Persistent issues
    row = section_title(ws, row + 1, "TOP PERSISTENT ISSUES", ncols)
    headers = ["Theme", "Description", "Duration"]
    for c, h in enumerate(headers, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, 3)
    row += 1
    start = row
    for item in es.get("top_persistent_issues", []):
        ws.cell(row=row, column=1, value=item["theme"])
        ws.cell(row=row, column=2, value=item["description"])
        ws.cell(row=row, column=3, value=f"{item.get('months_active', '')} months active")
        for c in range(1, 4):
            ws.cell(row=row, column=c).fill = CRITICAL_FILL
        row += 1
    style_rows(ws, start, row - 1, 3)

    # ── Emerging issues
    row = section_title(ws, row + 1, "TOP EMERGING ISSUES", ncols)
    headers = ["Theme", "Description", "First Seen"]
    for c, h in enumerate(headers, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, 3)
    row += 1
    start = row
    for item in es.get("top_emerging_issues", []):
        ws.cell(row=row, column=1, value=item["theme"])
        ws.cell(row=row, column=2, value=item["description"])
        ws.cell(row=row, column=3, value=item.get("first_seen", ""))
        for c in range(1, 4):
            ws.cell(row=row, column=c).fill = HIGH_FILL
        row += 1
    style_rows(ws, start, row - 1, 3)

    # ── Resolved issues
    row = section_title(ws, row + 1, "TOP RESOLVED ISSUES", ncols)
    headers = ["Theme", "Description", "Evidence"]
    for c, h in enumerate(headers, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, 3)
    row += 1
    start = row
    for item in es.get("top_resolved_issues", []):
        ws.cell(row=row, column=1, value=item["theme"])
        ws.cell(row=row, column=2, value=item["description"])
        ws.cell(row=row, column=3, value=item.get("evidence", ""))
        for c in range(1, 4):
            ws.cell(row=row, column=c).fill = GREEN_FILL
        row += 1
    style_rows(ws, start, row - 1, 3)

    set_col_widths(ws, [30, 60, 50, 40, 40])


# ── Sheet 2: Ranked UX Opportunities ────────────────────────────────────────

def build_ux_opportunities(wb, insights):
    ws = wb.create_sheet("Ranked UX Opportunities")
    headers = [
        "Rank", "Theme", "Description", "Severity (1-5)", "Frequency",
        "Priority Score", "Category", "Affected Journeys",
        "Business Impact Areas", "Recommendation", "User Quotes",
    ]
    for c, h in enumerate(headers, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(headers))

    row = 2
    for opp in insights.get("ranked_ux_opportunities", []):
        ws.cell(row=row, column=1, value=opp.get("rank"))
        ws.cell(row=row, column=2, value=opp.get("theme"))
        ws.cell(row=row, column=3, value=opp.get("description"))
        sev = opp.get("severity", 0)
        ws.cell(row=row, column=4, value=sev)
        ws.cell(row=row, column=5, value=opp.get("frequency"))
        ws.cell(row=row, column=6, value=opp.get("priority_score"))
        ws.cell(row=row, column=7, value=opp.get("category"))
        ws.cell(row=row, column=8, value=pipe_to_list(opp.get("affected_journey", "")))
        ws.cell(row=row, column=9, value=pipe_to_list(opp.get("business_impact", "")))
        ws.cell(row=row, column=10, value=opp.get("recommendation"))
        ws.cell(row=row, column=11, value=join_quotes(opp.get("user_quotes", [])))
        f = severity_fill(sev)
        if f:
            for c in range(1, len(headers) + 1):
                ws.cell(row=row, column=c).fill = f
        row += 1

    style_rows(ws, 2, row - 1, len(headers))
    set_col_widths(ws, [6, 22, 50, 12, 12, 14, 16, 40, 40, 55, 60])


# ── Sheet 3: Critical Pain Points (Comprehensive) ──────────────────────────

def build_critical_pain_points(wb, comp):
    ws = wb.create_sheet("Critical Pain Points")
    headers = [
        "Theme", "Description", "Severity (1-5)", "Frequency",
        "Affected Journeys", "Business Impact Areas", "User Quotes",
    ]
    for c, h in enumerate(headers, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(headers))

    row = 2
    for pp in comp.get("analysis", {}).get("critical_pain_points", []):
        ws.cell(row=row, column=1, value=pp.get("theme"))
        ws.cell(row=row, column=2, value=pp.get("description"))
        sev = pp.get("severity", 0)
        ws.cell(row=row, column=3, value=sev)
        ws.cell(row=row, column=4, value=pp.get("frequency"))
        ws.cell(row=row, column=5, value=pipe_to_list(pp.get("affected_journey", "")))
        ws.cell(row=row, column=6, value=pipe_to_list(pp.get("business_impact", "")))
        ws.cell(row=row, column=7, value=join_quotes(pp.get("user_quotes", [])))
        f = severity_fill(sev)
        if f:
            ws.cell(row=row, column=3).fill = f
        row += 1

    style_rows(ws, 2, row - 1, len(headers))
    set_col_widths(ws, [25, 55, 12, 12, 40, 40, 65])


# ── Sheet 4: Journey Friction Map ──────────────────────────────────────────

def build_journey_map(wb, journey):
    ws = wb.create_sheet("Journey Friction Map")
    ncols = 10

    # Section 1: Friction scores
    row = section_title(ws, 1, "JOURNEY FRICTION SCORES (ranked by friction)", ncols)
    h1 = ["#", "Journey", "Pain Point Count", "Friction Score", "Top Themes"]
    for c, h in enumerate(h1, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h1))
    row += 1
    start = row
    for i, js in enumerate(journey.get("journey_scores", []), 1):
        ws.cell(row=row, column=1, value=i)
        ws.cell(row=row, column=2, value=js["journey"].upper())
        ws.cell(row=row, column=3, value=js["pain_point_count"])
        ws.cell(row=row, column=4, value=js["friction_score"])
        ws.cell(row=row, column=5, value=", ".join(js.get("top_themes", [])))
        row += 1
    style_rows(ws, start, row - 1, len(h1))

    row += 1

    # Section 2: Screen-level mapping (one row per screen)
    row = section_title(ws, row, "SCREEN-LEVEL FRICTION MAPPING", ncols)
    h2 = [
        "Journey", "Improvement Priority", "Friction Summary",
        "Screen / UI Location", "Pain Points at Screen", "Severity (1-5)",
        "What Goes Wrong", "Recommendation",
        "Full Flow Sequence", "Highest Friction Screen",
    ]
    for c, h in enumerate(h2, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h2))
    row += 1
    start = row

    for j in journey.get("screen_mapping", {}).get("journeys", []):
        prio = j.get("improvement_priority", "")
        for screen in j.get("screens", []):
            ws.cell(row=row, column=1, value=j["journey"])
            ws.cell(row=row, column=2, value=prio.upper())
            ws.cell(row=row, column=3, value=j.get("friction_summary", ""))
            ws.cell(row=row, column=4, value=screen["screen"])
            ws.cell(row=row, column=5, value=", ".join(screen.get("pain_points", [])))
            sev = screen.get("severity", 0)
            ws.cell(row=row, column=6, value=sev)
            ws.cell(row=row, column=7, value=screen.get("description", ""))
            ws.cell(row=row, column=8, value=screen.get("recommendation", ""))
            ws.cell(row=row, column=9, value=" -> ".join(j.get("flow_sequence", [])))
            ws.cell(row=row, column=10, value=j.get("highest_friction_screen", ""))
            if prio == "critical":
                ws.cell(row=row, column=2).fill = CRITICAL_FILL
            elif prio == "high":
                ws.cell(row=row, column=2).fill = HIGH_FILL
            f = severity_fill(sev)
            if f:
                ws.cell(row=row, column=6).fill = f
            row += 1
    style_rows(ws, start, row - 1, len(h2))
    set_col_widths(ws, [14, 20, 45, 30, 25, 12, 50, 55, 45, 30])


# ── Sheet 5: Month-by-Month Deep Dive ──────────────────────────────────────

def build_monthly_deep_dive(wb, temporal):
    ws = wb.create_sheet("Monthly Deep Dive")
    ncols = 8

    row = 1
    for month in sorted(temporal.get("monthly_results", {}).keys()):
        data = temporal["monthly_results"][month]

        # ── Pain points section
        row = section_title(ws, row, f"{month} — PAIN POINTS", ncols)
        h = ["Theme", "Description", "Severity", "Frequency", "User Quotes"]
        for c, hdr in enumerate(h, 1):
            ws.cell(row=row, column=c, value=hdr)
        style_header(ws, row, len(h))
        row += 1
        start = row
        for pp in data.get("pain_points", []):
            ws.cell(row=row, column=1, value=pp.get("theme"))
            ws.cell(row=row, column=2, value=pp.get("description"))
            sev = pp.get("severity", 0)
            ws.cell(row=row, column=3, value=sev)
            ws.cell(row=row, column=4, value=pp.get("frequency"))
            ws.cell(row=row, column=5, value=join_quotes(pp.get("quotes", [])))
            f = severity_fill(sev)
            if f:
                ws.cell(row=row, column=3).fill = f
            row += 1
        style_rows(ws, start, row - 1, len(h))

        # ── Feature requests
        frs = data.get("feature_requests", [])
        if frs:
            row = section_title(ws, row + 1, f"{month} — FEATURE REQUESTS", ncols)
            h2 = ["Feature", "Description", "Frequency", "User Quotes"]
            for c, hdr in enumerate(h2, 1):
                ws.cell(row=row, column=c, value=hdr)
            style_header(ws, row, len(h2))
            row += 1
            start = row
            for fr in frs:
                ws.cell(row=row, column=1, value=fr.get("feature"))
                ws.cell(row=row, column=2, value=fr.get("description"))
                ws.cell(row=row, column=3, value=fr.get("frequency"))
                ws.cell(row=row, column=4, value=join_quotes(fr.get("quotes", [])))
                row += 1
            style_rows(ws, start, row - 1, len(h2))

        # ── Positive mentions
        pos = data.get("positive_mentions", [])
        if pos:
            row = section_title(ws, row + 1, f"{month} — POSITIVE SIGNALS", ncols)
            h3 = ["Theme", "Description", "Frequency"]
            for c, hdr in enumerate(h3, 1):
                ws.cell(row=row, column=c, value=hdr)
            style_header(ws, row, len(h3))
            row += 1
            start = row
            for p in pos:
                ws.cell(row=row, column=1, value=p.get("theme"))
                ws.cell(row=row, column=2, value=p.get("description"))
                ws.cell(row=row, column=3, value=p.get("frequency"))
                ws.cell(row=row, column=1).fill = GREEN_FILL
                row += 1
            style_rows(ws, start, row - 1, len(h3))

        # ── Competitive comparisons
        comps = data.get("competitive_comparisons", [])
        if comps:
            row = section_title(ws, row + 1, f"{month} — COMPETITIVE COMPARISONS", ncols)
            h4 = ["Competitor", "Context", "Sentiment", "User Quotes"]
            for c, hdr in enumerate(h4, 1):
                ws.cell(row=row, column=c, value=hdr)
            style_header(ws, row, len(h4))
            row += 1
            start = row
            for cc in comps:
                ws.cell(row=row, column=1, value=cc.get("competitor"))
                ws.cell(row=row, column=2, value=cc.get("context"))
                ws.cell(row=row, column=3, value=cc.get("sentiment"))
                ws.cell(row=row, column=4, value=join_quotes(cc.get("quotes", [])))
                row += 1
            style_rows(ws, start, row - 1, len(h4))

        row += 2  # gap between months

    set_col_widths(ws, [22, 55, 12, 12, 65, 55, 55, 55])


# ── Sheet 6: Temporal Trends ────────────────────────────────────────────────

def build_temporal_trends(wb, temporal):
    ws = wb.create_sheet("Temporal Trends")
    trends = temporal.get("trends", {})

    headers = [
        "Trend Type", "Theme", "Description", "Severity", "Frequency",
        "Months Present / Peak / First Seen", "Evidence",
    ]
    for c, h in enumerate(headers, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(headers))

    row = 2
    for item in trends.get("persistent_issues", []):
        ws.cell(row=row, column=1, value="PERSISTENT")
        ws.cell(row=row, column=2, value=item.get("theme"))
        ws.cell(row=row, column=3, value=item.get("description"))
        ws.cell(row=row, column=4, value=item.get("severity"))
        ws.cell(row=row, column=5, value=item.get("frequency"))
        ws.cell(row=row, column=6, value=", ".join(item.get("months_present", [])))
        ws.cell(row=row, column=7, value=item.get("evidence"))
        for c in range(1, len(headers) + 1):
            ws.cell(row=row, column=c).fill = CRITICAL_FILL
        row += 1

    for item in trends.get("emerging_issues", []):
        ws.cell(row=row, column=1, value="EMERGING")
        ws.cell(row=row, column=2, value=item.get("theme"))
        ws.cell(row=row, column=3, value=item.get("description"))
        ws.cell(row=row, column=4, value=item.get("severity"))
        ws.cell(row=row, column=5, value="")
        ws.cell(row=row, column=6, value=f"First seen: {item.get('first_seen', '')}")
        ws.cell(row=row, column=7, value=item.get("evidence"))
        for c in range(1, len(headers) + 1):
            ws.cell(row=row, column=c).fill = HIGH_FILL
        row += 1

    for item in trends.get("resolved_issues", []):
        ws.cell(row=row, column=1, value="RESOLVED")
        ws.cell(row=row, column=2, value=item.get("theme"))
        ws.cell(row=row, column=3, value=item.get("description"))
        ws.cell(row=row, column=4, value="")
        ws.cell(row=row, column=5, value="")
        ws.cell(row=row, column=6, value="Peak: " + ", ".join(item.get("peak_months", [])))
        ws.cell(row=row, column=7, value=item.get("evidence"))
        for c in range(1, len(headers) + 1):
            ws.cell(row=row, column=c).fill = GREEN_FILL
        row += 1

    style_rows(ws, 2, row - 1, len(headers))
    set_col_widths(ws, [16, 25, 55, 10, 12, 40, 60])


# ── Sheet 7: Feature Requests ──────────────────────────────────────────────

def build_feature_requests(wb, temporal, comp):
    ws = wb.create_sheet("Feature Requests")
    ncols = 7

    # Comprehensive (cross-cutting)
    row = section_title(ws, 1, "CROSS-CUTTING FEATURE REQUESTS (from comprehensive analysis)", ncols)
    headers = ["Feature", "User Need", "Frequency", "Impact Areas", "User Quotes"]
    for c, h in enumerate(headers, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(headers))
    row += 1
    start = row
    for fr in comp.get("analysis", {}).get("feature_requests", []):
        ws.cell(row=row, column=1, value=fr.get("feature"))
        ws.cell(row=row, column=2, value=fr.get("user_need", fr.get("description", "")))
        ws.cell(row=row, column=3, value=fr.get("frequency"))
        ws.cell(row=row, column=4, value=pipe_to_list(fr.get("impact_area", "")))
        ws.cell(row=row, column=5, value=join_quotes(fr.get("quotes", [])))
        row += 1
    style_rows(ws, start, row - 1, len(headers))

    # Monthly breakdown
    row = section_title(ws, row + 1, "MONTHLY FEATURE REQUESTS (temporal analysis)", ncols)
    headers2 = ["Month", "Feature", "Description", "Frequency", "User Quotes"]
    for c, h in enumerate(headers2, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(headers2))
    row += 1
    start = row
    for month in sorted(temporal.get("monthly_results", {}).keys()):
        data = temporal["monthly_results"][month]
        for fr in data.get("feature_requests", []):
            ws.cell(row=row, column=1, value=month)
            ws.cell(row=row, column=2, value=fr.get("feature"))
            ws.cell(row=row, column=3, value=fr.get("description"))
            ws.cell(row=row, column=4, value=fr.get("frequency"))
            ws.cell(row=row, column=5, value=join_quotes(fr.get("quotes", [])))
            row += 1
    style_rows(ws, start, row - 1, len(headers2))
    set_col_widths(ws, [12, 30, 55, 12, 40, 55, 55])


# ── Sheet 8: Quick Wins & Strategic Bets ────────────────────────────────────

def build_quick_wins_and_bets(wb, insights):
    ws = wb.create_sheet("Quick Wins & Strategic Bets")
    ncols = 7

    # Quick wins
    row = section_title(ws, 1, "QUICK WINS (low effort, high impact)", ncols)
    h1 = ["Issue", "Recommendation", "Effort", "Impact", "Rationale"]
    for c, h in enumerate(h1, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h1))
    row += 1
    start = row
    for qw in insights.get("quick_wins", []):
        ws.cell(row=row, column=1, value=qw.get("issue"))
        ws.cell(row=row, column=2, value=qw.get("recommendation"))
        ws.cell(row=row, column=3, value=qw.get("effort", "").upper())
        ws.cell(row=row, column=4, value=qw.get("impact", "").upper())
        ws.cell(row=row, column=5, value=qw.get("rationale"))
        for c in range(1, 6):
            ws.cell(row=row, column=c).fill = GREEN_FILL
        row += 1
    style_rows(ws, start, row - 1, len(h1))

    # Strategic bets
    row = section_title(ws, row + 1, "STRATEGIC BETS (high effort, high impact)", ncols)
    h2 = ["Initiative", "Description", "Effort", "Impact", "User Need", "Competitive Context"]
    for c, h in enumerate(h2, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h2))
    row += 1
    start = row
    for sb in insights.get("strategic_bets", []):
        ws.cell(row=row, column=1, value=sb.get("initiative"))
        ws.cell(row=row, column=2, value=sb.get("description"))
        ws.cell(row=row, column=3, value=sb.get("effort", "").upper())
        ws.cell(row=row, column=4, value=sb.get("impact", "").upper())
        ws.cell(row=row, column=5, value=sb.get("user_need"))
        ws.cell(row=row, column=6, value=sb.get("competitive_context"))
        for c in range(1, 7):
            ws.cell(row=row, column=c).fill = HIGH_FILL
        row += 1
    style_rows(ws, start, row - 1, len(h2))
    set_col_widths(ws, [40, 55, 10, 10, 40, 55, 55])


# ── Sheet 9: Competitive Analysis ──────────────────────────────────────────

def build_competitive(wb, insights, comp):
    ws = wb.create_sheet("Competitive Analysis")
    ncols = 7

    # Competitive gaps (from insights)
    row = section_title(ws, 1, "COMPETITIVE GAPS vs GCASH", ncols)
    h1 = ["Area", "Competitor", "Gap Description", "Recommendation", "User Quotes"]
    for c, h in enumerate(h1, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h1))
    row += 1
    start = row
    for gap in insights.get("competitive_gaps", []):
        ws.cell(row=row, column=1, value=gap.get("area"))
        ws.cell(row=row, column=2, value=gap.get("competitor"))
        ws.cell(row=row, column=3, value=gap.get("gap_description"))
        ws.cell(row=row, column=4, value=gap.get("recommendation"))
        ws.cell(row=row, column=5, value=join_quotes(gap.get("user_quotes", [])))
        row += 1
    style_rows(ws, start, row - 1, len(h1))

    # Competitive insights (from comprehensive)
    ci = comp.get("analysis", {}).get("competitive_insights", [])
    if ci:
        row = section_title(ws, row + 1, "COMPETITIVE INSIGHTS (from reviews)", ncols)
        h2 = ["Competitor", "Area", "User Preference", "Detail", "User Quotes"]
        for c, h in enumerate(h2, 1):
            ws.cell(row=row, column=c, value=h)
        style_header(ws, row, len(h2))
        row += 1
        start = row
        for item in ci:
            ws.cell(row=row, column=1, value=item.get("competitor"))
            ws.cell(row=row, column=2, value=item.get("area"))
            ws.cell(row=row, column=3, value=pipe_to_list(item.get("user_preference", "")))
            ws.cell(row=row, column=4, value=item.get("detail"))
            ws.cell(row=row, column=5, value=join_quotes(item.get("quotes", [])))
            row += 1
        style_rows(ws, start, row - 1, len(h2))

    set_col_widths(ws, [30, 15, 50, 55, 65, 55, 55])


# ── Sheet 10: User Segments ────────────────────────────────────────────────

def build_user_segments(wb, insights, comp):
    ws = wb.create_sheet("User Segments")
    ncols = 7

    # From insights
    row = section_title(ws, 1, "USER SEGMENT INSIGHTS", ncols)
    h1 = ["Segment", "Size Signal", "Top Needs", "Top Frustrations", "Opportunity"]
    for c, h in enumerate(h1, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h1))
    row += 1
    start = row
    for seg in insights.get("user_segment_insights", []):
        ws.cell(row=row, column=1, value=seg.get("segment"))
        ws.cell(row=row, column=2, value=seg.get("size_signal"))
        ws.cell(row=row, column=3, value=", ".join(seg.get("top_needs", [])))
        ws.cell(row=row, column=4, value=", ".join(seg.get("top_frustrations", [])))
        ws.cell(row=row, column=5, value=seg.get("opportunity"))
        row += 1
    style_rows(ws, start, row - 1, len(h1))

    # From comprehensive
    segs = comp.get("analysis", {}).get("user_segments", [])
    if segs:
        row = section_title(ws, row + 1, "USER SEGMENT PROFILES (from comprehensive analysis)", ncols)
        h2 = ["Segment", "Characteristics", "Primary Needs", "Primary Frustrations"]
        for c, h in enumerate(h2, 1):
            ws.cell(row=row, column=c, value=h)
        style_header(ws, row, len(h2))
        row += 1
        start = row
        for seg in segs:
            ws.cell(row=row, column=1, value=seg.get("segment"))
            ws.cell(row=row, column=2, value=seg.get("characteristics"))
            ws.cell(row=row, column=3, value=", ".join(seg.get("primary_needs", [])))
            ws.cell(row=row, column=4, value=", ".join(seg.get("primary_frustrations", [])))
            row += 1
        style_rows(ws, start, row - 1, len(h2))

    set_col_widths(ws, [20, 18, 40, 40, 55, 55, 55])


# ── Sheet 11: Trust & Security ─────────────────────────────────────────────

def build_trust_security(wb, comp):
    ws = wb.create_sheet("Trust & Security")
    headers = ["Concern", "Severity (1-5)", "Categories", "User Quotes"]
    for c, h in enumerate(headers, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(headers))

    row = 2
    for tc in comp.get("analysis", {}).get("trust_security_concerns", []):
        ws.cell(row=row, column=1, value=tc.get("concern"))
        sev = tc.get("severity", 0)
        ws.cell(row=row, column=2, value=sev)
        ws.cell(row=row, column=3, value=pipe_to_list(tc.get("category", "")))
        ws.cell(row=row, column=4, value=join_quotes(tc.get("quotes", [])))
        f = severity_fill(sev)
        if f:
            for c in range(1, len(headers) + 1):
                ws.cell(row=row, column=c).fill = f
        row += 1

    style_rows(ws, 2, row - 1, len(headers))
    set_col_widths(ws, [30, 14, 45, 65])


# ── Sheet 12: Version Analysis & Spike Details ─────────────────────────────

def build_version_analysis(wb, temporal):
    ws = wb.create_sheet("Version Analysis")
    va = temporal.get("version_analysis", {})
    ncols = 10

    # Baseline
    row = section_title(ws, 1, "BASELINE METRICS", ncols)
    baseline = va.get("baseline", {})
    ws.cell(row=row, column=1, value="Avg Rating (baseline)")
    ws.cell(row=row, column=2, value=baseline.get("avg_rating"))
    row += 1
    ws.cell(row=row, column=1, value="1-Star % (baseline)")
    ws.cell(row=row, column=2, value=baseline.get("one_star_pct"))
    row += 1
    ws.cell(row=row, column=1, value="Total Versioned Reviews")
    ws.cell(row=row, column=2, value=baseline.get("total_versioned_reviews"))
    row += 1
    ws.cell(row=row, column=1, value="Flagged Versions")
    ws.cell(row=row, column=2, value=", ".join(va.get("flagged_versions", [])))
    ws.cell(row=row, column=2).fill = CRITICAL_FILL
    style_rows(ws, 2, row, 2)
    row += 2

    # Version stats table
    row = section_title(ws, row, "VERSION STATS (sorted by 1-star %)", ncols)
    h = ["Version", "Review Count", "Avg Rating", "1-Star %", "1-Star Count",
         "First Review", "Last Review", "Spike Flagged"]
    for c, hdr in enumerate(h, 1):
        ws.cell(row=row, column=c, value=hdr)
    style_header(ws, row, len(h))
    row += 1
    start = row
    for vs in va.get("version_stats", []):
        ws.cell(row=row, column=1, value=vs["version"])
        ws.cell(row=row, column=2, value=vs["review_count"])
        ws.cell(row=row, column=3, value=vs["avg_rating"])
        ws.cell(row=row, column=4, value=vs["one_star_pct"])
        ws.cell(row=row, column=5, value=vs["one_star_count"])
        ws.cell(row=row, column=6, value=vs["date_first"])
        ws.cell(row=row, column=7, value=vs["date_last"])
        is_spike = str(vs.get("spike")) == "True"
        ws.cell(row=row, column=8, value="YES" if is_spike else "No")
        if is_spike:
            for c in range(1, len(h) + 1):
                ws.cell(row=row, column=c).fill = CRITICAL_FILL
        row += 1
    style_rows(ws, start, row - 1, len(h))

    # Spike deep dive
    spikes = va.get("spike_analyses", {})
    if spikes:
        row += 1
        row = section_title(ws, row, "SPIKE VERSION DEEP DIVE", ncols)
        h2 = ["Version", "Issue Theme", "Description", "Severity",
               "Affected Area", "Likely Cause", "User Quotes",
               "Comparison to Previous", "Root Cause Summary"]
        for c, hdr in enumerate(h2, 1):
            ws.cell(row=row, column=c, value=hdr)
        style_header(ws, row, len(h2))
        row += 1
        start = row
        for ver, spike_data in spikes.items():
            for issue in spike_data.get("primary_issues", []):
                ws.cell(row=row, column=1, value=ver)
                ws.cell(row=row, column=2, value=issue.get("theme"))
                ws.cell(row=row, column=3, value=issue.get("description"))
                ws.cell(row=row, column=4, value=issue.get("severity"))
                ws.cell(row=row, column=5, value=pipe_to_list(issue.get("affected_area", "")))
                ws.cell(row=row, column=6, value=pipe_to_list(issue.get("likely_cause", "")))
                ws.cell(row=row, column=7, value=join_quotes(issue.get("quotes", [])))
                ws.cell(row=row, column=8, value=spike_data.get("comparison_to_previous", ""))
                ws.cell(row=row, column=9, value=spike_data.get("likely_root_cause_summary", ""))
                for c in range(1, len(h2) + 1):
                    ws.cell(row=row, column=c).fill = CRITICAL_FILL
                row += 1
        style_rows(ws, start, row - 1, len(h2))

    set_col_widths(ws, [14, 14, 50, 10, 14, 14, 14, 60, 60, 60])


# ── Sheet 13: Positive Signals ─────────────────────────────────────────────

def build_positive_signals(wb, comp, temporal):
    ws = wb.create_sheet("Positive Signals")
    ncols = 5

    # From comprehensive
    row = section_title(ws, 1, "POSITIVE THEMES (from comprehensive analysis)", ncols)
    h1 = ["Theme", "Description", "Frequency", "User Journey"]
    for c, h in enumerate(h1, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h1))
    row += 1
    start = row
    for ps in comp.get("analysis", {}).get("positive_signals", []):
        ws.cell(row=row, column=1, value=ps.get("theme"))
        ws.cell(row=row, column=2, value=ps.get("description"))
        ws.cell(row=row, column=3, value=ps.get("frequency"))
        ws.cell(row=row, column=4, value=pipe_to_list(ps.get("user_journey", "")))
        for c in range(1, 5):
            ws.cell(row=row, column=c).fill = GREEN_FILL
        row += 1
    style_rows(ws, start, row - 1, len(h1))

    # Monthly positive mentions
    row = section_title(ws, row + 1, "MONTHLY POSITIVE MENTIONS", ncols)
    h2 = ["Month", "Theme", "Description", "Frequency"]
    for c, h in enumerate(h2, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h2))
    row += 1
    start = row
    for month in sorted(temporal.get("monthly_results", {}).keys()):
        data = temporal["monthly_results"][month]
        for p in data.get("positive_mentions", []):
            ws.cell(row=row, column=1, value=month)
            ws.cell(row=row, column=2, value=p.get("theme"))
            ws.cell(row=row, column=3, value=p.get("description"))
            ws.cell(row=row, column=4, value=p.get("frequency"))
            ws.cell(row=row, column=1).fill = GREEN_FILL
            row += 1
    style_rows(ws, start, row - 1, len(h2))

    set_col_widths(ws, [14, 25, 55, 12, 40])


# ── Sheet 14: Interaction Details ─────────────────────────────────────────

def build_interaction_details(wb, comp):
    ws = wb.create_sheet("Interaction Details")
    headers = [
        "Theme", "Screen Location", "Trigger Action", "UI Element",
        "Expected Behavior", "Actual Behavior", "Error Messages", "Severity",
    ]
    for c, h in enumerate(headers, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(headers))

    row = 2
    for pp in comp.get("analysis", {}).get("critical_pain_points", []):
        idet = pp.get("interaction_details", {})
        if not idet:
            continue
        ws.cell(row=row, column=1, value=pp.get("theme"))
        ws.cell(row=row, column=2, value=idet.get("screen_location", ""))
        ws.cell(row=row, column=3, value=idet.get("trigger_action", ""))
        ws.cell(row=row, column=4, value=idet.get("ui_element", ""))
        ws.cell(row=row, column=5, value=idet.get("expected_behavior", ""))
        ws.cell(row=row, column=6, value=idet.get("actual_behavior", ""))
        errors = idet.get("error_messages_seen", [])
        ws.cell(row=row, column=7, value="\n".join(errors) if errors else "")
        sev = pp.get("severity", 0)
        ws.cell(row=row, column=8, value=sev)
        f = severity_fill(sev)
        if f:
            ws.cell(row=row, column=8).fill = f
        row += 1

    style_rows(ws, 2, row - 1, len(headers))
    set_col_widths(ws, [25, 30, 30, 25, 35, 35, 40, 10])


# ── Sheet 15: Flow Maps ──────────────────────────────────────────────────

def build_flow_maps(wb, journey):
    ws = wb.create_sheet("Flow Maps")
    headers = [
        "Journey", "Step #", "Screen Name", "User Action",
        "Known Issues", "Drop-Off Risk",
    ]
    for c, h in enumerate(headers, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(headers))

    row = 2
    for j in journey.get("screen_mapping", {}).get("journeys", []):
        journey_name = j.get("journey", "?")
        flow_seq = j.get("flow_sequence", [])
        for step in flow_seq:
            if isinstance(step, dict):
                ws.cell(row=row, column=1, value=journey_name)
                ws.cell(row=row, column=2, value=step.get("step_number", ""))
                ws.cell(row=row, column=3, value=step.get("screen_name", ""))
                ws.cell(row=row, column=4, value=step.get("user_action", ""))
                issues = step.get("known_issues", [])
                ws.cell(row=row, column=5, value=", ".join(issues) if issues else "")
                risk = step.get("drop_off_risk", "")
                ws.cell(row=row, column=6, value=risk.upper() if risk else "")
                if risk == "high":
                    ws.cell(row=row, column=6).fill = CRITICAL_FILL
                elif risk == "medium":
                    ws.cell(row=row, column=6).fill = HIGH_FILL
                elif risk == "low":
                    ws.cell(row=row, column=6).fill = GREEN_FILL
                row += 1
            elif isinstance(step, str):
                # Legacy format: flow_sequence is a list of strings
                ws.cell(row=row, column=1, value=journey_name)
                ws.cell(row=row, column=3, value=step)
                row += 1

    style_rows(ws, 2, row - 1, len(headers))
    set_col_widths(ws, [16, 8, 30, 35, 40, 14])


# ── Sheet 16: Funnel Analysis ────────────────────────────────────────────

def build_funnel_analysis(wb, funnel):
    ws = wb.create_sheet("Funnel Analysis")
    ncols = 8

    # Sub-table 1: Drop-off hotspots
    row = section_title(ws, 1, "DROP-OFF HOTSPOTS", ncols)
    h1 = ["Screen/Step", "Journey", "Evidence Count", "Severity", "Signals", "Recommendation"]
    for c, h in enumerate(h1, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h1))
    row += 1
    start = row
    for h in funnel.get("drop_off_hotspots", []):
        ws.cell(row=row, column=1, value=h.get("screen_or_step", ""))
        ws.cell(row=row, column=2, value=h.get("journey", ""))
        ws.cell(row=row, column=3, value=h.get("evidence_count", ""))
        sev = h.get("severity", 0)
        ws.cell(row=row, column=4, value=sev)
        signals = h.get("signals", [])
        ws.cell(row=row, column=5, value=", ".join(signals) if signals else "")
        ws.cell(row=row, column=6, value=h.get("recommendation", ""))
        f = severity_fill(sev)
        if f:
            for c in range(1, len(h1) + 1):
                ws.cell(row=row, column=c).fill = f
        row += 1
    style_rows(ws, start, row - 1, len(h1))

    # Sub-table 2: Abandonment analysis
    row = section_title(ws, row + 1, "ABANDONMENT ANALYSIS", ncols)
    h2 = ["Journey", "Abandonment Point", "Destination", "Trigger", "Evidence Count", "Quotes"]
    for c, h in enumerate(h2, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h2))
    row += 1
    start = row
    for a in funnel.get("abandonment_analysis", []):
        ws.cell(row=row, column=1, value=a.get("journey", ""))
        ws.cell(row=row, column=2, value=a.get("abandonment_point", ""))
        ws.cell(row=row, column=3, value=a.get("destination", ""))
        ws.cell(row=row, column=4, value=a.get("trigger", ""))
        ws.cell(row=row, column=5, value=a.get("evidence_count", ""))
        ws.cell(row=row, column=6, value=join_quotes(a.get("quotes", []), 2))
        for c in range(1, len(h2) + 1):
            ws.cell(row=row, column=c).fill = CRITICAL_FILL
        row += 1
    style_rows(ws, start, row - 1, len(h2))

    # Sub-table 3: Retry patterns
    row = section_title(ws, row + 1, "RETRY PATTERNS", ncols)
    h3 = ["Journey", "Step", "Retry Count Range", "Eventual Outcome", "Evidence Count", "Quotes"]
    for c, h in enumerate(h3, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h3))
    row += 1
    start = row
    for r in funnel.get("retry_analysis", []):
        ws.cell(row=row, column=1, value=r.get("journey", ""))
        ws.cell(row=row, column=2, value=r.get("step", ""))
        ws.cell(row=row, column=3, value=r.get("retry_count_range", ""))
        ws.cell(row=row, column=4, value=r.get("eventual_outcome", ""))
        ws.cell(row=row, column=5, value=r.get("evidence_count", ""))
        ws.cell(row=row, column=6, value=join_quotes(r.get("quotes", []), 2))
        row += 1
    style_rows(ws, start, row - 1, len(h3))

    set_col_widths(ws, [30, 16, 30, 20, 14, 55, 55, 55])


# ── Sheet 17: Positive Flow Benchmarks ───────────────────────────────────

def build_positive_benchmarks(wb, insights):
    ws = wb.create_sheet("Positive Flow Benchmarks")
    headers = [
        "Flow", "Journey", "What Works", "Success Factors",
        "Competitive Advantage", "Preservation Priority", "Quotes",
    ]
    for c, h in enumerate(headers, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(headers))

    row = 2
    for bench in insights.get("positive_flow_benchmarks", []):
        ws.cell(row=row, column=1, value=bench.get("flow", ""))
        ws.cell(row=row, column=2, value=bench.get("journey", ""))
        ws.cell(row=row, column=3, value=bench.get("what_works", ""))
        factors = bench.get("success_factors", [])
        ws.cell(row=row, column=4, value=", ".join(factors) if factors else "")
        ws.cell(row=row, column=5, value=bench.get("competitive_advantage", ""))
        prio = bench.get("preservation_priority", "")
        ws.cell(row=row, column=6, value=prio.upper() if prio else "")
        ws.cell(row=row, column=7, value=join_quotes(bench.get("quotes", []), 3))
        for c in range(1, len(headers) + 1):
            ws.cell(row=row, column=c).fill = GREEN_FILL
        row += 1

    style_rows(ws, 2, row - 1, len(headers))
    set_col_widths(ws, [30, 16, 45, 40, 40, 22, 60])


# ── Sheet 18: Accessibility & Edge Cases ─────────────────────────────────

def build_accessibility(wb, access):
    ws = wb.create_sheet("Accessibility & Edge Cases")
    ncols = 8

    # Device distribution
    device_dist = access.get("device_distribution", {})
    row = section_title(ws, 1, "DEVICE DISTRIBUTION (from review mentions)", ncols)
    h0 = ["Brand", "Mention Count"]
    for c, h in enumerate(h0, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h0))
    row += 1
    start = row
    brands = device_dist.get("regex_brand_mentions", device_dist.get("top_mentioned_brands", []))
    for b in brands:
        ws.cell(row=row, column=1, value=b.get("brand", ""))
        ws.cell(row=row, column=2, value=b.get("mention_count", ""))
        row += 1
    style_rows(ws, start, row - 1, len(h0))

    # Connectivity issues
    row = section_title(ws, row + 1, "CONNECTIVITY ISSUES", ncols)
    h1 = ["Condition", "Affected Features", "Evidence Count", "Recommendation"]
    for c, h in enumerate(h1, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h1))
    row += 1
    start = row
    for ci in access.get("connectivity_issues", []):
        ws.cell(row=row, column=1, value=ci.get("condition", ""))
        features = ci.get("affected_features", [])
        ws.cell(row=row, column=2, value=", ".join(features) if features else "")
        ws.cell(row=row, column=3, value=ci.get("evidence_count", ""))
        ws.cell(row=row, column=4, value=ci.get("recommendation", ""))
        row += 1
    style_rows(ws, start, row - 1, len(h1))

    # Device compatibility
    row = section_title(ws, row + 1, "DEVICE COMPATIBILITY ISSUES", ncols)
    h2 = ["Device Segment", "Issues", "Evidence Count", "Recommendation"]
    for c, h in enumerate(h2, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h2))
    row += 1
    start = row
    for dc in access.get("device_compatibility", []):
        ws.cell(row=row, column=1, value=dc.get("device_segment", ""))
        issues = dc.get("issues", [])
        ws.cell(row=row, column=2, value=", ".join(issues) if issues else "")
        ws.cell(row=row, column=3, value=dc.get("evidence_count", ""))
        ws.cell(row=row, column=4, value=dc.get("recommendation", ""))
        row += 1
    style_rows(ws, start, row - 1, len(h2))

    # Accessibility gaps
    row = section_title(ws, row + 1, "ACCESSIBILITY GAPS", ncols)
    h3 = ["Issue", "Affected Users", "Evidence Count", "Recommendation"]
    for c, h in enumerate(h3, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h3))
    row += 1
    start = row
    for ag in access.get("accessibility_gaps", []):
        ws.cell(row=row, column=1, value=ag.get("issue", ""))
        ws.cell(row=row, column=2, value=ag.get("affected_users", ""))
        ws.cell(row=row, column=3, value=ag.get("evidence_count", ""))
        ws.cell(row=row, column=4, value=ag.get("recommendation", ""))
        row += 1
    style_rows(ws, start, row - 1, len(h3))

    # Edge cases
    row = section_title(ws, row + 1, "EDGE CASES", ncols)
    h4 = ["Scenario", "Current Handling", "Evidence Count", "Recommendation"]
    for c, h in enumerate(h4, 1):
        ws.cell(row=row, column=c, value=h)
    style_header(ws, row, len(h4))
    row += 1
    start = row
    for ec in access.get("edge_cases", []):
        ws.cell(row=row, column=1, value=ec.get("scenario", ""))
        ws.cell(row=row, column=2, value=ec.get("current_handling", ""))
        ws.cell(row=row, column=3, value=ec.get("evidence_count", ""))
        ws.cell(row=row, column=4, value=ec.get("recommendation", ""))
        row += 1
    style_rows(ws, start, row - 1, len(h4))

    set_col_widths(ws, [30, 40, 14, 55, 55, 55, 55, 55])


# ── Sheet 19: Raw Reviews Sample ──────────────────────────────────────────

def build_raw_reviews(wb):
    ws = wb.create_sheet("Raw Reviews (sample)")
    reviews = load_csv("raw_reviews.csv")
    if not reviews:
        ws.cell(row=1, column=1, value="No raw_reviews.csv found")
        return

    headers = ["Date", "Rating", "App Version", "Platform", "Review Text"]
    for c, h in enumerate(headers, 1):
        ws.cell(row=1, column=c, value=h)
    style_header(ws, 1, len(headers))

    # Include all 1-star (up to 500) + sample of others (up to 500)
    one_star = [r for r in reviews if r.get("rating") == "1"][:500]
    others = [r for r in reviews if r.get("rating") != "1"][:500]
    sample = one_star + others

    row = 2
    for r in sample:
        ws.cell(row=row, column=1, value=r.get("date", "")[:10])
        rating = r.get("rating", "")
        ws.cell(row=row, column=2, value=int(rating) if rating else "")
        ws.cell(row=row, column=3, value=r.get("app_version", ""))
        ws.cell(row=row, column=4, value=r.get("platform", ""))
        ws.cell(row=row, column=5, value=r.get("text", ""))

        try:
            rat = int(rating)
            if rat == 1:
                ws.cell(row=row, column=2).fill = CRITICAL_FILL
            elif rat == 2:
                ws.cell(row=row, column=2).fill = HIGH_FILL
            elif rat >= 4:
                ws.cell(row=row, column=2).fill = GREEN_FILL
        except (ValueError, TypeError):
            pass
        row += 1

    style_rows(ws, 2, row - 1, len(headers))
    set_col_widths(ws, [12, 8, 14, 10, 80])
    ws.cell(row=row + 1, column=1, value=f"Showing {len(sample)} of {len(reviews)} total reviews (all 1-star + sample of others)")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    insights = load_json("final_insights.json")
    comp = load_json("comprehensive_analysis.json")
    temporal = load_json("temporal_analysis.json")
    journey = load_json("journey_map.json")
    funnel = load_json("funnel_analysis.json")
    access = load_json("accessibility_analysis.json")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    build_executive_summary(wb, insights, comp, temporal)
    build_ux_opportunities(wb, insights)
    build_critical_pain_points(wb, comp)
    build_journey_map(wb, journey)
    build_monthly_deep_dive(wb, temporal)
    build_temporal_trends(wb, temporal)
    build_feature_requests(wb, temporal, comp)
    build_quick_wins_and_bets(wb, insights)
    build_competitive(wb, insights, comp)
    build_user_segments(wb, insights, comp)
    build_trust_security(wb, comp)
    build_version_analysis(wb, temporal)
    build_positive_signals(wb, comp, temporal)
    build_interaction_details(wb, comp)
    build_flow_maps(wb, journey)
    build_funnel_analysis(wb, funnel)
    build_positive_benchmarks(wb, insights)
    build_accessibility(wb, access)
    build_raw_reviews(wb)

    output = DATA_DIR / "maya_research_findings.xlsx"
    wb.save(output)
    print(f"Excel report saved to {output}")
    print(f"Sheets: {len(wb.sheetnames)}")
    for name in wb.sheetnames:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
