"""Tests for scraper module (pure helper functions)."""

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest

import scraper


def test_combine_and_clean_drops_empty(tmp_path):
    """Empty text rows are removed."""
    df1 = pd.DataFrame({
        "date": [datetime.now()],
        "rating": [5],
        "text": ["Great app"],
        "platform": ["Android"],
    })
    df2 = pd.DataFrame({
        "date": [datetime.now()],
        "rating": [1],
        "text": [""],
        "platform": ["iOS"],
    })
    result = scraper._combine_and_clean([df1, df2], tmp_path / "out.csv")
    assert len(result) == 1
    assert result.iloc[0]["text"] == "Great app"


def test_combine_and_clean_sorts_by_date(tmp_path):
    """Output is sorted by date descending."""
    now = datetime.now()
    df = pd.DataFrame({
        "date": [now - timedelta(days=5), now, now - timedelta(days=2)],
        "rating": [3, 4, 5],
        "text": ["old", "new", "mid"],
        "platform": ["Android"] * 3,
    })
    result = scraper._combine_and_clean([df], tmp_path / "out.csv")
    assert result.iloc[0]["text"] == "new"
    assert result.iloc[-1]["text"] == "old"


def test_combine_and_clean_concat(tmp_path):
    """Multiple DataFrames are concatenated."""
    df1 = pd.DataFrame({
        "date": [datetime.now()],
        "rating": [5],
        "text": ["A"],
        "platform": ["Android"],
    })
    df2 = pd.DataFrame({
        "date": [datetime.now()],
        "rating": [4],
        "text": ["B"],
        "platform": ["iOS"],
    })
    result = scraper._combine_and_clean([df1, df2], tmp_path / "out.csv")
    assert len(result) == 2
    assert (tmp_path / "out.csv").exists()
