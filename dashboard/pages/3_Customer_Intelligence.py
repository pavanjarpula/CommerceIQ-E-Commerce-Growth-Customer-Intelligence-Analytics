"""Customer Intelligence - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.utils.theme import inject_global_css, render_page_header, render_section_header, render_empty_state
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct
from dashboard.components.charts import rfm_pie_chart, rfm_revenue_bar
from dashboard.components.kpi_cards import render_segment_kpis
from dashboard.components.filters import apply_filters, count_active_filters
from dashboard.components.tables import render_styled_table
from dashboard.components.header import render_app_header

st.set_page_config(page_title="Customer Intelligence", page_icon="👥", layout="wide")
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
render_page_header("Customer Intelligence", "Who are our most valuable customers?", badge=badge)

# ── Customer KPIs ───────────────────────────────────────────────────────────
rfm = metrics.get("rfm", {})
if rfm:
    render_segment_kpis(
        segments=rfm.get("segments", []),
        total_customers=rfm.get("total_customers", 0),
        active_customers=rfm.get("active_customers", 0),
    )
else:
    render_empty_state("Customer metrics not available")

# ── RFM Segment Landscape ───────────────────────────────────────────────────
render_section_header("RFM Segment Landscape", icon="👥")

segments = rfm.get("segments", [])
if segments:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(rfm_pie_chart(segments), use_container_width=True)
    with col2:
        st.plotly_chart(rfm_revenue_bar(segments), use_container_width=True)
else:
    render_empty_state("RFM segment data not available")

# ── Customer Segment Economics ──────────────────────────────────────────────
render_section_header("Customer Segment Economics", icon="💰")

rfm_details = metrics.get("rfm_details", {})
detail_segments = rfm_details.get("segments", [])
if detail_segments:
    detail_df = pd.DataFrame(detail_segments)
    detail_df = detail_df[["rfm_segment", "customer_count", "avg_recency", "avg_frequency",
                           "avg_monetary", "revenue_share", "description"]]
    detail_df.columns = ["Segment", "Customers", "Avg Recency (days)", "Avg Frequency",
                         "Avg Revenue", "Revenue Share %", "Description"]
    detail_df["Revenue Share %"] = detail_df["Revenue Share %"].apply(lambda x: fmt_pct(x / 100) if pd.notna(x) else "N/A")
    detail_df["Avg Revenue"] = detail_df["Avg Revenue"].apply(lambda x: fmt_currency(x))

    render_styled_table(
        detail_df,
        columns={
            "Segment": "Segment",
            "Customers": "Customers",
            "Avg Recency (days)": "Avg Recency",
            "Avg Frequency": "Avg Frequency",
            "Avg Revenue": "Avg Revenue",
            "Revenue Share %": "Rev Share",
            "Description": "Description",
        },
    )
else:
    render_empty_state("RFM segment details not available")

# ── RFM Distribution ────────────────────────────────────────────────────────
render_section_header("RFM Score Distribution", icon="📊")

if figure_path("rfm_distribution.png").exists():
    st.image(figure_path("rfm_distribution.png"), caption="RFM Score Distribution", use_container_width=True)
else:
    render_empty_state("RFM distribution figure not available")
