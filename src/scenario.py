"""CommerceIQ - Scenario Analysis.

Channel ROI and category-level scenarios.
Adapted to actual schema (no discount/shipping fields).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from config import METRICS_DIR


def channel_roi_analysis(orders: pd.DataFrame, customers: pd.DataFrame) -> list[dict]:
    merged = orders.merge(customers[["customer_id", "channel"]], on="customer_id", how="left")
    completed = merged[merged["status"] == "completed"]

    ch = completed.groupby("channel").agg(
        total_orders=("order_id", "count"),
        total_revenue=("net_revenue", "sum"),
        total_margin=("gross_margin", "sum"),
        avg_order_value=("net_revenue", "mean"),
        unique_customers=("customer_id", "nunique"),
    ).reset_index()

    ch["revenue_per_customer"] = (ch["total_revenue"] / ch["unique_customers"]).round(2)
    ch["margin_per_customer"] = (ch["total_margin"] / ch["unique_customers"]).round(2)
    ch["total_revenue"] = ch["total_revenue"].round(2)
    ch["total_margin"] = ch["total_margin"].round(2)
    ch["avg_order_value"] = ch["avg_order_value"].round(2)

    return ch.sort_values("revenue_per_customer", ascending=False).to_dict(orient="records")


def category_profitability(products: pd.DataFrame) -> list[dict]:
    cat = products.groupby("category").agg(
        total_revenue=("total_revenue", "sum"),
        total_margin=("product_margin_total", "sum"),
        product_count=("product_id", "count"),
        avg_margin_pct=("margin_pct", "mean"),
    ).reset_index()
    cat["revenue_per_product"] = (cat["total_revenue"] / cat["product_count"]).round(2)
    cat["total_revenue"] = cat["total_revenue"].round(2)
    cat["total_margin"] = cat["total_margin"].round(2)
    cat["avg_margin_pct"] = cat["avg_margin_pct"].round(4)
    return cat.sort_values("total_margin", ascending=False).to_dict(orient="records")


def run_scenario_analysis(data: dict) -> dict:
    print("=" * 60)
    print("Phase 8b: Scenario Analysis")
    print("=" * 60)

    channel = channel_roi_analysis(data["orders"], data["customers"])
    cat_prof = category_profitability(data["products"])

    results = {
        "channel_roi": channel,
        "category_profitability": cat_prof,
    }

    with open(METRICS_DIR / "scenario_analysis.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"  Channel ROI: {len(channel)} channels analyzed")
    print(f"  Category profitability: {len(cat_prof)} categories")
    print("  Saved to scenario_analysis.json")

    print("\nPhase 8b complete.\n")
    return results