"""Tests for data_quality module."""

from datetime import datetime, timedelta

import pandas as pd
import pytest

import data_quality


def test_check_reviews_exist_empty(empty_df):
    """Empty DataFrame fails the existence check."""
    report = data_quality.run(empty_df)
    assert report["passed"] is False
    assert any("empty" in w.lower() for w in report["warnings"])


def test_check_reviews_exist_none():
    """None input fails gracefully."""
    report = data_quality.run(None)
    assert report["passed"] is False


def test_check_columns_missing():
    """Missing required columns are reported."""
    df = pd.DataFrame({"text": ["hello"], "rating": [5]})
    report = {"passed": True, "warnings": [], "info": {}}
    data_quality._check_columns(df, report)
    assert report["passed"] is False
    assert any("Missing required columns" in w for w in report["warnings"])


def test_check_date_range_stale():
    """Reviews older than stale_days trigger a warning."""
    old_date = datetime.now() - timedelta(days=100)
    df = pd.DataFrame({
        "date": [old_date] * 5,
        "rating": [3] * 5,
        "text": ["review"] * 5,
        "platform": ["Android"] * 5,
    })
    report = {"passed": True, "warnings": [], "info": {}}
    data_quality._check_date_range(df, report)
    assert any("stale" in w.lower() for w in report["warnings"])


def test_check_monthly_gaps():
    """Months with zero reviews are flagged."""
    dates = [datetime(2024, 1, 15), datetime(2024, 3, 15)]
    df = pd.DataFrame({
        "date": dates,
        "rating": [4, 3],
        "text": ["good", "ok"],
        "platform": ["Android", "iOS"],
    })
    report = {"passed": True, "warnings": [], "info": {}}
    data_quality._check_monthly_gaps(df, report)
    assert "gap_months" in report["info"]


def test_check_sample_size_small():
    """Small sample triggers a warning."""
    df = pd.DataFrame({
        "date": [datetime.now()] * 5,
        "rating": [3] * 5,
        "text": ["text"] * 5,
        "platform": ["Android"] * 5,
    })
    report = {"passed": True, "warnings": [], "info": {}}
    data_quality._check_sample_size(df, report)
    assert any("Only 5 reviews total" in w for w in report["warnings"])


def test_check_sample_size_per_platform():
    """Per-platform sample below threshold triggers a warning."""
    df = pd.DataFrame({
        "date": [datetime.now()] * 40,
        "rating": [4] * 40,
        "text": ["text"] * 40,
        "platform": ["Android"] * 35 + ["iOS"] * 5,
    })
    report = {"passed": True, "warnings": [], "info": {}}
    data_quality._check_sample_size(df, report)
    assert any("iOS" in w for w in report["warnings"])


def test_run_passes_good_data(sample_reviews_df):
    """A healthy DataFrame passes all checks."""
    report = data_quality.run(sample_reviews_df)
    assert report["passed"] is True


def test_run_warns_empty_text():
    """Rows with empty text are flagged."""
    df = pd.DataFrame({
        "date": [datetime.now()] * 35,
        "rating": [4] * 35,
        "text": ["good"] * 30 + [""] * 5,
        "platform": ["Android"] * 35,
    })
    report = data_quality.run(df)
    assert any("empty" in w.lower() for w in report["warnings"])
