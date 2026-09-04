"""CommerceIQ - Metric Definitions.

Computes all business metrics from feature-engineered data.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from config import METRICS_DIR


def _to_serializable(val):
    if isinstance(val, (np.integer,)):
        return int(val)
    if isinstance(val, (np.floating,)):
        return float(val)
    if isinstance(val, (pd.Period,)):
        return str(val)
    if isinstance(val, pd.Timestamp):
        return val.isoformat()
    if isinstance(val, np.ndarray):
        return val.tolist()
    return val


def _save_metrics(data: dict, name: str):
    path = METRICS_DIR / f"{name}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=_to_serializable)
    print(f"  Saved {path.name}")


def compute_revenue_metrics(data: dict) -> dict:
    orders = data["orders"]
    completed = orders[orders["status"] == "completed"]
    refunded = orders[orders["status"] == "refunded"]
    cancelled = orders[orders["status"] == "cancelled"]

    total_orders = len(orders)
    completed_orders = len(completed)
    total_gross = float(orders["gross_revenue"].sum())
    total_net = float(completed["net_revenue"].sum())
    total_margin = float(completed["gross_margin"].sum())
    total_refund = float(refunded["gross_revenue"].sum())

    metrics = {
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "refunded_orders": len(refunded),
        "cancelled_orders": len(cancelled),
        "completion_rate": round(completed_orders / total_orders, 4) if total_orders else 0,
        "refund_rate": round(len(refunded) / total_orders, 4) if total_orders else 0,
        "cancellation_rate": round(len(cancelled) / total_orders, 4) if total_orders else 0,
        "total_gross_revenue": round(total_gross, 2),
        "total_net_revenue": round(total_net, 2),
        "total_gross_margin": round(total_margin, 2),
        "margin_pct": round(total_margin / total_gross, 4) if total_gross else 0,
        "avg_order_value": round(total_net / completed_orders, 2) if completed_orders else 0,
        "avg_order_margin": round(total_margin / completed_orders, 2) if completed_orders else 0,
        "total_refund_revenue": round(total_refund, 2),
        "avg_items_per_order": round(float(completed["item_count"].mean()), 2) if len(completed) else 0,
    }
    return metrics


def compute_monthly_revenue(orders: pd.DataFrame) -> list[dict]:
    completed = orders[orders["status"] == "completed"].copy()
    monthly = completed.groupby("order_month").agg(
        orders=("order_id", "count"),
        gross_revenue=("gross_revenue", "sum"),
        net_revenue=("net_revenue", "sum"),
        avg_order_value=("net_revenue", "mean"),
        margin=("gross_margin", "sum"),
        avg_items=("item_count", "mean"),
    ).reset_index()

    for col in ["gross_revenue", "net_revenue", "avg_order_value", "margin", "avg_items"]:
        monthly[col] = monthly[col].round(2)
    monthly["revenue_mom_growth"] = monthly["net_revenue"].pct_change().round(4)
    monthly["orders_mom_growth"] = monthly["orders"].pct_change().round(4)

    return monthly.to_dict(orient="records")


def compute_channel_metrics(orders: pd.DataFrame, customers: pd.DataFrame) -> list[dict]:
    channel_data = orders.merge(customers[["customer_id", "channel"]], on="customer_id", how="left")
    completed = channel_data[channel_data["status"] == "completed"]

    ch = completed.groupby("channel").agg(
        total_orders=("order_id", "count"),
        total_revenue=("net_revenue", "sum"),
        total_margin=("gross_margin", "sum"),
        avg_order_value=("net_revenue", "mean"),
        unique_customers=("customer_id", "nunique"),
    ).reset_index()

    total_rev = ch["total_revenue"].sum()
    ch["revenue_pct"] = (ch["total_revenue"] / total_rev).round(4)
    ch["total_revenue"] = ch["total_revenue"].round(2)
    ch["total_margin"] = ch["total_margin"].round(2)
    ch["avg_order_value"] = ch["avg_order_value"].round(2)
    ch["margin_pct"] = (ch["total_margin"] / ch["total_revenue"]).round(4)
    return ch.to_dict(orient="records")


def compute_country_metrics(orders: pd.DataFrame, customers: pd.DataFrame) -> list[dict]:
    merged = orders.merge(customers[["customer_id", "country"]], on="customer_id", how="left")
    completed = merged[merged["status"] == "completed"]

    co = completed.groupby("country").agg(
        total_orders=("order_id", "count"),
        total_revenue=("net_revenue", "sum"),
        total_margin=("gross_margin", "sum"),
        avg_order_value=("net_revenue", "mean"),
        unique_customers=("customer_id", "nunique"),
    ).reset_index()

    total_rev = co["total_revenue"].sum()
    co["revenue_pct"] = (co["total_revenue"] / total_rev).round(4)
    co["total_revenue"] = co["total_revenue"].round(2)
    co["total_margin"] = co["total_margin"].round(2)
    co["avg_order_value"] = co["avg_order_value"].round(2)
    return co.sort_values("total_revenue", ascending=False).to_dict(orient="records")


def compute_category_metrics(products: pd.DataFrame) -> list[dict]:
    cat = products.groupby("category").agg(
        total_revenue=("total_revenue", "sum"),
        total_units=("total_units_sold", "sum"),
        total_margin=("product_margin_total", "sum"),
        product_count=("product_id", "count"),
        avg_selling_price=("avg_selling_price", "mean"),
    ).reset_index()

    total_rev = cat["total_revenue"].sum()
    cat["revenue_pct"] = (cat["total_revenue"] / total_rev).round(4)
    cat["total_revenue"] = cat["total_revenue"].round(2)
    cat["total_margin"] = cat["total_margin"].round(2)
    cat["avg_selling_price"] = cat["avg_selling_price"].round(2)
    cat["margin_pct"] = np.where(cat["total_revenue"] > 0, (cat["total_margin"] / cat["total_revenue"]).round(4), 0)
    return cat.sort_values("total_revenue", ascending=False).to_dict(orient="records")


def compute_top_products(products: pd.DataFrame, n: int = 10) -> list[dict]:
    top = products.nlargest(n, "total_revenue")[
        ["product_id", "product_name", "category", "total_revenue", "total_units_sold", "product_margin_total", "margin_pct"]
    ]
    return top.to_dict(orient="records")


def compute_rfm_summary(customers: pd.DataFrame) -> dict:
    segments = customers.groupby("rfm_segment").agg(
        customer_count=("customer_id", "count"),
        avg_revenue=("total_revenue", "mean"),
        avg_orders=("total_orders", "mean"),
        total_revenue=("total_revenue", "sum"),
    ).reset_index()

    total_rev = segments["total_revenue"].sum()
    segments["revenue_pct"] = (segments["total_revenue"] / total_rev).round(4)
    segments["avg_revenue"] = segments["avg_revenue"].round(2)
    segments["avg_orders"] = segments["avg_orders"].round(2)
    segments["total_revenue"] = segments["total_revenue"].round(2)

    summary = {
        "segments": segments.to_dict(orient="records"),
        "total_customers": int(len(customers)),
        "active_customers": int((customers["total_orders"] > 0).sum()),
        "avg_clv": round(float(customers["clv"].mean()), 2),
        "median_clv": round(float(customers["clv"].median()), 2),
    }
    return summary


def compute_cohort_summary(cohort_retention: pd.DataFrame) -> dict:
    """Compute cohort summary from retention data."""
    df = cohort_retention.copy()
    df["cohort_month_dt"] = pd.to_datetime(df["cohort_month"].astype(str) + "-01")
    df["order_month_dt"] = pd.to_datetime(df["order_month"].astype(str) + "-01")
    df["cohort_index"] = ((df["order_month_dt"].dt.year - df["cohort_month_dt"].dt.year) * 12
                          + (df["order_month_dt"].dt.month - df["cohort_month_dt"].dt.month))

    matrix = df.pivot_table(
        index="cohort_month",
        columns="cohort_index",
        values="retention_rate",
        aggfunc="first",
    ).fillna(0)

    cohort_sizes = df[df["cohort_index"] == 0].set_index("cohort_month")["cohort_size"].to_dict()

    result = {
        "cohort_months": [str(x) for x in matrix.index.tolist()],
        "cohort_sizes": {str(k): int(v) for k, v in cohort_sizes.items()},
        "retention_matrix": {
            str(k): {str(int(idx)): round(float(val), 4) for idx, val in v.items()}
            for k, v in matrix.to_dict(orient="index").items()
        },
    }
    return result


def run_metrics(data: dict) -> dict:
    print("=" * 60)
    print("Phase 4: Metric Definitions")
    print("=" * 60)

    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    revenue = compute_revenue_metrics(data)
    _save_metrics(revenue, "revenue_metrics")

    monthly = compute_monthly_revenue(data["orders"])
    _save_metrics({"monthly": monthly}, "monthly_revenue")

    channel = compute_channel_metrics(data["orders"], data["customers"])
    _save_metrics({"channels": channel}, "channel_metrics")

    country = compute_country_metrics(data["orders"], data["customers"])
    _save_metrics({"countries": country}, "country_metrics")

    category = compute_category_metrics(data["products"])
    _save_metrics({"categories": category}, "category_metrics")

    top_products = compute_top_products(data["products"])
    _save_metrics({"top_products": top_products}, "top_products")

    rfm = compute_rfm_summary(data["customers"])
    _save_metrics(rfm, "rfm_summary")

    cohort = compute_cohort_summary(data["cohort_retention"])
    _save_metrics(cohort, "cohort_summary")

    print("\nPhase 4 complete.\n")
    return revenue