"""Tests for config module."""

import os
from pathlib import Path

import pytest

import config


@pytest.fixture(autouse=True)
def _clear_config_cache():
    """Ensure each test starts with a fresh config cache."""
    config.load.cache_clear()
    yield
    config.load.cache_clear()


def test_load_yaml():
    """Config loads and contains expected top-level sections."""
    cfg = config.load()
    for section in ("scraper", "llm", "data_quality", "temporal", "comprehensive",
                    "competitor", "journey", "visualizations", "logging", "output"):
        assert section in cfg, f"Missing section: {section}"


def test_get_returns_default():
    """Missing key returns the supplied default."""
    assert config.get("nonexistent_section", "no_key", 42) == 42
    assert config.get("scraper", "nonexistent_key", "fallback") == "fallback"


def test_env_override(monkeypatch):
    """MAYA_SECTION__KEY env vars override YAML values."""
    monkeypatch.setenv("MAYA_SCRAPER__GPLAY_BATCH_SIZE", "100")
    cfg = config.load()
    assert cfg["scraper"]["gplay_batch_size"] == 100


def test_coerce_types(monkeypatch):
    """Env var strings are coerced to bool, int, float."""
    monkeypatch.setenv("MAYA_SCRAPER__GPLAY_BATCH_SIZE", "42")
    monkeypatch.setenv("MAYA_LLM__GEMINI_BASE_DELAY_SECONDS", "30.5")
    monkeypatch.setenv("MAYA_OUTPUT__ENABLED", "true")
    cfg = config.load()
    assert cfg["scraper"]["gplay_batch_size"] == 42
    assert cfg["llm"]["gemini_base_delay_seconds"] == 30.5
    assert cfg["output"]["enabled"] is True
