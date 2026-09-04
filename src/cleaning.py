"""CommerceIQ - Data Cleaning.

Type casting, null handling, and export to processed data.
"""
from pathlib import Path

import pandas as pd

from config import DATA_RAW, DATA_PROCESSED


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Clean orders table."""
    df = df.copy()
    df["order_ts"] = pd.to_datetime(df["order_ts"])
    df["order_date"] = df["order_ts"].dt.date
    df["order_month"] = df["order_ts"].dt.to_period("M").astype(str)
    return df


def clean_order_items(df: pd.DataFrame) -> pd.DataFrame:
    """Clean order_items table."""
    df = df.copy()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["line_total"] = df["quantity"] * df["unit_price"]
    return df


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """Clean products table."""
    df = df.copy()
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce")
    df["margin_pct"] = ((df["unit_price"] - df["unit_cost"]) / df["unit_price"]).round(4)
    return df


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Clean customers table."""
    df = df.copy()
    df["signup_date"] = pd.to_datetime(df["signup_date"]).dt.date
    return df


def clean_events(df: pd.DataFrame) -> pd.DataFrame:
    """Clean events table."""
    df = df.copy()
    df["event_ts"] = pd.to_datetime(df["event_ts"])
    return df


CLEANERS = {
    "orders": clean_orders,
    "order_items": clean_order_items,
    "products": clean_products,
    "customers": clean_customers,
    "events": clean_events,
}


def run_cleaning(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Apply cleaning to all tables and save processed CSVs."""
    print("=" * 60)
    print("Phase 2b: Data Cleaning")
    print("=" * 60)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    cleaned = {}
    for name, df in frames.items():
        cleaner = CLEANERS.get(name)
        if cleaner:
            cleaned_df = cleaner(df)
            cleaned[name] = cleaned_df
            out_path = DATA_PROCESSED / f"{name}.csv"
            cleaned_df.to_csv(out_path, index=False)
            print(f"  Cleaned {name}: {len(cleaned_df):,} rows -> {out_path.name}")
        else:
            cleaned[name] = df
            out_path = DATA_PROCESSED / f"{name}.csv"
            df.to_csv(out_path, index=False)
            print(f"  Copied {name}: {len(df):,} rows (no cleaning needed)")

    print("\nPhase 2b complete.\n")
    return cleaned