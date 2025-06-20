"""
Citi Handlowy Transactions to Firefly III CSV Converter

This Python script converts raw bank statement text copied from a web browser  into a structured `.csv` file ready for import into [Firefly III](https://firefly-iii.org/).

Features

- Detects transactions from pasted/exported bank statement text
- Converts Polish dates (`"19 maj 2025"`) to ISO format (`"2025-05-19"`)
- Filters out positive (credit) transactions if desired
- Extracts foreign currency transactions (e.g. `14,00EUR`)
- Outputs `;`-separated CSV files compatible with Firefly III importer
- Optionally splits output into chunks (e.g. max 60 transactions per file)

Usage:
    parse_txt_to_firefly_csv(
        input_file="statement.txt",
        output_file="transactions.csv",
        skip_positive=True,
        chunk_size=60
    )
"""
import csv
import os
import re


MONTHS_PL = {
    "sty": "01", "lut": "02", "mar": "03", "kwi": "04",
    "maj": "05", "cze": "06", "lip": "07", "sie": "08",
    "wrz": "09", "paź": "10", "paz": "10", "lis": "11", "gru": "12"
}

def read_input_file(filename):
    with open(filename, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def parse_date(date_str):
    match = re.match(r"(\d{1,2}) ([a-zA-Ząćęłńóśźż]+) (\d{4})", date_str)
    if not match:
        return None
    day, month_pl, year = match.groups()
    month_pl = (month_pl.lower().
                replace("ą", "a")
                .replace("ć", "c")
                .replace("ę", "e")
                .replace("ł", "l")
                .replace("ń", "n")
                .replace("ó", "o")
                .replace("ś", "s")
                .replace("ź", "z")
                .replace("ż", "z"))
    month = MONTHS_PL.get(month_pl[:3])
    if not month:
        return None
    return f"{year}-{month}-{int(day):02}"

def parse_transactions(lines):
    transactions = []
    i = 0
    while i < len(lines):
        if not parse_date(lines[i]):
            i += 1
            continue

        try:
            date = parse_date(lines[i])
            desc1 = lines[i + 1]
            amount_line = lines[i + 3]
            foreign_amount = ""
            foreign_currency = ""

            if i + 4 < len(lines) and re.match(r"[-+]?[\d,]+[A-Z]{3}", lines[i + 4]):
                foreign_line = lines[i + 4]
                foreign_match = re.match(r"([-+]?\d+[\d,]*)\s*([A-Z]{3})", foreign_line)
                if foreign_match:
                    foreign_amount = foreign_match.group(1).replace(",", ".")
                    foreign_currency = foreign_match.group(2)
                i += 1

            amount_match = re.match(r"([-+]?\d+[\d,]*)PLN", amount_line)
            if amount_match:
                amount = amount_match.group(1).replace(",", ".")
            else:
                i += 1
                continue

            transactions.append({
                "date": date,
                "description": desc1,
                "amount": amount,
                "currency": "PLN",
                "foreign_currency": foreign_currency,
                "foreign_amount": foreign_amount,
                "opposing_account_name": desc1
            })

            i += 4
        except (IndexError, ValueError) as e:
            print(f"Skipped malformed transaction at line {i}: {e}")
            i += 1
    return transactions

def filter_transactions(transactions):
    return [tx for tx in transactions if float(tx["amount"]) < 0]

def split_transactions(transactions, chunk_size):
    return [transactions[i:i + chunk_size] for i in range(0, len(transactions), chunk_size)]

def write_csv_chunks(base_filename, chunks):
    for idx, chunk in enumerate(chunks, 1):
        filename = f"{os.path.splitext(base_filename)[0]}_{idx}.csv" if len(chunks) > 1\
            else base_filename
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "date", "description", "amount", "currency",
                    "foreign_currency", "foreign_amount", "opposing_account_name"
                ],
                delimiter=";"
            )
            writer.writeheader()
            writer.writerows(chunk)
            print(f"Saved chunk {idx} "
                  f"with {len(chunk)} transactions to "
                  f"{filename}")

def parse_txt_to_firefly_csv(input_file, output_file, skip_positive=True, chunk_size=None):
    lines = read_input_file(input_file)
    transactions = parse_transactions(lines)
    if skip_positive:
        transactions = filter_transactions(transactions)
    chunks = split_transactions(transactions, chunk_size) if chunk_size else [transactions]
    write_csv_chunks(output_file, chunks)

parse_txt_to_firefly_csv("statement.txt", "firefly_import.csv", chunk_size=80)
