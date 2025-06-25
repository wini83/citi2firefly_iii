"""Unit test for the CSV exporter module."""
from bank_parser.csv_exporter import export_to_csv


def test_export_to_csv_creates_file(tmp_path):
    """Test that export_to_csv correctly creates a CSV file with expected contents."""
    transactions = [
        {
            "date": "2025-05-19",
            "description": "Zabka",
            "amount": -12.34,
            "currency": "PLN",
            "foreign_currency": "",
            "foreign_amount": "",
            "opposing_account_name": "Zabka"
        }
    ]

    output_base = tmp_path / "export"
    export_to_csv(transactions, base_filename=str(output_base), chunk_size=1)

    output_files = list(tmp_path.glob("*.csv"))
    assert output_files, "No CSV file was created"

    content = output_files[0].read_text(encoding="utf-8")
    assert (
        "date;description;amount;"
        "currency;foreign_currency;"
        "foreign_amount;opposing_account_name" in content
    )
    assert "2025-05-19;Zabka;-12.34;PLN;;;" in content
