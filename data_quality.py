"""
Data quality check module.
Validates scraped review data before analysis: verifies reviews exist,
reports date range coverage, identifies monthly gaps, and warns on small samples.
"""

from __future__ import annotations

import logging
from datetime import datetime

import pandas as pd

import config

logger = logging.getLogger(__name__)


def run(df: pd.DataFrame) -> dict:
    """
    Run all quality checks on the reviews DataFrame.
    Logs warnings for any issues found and returns a summary dict.
    """
    report: dict = {"passed": True, "warnings": [], "info": {}}

    _check_reviews_exist(df, report)
    if not report["passed"]:
        # Nothing else to check on an empty frame.
        _log_report(report)
        return report

    _check_columns(df, report)
    _check_date_range(df, report)
    _check_monthly_gaps(df, report)
    _check_sample_size(df, report)

    _log_report(report)
    return report


# ── Individual checks ────────────────────────────────────────────────────────

def _check_reviews_exist(df: pd.DataFrame, report: dict) -> None:
    """Verify that reviews were actually scraped."""
    if df is None or df.empty:
        report["passed"] = False
        report["warnings"].append("No reviews found — the DataFrame is empty.")
        return

    total = len(df)
    report["info"]["total_reviews"] = total

    empty_text = df["text"].isna().sum() + (df["text"].astype(str).str.strip() == "").sum()
    if empty_text:
        report["warnings"].append(
            f"{empty_text} review(s) have empty or missing text "
            f"({empty_text / total:.0%} of total)."
        )

    missing_ratings = df["rating"].isna().sum()
    if missing_ratings:
        report["warnings"].append(
            f"{missing_ratings} review(s) have no rating."
        )


def _check_columns(df: pd.DataFrame, report: dict) -> None:
    """Verify required columns are present."""
    required = {"date", "rating", "text", "platform"}
    missing = required - set(df.columns)
    if missing:
        report["passed"] = False
        report["warnings"].append(
            f"Missing required columns: {', '.join(sorted(missing))}."
        )


def _check_date_range(df: pd.DataFrame, report: dict) -> None:
    """Report the date range the data covers."""
    if "date" not in df.columns:
        return

    dates = pd.to_datetime(df["date"], errors="coerce").dropna()
    if dates.empty:
        report["warnings"].append("No valid dates found in the data.")
        return

    earliest = dates.min()
    latest = dates.max()
    span_days = (latest - earliest).days

    report["info"]["date_earliest"] = earliest.strftime("%Y-%m-%d")
    report["info"]["date_latest"] = latest.strftime("%Y-%m-%d")
    report["info"]["span_days"] = span_days
    report["info"]["span_months"] = round(span_days / 30.44)

    # Warn if the most recent review is stale.
    stale_days = config.get("data_quality", "stale_days", 60)
    days_stale = (datetime.now() - latest).days
    if days_stale > stale_days:
        report["warnings"].append(
            f"Most recent review is {days_stale} days old — data may be stale."
        )

    if span_days < 28:
        report["warnings"].append(
            f"Date range covers only {span_days} days — "
            "trends and temporal analysis will be very limited."
        )


def _check_monthly_gaps(df: pd.DataFrame, report: dict) -> None:
    """Identify calendar months with zero reviews within the data's date range."""
    if "date" not in df.columns:
        return

    dates = pd.to_datetime(df["date"], errors="coerce").dropna()
    if dates.empty:
        return

    # Build the full range of months between earliest and latest review.
    months_with_data = set(dates.dt.to_period("M"))
    full_range = pd.period_range(
        start=dates.min().to_period("M"),
        end=dates.max().to_period("M"),
        freq="M",
    )
    gap_months = sorted(set(full_range) - months_with_data)

    report["info"]["months_with_data"] = len(months_with_data)
    report["info"]["months_in_range"] = len(full_range)

    if gap_months:
        gaps_str = [str(m) for m in gap_months]
        report["info"]["gap_months"] = gaps_str
        report["warnings"].append(
            f"{len(gap_months)} month(s) have zero reviews: {', '.join(gaps_str)}."
        )

    # Also flag months with very few reviews.
    min_monthly = config.get("data_quality", "min_monthly_reviews", 5)
    monthly_counts = dates.dt.to_period("M").value_counts()
    thin_months = monthly_counts[monthly_counts < min_monthly]
    if not thin_months.empty:
        thin_str = [
            f"{m} ({c})" for m, c in sorted(thin_months.items())
        ]
        report["info"]["thin_months"] = {str(m): int(c) for m, c in thin_months.items()}
        report["warnings"].append(
            f"{len(thin_months)} month(s) have fewer than {min_monthly} "
            f"reviews: {', '.join(thin_str)}."
        )


def _check_sample_size(df: pd.DataFrame, report: dict) -> None:
    """Warn if total or per-platform sample sizes are too small."""
    min_total = config.get("data_quality", "min_total_reviews", 30)
    min_per_platform = config.get("data_quality", "min_per_platform", 10)

    total = len(df)
    if total < min_total:
        report["warnings"].append(
            f"Only {total} reviews total (minimum recommended: {min_total}). "
            "Analysis results may not be reliable."
        )

    if "platform" not in df.columns:
        return

    platform_counts = df["platform"].value_counts()
    report["info"]["platform_counts"] = {
        str(k): int(v) for k, v in platform_counts.items()
    }

    for platform, count in platform_counts.items():
        if count < min_per_platform:
            report["warnings"].append(
                f"Only {count} reviews for {platform} "
                f"(minimum recommended: {min_per_platform})."
            )


# ── Logging ──────────────────────────────────────────────────────────────────

def _log_report(report: dict) -> None:
    """Emit the quality report to the logger."""
    info = report["info"]

    if not report["passed"]:
        for w in report["warnings"]:
            logger.error(f"  DATA QUALITY: {w}")
        return

    total = info.get("total_reviews", 0)
    date_earliest = info.get("date_earliest", "?")
    date_latest = info.get("date_latest", "?")
    span = info.get("span_months", "?")
    months_data = info.get("months_with_data", "?")
    months_range = info.get("months_in_range", "?")

    logger.info(
        f"  Reviews:  {total} total | "
        f"{date_earliest} to {date_latest} ({span} months)"
    )

    platforms = info.get("platform_counts", {})
    if platforms:
        parts = [f"{p}: {c}" for p, c in platforms.items()]
        logger.info(f"  Platform: {' | '.join(parts)}")

    coverage = info.get("months_with_data", 0)
    total_months = info.get("months_in_range", 0)
    if total_months:
        logger.info(
            f"  Coverage: {coverage}/{total_months} months have reviews"
        )

    gaps = info.get("gap_months", [])
    if gaps:
        logger.warning(f"  Gaps:     {', '.join(gaps)}")

    for w in report["warnings"]:
        logger.warning(f"  DATA QUALITY: {w}")

    if not report["warnings"]:
        logger.info("  Quality:  All checks passed")
