import os
from click.testing import CliRunner
from main import run_parser
from pathlib import Path

def test_cli_with_sample_data(tmp_path):
    # Absolute path to the sample input file
    project_root = Path(__file__).resolve().parent.parent
    input_file = project_root / "sample_data" / "example_input.txt"
    assert input_file.exists(), f"Missing sample input file at {input_file}"

    # Output path
    output_base = tmp_path / "test_output"

    runner = CliRunner()
    result = runner.invoke(run_parser, [
        "--input", str(input_file),
        "--output", str(output_base),
        "--chunk-size", "2"
    ])

    assert result.exit_code == 0, result.output
    assert "Exporting" in result.output

    csv_files = list(tmp_path.glob("*.csv")) + list(tmp_path.glob("*.csv"))
    assert csv_files, "No CSV files were created"

    content = csv_files[0].read_text(encoding="utf-8")
    assert "Date;Amount;Payee" in content
