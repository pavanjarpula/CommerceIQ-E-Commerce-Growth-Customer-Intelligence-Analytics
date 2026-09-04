"""Insights & Decisions - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.utils.theme import inject_global_css, render_page_header, render_section_header, render_empty_state
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct
from dashboard.components.charts import channel_bar_chart, anomaly_scatter
from dashboard.components.filters import apply_filters, count_active_filters
from dashboard.components.insights import render_recommendation_card, render_anomaly_card, render_evidence_block
from dashboard.components.header import render_app_header

st.set_page_config(page_title="Insights & Decisions", page_icon="💡", layout="wide")
inject_global_css()

metrics = st.session_state.get("metrics", load_all_metrics())
orders = load_orders()
customers = load_customers()
products = load_products()
filters = st.session_state.get("filters", {})

render_app_header(metrics)

filtered_orders = apply_filters(orders, filters, customers)

if filtered_orders.empty:
    render_empty_state("No matching records", "Try broadening the selected filters.")
    st.stop()

active_filters = count_active_filters(filters, orders)
badge = f"{active_filters} filter{'s' if active_filters != 1 else ''} active" if active_filters > 0 else ""
render_page_header("Insights & Decisions", "What should the business investigate or act on?", badge=badge)

# ── Strategic Recommendations ───────────────────────────────────────────────
render_section_header("Strategic Recommendations", icon="💡")

recs = metrics.get("recommendations", [])
if recs:
    for rec in recs:
        render_recommendation_card(rec)
else:
    render_empty_state("No recommendations available")

# ── Channel ROI Analysis ────────────────────────────────────────────────────
render_section_header("Channel ROI Analysis", icon="📡")

channel_roi = metrics.get("channel_roi", [])
if channel_roi:
    st.plotly_chart(channel_bar_chart(channel_roi, metric="total_revenue", title="Channel Revenue vs Margin"), use_container_width=True)
    roi_df = pd.DataFrame(channel_roi).sort_values("total_revenue", ascending=False)
    roi_display = roi_df[["channel", "total_orders", "total_revenue", "avg_order_value",
                          "unique_customers", "revenue_per_customer"]].copy()
    roi_display.columns = ["Channel", "Orders", "Revenue", "AOV", "Customers", "Rev/Customer"]
    roi_display["Revenue"] = roi_display["Revenue"].apply(lambda x: fmt_currency(x))
    roi_display["AOV"] = roi_display["AOV"].apply(lambda x: fmt_currency(x))
    roi_display["Rev/Customer"] = roi_display["Rev/Customer"].apply(lambda x: fmt_currency(x))
    st.dataframe(roi_display, use_container_width=True, hide_index=True)
else:
    render_empty_state("Channel ROI data not available")

# ── Anomaly Detection ──────────────────────────────────────────────────────
render_section_header("Anomaly Detection", icon="⚠️")

anomaly = metrics.get("anomaly", {})
daily = anomaly.get("daily", {})

col1, col2, col3 = st.columns(3)
with col1:
    rev_anomaly = daily.get("revenue", {})
    iqr_count = rev_anomaly.get("iqr", {}).get("anomaly_count", 0)
    zscore_count = rev_anomaly.get("zscore", {}).get("anomaly_count", 0)
    render_anomaly_card("Revenue (IQR)", iqr_count, "IQR Method",
                        severity="moderate" if iqr_count > 0 else "normal",
                        details=f"Z-score method: {zscore_count} anomalies")
with col2:
    orders_anomaly = daily.get("orders", {})
    o_iqr = orders_anomaly.get("iqr", {}).get("anomaly_count", 0)
    o_zscore = orders_anomaly.get("zscore", {}).get("anomaly_count", 0)
    render_anomaly_card("Orders (IQR)", o_iqr, "IQR Method",
                        severity="moderate" if o_iqr > 0 else "normal",
                        details=f"Z-score method: {o_zscore} anomalies")
with col3:
    aov_anomaly = daily.get("avg_order_value", {})
    aov_anomalous_days = aov_anomaly.get("anomalous_days", [])
    aov_count = len(aov_anomalous_days)
    render_anomaly_card("AOV (IQR)", aov_count, "IQR Method",
                        severity="moderate" if aov_count > 0 else "normal",
                        details="Unusually high or low average order values")

# ── Product Margin Anomalies ────────────────────────────────────────────────
products_anomaly = anomaly.get("products", {}).get("margin_anomalies", {})
prod_stats = products_anomaly.get("stats", {})
if prod_stats:
    render_anomaly_card("Product Margins", prod_stats.get("anomaly_count", 0), "IQR Method",
                        severity="moderate" if prod_stats.get("anomaly_count", 0) > 0 else "normal",
                        details="Products with margin significantly outside expected range")

# ── Statistical Test Results ────────────────────────────────────────────────
render_section_header("Statistical Test Results", icon="📋")

stat_tests = metrics.get("statistical_tests", {})
if stat_tests:
    test_rows = []
    for key, test_info in stat_tests.items():
        test_rows.append({
            "Test": key,
            "Method": test_info.get("test", ""),
            "Statistic": round(test_info.get("statistic", 0), 4),
            "p-value": round(test_info.get("p_value", 0), 4),
            "Significant": "Yes" if test_info.get("significant", False) else "No",
        })
    test_df = pd.DataFrame(test_rows)
    st.dataframe(test_df, use_container_width=True, hide_index=True)
else:
    render_empty_state("Statistical test results not available")
