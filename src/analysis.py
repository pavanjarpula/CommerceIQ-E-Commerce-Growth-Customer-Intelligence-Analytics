"""CommerceIQ - EDA & Statistical Analysis.

Univariate, bivariate, correlation analysis, and statistical tests.
Adapted to actual schema (no discount/shipping on orders).
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from config import FIGURES_DIR, METRICS_DIR

sns.set_theme(style="whitegrid", palette="muted")


def plot_revenue_distribution(orders: pd.DataFrame):
    completed = orders[orders["status"] == "completed"]["net_revenue"]
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(completed, bins=50, color="#2196F3", edgecolor="white", alpha=0.8)
    axes[0].set_title("Revenue Distribution", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Net Revenue")
    axes[0].set_ylabel("Frequency")
    axes[1].hist(completed, bins=50, color="#2196F3", edgecolor="white", alpha=0.8)
    axes[1].set_yscale("log")
    axes[1].set_title("Revenue Distribution (Log Scale)", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Net Revenue")
    axes[1].set_ylabel("Frequency (log)")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "revenue_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_monthly_trends(orders: pd.DataFrame):
    completed = orders[orders["status"] == "completed"].copy()
    completed["order_ts"] = pd.to_datetime(completed["order_ts"])
    monthly = completed.groupby(completed["order_ts"].dt.to_period("M")).agg(
        revenue=("net_revenue", "sum"),
        orders=("order_id", "count"),
        aov=("net_revenue", "mean"),
    ).reset_index()
    monthly["order_ts"] = monthly["order_ts"].dt.to_timestamp()

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    axes[0].plot(monthly["order_ts"], monthly["revenue"], marker="o", color="#4CAF50", linewidth=2)
    axes[0].set_title("Monthly Revenue", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Revenue")
    axes[0].tick_params(axis="x", rotation=45)
    axes[1].plot(monthly["order_ts"], monthly["orders"], marker="o", color="#FF9800", linewidth=2)
    axes[1].set_title("Monthly Orders", fontsize=13, fontweight="bold")
    axes[1].set_ylabel("Order Count")
    axes[1].tick_params(axis="x", rotation=45)
    axes[2].plot(monthly["order_ts"], monthly["aov"], marker="o", color="#9C27B0", linewidth=2)
    axes[2].set_title("Monthly AOV", fontsize=13, fontweight="bold")
    axes[2].set_ylabel("Avg Order Value")
    axes[2].tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "monthly_trends.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_category_analysis(products: pd.DataFrame):
    cat = products.groupby("category").agg(
        revenue=("total_revenue", "sum"),
        margin=("product_margin_total", "sum"),
        units=("total_units_sold", "sum"),
    ).reset_index().sort_values("revenue", ascending=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    axes[0].barh(cat["category"], cat["revenue"], color="#2196F3")
    axes[0].set_title("Revenue by Category", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Revenue")
    axes[1].barh(cat["category"], cat["margin"], color="#4CAF50")
    axes[1].set_title("Margin by Category", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Gross Margin")
    axes[2].barh(cat["category"], cat["units"], color="#FF9800")
    axes[2].set_title("Units Sold by Category", fontsize=13, fontweight="bold")
    axes[2].set_xlabel("Units Sold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "category_analysis.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_channel_analysis(orders: pd.DataFrame, customers: pd.DataFrame):
    merged = orders.merge(customers[["customer_id", "channel"]], on="customer_id", how="left")
    completed = merged[merged["status"] == "completed"]
    ch = completed.groupby("channel").agg(
        revenue=("net_revenue", "sum"),
        orders=("order_id", "count"),
        avg_revenue=("net_revenue", "mean"),
    ).reset_index().sort_values("revenue", ascending=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    axes[0].barh(ch["channel"], ch["revenue"], color="#2196F3")
    axes[0].set_title("Revenue by Channel", fontsize=13, fontweight="bold")
    axes[1].barh(ch["channel"], ch["orders"], color="#4CAF50")
    axes[1].set_title("Orders by Channel", fontsize=13, fontweight="bold")
    axes[2].barh(ch["channel"], ch["avg_revenue"], color="#9C27B0")
    axes[2].set_title("Avg Revenue per Order by Channel", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "channel_analysis.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_rfm_distribution(customers: pd.DataFrame):
    active = customers[customers["total_orders"] > 0]
    seg_counts = active["rfm_segment"].value_counts()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336", "#795548", "#607D8B"]
    axes[0].pie(seg_counts.values, labels=seg_counts.index, autopct="%1.1f%%",
                colors=colors[:len(seg_counts)], startangle=90)
    axes[0].set_title("RFM Segment Distribution", fontsize=13, fontweight="bold")
    seg_revenue = active.groupby("rfm_segment")["total_revenue"].sum().sort_values(ascending=True)
    axes[1].barh(seg_revenue.index, seg_revenue.values, color=colors[:len(seg_revenue)])
    axes[1].set_title("Revenue by RFM Segment", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Total Revenue")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "rfm_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_country_analysis(orders: pd.DataFrame, customers: pd.DataFrame):
    merged = orders.merge(customers[["customer_id", "country"]], on="customer_id", how="left")
    completed = merged[merged["status"] == "completed"]
    country = completed.groupby("country").agg(
        revenue=("net_revenue", "sum"),
        orders=("order_id", "count"),
    ).reset_index().sort_values("revenue", ascending=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].barh(country["country"], country["revenue"], color="#2196F3")
    axes[0].set_title("Revenue by Country", fontsize=13, fontweight="bold")
    axes[1].barh(country["country"], country["orders"], color="#4CAF50")
    axes[1].set_title("Orders by Country", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "country_analysis.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_correlation_matrix(orders: pd.DataFrame):
    numeric_cols = ["gross_revenue", "net_revenue", "item_count", "total_quantity", "gross_margin", "net_margin"]
    available = [c for c in numeric_cols if c in orders.columns]
    corr = orders[available].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlBu_r",
                center=0, square=True, ax=ax)
    ax.set_title("Feature Correlation Matrix", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "correlation_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_status_analysis(orders: pd.DataFrame):
    """Plot order status distribution and revenue by status."""
    status_counts = orders["status"].value_counts()
    completed = orders[orders["status"] == "completed"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    colors = {"completed": "#4CAF50", "refunded": "#FF9800", "cancelled": "#F44336"}
    bar_colors = [colors.get(s, "#9E9E9E") for s in status_counts.index]
    axes[0].bar(status_counts.index, status_counts.values, color=bar_colors)
    axes[0].set_title("Order Status Distribution", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Count")

    status_rev = orders.groupby("status")["gross_revenue"].sum()
    bar_colors2 = [colors.get(s, "#9E9E9E") for s in status_rev.index]
    axes[1].bar(status_rev.index, status_rev.values, color=bar_colors2)
    axes[1].set_title("Revenue by Order Status", fontsize=13, fontweight="bold")
    axes[1].set_ylabel("Gross Revenue")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "status_analysis.png", dpi=150, bbox_inches="tight")
    plt.close()


def run_statistical_tests(orders: pd.DataFrame, customers: pd.DataFrame) -> dict:
    results = {}
    completed = orders[orders["status"] == "completed"]
    merged = completed.merge(customers[["customer_id", "channel", "country"]], on="customer_id", how="left")

    # Channel AOV test
    channel_groups = [g["net_revenue"].values for _, g in merged.groupby("channel") if len(g) > 2]
    if len(channel_groups) >= 2:
        stat, p_val = stats.kruskal(*channel_groups)
        results["channel_aov_test"] = {
            "test": "Kruskal-Wallis",
            "statistic": round(float(stat), 4),
            "p_value": round(float(p_val), 6),
            "significant": p_val < 0.05,
        }

    # Country AOV test
    country_groups = [g["net_revenue"].values for _, g in merged.groupby("country") if len(g) > 2]
    if len(country_groups) >= 2:
        stat, p_val = stats.kruskal(*country_groups)
        results["country_aov_test"] = {
            "test": "Kruskal-Wallis",
            "statistic": round(float(stat), 4),
            "p_value": round(float(p_val), 6),
            "significant": p_val < 0.05,
        }

    # Normality test
    sample = completed["net_revenue"].dropna().sample(min(5000, len(completed)), random_state=42)
    if len(sample) >= 8:
        stat, p_val = stats.shapiro(sample)
        results["revenue_normality"] = {
            "test": "Shapiro-Wilk",
            "statistic": round(float(stat), 4),
            "p_value": round(float(p_val), 6),
            "normal": p_val > 0.05,
        }

    return results


def run_analysis(data: dict):
    print("=" * 60)
    print("Phase 6: EDA & Statistical Analysis")
    print("=" * 60)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    orders = data["orders"]
    customers = data["customers"]
    products = data["products"]

    print("\nGenerating visualizations...")
    plot_revenue_distribution(orders)
    print("  revenue_distribution.png")
    plot_monthly_trends(orders)
    print("  monthly_trends.png")
    plot_category_analysis(products)
    print("  category_analysis.png")
    plot_channel_analysis(orders, customers)
    print("  channel_analysis.png")
    plot_rfm_distribution(customers)
    print("  rfm_distribution.png")
    plot_country_analysis(orders, customers)
    print("  country_analysis.png")
    plot_correlation_matrix(orders)
    print("  correlation_matrix.png")
    plot_status_analysis(orders)
    print("  status_analysis.png")

    print("\nRunning statistical tests...")
    tests = run_statistical_tests(orders, customers)
    # Convert numpy bools to Python bools for JSON serialization
    def convert_booleans(obj):
        if isinstance(obj, dict):
            return {k: convert_booleans(v) for k, v in obj.items()}
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        return obj
    tests = convert_booleans(tests)
    with open(METRICS_DIR / "statistical_tests.json", "w") as f:
        json.dump(tests, f, indent=2)
    print(f"  Saved {len(tests)} test results")

    print("\nPhase 6 complete.\n")