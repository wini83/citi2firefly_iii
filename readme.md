# Citi Handlowy Bank to Firefly III CSV Converter

This Python script converts raw bank statement text copied from a web browser  into a structured `.csv` file ready for import into [Firefly III](https://firefly-iii.org/).

## 🔧 Features

- Detects transactions from pasted/exported bank statement text
- Converts Polish dates (`"19 maj 2025"`) to ISO format (`"2025-05-19"`)
- Filters out positive (credit) transactions if desired
- Extracts foreign currency transactions (e.g. `14,00EUR`)
- Outputs `;`-separated CSV files compatible with Firefly III importer
- Optionally splits output into chunks (e.g. max 60 transactions per file)

## 📝 CSV Output Format

Each generated CSV file contains the following headers:

```csv
date;description;amount;currency;foreign_currency;foreign_amount;opposing_account_name
```

Example:

```csv
2025-05-19;ZABKA POZNAN;-7.50;PLN;;;
2025-05-18;PASIBUS Sw. Marcin;-98.24;PLN;;;
```

## 🚀 Usage

```python
from bank_to_firefly import parse_txt_to_firefly_csv

parse_txt_to_firefly_csv(
    input_file="bank_statement.txt",
    output_file="firefly_import.csv",
    skip_positive=True,
    chunk_size=60  # Optional: split output every 60 transactions
)
```

### Parameters

- `input_file` – path to your `.txt` file with raw bank data (copied from website)
- `output_file` – target CSV filename
- `skip_positive` – if `True`, skips transactions with positive amounts (default: `True`)
- `chunk_size` – if set, splits CSV into multiple parts (`file_1.csv`, `file_2.csv`, ...)

## 💡 Notes

- Make sure the input text is cleaned and copied in full from your banking site.
- Incomplete transactions (e.g. missing lines) will be skipped and logged to console.
- Opposing account name is inferred from the transaction description.

## 📁 Example File Input

```
19 maj 2028
ZABKA Z9999 K.2 POZNAN PL
ZABKA Z9999 K.2 POZNAN PL
-7,50PLN
16 sty 2020
Seabank Hotel Mellieha MT
Seabank Hotel Mellieha MT
-22,84PLN
5,00EUR
```

## 📦 Installation

No package needed. Just clone and run:

```bash

git clone https://github.com/wini83/citi2firefly_iii.git
cd citi2firefly_iii
python3 main.py
```

> You need Python 3.7+ installed.

## 📝 License

MIT License
