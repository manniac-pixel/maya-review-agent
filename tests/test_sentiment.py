"""Tests for sentiment module (TextBlob fallback functions)."""

import pytest

import sentiment


def test_detect_themes_login():
    """Login-related keywords map to the Login theme."""
    themes = sentiment._detect_themes("I can't login to my account")
    assert "Login/Authentication Issues" in themes


def test_detect_themes_multiple():
    """Multiple themes detected in one review."""
    text = "App crashes when I try to send money"
    themes = sentiment._detect_themes(text)
    assert "App Crashes/Performance" in themes
    assert "Transfer Problems" in themes


def test_detect_themes_no_match():
    """Generic text matches no themes."""
    themes = sentiment._detect_themes("Great weather today")
    assert themes == []


def test_detect_competitors():
    """Competitor names are detected case-insensitively."""
    comps = sentiment._detect_competitors("GCash is better than this app")
    assert "gcash" in comps


def test_detect_competitors_none():
    """No competitor keywords returns empty list."""
    assert sentiment._detect_competitors("good app") == []


def test_sentiment_positive():
    """Positive text returns positive polarity."""
    pol = sentiment._sentiment("This app is excellent and wonderful")
    assert pol > 0


def test_sentiment_negative():
    """Negative text returns negative polarity."""
    pol = sentiment._sentiment("This is terrible and awful")
    assert pol < 0


def test_freq_label():
    """Frequency labels map correctly from ratios."""
    assert sentiment._freq_label(20, 100) == "high"
    assert sentiment._freq_label(8, 100) == "medium"
    assert sentiment._freq_label(2, 100) == "low"


def test_severity_from_polarity():
    """Polarity-to-severity mapping covers range."""
    assert sentiment._severity_from_polarity(-0.5) == 5
    assert sentiment._severity_from_polarity(-0.3) == 4
    assert sentiment._severity_from_polarity(-0.1) == 3
    assert sentiment._severity_from_polarity(0.05) == 2
    assert sentiment._severity_from_polarity(0.5) == 1


def test_pick_quotes():
    """Longest quotes are picked, short ones skipped."""
    texts = [
        "short",
        "This is a longer quote that should be selected because it is informative",
        "Another medium-length quote for testing purposes here",
    ]
    picked = sentiment._pick_quotes(texts, n=1)
    assert len(picked) == 1
    assert "longer quote" in picked[0]
