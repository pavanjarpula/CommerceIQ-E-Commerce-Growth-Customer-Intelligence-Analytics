"""Tests for feature engineering module."""
import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from config import DATA_PROCESSED


class TestFeatures:
    """Test feature-engineered outputs."""

    def test_orders_have_features(self):
        orders = pd.read_csv(DATA_PROCESSED / "orders.csv")
        required = ["item_count", "total_quantity", "gross_revenue", "gross_margin", "net_revenue"]
        for col in required:
            assert col in orders.columns, f"Missing column: {col}"

    def test_customers_have_rfm(self):
        customers = pd.read_csv(DATA_PROCESSED / "customers.csv")
        required = ["rfm_r", "rfm_f", "rfm_m", "rfm_segment", "total_orders", "total_revenue"]
        for col in required:
            assert col in customers.columns, f"Missing column: {col}"

    def test_rfm_segments_valid(self):
        customers = pd.read_csv(DATA_PROCESSED / "customers.csv")
        valid = {"Champions", "Loyal Customers", "Potential Loyalists", "New Customers",
                 "At Risk", "Lost", "Others", "No Orders"}
        actual = set(customers["rfm_segment"].unique())
        assert actual.issubset(valid), f"Invalid segments: {actual - valid}"

    def test_products_have_margin(self):
        products = pd.read_csv(DATA_PROCESSED / "products.csv")
        assert "margin_pct" in products.columns
        assert "total_revenue" in products.columns
        assert "product_margin_total" in products.columns

    def test_cohort_retention_exists(self):
        cohort = pd.read_csv(DATA_PROCESSED / "cohort_retention.csv")
        assert "cohort_month" in cohort.columns
        assert "retention_rate" in cohort.columns
        assert len(cohort) > 0

    def test_margin_positive_for_products(self):
        products = pd.read_csv(DATA_PROCESSED / "products.csv")
        active = products[products["total_revenue"] > 0]
        assert (active["margin_pct"] >= 0).all(), "Some products have negative margin"