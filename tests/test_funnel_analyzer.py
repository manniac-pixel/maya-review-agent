"""Tests for funnel_analyzer module — regex pattern matching."""

import pandas as pd
import pytest

import funnel_analyzer


class TestRetryPatterns:
    """Verify RETRY_PATTERNS match expected review text."""

    def test_tried_n_times(self):
        text = "I tried 5 times to login but it keeps failing"
        assert any(p.search(text) for p in funnel_analyzer.RETRY_PATTERNS)

    def test_attempted_times(self):
        text = "attempted 3 times to verify my ID"
        assert any(p.search(text) for p in funnel_analyzer.RETRY_PATTERNS)

    def test_keeps_failing(self):
        text = "the app keeps failing when I try to send money"
        assert any(p.search(text) for p in funnel_analyzer.RETRY_PATTERNS)

    def test_always_crashes(self):
        text = "it always crashes during KYC verification"
        assert any(p.search(text) for p in funnel_analyzer.RETRY_PATTERNS)

    def test_every_time(self):
        text = "every time I try to open the app it shows error"
        assert any(p.search(text) for p in funnel_analyzer.RETRY_PATTERNS)

    def test_retry_keyword(self):
        text = "had to retry the OTP multiple times"
        assert any(p.search(text) for p in funnel_analyzer.RETRY_PATTERNS)

    def test_no_retry_signal(self):
        text = "great app, love the savings feature"
        assert not any(p.search(text) for p in funnel_analyzer.RETRY_PATTERNS)

    def test_still_getting_error(self):
        text = "I still keep getting error when sending money"
        assert any(p.search(text) for p in funnel_analyzer.RETRY_PATTERNS)


class TestAbandonmentPatterns:
    """Verify ABANDONMENT_PATTERNS match expected review text."""

    def test_gave_up(self):
        text = "I gave up trying to register, too many errors"
        assert any(p.search(text) for p in funnel_analyzer.ABANDONMENT_PATTERNS)

    def test_switched_to_gcash(self):
        text = "switched to GCash because Maya keeps crashing"
        assert any(p.search(text) for p in funnel_analyzer.ABANDONMENT_PATTERNS)

    def test_uninstalled(self):
        text = "uninstalled this useless app"
        assert any(p.search(text) for p in funnel_analyzer.ABANDONMENT_PATTERNS)

    def test_deleted_app(self):
        text = "deleted the app after days of frustration"
        assert any(p.search(text) for p in funnel_analyzer.ABANDONMENT_PATTERNS)

    def test_will_use_instead(self):
        text = "will use GCash instead, much more reliable"
        assert any(p.search(text) for p in funnel_analyzer.ABANDONMENT_PATTERNS)

    def test_no_longer_using(self):
        text = "I no longer use this app"
        assert any(p.search(text) for p in funnel_analyzer.ABANDONMENT_PATTERNS)

    def test_no_abandonment_signal(self):
        text = "easy to borrow money, love this app"
        assert not any(p.search(text) for p in funnel_analyzer.ABANDONMENT_PATTERNS)


class TestMultiStepPatterns:
    """Verify MULTI_STEP_PATTERNS match expected review text."""

    def test_step_sequence(self):
        text = "I entered my phone number then typed the OTP but then the app froze"
        assert any(p.search(text) for p in funnel_analyzer.MULTI_STEP_PATTERNS)

    def test_during_action(self):
        text = "during the KYC selfie capture the camera stopped working"
        assert any(p.search(text) for p in funnel_analyzer.MULTI_STEP_PATTERNS)

    def test_no_multi_step(self):
        text = "app is slow"
        assert not any(p.search(text) for p in funnel_analyzer.MULTI_STEP_PATTERNS)


class TestExtractSignals:
    """Test the _extract_signals function."""

    def test_empty_df(self):
        df = pd.DataFrame(columns=["date", "rating", "text", "platform"])
        result = funnel_analyzer._extract_signals(df)
        assert result.empty

    def test_extracts_retry(self):
        df = pd.DataFrame([{
            "date": "2025-01-01",
            "rating": 1,
            "text": "tried 3 times to login, keeps failing",
            "platform": "Android",
        }])
        result = funnel_analyzer._extract_signals(df)
        assert len(result) == 1
        assert result.iloc[0]["has_retry"] == True

    def test_extracts_abandonment(self):
        df = pd.DataFrame([{
            "date": "2025-01-01",
            "rating": 1,
            "text": "gave up and uninstalled the app",
            "platform": "iOS",
        }])
        result = funnel_analyzer._extract_signals(df)
        assert len(result) == 1
        assert result.iloc[0]["has_abandonment"] == True

    def test_skips_positive_reviews(self):
        df = pd.DataFrame([{
            "date": "2025-01-01",
            "rating": 5,
            "text": "great app for sending money",
            "platform": "Android",
        }])
        result = funnel_analyzer._extract_signals(df)
        assert result.empty

    def test_multiple_signals(self):
        df = pd.DataFrame([{
            "date": "2025-01-01",
            "rating": 1,
            "text": "tried 5 times, gave up and switched to GCash",
            "platform": "Android",
        }])
        result = funnel_analyzer._extract_signals(df)
        assert len(result) == 1
        assert result.iloc[0]["has_retry"] == True
        assert result.iloc[0]["has_abandonment"] == True
