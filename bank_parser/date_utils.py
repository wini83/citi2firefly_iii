from datetime import datetime

MONTHS_PL = {
    "sty": 1, "lut": 2, "mar": 3, "kwi": 4, "maj": 5, "cze": 6,
    "lip": 7, "sie": 8, "wrz": 9, "paź": 10, "paz": 10, "lis": 11, "gru": 12
}

def parse_polish_date(date_str):
    """
    Converts Polish-formatted date (e.g., '16 sty 2025') to ISO format ('2025-01-16').
    """
    try:
        parts = date_str.strip().split()
        if len(parts) != 3:
            return None
        day, month_str, year = parts
        day = int(day)
        month = MONTHS_PL.get(month_str[:3].lower())
        if not month:
            return None
        return datetime(int(year), month, day).strftime("%Y-%m-%d")
    except Exception:
        return None
