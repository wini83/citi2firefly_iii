import re
from bank_parser.date_utils import parse_polish_date

date_pattern = re.compile(r"\d{1,2} \w+ \d{4}")
foreign_currency_pattern = re.compile(r"-?\d+,\d{2}[A-Z]{3}")

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
        line = lines[i]
        if date_pattern.fullmatch(line.lower()):
            try:
                raw_date = line
                date = parse_polish_date(raw_date)

                description = lines[i + 1]
                pln_line = lines[i + 3]
                amount = float(
                    pln_line.replace("PLN", "").replace(",", ".").replace(" ", "")
                )

                if not include_positive and amount >= 0:
                    i += 4
                    continue

                currency = "PLN"
                foreign_currency = ""
                foreign_amount = ""

                # Optional foreign currency line
                if i + 4 < len(lines):
                    fc_line_raw = lines[i + 4].replace(" ", "")
                    if foreign_currency_pattern.fullmatch(fc_line_raw):
                        fc_line = fc_line_raw.replace(",", ".")
                        foreign_amount = re.findall(r"\d+\.\d{2}", fc_line)[0]
                        foreign_currency = re.findall(r"[A-Z]{3}", fc_line)[-1]
                        i += 5
                    else:
                        i += 4
                else:
                    i += 4

                transaction = {
                    "date": date,
                    "description": description,
                    "amount": amount,
                    "currency": currency,
                    "foreign_currency": foreign_currency,
                    "foreign_amount": foreign_amount,
                    "opposing_account_name": description
                }

                transactions.append(transaction)

            except (IndexError, ValueError) as e:
                print(f"Skipped malformed transaction at line {i}: {e}")
                i += 1
        else:
            i += 1

    return transactions
