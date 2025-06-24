"""Exports parsed transaction data to CSV files compatible with Firefly III."""
import csv

def export_to_csv(transactions, base_filename="output", chunk_size=60):
    """Exports parsed transaction data to CSV files compatible with Firefly III."""
    headers = [
        "Date", "Amount", "Payee", "Description", "Category",
        "Source account", "Destination account", "Tags", "Notes"
    ]
    chunks = [transactions[i:i+chunk_size] for i in range(0, len(transactions), chunk_size)]
    for idx, chunk in enumerate(chunks, 1):
        filename = f"{base_filename}_{idx}.csv" if len(chunks) > 1 else f"{base_filename}.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers, delimiter=";")
            writer.writeheader()
            writer.writerows(chunk)
