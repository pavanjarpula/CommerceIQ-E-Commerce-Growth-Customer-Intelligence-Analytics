"""Tests for metrics module."""
import sys
import json
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from config import METRICS_DIR


def load_metric(name):
    with open(METRICS_DIR / f"{name}.json") as f:
        return json.load(f)


class TestRevenueMetrics:
    def test_revenue_metrics_exist(self):
        m = load_metric("revenue_metrics")
        assert m["total_orders"] == 12000
        assert m["completed_orders"] > 0
        assert m["total_gross_revenue"] > 0
        assert m["total_net_revenue"] > 0

    def test_rates_sum_to_one(self):
        m = load_metric("revenue_metrics")
        total = m["completion_rate"] + m["refund_rate"] + m["cancellation_rate"]
        assert abs(total - 1.0) < 0.01, f"Rates sum to {total}"

    def test_margin_positive(self):
        m = load_metric("revenue_metrics")
        assert m["total_gross_margin"] > 0
        assert 0 < m["margin_pct"] < 1

    def test_aov_reasonable(self):
        m = load_metric("revenue_metrics")
        assert 10 < m["avg_order_value"] < 10000, f"AOV {m['avg_order_value']} seems unreasonable"


class TestMonthlyRevenue:
    def test_monthly_data_exists(self):
        m = load_metric("monthly_revenue")
        assert "monthly" in m
        assert len(m["monthly"]) > 0

    def test_growth_rates(self):
        m = load_metric("monthly_revenue")
        for month in m["monthly"][1:]:
            assert "revenue_mom_growth" in month
            assert "orders_mom_growth" in month


class TestChannelMetrics:
    def test_channels_exist(self):
        m = load_metric("channel_metrics")
        assert "channels" in m
        assert len(m["channels"]) == 6

    def test_revenue_pct_sums_to_one(self):
        m = load_metric("channel_metrics")
        total = sum(c["revenue_pct"] for c in m["channels"])
        assert abs(total - 1.0) < 0.01


class TestCategoryMetrics:
    def test_categories_exist(self):
        m = load_metric("category_metrics")
        assert "categories" in m
        assert len(m["categories"]) == 6

    def test_revenue_sorted_desc(self):
        m = load_metric("category_metrics")
        revenues = [c["total_revenue"] for c in m["categories"]]
        assert revenues == sorted(revenues, reverse=True)


class TestRFMSummary:
    def test_segments_exist(self):
        m = load_metric("rfm_summary")
        assert "segments" in m
        assert m["active_customers"] > 0

    def test_total_customers(self):
        m = load_metric("rfm_summary")
        assert m["total_customers"] == 2000


class TestReconciliation:
    """Test that SQL analysis produced results."""
    def test_reconciliation_exists(self):
        from config import SQL_RESULTS_DIR
        recon_path = SQL_RESULTS_DIR / "05_reconciliation.csv"
        assert recon_path.exists()

    def test_reconciliation_has_data(self):
        import pandas as pd
        from config import SQL_RESULTS_DIR
        sql = pd.read_csv(SQL_RESULTS_DIR / "05_reconciliation.csv")
        assert len(sql) > 0
        assert "revenue" in sql.columns or "sql_value" in sql.columns