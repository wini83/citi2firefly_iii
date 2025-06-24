from bank_parser.date_utils import parse_polish_date

def test_parse_polish_date_valid():
    assert parse_polish_date("19 maj 2025") == "2025-05-19"

def test_parse_polish_date_invalid():
    assert parse_polish_date("niepoprawna data") is None
