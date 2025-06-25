"""Unit tests for the date_utils module."""

from bank_parser.date_utils import parse_polish_date


def test_parse_polish_date_valid():
    """Test parsing a correct Polish date string."""
    assert parse_polish_date("19 maj 2025") == "2025-05-19"


def test_parse_polish_date_invalid():
    """Test parsing an invalid date string returns None."""
    assert parse_polish_date("niepoprawna data") is None
