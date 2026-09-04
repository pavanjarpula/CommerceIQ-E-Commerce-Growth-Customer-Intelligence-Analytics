"""CommerceIQ - Cohort Analysis.

Cohort retention analysis with visualization data.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from config import FIGURES_DIR, METRICS_DIR


def _add_cohort_index(df: pd.DataFrame) -> pd.DataFrame:
    """Add cohort_index computed from cohort_month and order_month."""
    df = df.copy()
    if "cohort_index" not in df.columns:
        df["cohort_month_dt"] = pd.to_datetime(df["cohort_month"].astype(str) + "-01")
        df["order_month_dt"] = pd.to_datetime(df["order_month"].astype(str) + "-01")
        df["cohort_index"] = ((df["order_month_dt"].dt.year - df["cohort_month_dt"].dt.year) * 12
                              + (df["order_month_dt"].dt.month - df["cohort_month_dt"].dt.month))
    return df


def plot_cohort_heatmap(cohort_retention: pd.DataFrame):
    """Plot cohort retention heatmap."""
    cohort_retention = _add_cohort_index(cohort_retention)
    matrix = cohort_retention.pivot_table(
        index="cohort_month",
        columns="cohort_index",
        values="retention_rate",
        aggfunc="first",
    ).fillna(0)

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(
        matrix, annot=True, fmt=".0%", cmap="YlGnBu",
        linewidths=0.5, ax=ax, vmin=0, vmax=1,
        cbar_kws={"label": "Retention Rate"},
    )
    ax.set_title("Monthly Cohort Retention Matrix", fontsize=14, fontweight="bold")
    ax.set_xlabel("Months Since Signup", fontsize=12)
    ax.set_ylabel("Signup Cohort Month", fontsize=12)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "cohort_retention_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_retention_curves(cohort_retention: pd.DataFrame):
    """Plot average retention curves."""
    cohort_retention = _add_cohort_index(cohort_retention)
    avg_retention = cohort_retention.groupby("cohort_index")["retention_rate"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(avg_retention["cohort_index"], avg_retention["retention_rate"],
            marker="o", linewidth=2, color="#2196F3", markersize=8)
    ax.fill_between(avg_retention["cohort_index"], avg_retention["retention_rate"],
                     alpha=0.2, color="#2196F3")
    ax.set_title("Average Customer Retention Curve", fontsize=14, fontweight="bold")
    ax.set_xlabel("Months Since Signup", fontsize=12)
    ax.set_ylabel("Retention Rate", fontsize=12)
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "retention_curves.png", dpi=150, bbox_inches="tight")
    plt.close()


def run_cohorts(data: dict):
    """Run cohort analysis and generate visualizations."""
    print("=" * 60)
    print("Phase 7b: Cohort Analysis")
    print("=" * 60)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    cohort_retention = data["cohort_retention"]

    plot_cohort_heatmap(cohort_retention)
    print("  cohort_retention_heatmap.png")
    plot_retention_curves(cohort_retention)
    print("  retention_curves.png")

    # Average retention by period
    cohort_with_index = _add_cohort_index(cohort_retention)
    avg_ret = cohort_with_index.groupby("cohort_index")["retention_rate"].mean().to_dict()
    avg_ret = {str(int(k)): round(float(v), 4) for k, v in avg_ret.items()}
    with open(METRICS_DIR / "avg_retention_by_period.json", "w") as f:
        json.dump(avg_ret, f, indent=2)
    print("  Saved avg_retention_by_period.json")

    print("\nPhase 7b complete.\n")