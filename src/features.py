"""CommerceIQ - Feature Engineering.

RFM scoring, cohort assignment, margin calculations, time features.
Adapted to actual dataset schema (no discount_pct/shipping_cost on orders).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from config import DATA_PROCESSED, METRICS_DIR


def build_order_features(orders: pd.DataFrame, items: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Compute order-level features with item and product data."""
    # Aggregate item-level data per order
    item_agg = items.groupby("order_id").agg(
        item_count=("order_item_id", "count"),
        total_quantity=("quantity", "sum"),
        gross_revenue=("line_total", "sum"),
    ).reset_index()

    # Join with products to get cost
    items_with_cost = items.merge(
        products[["product_id", "unit_cost"]], on="product_id", how="left"
    )
    items_with_cost["cost_total"] = items_with_cost["quantity"] * items_with_cost["unit_cost"]
    items_with_cost["margin_total"] = items_with_cost["line_total"] - items_with_cost["cost_total"]

    cost_agg = items_with_cost.groupby("order_id").agg(
        total_cost=("cost_total", "sum"),
        gross_margin=("margin_total", "sum"),
    ).reset_index()

    # Build order features
    orders = orders.copy()
    orders = orders.merge(item_agg, on="order_id", how="left")
    orders = orders.merge(cost_agg, on="order_id", how="left")

    # Fill NaN for orders without items (e.g. cancelled before itemization)
    orders["item_count"] = orders["item_count"].fillna(0).astype(int)
    orders["total_quantity"] = orders["total_quantity"].fillna(0).astype(int)
    orders["gross_revenue"] = orders["gross_revenue"].fillna(0)
    orders["total_cost"] = orders["total_cost"].fillna(0)
    orders["gross_margin"] = orders["gross_margin"].fillna(0)

    # Net revenue = gross (no discount or shipping fields in this dataset)
    orders["net_revenue"] = orders["gross_revenue"]
    orders["net_margin"] = orders["gross_margin"]

    # Cost basis
    orders["cost_pct"] = np.where(
        orders["gross_revenue"] > 0,
        (orders["total_cost"] / orders["gross_revenue"]).round(4),
        0,
    )

    return orders


def build_customer_features(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Compute customer-level features from orders."""
    cust_agg = orders[orders["status"] == "completed"].groupby("customer_id").agg(
        total_orders=("order_id", "count"),
        total_revenue=("net_revenue", "sum"),
        total_gross_margin=("gross_margin", "sum"),
        first_order_date=("order_ts", "min"),
        last_order_date=("order_ts", "max"),
        avg_order_value=("net_revenue", "mean"),
    ).reset_index()

    customers = customers.copy()
    customers = customers.merge(cust_agg, on="customer_id", how="left")

    # Fill NaN for customers with no completed orders
    for col in ["total_orders", "total_revenue", "total_gross_margin", "avg_order_value"]:
        customers[col] = customers[col].fillna(0)

    # Customer tenure
    customers["signup_date"] = pd.to_datetime(customers["signup_date"])
    ref_date = customers["last_order_date"].max() if customers["last_order_date"].notna().any() else pd.Timestamp.now()
    customers["recency_days"] = (ref_date - customers["last_order_date"]).dt.days
    customers["tenure_days"] = (ref_date - customers["signup_date"]).dt.days
    customers["recency_days"] = customers["recency_days"].fillna(customers["tenure_days"])

    # Customer lifetime value
    customers["clv"] = customers["total_revenue"]

    return customers


def compute_rfm(customers: pd.DataFrame) -> pd.DataFrame:
    """Compute RFM scores and segments."""
    df = customers.copy()

    # Only consider customers with at least one order
    active = df[df["total_orders"] > 0].copy()

    if len(active) == 0:
        df["rfm_r"] = 0
        df["rfm_f"] = 0
        df["rfm_m"] = 0
        df["rfm_segment"] = "No Orders"
        return df

    # Recency: lower days = better (invert for scoring)
    active["rfm_r"] = pd.qcut(
        active["recency_days"], q=5, labels=[5, 4, 3, 2, 1], duplicates="drop"
    ).astype(int)

    # Frequency: more orders = better
    active["rfm_f"] = pd.qcut(
        active["total_orders"].clip(lower=1), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop"
    ).astype(int)

    # Monetary: higher spend = better
    active["rfm_m"] = pd.qcut(
        active["total_revenue"].clip(lower=0.01), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop"
    ).astype(int)

    # Segment labels
    active["rfm_score"] = active["rfm_r"] + active["rfm_f"] + active["rfm_m"]

    def assign_segment(row):
        r, f, m = row["rfm_r"], row["rfm_f"], row["rfm_m"]
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        elif r >= 3 and f >= 3 and m >= 3:
            return "Loyal Customers"
        elif r >= 4 and f <= 2:
            return "New Customers"
        elif r >= 3 and f >= 2 and m >= 2:
            return "Potential Loyalists"
        elif r <= 2 and f >= 3:
            return "At Risk"
        elif r <= 2 and f <= 2:
            return "Lost"
        else:
            return "Others"

    active["rfm_segment"] = active.apply(assign_segment, axis=1)

    df = df.merge(
        active[["customer_id", "rfm_r", "rfm_f", "rfm_m", "rfm_score", "rfm_segment"]],
        on="customer_id",
        how="left",
    )
    df["rfm_segment"] = df["rfm_segment"].fillna("No Orders")
    return df


def compute_cohorts(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Assign cohort months and compute retention."""
    orders = orders.copy()
    customers = customers.copy()

    # Cohort month from signup
    customers["cohort_month"] = pd.to_datetime(customers["signup_date"]).dt.to_period("M")

    # Order month
    orders["order_month"] = pd.to_datetime(orders["order_ts"]).dt.to_period("M")

    # Merge
    cohort_orders = orders.merge(
        customers[["customer_id", "cohort_month"]], on="customer_id", how="left"
    )

    # Cohort index (months between cohort and order)
    cohort_orders["cohort_index"] = (
        cohort_orders["order_month"] - cohort_orders["cohort_month"]
    ).apply(lambda x: x.n if hasattr(x, "n") else 0)

    return cohort_orders


def build_cohort_retention_matrix(cohort_orders: pd.DataFrame) -> pd.DataFrame:
    """Build cohort retention matrix."""
    cohort_data = cohort_orders.groupby(["cohort_month", "order_month"]).agg(
        n_customers=("customer_id", "nunique")
    ).reset_index()

    cohort_sizes = cohort_data[cohort_data["cohort_month"] == cohort_data["order_month"]][
        ["cohort_month", "n_customers"]
    ].rename(columns={"n_customers": "cohort_size"})

    cohort_data = cohort_data.merge(cohort_sizes, on="cohort_month", how="left")
    cohort_data["retention_rate"] = (cohort_data["n_customers"] / cohort_data["cohort_size"]).round(4)

    return cohort_data


def build_product_features(items: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Compute product-level aggregated features."""
    prod_agg = items.groupby("product_id").agg(
        total_units_sold=("quantity", "sum"),
        total_revenue=("line_total", "sum"),
        order_count=("order_id", "nunique"),
        avg_selling_price=("unit_price", "mean"),
    ).reset_index()

    products = products.copy()
    products = products.merge(prod_agg, on="product_id", how="left")
    for col in ["total_units_sold", "total_revenue", "order_count"]:
        products[col] = products[col].fillna(0)

    products["product_margin_total"] = (
        (products["unit_price"] - products["unit_cost"]) * products["total_units_sold"]
    ).round(2)

    return products


def run_feature_engineering(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Execute full feature engineering pipeline."""
    print("=" * 60)
    print("Phase 3: Feature Engineering")
    print("=" * 60)

    orders = build_order_features(frames["orders"], frames["order_items"], frames["products"])
    customers = build_customer_features(orders, frames["customers"])
    customers = compute_rfm(customers)
    cohort_orders = compute_cohorts(orders, frames["customers"])
    cohort_retention = build_cohort_retention_matrix(cohort_orders)
    products = build_product_features(frames["order_items"], frames["products"])

    result = {
        "orders": orders,
        "customers": customers,
        "cohort_orders": cohort_orders,
        "cohort_retention": cohort_retention,
        "products": products,
        "order_items": frames["order_items"],
        "events": frames["events"],
    }

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    for name, df in result.items():
        out = DATA_PROCESSED / f"{name}.csv"
        df.to_csv(out, index=False)
        print(f"  Saved {name}: {len(df):,} rows")

    print("\nPhase 3 complete.\n")
    return result