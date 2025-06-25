"""
Module for Extracting transaction data from a list of lines and returns a list of dicts
"""
import re
import click
from bank_parser.date_utils import parse_polish_date

date_pattern = re.compile(r"\d{1,2} \w+ \d{4}")
foreign_currency_pattern = re.compile(r"-?\d+,\d{2}[A-Z]{3}")

def parse_foreign_currency(line: str) -> tuple[str, str] | tuple[None, None]:
    """
    Parses a line containing a foreign currency amount like '14,00EUR'.

    Args:
        line (str): Raw line from the file (may contain spaces or commas)

    Returns:
        (amount_str, currency_str) or (None, None) if not matched
    """
    clean = line.replace(" ", "")
    if foreign_currency_pattern.fullmatch(clean):
        normalized = clean.replace(",", ".")
        amount = re.findall(r"\d+\.\d{2}", normalized)[0]
        currency = re.findall(r"[A-Z]{3}", normalized)[-1]
        return amount, currency
    return None, None

def parse_transaction_block(lines: list[str], i: int, include_positive: bool) \
        -> tuple[dict | None, int]:
    """Parses a single transaction block starting at index i."""
    raw_date = lines[i]
    date = parse_polish_date(raw_date)

    description = lines[i + 1]
    pln_line = lines[i + 3]
    amount = float(pln_line.replace("PLN", "").replace(",", ".").replace(" ", ""))

    if not include_positive and amount >= 0:
        return None, i + 4

    foreign_amount, foreign_currency = "", ""
    if i + 4 < len(lines):
        parsed = parse_foreign_currency(lines[i + 4])
        if parsed != (None, None):
            foreign_amount, foreign_currency = parsed
            i += 5
        else:
            i += 4
    else:
        i += 4

    transaction = {
        "date": date,
        "description": description,
        "amount": amount,
        "currency": "PLN",
        "foreign_currency": foreign_currency,
        "foreign_amount": foreign_amount,
        "opposing_account_name": description
    }

    return transaction, i


def extract_transactions(lines, include_positive=False):
    """
        Extracts transaction data from a list of lines and returns a list of dicts.

        Each transaction is expected to follow this structure:
            - date
            - description (duplicated line)
            - PLN amount (line 4)
            - [optional] foreign amount with currency (line 5)

        Args:
            lines (list[str]): List of text lines from the source file.
            include_positive (bool): Whether to include positive-value transactions.

        Returns:
            list[dict]: Parsed transaction dictionaries for Firefly III export.
        """
    transactions = []
    i = 0
    while i < len(lines):
        if date_pattern.fullmatch(lines[i].lower()):
            try:
                transaction, next_i = parse_transaction_block(lines, i, include_positive)
                if transaction:
                    transactions.append(transaction)
                i = next_i
            except (IndexError, ValueError) as e:
                click.echo(f"⚠️ Skipped malformed transaction at line {i}: {e}")
                i += 1
        else:
            i += 1

    return transactions
