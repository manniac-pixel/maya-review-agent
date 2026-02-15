"""Tests for accessibility_analyzer module — regex pattern matching."""

import pandas as pd
import pytest

import accessibility_analyzer


class TestDevicePatterns:
    """Verify DEVICE_PATTERNS match expected device mentions."""

    def test_samsung(self):
        text = "crashes on my Samsung Galaxy S21"
        assert any(p.search(text) for p in accessibility_analyzer.DEVICE_PATTERNS)

    def test_xiaomi(self):
        text = "not working on Xiaomi phone"
        assert any(p.search(text) for p in accessibility_analyzer.DEVICE_PATTERNS)

    def test_oppo(self):
        text = "app freezes on my OPPO device"
        assert any(p.search(text) for p in accessibility_analyzer.DEVICE_PATTERNS)

    def test_vivo(self):
        text = "using Vivo and the camera doesn't work"
        assert any(p.search(text) for p in accessibility_analyzer.DEVICE_PATTERNS)

    def test_iphone(self):
        text = "works fine on my iPhone 13"
        assert any(p.search(text) for p in accessibility_analyzer.DEVICE_PATTERNS)

    def test_old_phone(self):
        text = "I have an old phone and the app is very slow"
        assert any(p.search(text) for p in accessibility_analyzer.DEVICE_PATTERNS)

    def test_cherry_mobile(self):
        text = "using Cherry Mobile, app keeps crashing"
        assert any(p.search(text) for p in accessibility_analyzer.DEVICE_PATTERNS)

    def test_android_version(self):
        text = "doesn't work on Android 10"
        assert any(p.search(text) for p in accessibility_analyzer.DEVICE_PATTERNS)

    def test_no_device(self):
        text = "the app is great for sending money"
        assert not any(p.search(text) for p in accessibility_analyzer.DEVICE_PATTERNS)


class TestConnectivityPatterns:
    """Verify CONNECTIVITY_PATTERNS match connectivity issues."""

    def test_slow_internet(self):
        text = "can't load with slow internet in province"
        assert any(p.search(text) for p in accessibility_analyzer.CONNECTIVITY_PATTERNS)

    def test_no_signal(self):
        text = "no signal in our area, app won't work"
        assert any(p.search(text) for p in accessibility_analyzer.CONNECTIVITY_PATTERNS)

    def test_province(self):
        text = "I'm in the province and the app is useless"
        assert any(p.search(text) for p in accessibility_analyzer.CONNECTIVITY_PATTERNS)

    def test_timeout(self):
        text = "the transfer keeps timing out"
        assert any(p.search(text) for p in accessibility_analyzer.CONNECTIVITY_PATTERNS)

    def test_mobile_data(self):
        text = "using mobile data only, app uses too much"
        assert any(p.search(text) for p in accessibility_analyzer.CONNECTIVITY_PATTERNS)

    def test_no_connectivity(self):
        text = "love the crypto feature"
        assert not any(p.search(text) for p in accessibility_analyzer.CONNECTIVITY_PATTERNS)


class TestAccessibilityPatterns:
    """Verify ACCESSIBILITY_PATTERNS match accessibility concerns."""

    def test_cant_read(self):
        text = "can't read the text, too small"
        assert any(p.search(text) for p in accessibility_analyzer.ACCESSIBILITY_PATTERNS)

    def test_tagalog(self):
        text = "please add Tagalog language option"
        assert any(p.search(text) for p in accessibility_analyzer.ACCESSIBILITY_PATTERNS)

    def test_senior(self):
        text = "my lola can't figure out how to use this"
        assert any(p.search(text) for p in accessibility_analyzer.ACCESSIBILITY_PATTERNS)

    def test_confusing(self):
        text = "the interface is very confusing"
        assert any(p.search(text) for p in accessibility_analyzer.ACCESSIBILITY_PATTERNS)

    def test_font_size(self):
        text = "need bigger font size for elderly users"
        assert any(p.search(text) for p in accessibility_analyzer.ACCESSIBILITY_PATTERNS)

    def test_dark_mode(self):
        text = "please add dark mode"
        assert any(p.search(text) for p in accessibility_analyzer.ACCESSIBILITY_PATTERNS)


class TestEdgeCasePatterns:
    """Verify EDGE_CASE_PATTERNS match edge-case scenarios."""

    def test_phone_stolen(self):
        text = "my phone was stolen and I can't recover my account"
        assert any(p.search(text) for p in accessibility_analyzer.EDGE_CASE_PATTERNS)

    def test_changed_sim(self):
        text = "changed my SIM card and now can't login"
        assert any(p.search(text) for p in accessibility_analyzer.EDGE_CASE_PATTERNS)

    def test_ofw(self):
        text = "I'm an OFW in Dubai and can't verify my account"
        assert any(p.search(text) for p in accessibility_analyzer.EDGE_CASE_PATTERNS)

    def test_overseas(self):
        text = "overseas and the app doesn't work outside Philippines"
        assert any(p.search(text) for p in accessibility_analyzer.EDGE_CASE_PATTERNS)

    def test_new_phone(self):
        text = "got a new phone, can't transfer my account"
        assert any(p.search(text) for p in accessibility_analyzer.EDGE_CASE_PATTERNS)

    def test_no_edge_case(self):
        text = "quick and easy loan approval, love it"
        assert not any(p.search(text) for p in accessibility_analyzer.EDGE_CASE_PATTERNS)


class TestExtractSignals:
    """Test the _extract_signals function."""

    def test_empty_df(self):
        df = pd.DataFrame(columns=["date", "rating", "text", "platform"])
        result_df, device_mentions = accessibility_analyzer._extract_signals(df)
        assert result_df.empty
        assert device_mentions == {}

    def test_extracts_device(self):
        df = pd.DataFrame([{
            "date": "2025-01-01",
            "rating": 1,
            "text": "crashes on my Samsung phone every time",
            "platform": "Android",
        }])
        result_df, device_mentions = accessibility_analyzer._extract_signals(df)
        assert len(result_df) == 1
        assert result_df.iloc[0]["has_device"] == True
        assert "samsung" in device_mentions

    def test_extracts_connectivity(self):
        df = pd.DataFrame([{
            "date": "2025-01-01",
            "rating": 2,
            "text": "slow internet makes the app unusable in province",
            "platform": "Android",
        }])
        result_df, _ = accessibility_analyzer._extract_signals(df)
        assert len(result_df) == 1
        assert result_df.iloc[0]["has_connectivity"] == True

    def test_extracts_edge_case(self):
        df = pd.DataFrame([{
            "date": "2025-01-01",
            "rating": 1,
            "text": "I'm an OFW abroad and can't verify my identity",
            "platform": "iOS",
        }])
        result_df, _ = accessibility_analyzer._extract_signals(df)
        assert len(result_df) == 1
        assert result_df.iloc[0]["has_edge_case"] == True

    def test_skips_no_signals(self):
        df = pd.DataFrame([{
            "date": "2025-01-01",
            "rating": 5,
            "text": "love the app",
            "platform": "Android",
        }])
        result_df, _ = accessibility_analyzer._extract_signals(df)
        assert result_df.empty

    def test_multiple_signals(self):
        df = pd.DataFrame([{
            "date": "2025-01-01",
            "rating": 1,
            "text": "on my old Xiaomi phone with slow internet in the province, can't read the small text",
            "platform": "Android",
        }])
        result_df, _ = accessibility_analyzer._extract_signals(df)
        assert len(result_df) == 1
        assert result_df.iloc[0]["has_device"] == True
        assert result_df.iloc[0]["has_connectivity"] == True
        assert result_df.iloc[0]["has_accessibility"] == True
