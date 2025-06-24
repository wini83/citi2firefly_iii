"""Parses lines of text and extracts transaction entries."""
from bank_parser.date_utils import parse_polish_date

def extract_transactions(lines, skip_positive=True):
    """
    Parses raw text lines to extract transaction dictionaries.
    """
    transactions = []
    i = 0
    while i < len(lines) - 3:
        date = parse_polish_date(lines[i].strip())
        if not date:
            i += 1
            continue
        payee = lines[i + 1].strip()
        amount_line = lines[i + 3].strip().replace("PLN", "").replace(",", ".")
        try:
            amount = float(amount_line)
            if skip_positive and amount > 0:
                i += 4
                continue
            transactions.append({
                "Date": date,
                "Amount": f"{amount:.2f}",
                "Payee": payee,
                "Description": payee,
                "Category": "",
                "Source account": "Bank",
                "Destination account": payee,
                "Tags": "",
                "Notes": ""
            })
        except ValueError:
        except ValueError:
            pass
        i += 4
    return transactions
