"""Tests for data ingestion module."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from config import DATA_RAW


class TestIngestion:
    """Test that data files exist and have expected structure."""

    def test_raw_csvs_exist(self):
        expected = ["customers.csv", "products.csv", "orders.csv", "order_items.csv", "events.csv"]
        for name in expected:
            assert (DATA_RAW / name).exists(), f"Missing {name}"

    def test_raw_row_counts(self):
        import pandas as pd
        counts = {
            "customers.csv": 2000,
            "products.csv": 120,
            "orders.csv": 12000,
            "order_items.csv": 30120,
        }
        for name, expected in counts.items():
            df = pd.read_csv(DATA_RAW / name)
            assert len(df) == expected, f"{name}: expected {expected}, got {len(df)}"

    def test_raw_schema(self):
        import pandas as pd
        customers = pd.read_csv(DATA_RAW / "customers.csv")
        assert set(customers.columns) == {"customer_id", "signup_date", "channel", "country"}

        products = pd.read_csv(DATA_RAW / "products.csv")
        assert set(products.columns) == {"product_id", "product_name", "category", "unit_price", "unit_cost"}

        orders = pd.read_csv(DATA_RAW / "orders.csv")
        assert set(orders.columns) == {"order_id", "customer_id", "order_ts", "status"}