"""Tests for main module CLI helpers."""

import argparse

import pytest

from main import parse_stars, output_suffix


def test_parse_stars_single():
    """Single star rating parsed correctly."""
    assert parse_stars("3") == [3]


def test_parse_stars_multi():
    """Comma-separated values parsed and sorted."""
    assert parse_stars("3,1,2") == [1, 2, 3]


def test_parse_stars_dedup():
    """Duplicate values are removed."""
    assert parse_stars("2,2,3") == [2, 3]


def test_parse_stars_invalid():
    """Out-of-range value raises ArgumentTypeError."""
    with pytest.raises(argparse.ArgumentTypeError):
        parse_stars("0")
    with pytest.raises(argparse.ArgumentTypeError):
        parse_stars("6")


def test_output_suffix_none():
    """No stars returns empty suffix."""
    assert output_suffix(None) == ""
    assert output_suffix([]) == ""


def test_output_suffix_single():
    """Single star returns '_1star'."""
    assert output_suffix([1]) == "_1star"


def test_output_suffix_multi():
    """Multiple stars return sorted suffix."""
    assert output_suffix([3, 1]) == "_1_3star"
