"""
Maya Review Agent — Interactive Dashboard
==========================================
Streamlit web app for exploring the agent's findings.
Run: streamlit run streamlit_app.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import streamlit as st

# -- Config -------------------------------------------------------------------

DATA_DIR = Path("data")
CHARTS_DIR = DATA_DIR / "charts"

# Maya brand colors
MAYA_MINT = "#2FF29E"
MAYA_DARK = "#112432"
MAYA_JADE = "#00B463"
MAYA_SAND = "#D69474"
MAYA_GRAY = "#9CA3AF"
MAYA_LIGHT = "#F9FAFB"

st.set_page_config(
    page_title="Maya Review Agent",
    page_icon="data/charts/rating_trend.png" if (CHARTS_DIR / "rating_trend.png").exists() else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# -- Custom CSS (Maya branding) -----------------------------------------------

st.markdown(f"""
<style>
    /* Import a clean sans-serif */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global */
    html, body, .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .stApp {{
        background: #FFFFFF;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {MAYA_DARK};
        color: white;
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stRadio label span {{
        color: #CBD5E1 !important;
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: white !important;
    }}
    section[data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.1);
    }}
    section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] {{
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 6px 12px;
        margin-bottom: 2px;
    }}
    section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:hover {{
        background: rgba(47, 242, 158, 0.1);
    }}

    /* Headings */
    h1 {{
        color: {MAYA_DARK} !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }}
    h2, h3 {{
        color: {MAYA_DARK} !important;
        font-weight: 700 !important;
    }}

    /* Metrics */
    [data-testid="stMetric"] {{
        background: {MAYA_LIGHT};
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px 20px;
    }}
    [data-testid="stMetricLabel"] p {{
        color: {MAYA_GRAY} !important;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    [data-testid="stMetricValue"] {{
        color: {MAYA_DARK} !important;
        font-weight: 800 !important;
    }}
    [data-testid="stMetricDelta"] {{
        font-weight: 600;
    }}

    /* Tables */
    .stTable table {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E5E7EB;
    }}
    .stTable th {{
        background: {MAYA_DARK} !important;
        color: white !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
    }}
    .stTable td {{
        font-size: 0.9rem;
    }}

    /* Expanders */
    .streamlit-expanderHeader {{
        background: {MAYA_LIGHT};
        border-radius: 8px;
        font-weight: 600;
        color: {MAYA_DARK};
    }}

    /* Info / warning boxes */
    .stAlert {{
        border-radius: 12px;
        border-left-width: 4px;
    }}

    /* Dividers */
    hr {{
        border-color: #E5E7EB;
    }}

    /* Hide Streamlit hamburger & footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Custom brand header */
    .maya-brand {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 4px;
    }}
    .maya-logo {{
        width: 40px;
        height: 40px;
        background: {MAYA_DARK};
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: {MAYA_MINT};
        font-weight: 800;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
    }}
    .maya-title {{
        font-size: 1.4rem;
        font-weight: 800;
        color: white;
        letter-spacing: -0.01em;
    }}
    .maya-subtitle {{
        font-size: 0.8rem;
        color: {MAYA_GRAY};
        margin-top: -2px;
    }}

    /* Pill badge */
    .pill {{
        display: inline-block;
        padding: 3px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }}
    .pill-red {{ background: #FEE2E2; color: #DC2626; }}
    .pill-green {{ background: #D1FAE5; color: #059669; }}
    .pill-amber {{ background: #FEF3C7; color: #D97706; }}
    .pill-navy {{ background: {MAYA_DARK}; color: white; }}
    .pill-mint {{ background: rgba(47,242,158,0.15); color: #059669; }}

    /* Issue card */
    .issue-card {{
        background: {MAYA_LIGHT};
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
    }}
    .issue-card h4 {{
        margin: 0 0 4px 0;
        color: {MAYA_DARK};
    }}
    .issue-meta {{
        color: {MAYA_GRAY};
        font-size: 0.85rem;
    }}

    /* Severity bar */
    .severity-bar {{
        height: 6px;
        border-radius: 3px;
        background: #E5E7EB;
        margin-top: 8px;
    }}
    .severity-fill {{
        height: 100%;
        border-radius: 3px;
    }}

    /* User quote */
    .user-quote {{
        background: {MAYA_LIGHT};
        border-left: 3px solid {MAYA_MINT};
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 8px 0;
        font-style: italic;
        color: #374151;
        font-size: 0.9rem;
    }}

    /* Stat highlight */
    .stat-highlight {{
        background: linear-gradient(135deg, rgba(47,242,158,0.08), rgba(0,180,99,0.08));
        border: 1px solid rgba(47,242,158,0.2);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }}
    .stat-big {{
        font-size: 2.5rem;
        font-weight: 800;
        color: {MAYA_DARK};
        line-height: 1;
    }}
    .stat-label {{
        font-size: 0.85rem;
        color: {MAYA_GRAY};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }}
</style>
""", unsafe_allow_html=True)


# -- Data loading -------------------------------------------------------------

@st.cache_data
def load_json(path_str: str) -> Optional[dict]:
    p = Path(path_str)
    if p.exists():
        return json.loads(p.read_text())
    return None


@st.cache_data
def load_markdown(path_str: str) -> Optional[str]:
    p = Path(path_str)
    if p.exists():
        return p.read_text()
    return None


def load_insights(suffix: str = "") -> Optional[dict]:
    return load_json(str(DATA_DIR / f"final_insights{suffix}.json"))


def load_report(suffix: str = "") -> Optional[str]:
    return load_markdown(str(DATA_DIR / f"maya_insights_report{suffix}.md"))


def chart_path(name: str) -> Path:
    return CHARTS_DIR / name


def get_nested(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d


def severity_color(sev: int) -> str:
    if sev >= 5:
        return "#DC2626"
    elif sev >= 4:
        return "#D97706"
    elif sev >= 3:
        return "#F59E0B"
    else:
        return MAYA_JADE


def freq_label(freq: str) -> str:
    f = freq.lower() if isinstance(freq, str) else "?"
    colors = {"high": "pill-red", "medium": "pill-amber", "low": "pill-green"}
    cls = colors.get(f, "pill-navy")
    return f'<span class="pill {cls}">{f.upper()}</span>'


# -- Sidebar ------------------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div class="maya-brand">
        <div class="maya-logo">M</div>
        <div>
            <div class="maya-title">Maya Review Agent</div>
            <div class="maya-subtitle">AI-Powered UX Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Dataset selector
    has_all = (DATA_DIR / "final_insights.json").exists()
    has_1star = (DATA_DIR / "final_insights_1star.json").exists()

    datasets = []
    if has_all:
        datasets.append("All Reviews")
    if has_1star:
        datasets.append("1-Star Only")

    if not datasets:
        st.error("No analysis data found. Run the agent first:\n```\npython main.py\n```")
        st.stop()

    selected_dataset = st.radio("Dataset", datasets, index=0)
    suffix = "_1star" if "1-Star" in selected_dataset else ""

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Ranked Issues",
            "Funnel Drop-offs",
            "Version Analysis",
            "Competitor Analysis",
            "Charts",
            "Full Report",
        ],
    )

    st.divider()
    st.markdown(f"""
    <div style="font-size: 0.75rem; color: {MAYA_GRAY};">
        Built by Manpreet Bhattee<br>
        February 2026
    </div>
    """, unsafe_allow_html=True)

# -- Load data ----------------------------------------------------------------

insights = load_insights(suffix)
report_md = load_report(suffix)

if insights is None:
    st.error("Could not load insights data. Run the agent first: `python main.py`")
    st.stop()


# -- Pages --------------------------------------------------------------------

if page == "Overview":
    st.markdown(f"""
    <h1 style="margin-bottom: 0;">Maya UX Intelligence</h1>
    <p style="color: {MAYA_GRAY}; font-size: 1.1rem; margin-top: 4px;">
        AI-driven analysis of {selected_dataset.lower()} from the Google Play Store
    </p>
    """, unsafe_allow_html=True)

    exec_summary = get_nested(insights, "executive_summary", default={})
    opportunities = insights.get("ranked_ux_opportunities", [])
    version_data = insights.get("_version_analysis", {})
    trend_summary = insights.get("trend_summary", {})

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    total = exec_summary.get("total_reviews_analyzed", "12,345")
    col1.metric("Reviews Analyzed", f"{total:,}" if isinstance(total, int) else str(total))

    date_range = exec_summary.get("date_range", "Aug 2025 - Feb 2026")
    col2.metric("Date Range", str(date_range))

    col3.metric("Issues Found", len(opportunities))

    severities = [o.get("severity", 0) for o in opportunities if isinstance(o.get("severity"), int)]
    max_sev = max(severities, default=0)
    col4.metric("Max Severity", f"{max_sev}/5" if max_sev else "N/A")

    st.divider()

    # Sentiment summary
    sentiment_text = exec_summary.get("overall_sentiment", "Mixed-negative")
    st.markdown(f"""
    <div class="stat-highlight">
        <div style="font-size: 1rem; font-weight: 600; color: {MAYA_DARK}; margin-bottom: 8px;">
            Overall Sentiment
        </div>
        <div style="font-size: 1.1rem; color: #374151;">
            {sentiment_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # Top persistent issues
    persistent = exec_summary.get("top_persistent_issues", [])
    emerging = exec_summary.get("top_emerging_issues", [])

    if persistent or emerging:
        col_p, col_e = st.columns(2)
        with col_p:
            st.markdown(f'#### Persistent Issues')
            for item in persistent:
                months = item.get("months_active", "?")
                st.markdown(f"""
                <div class="issue-card">
                    <h4>{item.get("theme", "Unknown")}</h4>
                    <span class="pill pill-red">{months} months active</span>
                    <p class="issue-meta" style="margin-top: 8px;">{item.get("description", "")}</p>
                </div>
                """, unsafe_allow_html=True)

        with col_e:
            st.markdown(f'#### Emerging Issues')
            for item in emerging:
                first_seen = item.get("first_seen", "?")
                st.markdown(f"""
                <div class="issue-card">
                    <h4>{item.get("theme", "Unknown")}</h4>
                    <span class="pill pill-amber">Since {first_seen}</span>
                    <p class="issue-meta" style="margin-top: 8px;">{item.get("description", "")}</p>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # Top 5 issues
    st.markdown("#### Top 5 UX Issues")
    for i, opp in enumerate(opportunities[:5], 1):
        theme = opp.get("theme", opp.get("issue", opp.get("name", "Unknown")))
        sev = opp.get("severity", 0)
        score = opp.get("priority_score", "?")
        cat = opp.get("category", "?").replace("_", " ").title()
        sev_pct = (sev / 5) * 100

        st.markdown(f"""
        <div class="issue-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin:0;">#{i} {theme}</h4>
                <span class="pill pill-navy">Score: {score}</span>
            </div>
            <div style="display: flex; gap: 8px; margin-top: 8px;">
                <span class="pill pill-{'red' if sev >= 4 else 'amber' if sev >= 3 else 'green'}">Severity {sev}/5</span>
                <span class="pill pill-mint">{cat}</span>
            </div>
            <div class="severity-bar">
                <div class="severity-fill" style="width: {sev_pct}%; background: {severity_color(sev)};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Rating trend chart
    rating_chart = chart_path("rating_trend.png")
    if rating_chart.exists():
        st.markdown("#### Rating Trend Over Time")
        st.image(str(rating_chart), use_container_width=True)

    # Trend summary
    if trend_summary:
        st.divider()
        col_imp, col_dec, col_stab = st.columns(3)
        with col_imp:
            st.markdown(f"**Improving**")
            for area in trend_summary.get("improving_areas", []):
                st.markdown(f'<span class="pill pill-green">{area}</span>', unsafe_allow_html=True)
        with col_dec:
            st.markdown(f"**Declining**")
            for area in trend_summary.get("declining_areas", []):
                st.markdown(f'<span class="pill pill-red">{area}</span>', unsafe_allow_html=True)
        with col_stab:
            st.markdown(f"**Stable Pain Points**")
            for area in trend_summary.get("stable_pain_points", []):
                st.markdown(f'<span class="pill pill-amber">{area}</span>', unsafe_allow_html=True)

    st.divider()

    # User voices
    st.markdown("#### User Voices")
    quotes = []
    for opp in opportunities[:5]:
        for q in opp.get("user_quotes", [])[:1]:
            quotes.append(q)
    if not quotes:
        quotes = [
            "I've tried several times today, but I can't get in.",
            "My phone was stolen and the hacker was able to access this app and took my savings.",
            "I tried calling your toll-free hotline, but no one answered.",
        ]
    for q in quotes:
        st.markdown(f'<div class="user-quote">"{q}"</div>', unsafe_allow_html=True)


elif page == "Ranked Issues":
    st.markdown(f"""
    <h1 style="margin-bottom: 0;">Ranked UX Opportunities</h1>
    <p style="color: {MAYA_GRAY}; font-size: 1rem; margin-top: 4px;">
        Prioritized by severity, frequency, and business impact
    </p>
    """, unsafe_allow_html=True)

    opportunities = insights.get("ranked_ux_opportunities", [])

    if not opportunities:
        st.warning("No ranked opportunities found in the data.")
    else:
        # Summary table
        st.markdown("#### Priority Ranking")
        import pandas as pd
        table_data = []
        for i, opp in enumerate(opportunities, 1):
            table_data.append({
                "Rank": i,
                "Issue": opp.get("theme", opp.get("issue", "Unknown")),
                "Severity": opp.get("severity", "?"),
                "Frequency": opp.get("frequency", "?"),
                "Score": opp.get("priority_score", "?"),
                "Category": opp.get("category", "?").replace("_", " ").title(),
            })
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Priority scores chart
        priority_chart = chart_path("priority_scores.png")
        if priority_chart.exists():
            st.image(str(priority_chart), use_container_width=True)

        st.divider()

        # Detailed cards
        st.markdown("#### Issue Details")
        for opp in opportunities:
            theme = opp.get("theme", opp.get("issue", "Unknown"))
            sev = opp.get("severity", "?")
            with st.expander(f"{theme} (Severity {sev}/5)"):
                desc = opp.get("description", "")
                if desc:
                    st.markdown(desc)

                journey = opp.get("affected_journey", "")
                if journey:
                    journeys = journey.split("|") if isinstance(journey, str) else [journey]
                    pills = " ".join([f'<span class="pill pill-mint">{j.strip()}</span>' for j in journeys[:4]])
                    st.markdown(f"**Journeys:** {pills}", unsafe_allow_html=True)

                impact = opp.get("business_impact", "")
                if impact:
                    impacts = impact.split("|") if isinstance(impact, str) else ([impact] if isinstance(impact, str) else impact)
                    pills = " ".join([f'<span class="pill pill-amber">{i.strip()}</span>' for i in impacts[:4]])
                    st.markdown(f"**Business Impact:** {pills}", unsafe_allow_html=True)

                rec = opp.get("recommendation", "")
                if rec:
                    st.success(f"**Recommendation:** {rec}")

                user_quotes = opp.get("user_quotes", [])
                for q in user_quotes:
                    st.markdown(f'<div class="user-quote">"{q}"</div>', unsafe_allow_html=True)

        # Quick wins
        quick_wins = insights.get("quick_wins", [])
        if quick_wins:
            st.divider()
            st.markdown("#### Quick Wins")
            for qw in quick_wins:
                st.markdown(f"""
                <div class="issue-card">
                    <h4>{qw.get("issue", "Unknown")}</h4>
                    <div style="display: flex; gap: 8px; margin: 8px 0;">
                        <span class="pill pill-green">Effort: {qw.get("effort", "?")}</span>
                        <span class="pill pill-navy">Impact: {qw.get("impact", "?")}</span>
                    </div>
                    <p class="issue-meta">{qw.get("recommendation", "")}</p>
                </div>
                """, unsafe_allow_html=True)

        # Strategic bets
        strat_bets = insights.get("strategic_bets", [])
        if strat_bets:
            st.divider()
            st.markdown("#### Strategic Bets")
            for sb in strat_bets:
                with st.expander(sb.get("initiative", "Unknown")):
                    st.markdown(sb.get("description", ""))
                    st.markdown(f"**User Need:** {sb.get('user_need', '')}")
                    st.markdown(f"**Competitive Context:** {sb.get('competitive_context', '')}")
                    st.markdown(f"""
                    <div style="display: flex; gap: 8px; margin-top: 8px;">
                        <span class="pill pill-red">Effort: {sb.get("effort", "?")}</span>
                        <span class="pill pill-navy">Impact: {sb.get("impact", "?")}</span>
                    </div>
                    """, unsafe_allow_html=True)


elif page == "Funnel Drop-offs":
    st.markdown(f"""
    <h1 style="margin-bottom: 0;">Funnel Drop-off Hotspots</h1>
    <p style="color: {MAYA_GRAY}; font-size: 1rem; margin-top: 4px;">
        Where users abandon key journeys
    </p>
    """, unsafe_allow_html=True)

    funnel = load_json(str(DATA_DIR / f"funnel_analysis{suffix}.json"))
    if not funnel:
        funnel = load_json(str(DATA_DIR / "funnel_analysis.json"))

    # Show the chart
    funnel_chart = chart_path("funnel_dropoff.png")
    if funnel_chart.exists():
        st.image(str(funnel_chart), use_container_width=True)

    st.divider()

    if funnel:
        # Signal breakdown
        breakdown = funnel.get("signal_breakdown", {})
        if breakdown:
            st.markdown("#### Behavioral Signals")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Scanned", f"{funnel.get('total_reviews_scanned', 0):,}")
            col2.metric("Retry Signals", breakdown.get("retry", 0))
            col3.metric("Abandonment", breakdown.get("abandonment", 0))
            col4.metric("Multi-step Failures", breakdown.get("multi_step", 0))
            st.divider()

        # Hotspots
        hotspots = funnel.get("drop_off_hotspots", [])
        if hotspots:
            st.markdown("#### Screen-Level Drop-offs")
            import pandas as pd
            hotspot_data = []
            for spot in hotspots:
                hotspot_data.append({
                    "Screen": spot.get("screen_or_step", spot.get("screen", "Unknown")),
                    "Journey": spot.get("journey", "?").title(),
                    "Severity": f"{spot.get('severity', '?')}/5",
                    "Evidence": f"{spot.get('evidence_count', spot.get('evidence', '?'))} reviews",
                    "Signals": ", ".join(spot.get("signals", [])),
                    "Recommendation": spot.get("recommendation", ""),
                })
            df = pd.DataFrame(hotspot_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.divider()

            # Detailed cards
            for spot in hotspots:
                screen = spot.get("screen_or_step", spot.get("screen", "Unknown"))
                sev = spot.get("severity", 0)
                st.markdown(f"""
                <div class="issue-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin:0;">{screen}</h4>
                        <span class="pill pill-{'red' if sev >= 4 else 'amber'}">{spot.get('journey', '?').title()}</span>
                    </div>
                    <div style="margin-top: 8px;">
                        <span class="pill pill-navy">Severity {sev}/5</span>
                        <span class="pill pill-mint">{spot.get('evidence_count', '?')} reviews</span>
                    </div>
                    <div class="severity-bar" style="margin-top: 12px;">
                        <div class="severity-fill" style="width: {(sev/5)*100}%; background: {severity_color(sev)};"></div>
                    </div>
                    <p style="margin-top: 12px; color: {MAYA_JADE}; font-weight: 600;">{spot.get("recommendation", "")}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Run the agent with funnel analysis to see drop-off data: `python main.py`")


elif page == "Version Analysis":
    st.markdown(f"""
    <h1 style="margin-bottom: 0;">Version Spike Analysis</h1>
    <p style="color: {MAYA_GRAY}; font-size: 1rem; margin-top: 4px;">
        Identifying regression releases and their root causes
    </p>
    """, unsafe_allow_html=True)

    version_data = insights.get("_version_analysis", {})

    # Version chart
    version_chart = chart_path("version_ratings.png")
    if version_chart.exists():
        st.image(str(version_chart), use_container_width=True)

    st.divider()

    if version_data:
        baseline = version_data.get("baseline", {})

        # Baseline metrics
        st.markdown("#### Baseline Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Rating", f"{baseline.get('avg_rating', 0):.2f}")
        col2.metric("1-Star Baseline", f"{baseline.get('one_star_pct', 0):.1f}%")
        col3.metric("Versioned Reviews", f"{baseline.get('total_versioned_reviews', 0):,}")

        st.divider()

        # Flagged versions
        flagged = version_data.get("flagged_versions", [])
        spike_analyses = version_data.get("spike_analyses", {})

        for ver in flagged:
            analysis = spike_analyses.get(ver, {})
            st.markdown(f"""
            <div class="stat-highlight" style="background: linear-gradient(135deg, rgba(220,38,38,0.05), rgba(217,119,6,0.05)); border-color: rgba(220,38,38,0.2);">
                <div class="stat-big" style="color: #DC2626;">v{ver}</div>
                <div class="stat-label">Regression Release</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("")

            # Find version stats
            vstats = next((v for v in version_data.get("version_stats", []) if v.get("version") == ver), {})
            if vstats:
                col1, col2, col3 = st.columns(3)
                col1.metric("1-Star Rate", f"{vstats.get('one_star_pct', 0):.1f}%",
                           f"+{vstats.get('one_star_pct', 0) - baseline.get('one_star_pct', 0):.1f}pp vs baseline")
                col2.metric("Reviews", vstats.get("review_count", 0))
                col3.metric("Avg Rating", f"{vstats.get('avg_rating', 0):.2f}")

            # Root causes
            primary = analysis.get("primary_issues", [])
            if primary:
                st.markdown("**Root causes identified:**")
                for issue in primary:
                    sev = issue.get("severity", 0)
                    st.markdown(f"""
                    <div class="issue-card">
                        <h4>{issue.get("theme", "Unknown")}</h4>
                        <div style="display: flex; gap: 8px; margin: 8px 0;">
                            <span class="pill pill-{'red' if sev >= 4 else 'amber'}">Severity {sev}/5</span>
                            <span class="pill pill-navy">{issue.get("likely_cause", "?").replace("|", " / ")}</span>
                        </div>
                        <p class="issue-meta">{issue.get("description", "")}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    for q in issue.get("quotes", []):
                        st.markdown(f'<div class="user-quote">"{q}"</div>', unsafe_allow_html=True)

            summary = analysis.get("likely_root_cause_summary", "")
            if summary:
                st.info(f"**Summary:** {summary}")

        st.divider()

        # All versions table
        st.markdown("#### All Versions by 1-Star Rate")
        import pandas as pd
        vstats_list = version_data.get("version_stats", [])
        if vstats_list:
            vdf = pd.DataFrame([{
                "Version": f"v{v.get('version', '?')}",
                "Reviews": v.get("review_count", 0),
                "Avg Rating": f"{v.get('avg_rating', 0):.2f}",
                "1-Star Rate": f"{v.get('one_star_pct', 0):.1f}%",
                "1-Star Count": v.get("one_star_count", 0),
                "Status": "SPIKE" if v.get("spike") == "True" else ("Best" if v.get("one_star_pct", 100) < 20 else ""),
            } for v in vstats_list])
            st.dataframe(vdf, use_container_width=True, hide_index=True)

    # Lifecycle chart
    lifecycle_chart = chart_path("issue_lifecycle.png")
    if lifecycle_chart.exists():
        st.divider()
        st.markdown("#### Issue Lifecycle Over Time")
        st.image(str(lifecycle_chart), use_container_width=True)


elif page == "Competitor Analysis":
    st.markdown(f"""
    <h1 style="margin-bottom: 0;">Maya vs GCash</h1>
    <p style="color: {MAYA_GRAY}; font-size: 1rem; margin-top: 4px;">
        Competitive analysis based on user review intelligence
    </p>
    """, unsafe_allow_html=True)

    comparison = load_json(str(DATA_DIR / f"competitor_comparison{suffix}.json"))
    if not comparison:
        comparison = load_json(str(DATA_DIR / "competitor_comparison.json"))

    if comparison:
        summary_text = comparison.get("summary", "")
        if summary_text:
            st.markdown(f"""
            <div class="stat-highlight">
                <div style="font-size: 1rem; color: #374151;">{summary_text}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")

        # Comparative metrics
        metrics = comparison.get("comparative_metrics", {})
        if metrics:
            st.markdown("#### Head-to-Head Metrics")
            cols = st.columns(3)

            ratings = metrics.get("average_rating", {})
            cols[0].metric("Maya Rating", ratings.get("Maya", "?"))
            cols[0].metric("GCash Rating", ratings.get("GCash", "?"))

            sentiment = metrics.get("sentiment_score", {})
            cols[1].metric("Maya Sentiment", f"{sentiment.get('Maya', 0):.0%}" if isinstance(sentiment.get("Maya"), (int, float)) else "?")
            cols[1].metric("GCash Sentiment", f"{sentiment.get('GCash', 0):.0%}" if isinstance(sentiment.get("GCash"), (int, float)) else "?")

            issues = metrics.get("issue_frequency", {})
            cols[2].metric("Maya Issue Freq", f"{issues.get('Maya', 0):.0%}" if isinstance(issues.get("Maya"), (int, float)) else "?")
            cols[2].metric("GCash Issue Freq", f"{issues.get('GCash', 0):.0%}" if isinstance(issues.get("GCash"), (int, float)) else "?")

            st.divider()

        # Key differentiators
        diffs = comparison.get("key_differentiators", [])
        if diffs:
            st.markdown("#### Key Differentiators")
            for d in diffs:
                st.markdown(f'<div class="user-quote">{d}</div>', unsafe_allow_html=True)
            st.divider()

        # Feature gaps
        gaps = comparison.get("feature_gaps", [])
        if gaps:
            st.markdown("#### Feature Gaps")
            import pandas as pd
            gap_df = pd.DataFrame([{
                "Feature": g.get("feature", "?"),
                "Gap": g.get("gap", "?"),
                "Impact": g.get("impact", "?"),
            } for g in gaps])
            st.dataframe(gap_df, use_container_width=True, hide_index=True)

        # Competitive gaps from insights
        comp_gaps = insights.get("competitive_gaps", [])
        if comp_gaps:
            st.divider()
            st.markdown("#### Detailed Competitive Gaps")
            for gap in comp_gaps:
                with st.expander(f"{gap.get('area', 'Unknown')} vs {gap.get('competitor', 'Competitor')}"):
                    st.markdown(gap.get("gap_description", ""))
                    rec = gap.get("recommendation", "")
                    if rec:
                        st.success(f"**Recommendation:** {rec}")
                    for q in gap.get("user_quotes", []):
                        st.markdown(f'<div class="user-quote">"{q}"</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown(f"""
        <div class="issue-card" style="border-left: 4px solid #DC2626;">
            <h4 style="color: #DC2626;">Key Risk</h4>
            <p>Users are actively switching to GCash, citing reliability and security as primary reasons.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Competitor comparison data not found. Run the agent with competitor analysis enabled.")


elif page == "Charts":
    st.markdown(f"""
    <h1 style="margin-bottom: 0;">Visualizations</h1>
    <p style="color: {MAYA_GRAY}; font-size: 1rem; margin-top: 4px;">
        Auto-generated charts from the Maya Review Agent pipeline
    </p>
    """, unsafe_allow_html=True)

    chart_files = [
        ("rating_trend.png", "Rating Trend Over Time"),
        ("sentiment_distribution.png", "Sentiment Distribution"),
        ("priority_scores.png", "Priority Scores"),
        ("severity_frequency.png", "Severity vs Frequency"),
        ("pain_point_frequency.png", "Pain Point Frequency"),
        ("business_impact.png", "Business Impact Distribution"),
        ("version_ratings.png", "Version Ratings (1-Star Rate)"),
        ("issue_lifecycle.png", "Issue Lifecycle Over Time"),
        ("funnel_dropoff.png", "Funnel Drop-off Points"),
    ]

    found_any = False
    for filename, title in chart_files:
        path = chart_path(filename)
        if path.exists():
            found_any = True
            st.markdown(f"#### {title}")
            st.image(str(path), use_container_width=True)
            st.divider()

    if not found_any:
        st.warning("No charts found. Run the agent first: `python main.py`")


elif page == "Full Report":
    st.markdown(f"""
    <h1 style="margin-bottom: 0;">Full Insights Report</h1>
    <p style="color: {MAYA_GRAY}; font-size: 1rem; margin-top: 4px;">
        Complete markdown report generated by the agent
    </p>
    """, unsafe_allow_html=True)

    if report_md:
        # Replace image references with actual images
        lines = report_md.split("\n")
        cleaned_lines = []
        for line in lines:
            if line.strip().startswith("![") and "data/charts/" in line:
                # Extract image path and render inline
                try:
                    img_name = line.split("(")[-1].rstrip(")")
                    img_path = Path(img_name)
                    if img_path.exists():
                        st.markdown("\n".join(cleaned_lines))
                        cleaned_lines = []
                        st.image(str(img_path), use_container_width=True)
                        continue
                except Exception:
                    pass
            cleaned_lines.append(line)

        if cleaned_lines:
            st.markdown("\n".join(cleaned_lines))
    else:
        st.warning("Report not found. Run the agent first: `python main.py`")

    # User segment insights
    segments = insights.get("user_segment_insights", [])
    if segments:
        st.divider()
        st.markdown("#### User Segments")
        cols = st.columns(len(segments))
        for i, seg in enumerate(segments):
            with cols[i]:
                st.markdown(f"""
                <div class="issue-card" style="text-align: center;">
                    <h4>{seg.get("segment", "?")}</h4>
                    <span class="pill pill-navy">{seg.get("size_signal", "?").title()} volume</span>
                    <p class="issue-meta" style="margin-top: 12px;"><strong>Needs:</strong> {", ".join(seg.get("top_needs", []))}</p>
                    <p class="issue-meta"><strong>Frustrations:</strong> {", ".join(seg.get("top_frustrations", []))}</p>
                </div>
                """, unsafe_allow_html=True)
