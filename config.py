"""
Configuration loader for Maya Review Analysis Agent.
Reads config.yaml once (cached), with environment variable overrides.
Env pattern: MAYA_SECTION__KEY=value (double underscore separator).
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml

_CONFIG_PATH = Path(__file__).parent / "config.yaml"


@lru_cache(maxsize=1)
def load(config_path: str | None = None) -> dict:
    """Load configuration from YAML file, then apply env var overrides."""
    path = Path(config_path) if config_path else _CONFIG_PATH
    with open(path) as f:
        cfg = yaml.safe_load(f) or {}
    _apply_env_overrides(cfg)
    return cfg


def _coerce(value: str):
    """Coerce string env values to native Python types."""
    if value.lower() in ("true", "yes"):
        return True
    if value.lower() in ("false", "no"):
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _apply_env_overrides(cfg: dict) -> None:
    """Override config values with MAYA_SECTION__KEY environment variables."""
    prefix = "MAYA_"
    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue
        parts = key[len(prefix):].lower().split("__")
        if len(parts) != 2:
            continue
        section, option = parts
        if section not in cfg:
            cfg[section] = {}
        cfg[section][option] = _coerce(value)


def get(section: str, key: str, default=None):
    """Convenience accessor: config.get('scraper', 'gplay_batch_size', 200)."""
    cfg = load()
    return cfg.get(section, {}).get(key, default)


def output_dir() -> Path:
    """Return the configured output directory as a Path."""
    return Path(get("output", "data_dir", "data"))
