"""Tests for competitor_analysis module (pure helper functions)."""

from datetime import datetime

import pandas as pd
import pytest

import competitor_analysis


def _make_reviews(n=200):
    """Create a DataFrame with a mix of ratings."""
    return pd.DataFrame({
        "date": [datetime.now()] * n,
        "rating": [(i % 5) + 1 for i in range(n)],
        "text": [f"review {i}" for i in range(n)],
        "platform": ["Android" if i % 2 == 0 else "iOS" for i in range(n)],
    })


def test_sample_reviews_stratified():
    """Sampled output preserves rating diversity."""
    df = _make_reviews(200)
    sampled = competitor_analysis._sample_reviews(df, n=50)
    assert len(sampled) <= 50
    # All 5 rating values should be represented
    assert sampled["rating"].nunique() == 5


def test_format_reviews():
    """Output format includes star markers and platform."""
    df = pd.DataFrame({
        "date": [datetime(2024, 6, 1)],
        "rating": [4],
        "text": ["Good app"],
        "platform": ["Android"],
    })
    result = competitor_analysis._format_reviews(df)
    assert "[****]" in result
    assert "Good app" in result
