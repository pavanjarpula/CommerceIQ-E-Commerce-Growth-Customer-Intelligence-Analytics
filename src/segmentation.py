"""CommerceIQ - RFM Segmentation.

Detailed segment analysis and visualization data.
"""
import json
from pathlib import Path

import pandas as pd

from config import METRICS_DIR


SEGMENT_DESCRIPTIONS = {
    "Champions": "Best customers: recent, frequent, high spenders. Reward them with loyalty programs.",
    "Loyal Customers": "Regular buyers with good frequency and spend. Upsell premium products.",
    "Potential Loyalists": "Recent buyers with moderate spend. Nurture with targeted campaigns.",
    "New Customers": "Just signed up, recent first purchase. Onboard with welcome sequences.",
    "At Risk": "Used to buy frequently but haven't returned recently. Win back with re-engagement.",
    "Lost": "Haven't purchased in a long time with low frequency. Reactivation campaigns needed.",
    "Others": "Customers who don't fit standard RFM segments clearly.",
    "No Orders": "Registered customers who have never placed an order.",
}


def compute_segment_details(customers: pd.DataFrame, orders: pd.DataFrame) -> dict:
    """Compute detailed metrics per RFM segment."""
    active = customers[customers["total_orders"] > 0].copy()

    segments = active.groupby("rfm_segment").agg(
        customer_count=("customer_id", "count"),
        avg_recency=("recency_days", "mean"),
        avg_frequency=("total_orders", "mean"),
        avg_monetary=("total_revenue", "mean"),
        total_revenue=("total_revenue", "sum"),
        total_margin=("total_gross_margin", "sum"),
        avg_clv=("clv", "mean"),
        median_clv=("clv", "median"),
    ).reset_index()

    total_revenue = segments["total_revenue"].sum()
    segments["revenue_share"] = (segments["total_revenue"] / total_revenue * 100).round(1)
    segments["avg_recency"] = segments["avg_recency"].round(0).astype(int)
    segments["avg_frequency"] = segments["avg_frequency"].round(1)
    segments["avg_monetary"] = segments["avg_monetary"].round(2)
    segments["total_revenue"] = segments["total_revenue"].round(2)
    segments["total_margin"] = segments["total_margin"].round(2)
    segments["avg_clv"] = segments["avg_clv"].round(2)
    segments["median_clv"] = segments["median_clv"].round(2)
    segments["description"] = segments["rfm_segment"].map(SEGMENT_DESCRIPTIONS)

    return {
        "segments": segments.to_dict(orient="records"),
        "total_customers": int(len(customers)),
        "active_customers": int(len(active)),
    }


def run_segmentation(data: dict) -> dict:
    """Run segmentation analysis."""
    print("=" * 60)
    print("Phase 7a: RFM Segmentation Analysis")
    print("=" * 60)

    result = compute_segment_details(data["customers"], data["orders"])

    with open(METRICS_DIR / "rfm_segment_details.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"  Analyzed {result['active_customers']}/{result['total_customers']} active customers")
    print(f"  Found {len(result['segments'])} segments")
    print("  Saved to rfm_segment_details.json")

    print("\nPhase 7a complete.\n")
    return result