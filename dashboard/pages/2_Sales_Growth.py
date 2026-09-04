"""Sales & Growth - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.utils.theme import inject_global_css, render_page_header, render_section_header, render_empty_state
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct
from dashboard.components.charts import revenue_trend_chart, orders_trend_chart, aov_trend_chart, growth_rate_chart
from dashboard.components.filters import apply_filters, count_active_filters
from dashboard.components.header import render_app_header

st.set_page_config(page_title="Sales & Growth", page_icon="📈", layout="wide")
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
render_page_header("Sales & Growth", "Where is growth coming from?", badge=badge)

# ── KPI Strip ───────────────────────────────────────────────────────────────
monthly = metrics.get("monthly", [])
if monthly:
    latest = monthly[-1]
    prev = monthly[-2] if len(monthly) > 1 else None
    rev_delta = (latest.get("gross_revenue", 0) - prev.get("gross_revenue", 0)) / prev.get("gross_revenue", 1) if prev else None
    orders_delta = (latest.get("orders", 0) - prev.get("orders", 0)) / prev.get("orders", 1) if prev else None
    aov_delta = (latest.get("avg_order_value", 0) - prev.get("avg_order_value", 0)) / prev.get("avg_order_value", 1) if prev else None

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.metric("Latest Revenue", fmt_currency(latest.get("gross_revenue", 0)), delta=fmt_pct(rev_delta) if rev_delta else None)
    with kpi_cols[1]:
        st.metric("Latest Orders", fmt_number(latest.get("orders", 0)), delta=fmt_pct(orders_delta) if orders_delta else None)
    with kpi_cols[2]:
        st.metric("Latest AOV", fmt_currency(latest.get("avg_order_value", 0)), delta=fmt_pct(aov_delta) if aov_delta else None)
    with kpi_cols[3]:
        total_rev = sum(m.get("gross_revenue", 0) for m in monthly)
        st.metric("YTD Revenue", fmt_currency(total_rev))

# ── Main Visualizations ─────────────────────────────────────────────────────
render_section_header("Revenue & Orders Trend", icon="📈")

if monthly:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(revenue_trend_chart(monthly), use_container_width=True)
    with col2:
        st.plotly_chart(orders_trend_chart(monthly), use_container_width=True)

    render_section_header("Average Order Value", icon="🎯")
    st.plotly_chart(aov_trend_chart(monthly), use_container_width=True)
else:
    render_empty_state("Monthly trend data not available")

# ── Growth Rate Analysis ────────────────────────────────────────────────────
render_section_header("Growth Rate Analysis", icon="📊")

if monthly:
    st.plotly_chart(growth_rate_chart(monthly), use_container_width=True)

# ── Growth Rates Table ──────────────────────────────────────────────────────
render_section_header("Month-over-Month Growth Rates", icon="📋")

if monthly:
    growth_data = []
    for m in monthly:
        growth_data.append({
            "Month": m.get("order_month", ""),
            "Revenue": fmt_currency(m.get("gross_revenue", 0)),
            "Orders": fmt_number(m.get("orders", 0)),
            "AOV": fmt_currency(m.get("avg_order_value", 0)),
            "Rev MoM": fmt_pct(m.get("revenue_mom_growth")) if m.get("revenue_mom_growth") is not None else "N/A",
            "Orders MoM": fmt_pct(m.get("orders_mom_growth")) if m.get("orders_mom_growth") is not None else "N/A",
        })
    growth_df = pd.DataFrame(growth_data)
    st.dataframe(growth_df, use_container_width=True, hide_index=True)
else:
    render_empty_state("Growth rate data not available")

# ── Moving Averages ─────────────────────────────────────────────────────────
render_section_header("Moving Average Trends", icon="📉")

if figure_path("monthly_trends.png").exists():
    st.image(figure_path("monthly_trends.png"), caption="Monthly Revenue & Orders with Moving Averages", use_container_width=True)
else:
    render_empty_state("Moving average figure not available")
