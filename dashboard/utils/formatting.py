"""Dashboard - Formatting utilities."""
import locale


def fmt_currency(val, decimals=0):
    if val is None:
        return "$0"
    if abs(val) >= 1_000_000:
        return f"${val/1_000_000:,.{decimals}f}M"
    if abs(val) >= 1_000:
        return f"${val/1_000:,.{decimals}f}K"
    return f"${val:,.{decimals}f}"


def fmt_number(val, decimals=0):
    if val is None:
        return "0"
    if abs(val) >= 1_000_000:
        return f"{val/1_000_000:,.{decimals}f}M"
    if abs(val) >= 1_000:
        return f"{val/1_000:,.{decimals}f}K"
    return f"{val:,.{decimals}f}"


def fmt_pct(val, decimals=1):
    if val is None:
        return "0%"
    return f"{val*100:.{decimals}f}%"


def fmt_delta(val):
    if val is None:
        return None
    sign = "+" if val >= 0 else ""
    return f"{sign}{val*100:.1f}%"