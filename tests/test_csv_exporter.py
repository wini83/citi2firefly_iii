from bank_parser.csv_exporter import export_to_csv
from pathlib import Path

def test_export_to_csv_creates_file(tmp_path):
    transactions = [
        {
            "date": "2025-05-19",
            "amount": -12.34,
            "payee": "Zabka",
            "description": "Zabka",
            "category": "",
            "source_account": "Bank",
            "destination_account": "Zabka",
            "tags": "",
            "notes": ""
        }
    ]

    output_base = tmp_path / "export"
    export_to_csv(transactions, output_base, chunk_size=1)

    output_files = list(tmp_path.glob("*.csv"))
    assert output_files, "No CSV file was created"

    content = output_files[0].read_text(encoding="utf-8")
    assert "Date;Amount;Payee" in content
    assert "2025-05-19;-12.34;Zabka" in content
