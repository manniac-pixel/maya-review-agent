"""
TextBlob-based sentiment analysis fallback.
Used when LLM calls fail (rate limits, network errors, etc.).
Produces structured output similar to the LLM analysis using
keyword matching + sentiment scoring.
"""

import logging
import re
from collections import Counter

import pandas as pd
from textblob import TextBlob

logger = logging.getLogger(__name__)

# ── Fintech keyword → theme mapping ─────────────────────────────────────

THEME_KEYWORDS = {
    "Login/Authentication Issues": [
        "login", "log in", "log-in", "sign in", "signin", "can't login",
        "cannot login", "otp", "one time", "password", "biometric",
        "fingerprint", "face id", "locked out", "locked account",
    ],
    "Payment/Transaction Failures": [
        "payment fail", "transaction fail", "error paying", "can't pay",
        "cannot pay", "payment error", "declined", "not going through",
        "double charge", "charged twice",
    ],
    "Cash-In/Cash-Out Issues": [
        "cash in", "cash-in", "cashin", "cash out", "cash-out", "cashout",
        "top up", "top-up", "not reflected", "not credited", "pending",
        "deposit", "withdraw",
    ],
    "Transfer Problems": [
        "transfer fail", "send money", "can't transfer", "cannot transfer",
        "wrong account", "wrong number", "delayed transfer", "bank transfer",
    ],
    "App Crashes/Performance": [
        "crash", "crashes", "slow", "lag", "laggy", "freeze", "frozen",
        "hang", "not loading", "blank screen", "force close", "bug",
        "glitch", "not working", "not responding",
    ],
    "Customer Support Issues": [
        "customer service", "customer support", "support", "hotline",
        "chat support", "no response", "no reply", "unhelpful",
        "automated", "bot response", "ticket", "complaint",
    ],
    "KYC/Verification Issues": [
        "kyc", "verification", "verify", "id verification", "selfie",
        "valid id", "upgrade", "full verified", "account upgrade",
    ],
    "Security/Fraud Concerns": [
        "hack", "hacked", "stolen", "unauthorized", "fraud", "scam",
        "phishing", "security", "not secure", "compromised", "data breach",
    ],
    "Loan/Credit Issues": [
        "loan", "credit", "credit line", "interest", "billing",
        "installment", "repayment", "credit score", "maya credit",
    ],
    "UI/UX Problems": [
        "confusing", "hard to use", "not intuitive", "complicated",
        "ugly", "redesign", "interface", "navigation", "hard to find",
        "user friendly", "user-friendly",
    ],
    "Savings Issues": [
        "savings", "interest rate", "savings account", "earn", "yields",
    ],
    "Crypto Issues": [
        "crypto", "bitcoin", "cryptocurrency", "coin", "trading",
    ],
}

COMPETITOR_KEYWORDS = [
    "gcash", "g-cash", "grabpay", "grab pay", "coins.ph", "coins ph",
    "unionbank", "bpi", "bdo",
]

JOURNEY_MAP = {
    "Login/Authentication Issues": "onboarding",
    "Payment/Transaction Failures": "payments",
    "Cash-In/Cash-Out Issues": "payments",
    "Transfer Problems": "transfers",
    "App Crashes/Performance": "general",
    "Customer Support Issues": "support",
    "KYC/Verification Issues": "onboarding",
    "Security/Fraud Concerns": "general",
    "Loan/Credit Issues": "credit",
    "UI/UX Problems": "general",
    "Savings Issues": "savings",
    "Crypto Issues": "crypto",
}

IMPACT_MAP = {
    "Login/Authentication Issues": "activation",
    "Payment/Transaction Failures": "transaction_volume",
    "Cash-In/Cash-Out Issues": "transaction_volume",
    "Transfer Problems": "transaction_volume",
    "App Crashes/Performance": "retention",
    "Customer Support Issues": "trust",
    "KYC/Verification Issues": "activation",
    "Security/Fraud Concerns": "trust",
    "Loan/Credit Issues": "revenue",
    "UI/UX Problems": "retention",
    "Savings Issues": "retention",
    "Crypto Issues": "retention",
}


def _detect_themes(text: str) -> list[str]:
    """Return list of themes matched by keywords in the text."""
    text_lower = text.lower()
    matched = []
    for theme, keywords in THEME_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                matched.append(theme)
                break
    return matched


def _detect_competitors(text: str) -> list[str]:
    """Return list of competitor names mentioned in the text."""
    text_lower = text.lower()
    return [c for c in COMPETITOR_KEYWORDS if c in text_lower]


def _sentiment(text: str) -> float:
    """Return polarity score from -1 (negative) to 1 (positive)."""
    return TextBlob(text).sentiment.polarity


def _freq_label(count: int, total: int) -> str:
    """Convert a count to a frequency label."""
    ratio = count / max(total, 1)
    if ratio > 0.15:
        return "high"
    if ratio > 0.05:
        return "medium"
    return "low"


def _severity_from_polarity(polarity: float) -> int:
    """Map average polarity to a 1-5 severity score (more negative = higher)."""
    if polarity <= -0.4:
        return 5
    if polarity <= -0.2:
        return 4
    if polarity <= -0.05:
        return 3
    if polarity <= 0.1:
        return 2
    return 1


def _pick_quotes(texts: list[str], n: int = 2) -> list[str]:
    """Pick the most informative quotes (longest, cleaned)."""
    cleaned = [t.strip().replace("\n", " ")[:300] for t in texts if len(t.strip()) > 20]
    cleaned.sort(key=len, reverse=True)
    return cleaned[:n]


# ── Public fallback functions ───────────────────────────────────────────

def analyze_month_fallback(month_label: str, df: pd.DataFrame) -> dict:
    """
    TextBlob fallback for monthly analysis.
    Returns the same structure as the LLM prompt expects.
    """
    logger.info(f"  [TextBlob fallback] Analyzing {month_label} ({len(df)} reviews)")

    theme_reviews = {}  # theme -> list of (text, polarity)
    competitor_mentions = []

    for _, row in df.iterrows():
        text = str(row.get("text", ""))
        if not text.strip():
            continue
        polarity = _sentiment(text)
        themes = _detect_themes(text)

        for theme in themes:
            theme_reviews.setdefault(theme, []).append((text, polarity))

        comps = _detect_competitors(text)
        for c in comps:
            competitor_mentions.append((c, text, polarity))

    total = len(df)

    # Pain points: themes where average sentiment is negative
    pain_points = []
    positive_mentions = []
    for theme, entries in sorted(
        theme_reviews.items(), key=lambda x: len(x[1]), reverse=True
    ):
        texts = [e[0] for e in entries]
        avg_pol = sum(e[1] for e in entries) / len(entries)
        freq = _freq_label(len(entries), total)

        if avg_pol < 0.1:
            pain_points.append({
                "theme": theme,
                "description": f"Users report issues with {theme.lower()}",
                "severity": _severity_from_polarity(avg_pol),
                "frequency": freq,
                "quotes": _pick_quotes(texts),
            })
        else:
            positive_mentions.append({
                "theme": theme,
                "description": f"Users are positive about {theme.lower()}",
                "frequency": freq,
            })

    # Competitive comparisons
    comp_counter = Counter(c for c, _, _ in competitor_mentions)
    competitive_comparisons = []
    for comp, count in comp_counter.most_common(5):
        comp_texts = [t for c, t, _ in competitor_mentions if c == comp]
        comp_pols = [p for c, _, p in competitor_mentions if c == comp]
        avg_pol = sum(comp_pols) / len(comp_pols) if comp_pols else 0
        sentiment = (
            "maya_better" if avg_pol > 0.1
            else "competitor_better" if avg_pol < -0.1
            else "neutral"
        )
        competitive_comparisons.append({
            "competitor": comp.title(),
            "context": f"Users comparing Maya with {comp.title()}",
            "sentiment": sentiment,
            "quotes": _pick_quotes(comp_texts, 1),
        })

    # Feature requests (from positive-sentiment reviews mentioning "wish", "should", "need")
    request_pattern = re.compile(
        r"(wish|should|need|please add|hope|would be nice|want)", re.IGNORECASE
    )
    feature_texts = [
        str(row["text"]) for _, row in df.iterrows()
        if request_pattern.search(str(row.get("text", "")))
    ]
    feature_requests = []
    if feature_texts:
        feature_requests.append({
            "feature": "User-requested improvements",
            "description": "Various feature requests extracted from reviews",
            "frequency": _freq_label(len(feature_texts), total),
            "quotes": _pick_quotes(feature_texts),
        })

    return {
        "_fallback": "textblob",
        "pain_points": pain_points[:10],
        "feature_requests": feature_requests,
        "positive_mentions": positive_mentions[:5],
        "competitive_comparisons": competitive_comparisons,
    }


def analyze_comprehensive_fallback(df: pd.DataFrame) -> dict:
    """
    TextBlob fallback for comprehensive analysis.
    Returns the same structure as the LLM prompt expects.
    """
    logger.info(f"  [TextBlob fallback] Comprehensive analysis ({len(df)} reviews)")

    theme_reviews = {}
    competitor_mentions = []
    trust_reviews = []
    segment_signals = {"first_time": [], "power_user": [], "credit_user": []}

    first_time_kw = ["new user", "first time", "just installed", "just downloaded", "new account"]
    power_user_kw = ["always use", "everyday", "daily", "for years", "long time"]
    credit_user_kw = ["loan", "credit line", "credit", "installment", "billing"]

    for _, row in df.iterrows():
        text = str(row.get("text", ""))
        if not text.strip():
            continue
        text_lower = text.lower()
        polarity = _sentiment(text)
        themes = _detect_themes(text)

        for theme in themes:
            theme_reviews.setdefault(theme, []).append((text, polarity))

        if any(kw in text_lower for kw in ["hack", "fraud", "stolen", "unauthorized", "security", "scam"]):
            trust_reviews.append((text, polarity))

        for kw in first_time_kw:
            if kw in text_lower:
                segment_signals["first_time"].append(text)
                break
        for kw in power_user_kw:
            if kw in text_lower:
                segment_signals["power_user"].append(text)
                break
        for kw in credit_user_kw:
            if kw in text_lower:
                segment_signals["credit_user"].append(text)
                break

        comps = _detect_competitors(text)
        for c in comps:
            competitor_mentions.append((c, text, polarity))

    total = len(df)

    # Critical pain points
    critical_pain_points = []
    positive_signals = []
    for theme, entries in sorted(
        theme_reviews.items(), key=lambda x: len(x[1]), reverse=True
    ):
        texts = [e[0] for e in entries]
        avg_pol = sum(e[1] for e in entries) / len(entries)
        freq = _freq_label(len(entries), total)
        severity = _severity_from_polarity(avg_pol)

        if avg_pol < 0.1:
            critical_pain_points.append({
                "theme": theme,
                "description": f"Users report issues with {theme.lower()}",
                "affected_journey": JOURNEY_MAP.get(theme, "general"),
                "business_impact": IMPACT_MAP.get(theme, "retention"),
                "severity": severity,
                "frequency": freq,
                "user_quotes": _pick_quotes(texts, 3),
            })
        else:
            positive_signals.append({
                "theme": theme,
                "description": f"Users are satisfied with {theme.lower()}",
                "frequency": freq,
                "user_journey": JOURNEY_MAP.get(theme, "general"),
            })

    # Competitive insights
    comp_counter = Counter(c for c, _, _ in competitor_mentions)
    competitive_insights = []
    for comp, count in comp_counter.most_common(5):
        comp_texts = [t for c, t, _ in competitor_mentions if c == comp]
        comp_pols = [p for c, _, p in competitor_mentions if c == comp]
        avg_pol = sum(comp_pols) / len(comp_pols) if comp_pols else 0
        pref = (
            "maya" if avg_pol > 0.1
            else "competitor" if avg_pol < -0.1
            else "mixed"
        )
        competitive_insights.append({
            "competitor": comp.title(),
            "area": "general comparison",
            "user_preference": pref,
            "detail": f"{count} reviews mention {comp.title()}",
            "quotes": _pick_quotes(comp_texts, 1),
        })

    # Trust / security
    trust_security_concerns = []
    if trust_reviews:
        avg_pol = sum(p for _, p in trust_reviews) / len(trust_reviews)
        trust_security_concerns.append({
            "concern": "Account security and unauthorized access",
            "severity": _severity_from_polarity(avg_pol),
            "category": "account_security",
            "quotes": _pick_quotes([t for t, _ in trust_reviews], 2),
        })

    # Feature requests
    feature_requests = []
    request_pattern = re.compile(
        r"(wish|should|need|please add|hope|would be nice|want)", re.IGNORECASE
    )
    request_texts = [
        str(row["text"]) for _, row in df.iterrows()
        if request_pattern.search(str(row.get("text", "")))
    ]
    if request_texts:
        feature_requests.append({
            "feature": "User-requested improvements",
            "user_need": "Better reliability and features",
            "frequency": _freq_label(len(request_texts), total),
            "impact_area": "retention",
            "quotes": _pick_quotes(request_texts, 2),
        })

    # User segments
    user_segments = []
    for seg_key, seg_label, needs, frustrations in [
        ("first_time", "First-time users",
         ["Easy onboarding", "Clear instructions"],
         ["Login issues", "KYC difficulties"]),
        ("power_user", "Power users",
         ["Reliability", "Fast transactions"],
         ["Crashes", "Customer support"]),
        ("credit_user", "Credit/Loan users",
         ["Easy credit access", "Fair rates"],
         ["Loan issues", "Billing problems"]),
    ]:
        texts = segment_signals[seg_key]
        if texts:
            user_segments.append({
                "segment": seg_label,
                "characteristics": f"Identified from {len(texts)} reviews with segment-specific keywords",
                "primary_needs": needs,
                "primary_frustrations": frustrations,
            })

    return {
        "_fallback": "textblob",
        "critical_pain_points": critical_pain_points[:10],
        "competitive_insights": competitive_insights,
        "trust_security_concerns": trust_security_concerns,
        "feature_requests": feature_requests,
        "positive_signals": positive_signals[:5],
        "user_segments": user_segments,
    }
