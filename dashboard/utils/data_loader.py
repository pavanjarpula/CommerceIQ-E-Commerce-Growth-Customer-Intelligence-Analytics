"""Dashboard - Data Loader.

Loads pipeline outputs for dashboard consumption with caching.
"""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
METRICS_DIR = PROJECT_ROOT / "outputs" / "metrics"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


@st.cache_data
def load_json(name: str) -> dict:
    path = METRICS_DIR / f"{name}.json"
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


@st.cache_data
def load_processed(name: str) -> pd.DataFrame:
    path = PROCESSED_DIR / f"{name}.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_all_metrics() -> dict:
    monthly_raw = load_json("monthly_revenue")
    channel_raw = load_json("channel_metrics")
    country_raw = load_json("country_metrics")
    category_raw = load_json("category_metrics")
    top_products_raw = load_json("top_products")
    recommendations_raw = load_json("recommendations")
    scenario_raw = load_json("scenario_analysis")
    rfm_raw = load_json("rfm_summary")
    rfm_details_raw = load_json("rfm_segment_details")
    anomaly_raw = load_json("anomaly_detection")
    cohort_raw = load_json("cohort_summary")

    return {
        "revenue": load_json("revenue_metrics"),
        "monthly": monthly_raw.get("monthly", []) if isinstance(monthly_raw, dict) else [],
        "channels": channel_raw.get("channels", []) if isinstance(channel_raw, dict) else [],
        "countries": country_raw.get("countries", []) if isinstance(country_raw, dict) else [],
        "categories": category_raw.get("categories", []) if isinstance(category_raw, dict) else [],
        "top_products": top_products_raw.get("top_products", []) if isinstance(top_products_raw, dict) else [],
        "rfm": rfm_raw,
        "rfm_segments": rfm_raw.get("segments", []) if isinstance(rfm_raw, dict) else [],
        "rfm_details": rfm_details_raw,
        "cohort": cohort_raw,
        "anomaly": anomaly_raw,
        "scenario": scenario_raw,
        "channel_roi": scenario_raw.get("channel_roi", []) if isinstance(scenario_raw, dict) else [],
        "category_profitability": scenario_raw.get("category_profitability", []) if isinstance(scenario_raw, dict) else [],
        "recommendations": recommendations_raw.get("recommendations", []) if isinstance(recommendations_raw, dict) else [],
        "statistical_tests": load_json("statistical_tests"),
        "validation": load_json("validation_report"),
        "data_profile": load_json("data_profile"),
    }


@st.cache_data
def load_orders() -> pd.DataFrame:
    return load_processed("orders")


@st.cache_data
def load_customers() -> pd.DataFrame:
    return load_processed("customers")


@st.cache_data
def load_products() -> pd.DataFrame:
    return load_processed("products")


def figure_path(name: str) -> Path:
    return FIGURES_DIR / name