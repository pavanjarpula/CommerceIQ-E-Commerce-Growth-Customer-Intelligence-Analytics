"""CommerceIQ - Utilities.

Formatting, date helpers, and export functions.
"""
from pathlib import Path

import pandas as pd


def format_currency(val: float) -> str:
    """Format number as currency."""
    if val >= 1_000_000:
        return f"${val / 1_000_000:,.2f}M"
    elif val >= 1_000:
        return f"${val / 1_000:,.1f}K"
    return f"${val:,.2f}"


def format_number(val: float) -> str:
    """Format large numbers with suffixes."""
    if val >= 1_000_000:
        return f"{val / 1_000_000:,.2f}M"
    elif val >= 1_000:
        return f"{val / 1_000:,.1f}K"
    return f"{val:,.0f}"


def format_pct(val: float) -> str:
    """Format as percentage."""
    return f"{val:.1%}"


def load_processed(name: str) -> pd.DataFrame:
    """Load a processed CSV."""
    from config import DATA_PROCESSED
    return pd.read_csv(DATA_PROCESSED / f"{name}.csv")