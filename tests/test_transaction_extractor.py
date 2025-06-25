"""Unit tests for the transaction_extractor module."""

from bank_parser.transaction_extractor import extract_transactions


def test_extract_single_transaction():
    """Test that a single valid transaction is parsed correctly."""
    lines = [
        "19 maj 2025",
        "ZABKA Z123",
        "ZABKA Z123",
        "-12,34PLN"
    ]
    result = extract_transactions(lines)
    assert len(result) == 1
    assert result[0]["amount"] == -12.34
    assert result[0]["date"] == "2025-05-19"


def test_ignore_positive_transactions():
    """Test that positive transactions are skipped when include_positive=False."""
    lines = [
        "20 maj 2025",
        "SOME REFUND",
        "SOME REFUND",
        "25,00PLN"
    ]
    result = extract_transactions(lines, include_positive=False)
    assert not result


def test_extract_transaction_with_foreign_currency():
    """Test that foreign currency and amount are parsed correctly when present."""
    lines = [
        "16 sty 2025",
        "MALTA PUBLIC TRANSPORT LUQA MT",
        "MALTA PUBLIC TRANSPORT LUQA MT",
        "-63,97PLN",
        "14,00EUR"
    ]

    transactions = extract_transactions(lines)
    assert len(transactions) == 1

    t = transactions[0]
    assert t["date"] == "2025-01-16"
    assert t["description"] == "MALTA PUBLIC TRANSPORT LUQA MT"
    assert t["amount"] == -63.97
    assert t["currency"] == "PLN"
    assert t["foreign_currency"] == "EUR"
    assert t["foreign_amount"] == "14.00"
    assert t["opposing_account_name"] == "MALTA PUBLIC TRANSPORT LUQA MT"


def test_extract_transaction_without_foreign_currency():
    """Test that transactions without foreign currency are still parsed correctly."""
    lines = [
        "17 sty 2025",
        "LIDL 28 CZERWCA 1956 Poznan PL",
        "LIDL 28 CZERWCA 1956 Poznan PL",
        "-12,99PLN"
    ]

    transactions = extract_transactions(lines)
    assert len(transactions) == 1

    t = transactions[0]
    assert t["foreign_currency"] == ""
    assert t["foreign_amount"] == ""
