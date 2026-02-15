"""
Visualization module for Maya Insights Report.
Generates PNG charts from analysis data and returns paths for markdown embedding.
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

import config

logger = logging.getLogger(__name__)

# ── Shared style ────────────────────────────────────────────────────────────
plt.style.use("ggplot")
CATEGORY_COLORS = {
    "quick_win": "#2ecc71",
    "strategic_bet": "#3498db",
    "maintenance": "#95a5a6",
}
IMPACT_COLORS = {
    "trust": "#e74c3c",
    "revenue": "#f39c12",
    "retention": "#3498db",
    "activation": "#2ecc71",
    "transaction_volume": "#9b59b6",
}


def _save(fig: plt.Figure, path: Path) -> str:
    """Save figure, close it, and return the relative path string."""
    dpi = config.get("visualizations", "dpi", 150)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    logger.info(f"Saved chart: {path}")
    return str(path)


# ── 1. Priority Score Bar Chart ─────────────────────────────────────────────

def priority_bar_chart(
    insights: dict, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Horizontal bar chart of top UX issues ranked by priority_score."""
    opps = insights.get("ranked_ux_opportunities", [])
    if not opps:
        return None

    # Take top 15 at most, reversed so highest score is on top
    opps = sorted(opps, key=lambda x: x.get("priority_score", 0))[-15:]

    themes = [o.get("theme", "?")[:40] for o in opps]
    scores = [o.get("priority_score", 0) for o in opps]
    colors = [CATEGORY_COLORS.get(o.get("category", ""), "#7f8c8d") for o in opps]

    fig, ax = plt.subplots(figsize=(10, max(4, len(opps) * 0.45)))
    bars = ax.barh(themes, scores, color=colors, edgecolor="white", linewidth=0.5)

    ax.set_xlabel("Priority Score")
    ax.set_title("Top UX Issues by Priority Score", fontsize=14, fontweight="bold")

    # Legend
    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor=c, label=k.replace("_", " ").title())
        for k, c in CATEGORY_COLORS.items()
    ]
    ax.legend(handles=legend_items, loc="lower right", fontsize=8)

    return _save(fig, chart_dir / f"priority_scores{suffix}.png")


# ── 2. Monthly Severity Heatmap ─────────────────────────────────────────────

def monthly_severity_heatmap(
    temporal_data: dict, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Heatmap of themes (Y) vs months (X), cell color = severity 1-5."""
    monthly = temporal_data.get("monthly_results", [])
    if not monthly:
        return None

    # Collect all themes and months
    theme_severity: dict[str, dict[str, float]] = {}
    months_order: list[str] = []
    for month_entry in monthly:
        month_label = month_entry.get("month", "?")
        if month_label not in months_order:
            months_order.append(month_label)
        analysis = month_entry.get("analysis", {})
        themes = analysis.get("key_themes", [])
        if not themes:
            themes = analysis.get("themes", [])
        for theme in themes:
            name = theme.get("theme", theme.get("name", "?"))
            sev = theme.get("severity", 0)
            if name not in theme_severity:
                theme_severity[name] = {}
            theme_severity[name][month_label] = sev

    if not theme_severity or not months_order:
        return None

    # Keep top themes by average severity
    avg_sev = {
        t: np.mean(list(sevs.values())) for t, sevs in theme_severity.items()
    }
    top_themes = sorted(avg_sev, key=avg_sev.get, reverse=True)[:12]

    matrix = []
    for theme in top_themes:
        row = [theme_severity.get(theme, {}).get(m, 0) for m in months_order]
        matrix.append(row)

    matrix = np.array(matrix, dtype=float)
    fig, ax = plt.subplots(figsize=(max(8, len(months_order) * 0.9), max(4, len(top_themes) * 0.5)))

    im = ax.imshow(matrix, aspect="auto", cmap="YlOrRd", vmin=0, vmax=5)
    ax.set_xticks(range(len(months_order)))
    ax.set_xticklabels(months_order, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(top_themes)))
    ax.set_yticklabels([t[:35] for t in top_themes], fontsize=8)
    ax.set_title("Monthly Issue Severity Heatmap", fontsize=14, fontweight="bold")
    fig.colorbar(im, ax=ax, label="Severity (1-5)", shrink=0.8)

    # Annotate cells
    for i in range(len(top_themes)):
        for j in range(len(months_order)):
            val = matrix[i, j]
            if val > 0:
                color = "white" if val > 3 else "black"
                ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                        fontsize=7, color=color)

    return _save(fig, chart_dir / f"severity_heatmap{suffix}.png")


# ── 3. Version 1-Star Rate ──────────────────────────────────────────────────

def version_rating_chart(
    insights: dict, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Bar chart of 1-star % per version with spike flagging."""
    va = insights.get("_version_analysis", {})
    version_stats = va.get("version_stats", [])
    if not version_stats:
        return None

    baseline = va.get("baseline", {})
    baseline_pct = baseline.get("one_star_pct", 0)
    spike_versions = set(va.get("spike_analyses", {}).keys())

    versions = [v["version"] for v in version_stats]
    pcts = [v.get("one_star_pct", 0) for v in version_stats]
    colors = ["#e74c3c" if v["version"] in spike_versions else "#3498db"
              for v in version_stats]

    fig, ax = plt.subplots(figsize=(max(8, len(versions) * 0.7), 5))
    ax.bar(versions, pcts, color=colors, edgecolor="white", linewidth=0.5)
    ax.axhline(y=baseline_pct, color="#2c3e50", linestyle="--", linewidth=1.5,
               label=f"Baseline ({baseline_pct:.1f}%)")

    ax.set_xlabel("App Version")
    ax.set_ylabel("1-Star Review %")
    ax.set_title("1-Star Review Rate by Version", fontsize=14, fontweight="bold")
    ax.legend(fontsize=9)
    plt.xticks(rotation=45, ha="right", fontsize=8)

    return _save(fig, chart_dir / f"version_ratings{suffix}.png")


# ── 4. Trend Classification ─────────────────────────────────────────────────

def trend_classification_chart(
    temporal_data: dict, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Bar chart showing counts of resolved / persistent / emerging issues."""
    trends = temporal_data.get("trends", {})
    if not trends:
        return None

    categories = {
        "Resolved": len(trends.get("resolved", [])),
        "Persistent": len(trends.get("persistent", [])),
        "Emerging": len(trends.get("emerging", [])),
    }

    if all(v == 0 for v in categories.values()):
        return None

    colors = ["#2ecc71", "#e67e22", "#e74c3c"]
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(categories.keys(), categories.values(), color=colors,
                  edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, categories.values()):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                    str(val), ha="center", va="bottom", fontweight="bold")

    ax.set_ylabel("Number of Issues")
    ax.set_title("Issue Trend Classification", fontsize=14, fontweight="bold")
    ax.set_ylim(0, max(categories.values()) * 1.25 + 1)

    return _save(fig, chart_dir / f"trend_classification{suffix}.png")


# ── 5. Business Impact Distribution ─────────────────────────────────────────

def business_impact_donut(
    insights: dict, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Donut chart of business impact areas across ranked opportunities."""
    opps = insights.get("ranked_ux_opportunities", [])
    if not opps:
        return None

    counts: dict[str, int] = {}
    for o in opps:
        impact = o.get("business_impact", "other")
        counts[impact] = counts.get(impact, 0) + 1

    if not counts:
        return None

    labels = list(counts.keys())
    sizes = list(counts.values())
    colors = [IMPACT_COLORS.get(l, "#bdc3c7") for l in labels]
    display_labels = [l.replace("_", " ").title() for l in labels]

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=display_labels, colors=colors, autopct="%1.0f%%",
        startangle=90, pctdistance=0.78, wedgeprops=dict(width=0.4, edgecolor="white"),
    )
    for t in autotexts:
        t.set_fontsize(9)
        t.set_fontweight("bold")
    ax.set_title("Business Impact Distribution", fontsize=14, fontweight="bold", pad=20)

    return _save(fig, chart_dir / f"business_impact{suffix}.png")


# ── 6. Severity vs Frequency Bubble ─────────────────────────────────────────

def severity_frequency_bubble(
    insights: dict, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Bubble chart: X=severity, Y=frequency, size=priority_score."""
    opps = insights.get("ranked_ux_opportunities", [])
    if not opps:
        return None

    freq_map = {"low": 1, "medium": 2, "high": 3}

    severities = []
    frequencies = []
    scores = []
    labels = []
    colors = []

    for o in opps:
        sev = o.get("severity", 0)
        freq_str = o.get("frequency", "medium")
        freq = freq_map.get(freq_str.lower(), 2) if isinstance(freq_str, str) else 2
        score = o.get("priority_score", 1)

        severities.append(sev)
        frequencies.append(freq)
        scores.append(score)
        labels.append(o.get("theme", "?")[:25])
        colors.append(CATEGORY_COLORS.get(o.get("category", ""), "#7f8c8d"))

    if not severities:
        return None

    # Scale bubble sizes
    min_s, max_s = min(scores), max(scores)
    range_s = max_s - min_s if max_s != min_s else 1
    bubble_sizes = [100 + 600 * ((s - min_s) / range_s) for s in scores]

    fig, ax = plt.subplots(figsize=(9, 7))
    scatter = ax.scatter(
        severities, frequencies, s=bubble_sizes, c=colors, alpha=0.7,
        edgecolors="white", linewidth=1,
    )

    # Label bubbles
    for i, label in enumerate(labels):
        ax.annotate(label, (severities[i], frequencies[i]),
                    fontsize=6.5, ha="center", va="bottom",
                    xytext=(0, 8), textcoords="offset points")

    ax.set_xlabel("Severity (1-5)")
    ax.set_ylabel("Frequency")
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Low", "Medium", "High"])
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 3.5)
    ax.set_title("Severity vs Frequency (bubble size = priority score)",
                 fontsize=13, fontweight="bold")

    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor=c, label=k.replace("_", " ").title())
        for k, c in CATEGORY_COLORS.items()
    ]
    ax.legend(handles=legend_items, loc="lower right", fontsize=8)

    return _save(fig, chart_dir / f"severity_frequency{suffix}.png")


# ── 7. Rating Trend Over Time ────────────────────────────────────────────────

def rating_trend_chart(
    reviews_df: pd.DataFrame | None, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Line chart of average rating per month over time."""
    if reviews_df is None or reviews_df.empty:
        return None

    df = reviews_df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "rating"])
    if len(df) < 2:
        return None

    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("month").agg(
        avg_rating=("rating", "mean"),
        count=("rating", "size"),
    ).sort_index()

    if len(monthly) < 2:
        return None

    x_labels = [str(m) for m in monthly.index]
    x_pos = range(len(x_labels))
    ratings = monthly["avg_rating"].values
    counts = monthly["count"].values

    fig, ax1 = plt.subplots(figsize=(max(8, len(x_labels) * 0.8), 5))

    # Rating line
    color_line = "#2c3e50"
    ax1.plot(x_pos, ratings, color=color_line, marker="o", linewidth=2.5,
             markersize=6, zorder=3, label="Avg Rating")
    ax1.fill_between(x_pos, ratings, alpha=0.08, color=color_line)
    ax1.set_ylabel("Average Rating (1-5)", color=color_line)
    ax1.set_ylim(max(0.5, min(ratings) - 0.5), 5.2)
    ax1.tick_params(axis="y", labelcolor=color_line)

    # Review count bars on secondary axis
    ax2 = ax1.twinx()
    ax2.bar(x_pos, counts, alpha=0.18, color="#3498db", width=0.6, label="Review Count")
    ax2.set_ylabel("Reviews per Month", color="#3498db", alpha=0.7)
    ax2.tick_params(axis="y", labelcolor="#3498db")

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=8)
    ax1.set_title("Rating Trend Over Time", fontsize=14, fontweight="bold")
    ax1.set_zorder(ax2.get_zorder() + 1)
    ax1.patch.set_visible(False)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower left", fontsize=8)

    return _save(fig, chart_dir / f"rating_trend{suffix}.png")


# ── 8. Pain Point Frequency ─────────────────────────────────────────────────

def pain_point_frequency_chart(
    comprehensive_data: dict, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Horizontal bar chart of critical pain points ranked by frequency/severity."""
    analysis = comprehensive_data.get("analysis", {})
    pain_points = analysis.get("critical_pain_points", [])
    if not pain_points:
        return None

    freq_map = {"high": 3, "medium": 2, "low": 1}
    # Sort by composite score: severity * frequency
    scored = []
    for pp in pain_points:
        sev = pp.get("severity", 1)
        freq_str = pp.get("frequency", "medium")
        freq_val = freq_map.get(freq_str.lower(), 2) if isinstance(freq_str, str) else 2
        scored.append({
            "theme": pp.get("theme", "?")[:35],
            "severity": sev,
            "freq_val": freq_val,
            "freq_label": freq_str,
            "score": sev * freq_val,
        })

    scored.sort(key=lambda x: x["score"])
    scored = scored[-15:]  # top 15

    themes = [s["theme"] for s in scored]
    severities = [s["severity"] for s in scored]
    freq_vals = [s["freq_val"] for s in scored]

    freq_colors = {1: "#f1c40f", 2: "#e67e22", 3: "#e74c3c"}
    colors = [freq_colors.get(s["freq_val"], "#95a5a6") for s in scored]

    fig, ax = plt.subplots(figsize=(10, max(4, len(scored) * 0.45)))
    bars = ax.barh(themes, severities, color=colors, edgecolor="white", linewidth=0.5)

    # Annotate severity values
    for bar, sev in zip(bars, severities):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                f"{sev}/5", va="center", fontsize=8, color="#555")

    ax.set_xlabel("Severity (1-5)")
    ax.set_xlim(0, 5.8)
    ax.set_title("Critical Pain Points by Severity", fontsize=14, fontweight="bold")

    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor="#e74c3c", label="High frequency"),
        Patch(facecolor="#e67e22", label="Medium frequency"),
        Patch(facecolor="#f1c40f", label="Low frequency"),
    ]
    ax.legend(handles=legend_items, loc="lower right", fontsize=8)

    return _save(fig, chart_dir / f"pain_point_frequency{suffix}.png")


# ── 9. Sentiment Distribution ────────────────────────────────────────────────

def sentiment_distribution_chart(
    reviews_df: pd.DataFrame | None, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Pie chart of sentiment distribution derived from star ratings."""
    if reviews_df is None or reviews_df.empty:
        return None

    ratings = reviews_df["rating"].dropna()
    if ratings.empty:
        return None

    negative = int((ratings <= 2).sum())
    neutral = int((ratings == 3).sum())
    positive = int((ratings >= 4).sum())
    total = negative + neutral + positive

    if total == 0:
        return None

    labels = ["Negative (1-2)", "Neutral (3)", "Positive (4-5)"]
    sizes = [negative, neutral, positive]
    colors = ["#e74c3c", "#f39c12", "#2ecc71"]
    explode = (0.04, 0.04, 0.04)

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct=lambda p: f"{p:.1f}%\n({int(p*total/100)})",
        startangle=90, explode=explode,
        wedgeprops=dict(edgecolor="white", linewidth=2),
    )
    for t in autotexts:
        t.set_fontsize(9)
        t.set_fontweight("bold")
    for t in texts:
        t.set_fontsize(10)

    ax.set_title(
        f"Sentiment Distribution ({total:,} reviews)",
        fontsize=14, fontweight="bold", pad=20,
    )

    return _save(fig, chart_dir / f"sentiment_distribution{suffix}.png")


# ── 10. Issue Lifecycle Stacked Chart ────────────────────────────────────────

def issue_lifecycle_chart(
    temporal_data: dict, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Stacked horizontal bar chart of resolved/persistent/emerging issues with severity."""
    trends = temporal_data.get("trends", {})
    if not trends:
        return None

    categories = [
        ("Resolved", trends.get("resolved_issues", trends.get("resolved", [])), "#2ecc71"),
        ("Persistent", trends.get("persistent_issues", trends.get("persistent", [])), "#e67e22"),
        ("Emerging", trends.get("emerging_issues", trends.get("emerging", [])), "#e74c3c"),
    ]

    # Collect all themes with their severity and category
    items: list[dict] = []
    for cat_label, issues, color in categories:
        if not isinstance(issues, list):
            continue
        for issue in issues:
            theme = issue.get("theme", "?")[:30] if isinstance(issue, dict) else str(issue)[:30]
            sev = issue.get("severity", 3) if isinstance(issue, dict) else 3
            items.append({"theme": theme, "severity": sev, "category": cat_label, "color": color})

    if not items:
        return None

    # Sort: emerging first (most urgent), then persistent, then resolved
    cat_order = {"Emerging": 0, "Persistent": 1, "Resolved": 2}
    items.sort(key=lambda x: (cat_order.get(x["category"], 9), -x["severity"]))

    themes = [it["theme"] for it in items]
    severities = [it["severity"] for it in items]
    colors = [it["color"] for it in items]

    fig, ax = plt.subplots(figsize=(10, max(4, len(items) * 0.4)))
    bars = ax.barh(themes, severities, color=colors, edgecolor="white", linewidth=0.5)

    ax.set_xlabel("Severity (1-5)")
    ax.set_xlim(0, 5.8)
    ax.set_title("Issue Lifecycle: Emerging → Persistent → Resolved",
                 fontsize=13, fontweight="bold")

    from matplotlib.patches import Patch
    legend_items = [Patch(facecolor=c, label=l) for l, _, c in categories]
    ax.legend(handles=legend_items, loc="lower right", fontsize=9)

    return _save(fig, chart_dir / f"issue_lifecycle{suffix}.png")


# ── 11. Funnel Drop-off Hotspots ─────────────────────────────────────────────

def funnel_dropoff_chart(
    funnel_data: dict, chart_dir: Path, suffix: str = "",
) -> str | None:
    """Horizontal bar chart of drop-off hotspots by evidence count."""
    hotspots = funnel_data.get("drop_off_hotspots", [])
    if not hotspots:
        return None

    # Sort by evidence count
    hotspots.sort(key=lambda x: x.get("evidence_count", 0))
    hotspots = hotspots[-15:]  # top 15

    labels = [h.get("screen_or_step", "?")[:35] for h in hotspots]
    counts = [h.get("evidence_count", 0) for h in hotspots]
    severities = [h.get("severity", 1) for h in hotspots]

    # Color by severity
    cmap = matplotlib.colormaps.get_cmap("YlOrRd")
    norm = matplotlib.colors.Normalize(vmin=1, vmax=5)
    colors = [cmap(norm(s)) for s in severities]

    fig, ax = plt.subplots(figsize=(10, max(4, len(hotspots) * 0.45)))
    bars = ax.barh(labels, counts, color=colors, edgecolor="white", linewidth=0.5)

    # Annotate counts
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(count), va="center", fontsize=8, color="#555")

    ax.set_xlabel("Evidence Count")
    ax.set_title("Top Drop-off Hotspots (Color by Severity)", fontsize=14, fontweight="bold")
    
    # Add colorbar manually or just legend
    from matplotlib.cm import ScalarMappable
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.5)
    cbar.set_label("Severity (1-5)")

    return _save(fig, chart_dir / f"funnel_dropoff{suffix}.png")


# ── Orchestrator ─────────────────────────────────────────────────────────────

def generate_all_charts(
    insights: dict,
    temporal_data: dict,
    comprehensive_data: dict,
    funnel_data: dict,
    suffix: str = "",
    reviews_df: pd.DataFrame | None = None,
) -> dict[str, str]:
    """
    Generate all charts and return a dict mapping chart name to relative path.
    Each chart is independently wrapped so one failure doesn't block others.
    """
    chart_dir = config.output_dir() / f"charts{suffix}"
    chart_dir.mkdir(parents=True, exist_ok=True)

    chart_funcs: list[tuple[str, callable]] = [
        ("priority_bar", lambda: priority_bar_chart(insights, chart_dir, suffix)),
        ("severity_heatmap", lambda: monthly_severity_heatmap(temporal_data, chart_dir, suffix)),
        ("version_ratings", lambda: version_rating_chart(insights, chart_dir, suffix)),
        ("trend_classification", lambda: trend_classification_chart(temporal_data, chart_dir, suffix)),
        ("business_impact", lambda: business_impact_donut(insights, chart_dir, suffix)),
        ("severity_frequency", lambda: severity_frequency_bubble(insights, chart_dir, suffix)),
        ("rating_trend", lambda: rating_trend_chart(reviews_df, chart_dir, suffix)),
        ("pain_point_frequency", lambda: pain_point_frequency_chart(comprehensive_data, chart_dir, suffix)),
        ("sentiment_distribution", lambda: sentiment_distribution_chart(reviews_df, chart_dir, suffix)),
        ("issue_lifecycle", lambda: issue_lifecycle_chart(temporal_data, chart_dir, suffix)),
        ("funnel_dropoff", lambda: funnel_dropoff_chart(funnel_data, chart_dir, suffix)),
    ]

    paths: dict[str, str] = {}
    for name, func in chart_funcs:
        try:
            result = func()
            if result:
                paths[name] = result
        except Exception:
            logger.exception(f"Failed to generate chart: {name}")

    logger.info(f"Generated {len(paths)}/{len(chart_funcs)} charts in {chart_dir}")
    return paths
