"""CLI tool to convert raw bank exports to Firefly III-compatible CSV files."""
import glob
import click

from bank_parser.summarizer import summarize_exports
from bank_parser.transaction_extractor import extract_transactions
from bank_parser.csv_exporter import export_to_csv


@click.command()
@click.option('--input', '-i', 'input_path', required=True, type=click.Path(exists=True),
              help='Path to input .txt file with raw bank data.')
@click.option('--output', '-o', 'output_name', default="output",
              help='Base name for output CSV file (without extension).')
@click.option('--include-positive', is_flag=True, default=False,
              help='Include transactions with positive amounts.')
@click.option('--chunk-size', default=None, type=int,
              help='Max number of transactions per CSV file.')
def run_parser(input_path, output_name, include_positive, chunk_size):
    """
    CLI tool to parse bank transaction logs and export to Firefly III-compatible CSV.
    """
    click.echo(f"📥 Reading: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    click.echo("🔍 Parsing transactions...")
    transactions = extract_transactions(lines, include_positive=include_positive)
    if not transactions:
        click.echo("⚠️ No valid transactions found.")
        return
    click.echo(f"💾 Exporting {len(transactions)} transactions to CSV...")
    export_to_csv(transactions, base_filename=output_name, chunk_size=chunk_size)
    click.echo("✅ Done!")
    summarize_exports(output_name)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run_parser()
