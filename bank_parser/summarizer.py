"""Module for summarizing exported CSV transactions (file count, date range, etc.)."""
import glob
import csv
from datetime import datetime
import click

def summarize_exports(base_filename: str):
    """Prints summary of CSV files exported: count, date range, file size."""
    csv_files = sorted(glob.glob(f"{base_filename}*.csv"))
    click.echo(f"\n📁 Total files exported: {len(csv_files)}")

    for file in csv_files:
        try:
            with open(file, encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                dates = [row["date"] for row in reader if "date" in row]

            parsed_dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
            min_date = min(parsed_dates).strftime("%Y-%m-%d")
            max_date = max(parsed_dates).strftime("%Y-%m-%d")

            click.echo(f"✔ '{file}': {len(dates)} transactions "
                       f"({min_date} to {max_date})")

        except (OSError, ValueError, KeyError) as e:
            click.echo(f"⚠️ Could not summarize '{file}': {e}")

@click.command()
@click.argument("base_filename")
def cli(base_filename):
    """CLI entry point for summarizing CSV exports."""
    summarize_exports(base_filename)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
