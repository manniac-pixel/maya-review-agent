"""Shared fixtures for Maya agent tests."""

import sys
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import pytest

# Ensure project root is on sys.path so imports work.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture()
def sample_reviews_df():
    """A 50-row DataFrame resembling scraped reviews."""
    now = datetime.now()
    rows = []
    for i in range(50):
        rows.append({
            "date": now - timedelta(days=i * 3),
            "rating": (i % 5) + 1,
            "text": f"Sample review text number {i} about the app experience.",
            "app_version": f"4.{i // 10}.0",
            "platform": "Android" if i % 2 == 0 else "iOS",
        })
    return pd.DataFrame(rows)


@pytest.fixture()
def empty_df():
    """An empty DataFrame with the expected columns."""
    return pd.DataFrame(columns=["date", "rating", "text", "app_version", "platform"])


@pytest.fixture()
def sample_insights():
    """A minimal insights dict for journey mapping tests."""
    return {
        "ranked_ux_opportunities": [
            {
                "theme": "Login failures",
                "affected_journey": "onboarding",
                "severity": 4,
                "frequency": "high",
                "user_quotes": ["Cannot login at all"],
            },
            {
                "theme": "Slow transfers",
                "affected_journey": "transfers",
                "severity": 3,
                "frequency": "medium",
                "user_quotes": ["Transfer took 3 days"],
            },
        ],
    }
