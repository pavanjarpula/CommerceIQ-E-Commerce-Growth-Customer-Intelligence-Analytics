"""CommerceIQ - Evidence-Based Recommendations.

Generates actionable insights from computed metrics.
"""
import json
from pathlib import Path

from config import METRICS_DIR


def generate_recommendations(data: dict, metrics: dict) -> list[dict]:
    recommendations = []
    customers = data["customers"]
    orders = data["orders"]
    products = data["products"]

    # 1. Customer Retention
    active = customers[customers["total_orders"] > 0]
    at_risk = active[active["rfm_segment"] == "At Risk"]
    lost = active[active["rfm_segment"] == "Lost"]

    if len(at_risk) > 0:
        at_risk_revenue = at_risk["total_revenue"].sum()
        recommendations.append({
            "category": "Customer Retention",
            "priority": "High",
            "finding": f"{len(at_risk)} customers classified as 'At Risk' with ${at_risk_revenue:,.2f} in historical revenue.",
            "recommendation": "Implement re-engagement campaigns targeting At Risk customers with personalized offers.",
            "expected_impact": f"Recovering 20% could recover ~${at_risk_revenue * 0.2:,.2f} in revenue.",
        })

    if len(lost) > 0:
        lost_revenue = lost["total_revenue"].sum()
        recommendations.append({
            "category": "Customer Retention",
            "priority": "Medium",
            "finding": f"{len(lost)} customers classified as 'Lost' (${lost_revenue:,.2f} historical).",
            "recommendation": "Evaluate win-back campaign ROI for high-value lost customers.",
        })

    # 2. Channel Optimization
    ch_merged = orders.merge(customers[["customer_id", "channel"]], on="customer_id", how="left")
    completed_ch = ch_merged[ch_merged["status"] == "completed"]
    channel_perf = completed_ch.groupby("channel").agg(
        rev=("net_revenue", "sum"),
        aov=("net_revenue", "mean"),
        customers=("customer_id", "nunique"),
    )
    if len(channel_perf) > 1:
        best = channel_perf["aov"].idxmax()
        worst = channel_perf["aov"].idxmin()
        recommendations.append({
            "category": "Channel Strategy",
            "priority": "Medium",
            "finding": f"'{best}' has highest AOV (${channel_perf.loc[best, 'aov']:,.2f}), '{worst}' lowest.",
            "recommendation": f"Shift marketing spend toward '{best}'. Investigate '{worst}' audience targeting.",
        })

    # 3. Product Portfolio
    prod_margin = products[products["total_revenue"] > 0]
    low_margin = prod_margin[prod_margin["margin_pct"] < 0.1]
    if len(low_margin) > 0:
        recommendations.append({
            "category": "Product Portfolio",
            "priority": "Medium",
            "finding": f"{len(low_margin)} products have margin below 10%.",
            "recommendation": "Review low-margin products for repricing, bundling, or discontinuation.",
        })

    # 4. Geographic
    geo = completed_ch.merge(customers[["customer_id", "country"]], on="customer_id")
    country_perf = geo.groupby("country")["net_revenue"].agg(["sum", "count"])
    if len(country_perf) > 1:
        top = country_perf["sum"].idxmax()
        bottom = country_perf["sum"].idxmin()
        recommendations.append({
            "category": "Geographic Strategy",
            "priority": "Low",
            "finding": f"'{top}' leads revenue (${country_perf.loc[top, 'sum']:,.2f}), '{bottom}' lags.",
            "recommendation": f"Investigate barriers in '{bottom}'. Consider localized marketing.",
        })

    # 5. High-Value Customers
    if "Champions" in active["rfm_segment"].values:
        champions = active[active["rfm_segment"] == "Champions"]
        champ_rev = champions["total_revenue"].sum()
        total_rev = active["total_revenue"].sum()
        recommendations.append({
            "category": "VIP Program",
            "priority": "High",
            "finding": f"Champions represent {len(champions)} customers but ${champ_rev:,.2f} ({champ_rev/total_rev:.0%}) of revenue.",
            "recommendation": "Launch exclusive loyalty program for Champions with early access and premium perks.",
            "expected_impact": f"Improving Champion retention by 5% could add ~${champ_rev * 0.05:,.2f}.",
        })

    return recommendations


def run_recommendations(data: dict, metrics: dict) -> list[dict]:
    print("=" * 60)
    print("Phase 8c: Recommendations")
    print("=" * 60)

    recs = generate_recommendations(data, metrics)

    with open(METRICS_DIR / "recommendations.json", "w") as f:
        json.dump({"recommendations": recs, "total": len(recs)}, f, indent=2)

    print(f"  Generated {len(recs)} recommendations")
    for r in recs:
        print(f"    [{r['priority']}] {r['category']}: {r['finding'][:60]}...")
    print("  Saved to recommendations.json")

    print("\nPhase 8c complete.\n")
    return recs