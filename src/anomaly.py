"""CommerceIQ - Anomaly Detection.

IQR and Z-score anomaly detection with root-cause drill-down.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from config import METRICS_DIR


def detect_iqr_anomalies(series: pd.Series, factor: float = 1.5):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    mask = (series < lower) | (series > upper)
    info = {"q1": round(float(q1), 4), "q3": round(float(q3), 4),
            "iqr": round(float(iqr), 4), "lower": round(float(lower), 4),
            "upper": round(float(upper), 4), "anomaly_count": int(mask.sum())}
    return mask, info


def detect_zscore_anomalies(series: pd.Series, threshold: float = 3.0):
    mean = series.mean()
    std = series.std()
    z = (series - mean) / std if std > 0 else pd.Series(0, index=series.index)
    mask = z.abs() > threshold
    info = {"mean": round(float(mean), 4), "std": round(float(std), 4),
            "threshold": threshold, "anomaly_count": int(mask.sum())}
    return mask, info


def detect_daily_anomalies(orders: pd.DataFrame) -> dict:
    completed = orders[orders["status"] == "completed"].copy()
    completed["order_date"] = pd.to_datetime(completed["order_ts"]).dt.date

    daily = completed.groupby("order_date").agg(
        revenue=("net_revenue", "sum"),
        orders=("order_id", "count"),
        avg_order_value=("net_revenue", "mean"),
    ).reset_index()

    results = {}
    for col in ["revenue", "orders", "avg_order_value"]:
        if col in daily.columns:
            mask_iqr, info_iqr = detect_iqr_anomalies(daily[col])
            mask_z, info_z = detect_zscore_anomalies(daily[col])
            anomalous_days = daily[mask_iqr | mask_z].to_dict(orient="records")
            for d in anomalous_days:
                d["order_date"] = str(d["order_date"])
            results[col] = {"iqr": info_iqr, "zscore": info_z, "anomalous_days": anomalous_days[:10]}
    return results


def detect_product_anomalies(products: pd.DataFrame) -> dict:
    active = products[products["total_revenue"] > 0].copy()
    if len(active) == 0:
        return {}
    mask, info = detect_iqr_anomalies(active["margin_pct"])
    anomalous = active[mask][["product_id", "product_name", "category", "margin_pct", "total_revenue"]]
    return {
        "margin_anomalies": {
            "stats": info,
            "products": anomalous.to_dict(orient="records"),
        }
    }


def run_anomaly_detection(data: dict) -> dict:
    print("=" * 60)
    print("Phase 8a: Anomaly Detection")
    print("=" * 60)

    daily = detect_daily_anomalies(data["orders"])
    product = detect_product_anomalies(data["products"])
    results = {"daily": daily, "products": product}

    with open(METRICS_DIR / "anomaly_detection.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    total_anomalies = sum(len(v.get("anomalous_days", [])) for v in daily.values())
    print(f"  Detected {total_anomalies} daily anomalies")
    print("  Saved to anomaly_detection.json")

    print("\nPhase 8a complete.\n")
    return results