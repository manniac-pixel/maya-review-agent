"""Tests for journey_mapping module."""

import pytest

import journey_mapping


def test_normalize_journey_direct():
    """Canonical names pass through."""
    assert journey_mapping._normalize_journey("payments") == "payments"
    assert journey_mapping._normalize_journey("onboarding") == "onboarding"


def test_normalize_journey_alias():
    """Known aliases resolve to canonical names."""
    assert journey_mapping._normalize_journey("registration") == "onboarding"
    assert journey_mapping._normalize_journey("send") == "transfers"
    assert journey_mapping._normalize_journey("loan") == "credit"
    assert journey_mapping._normalize_journey("customer support") == "support"


def test_normalize_journey_unknown():
    """Unknown strings fall back to 'general'."""
    assert journey_mapping._normalize_journey("random_thing") == "general"


def test_normalize_journey_empty():
    """Empty / None input returns 'general'."""
    assert journey_mapping._normalize_journey("") == "general"
    assert journey_mapping._normalize_journey(None) == "general"


def test_score_journey():
    """Friction score = sum of severity * freq_weight * trend_weight."""
    points = [
        {"severity": 4, "frequency": "high", "trend": "persistent"},
        {"severity": 2, "frequency": "low", "trend": "resolved"},
    ]
    score = journey_mapping._score_journey(points)
    # 4 * 3 * 1.2 + 2 * 1 * 0.3 = 14.4 + 0.6 = 15.0
    assert score == 15.0


def test_group_by_journey():
    """Pain points are grouped by their journey field."""
    points = [
        {"journey": "payments", "theme": "A"},
        {"journey": "payments", "theme": "B"},
        {"journey": "onboarding", "theme": "C"},
    ]
    grouped = journey_mapping._group_by_journey(points)
    assert len(grouped["payments"]) == 2
    assert len(grouped["onboarding"]) == 1


def test_collect_pain_points_dedup(sample_insights):
    """Duplicate themes are deduplicated."""
    # Provide the same theme in both insights and comprehensive
    comprehensive = {
        "analysis": {
            "critical_pain_points": [
                {
                    "theme": "Login failures",
                    "affected_journey": "onboarding",
                    "severity": 4,
                    "frequency": "high",
                },
            ],
        },
    }
    temporal = {"trends": {}}
    points = journey_mapping._collect_pain_points(sample_insights, comprehensive, temporal)
    themes = [p["theme"] for p in points]
    assert themes.count("Login failures") == 1


def test_collect_pain_points_from_temporal(sample_insights):
    """Temporal trends are collected with correct lifecycle tags."""
    temporal = {
        "trends": {
            "persistent_issues": [
                {"theme": "Crashes", "severity": 3, "frequency": "medium"},
            ],
            "emerging_issues": [
                {"theme": "New bug", "severity": 4},
            ],
        },
    }
    points = journey_mapping._collect_pain_points(sample_insights, {"analysis": {}}, temporal)
    trend_tags = {p["theme"]: p["trend"] for p in points}
    assert trend_tags.get("Crashes") == "persistent"
    assert trend_tags.get("New bug") == "emerging"
