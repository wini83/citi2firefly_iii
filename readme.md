# 🏦 Citi Handlowy Bank → Firefly III CSV Converter (CLI Edition)

[![Python application](https://github.com/wini83/citi2firefly_iii/actions/workflows/python-app.yml/badge.svg)](https://github.com/wini83/citi2firefly_iii/actions/workflows/python-app.yml)
[![Pylint](https://github.com/wini83/citi2firefly_iii/actions/workflows/pylint.yml/badge.svg)](https://github.com/wini83/citi2firefly_iii/actions/workflows/pylint.yml)
[![CodeQL Advanced](https://github.com/wini83/citi2firefly_iii/actions/workflows/codeql.yml/badge.svg)](https://github.com/wini83/citi2firefly_iii/actions/workflows/codeql.yml)

This Python CLI tool converts raw text exports from bank statements into `.csv` files compatible with [Firefly III](https://firefly-iii.org/).

## 🔧 Features

- Parses raw statement data (copied from website)
- Converts Polish dates (e.g. `"19 maj 2025"`) to ISO format (`"2025-05-19"`)
- Filters out positive (credit) transactions by default
- Optionally splits output into chunks (e.g. max 60 transactions per file)
- Fully CLI-based using [`click`](https://palletsprojects.com/p/click/)
- Easily testable using `pytest`

## 🚀 CLI Usage

```bash
python main.py --input sample_data/example_input.txt --output transactions --chunk-size 60
```

### 🔁 Parameters

| Flag                | Description                                        |
|---------------------|----------------------------------------------------|
| `--input`, `-i`     | Path to the input `.txt` file (required)          |
| `--output`, `-o`    | Output base filename (default: `output`)          |
| `--chunk-size`      | Number of transactions per file (default: `60`)   |
| `--include-positive`| Include positive amounts (disabled by default)    |

## 📄 Example Input

```text
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

## 📤 Output Format

Each `.csv` file contains the following columns:

```csv
Date;Amount;Payee;Description;Category;Source account;Destination account;Tags;Notes
```

Example:

```csv
2025-05-19;-7.50;ZABKA POZNAN;ZABKA POZNAN;;;Bank;ZABKA POZNAN;;
```

## 📁 Project Structure

```
bank_parser_project/
├── main.py
├── parser/
│   ├── __init__.py
│   ├── date_utils.py
│   ├── transaction_extractor.py
│   └── csv_exporter.py
├── tests/
│   ├── __init__.py
│   └── test_cli.py
├── sample_data/
│   └── example_input.txt
└── requirements.txt
```

## 🧪 Running Tests

```bash
pip install -r requirements.txt
pytest
```

Tests are implemented with `click.testing.CliRunner` to validate end-to-end usage.

## 📦 Installation

No installation required. Just clone and run:

```bash
git clone https://github.com/YOUR_USERNAME/citi2firefly_iii.git
cd citi2firefly_iii
python main.py --input your_file.txt
```

> Requires Python 3.7+

## 📄 License

MIT License
