"""Regional Performance - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.utils.theme import inject_global_css, render_page_header, render_section_header, render_empty_state
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct
from dashboard.components.charts import country_bar_chart, channel_bar_chart
from dashboard.components.kpi_cards import render_kpi_row
from dashboard.components.filters import apply_filters, count_active_filters
from dashboard.components.header import render_app_header

st.set_page_config(page_title="Regional Performance", page_icon="🌍", layout="wide")
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
render_page_header("Regional Performance", "Which markets and channels perform best?", badge=badge)

# ── Regional KPIs ───────────────────────────────────────────────────────────
countries = metrics.get("countries", [])
if countries:
    total_rev = sum(c.get("total_revenue", 0) for c in countries)
    total_orders = sum(c.get("total_orders", 0) for c in countries)
    total_customers = sum(c.get("unique_customers", 0) for c in countries)
    render_kpi_row([
        {"label": "Total Revenue", "value": total_rev, "format": "currency"},
        {"label": "Total Orders", "value": total_orders, "format": "number"},
        {"label": "Total Customers", "value": total_customers, "format": "number"},
        {"label": "Markets", "value": len(countries), "format": "number"},
    ])

# ── Top Performing Markets ──────────────────────────────────────────────────
render_section_header("Revenue by Country", icon="🌍")

if countries:
    st.plotly_chart(country_bar_chart(countries), use_container_width=True)

    market_df = pd.DataFrame(countries).sort_values("total_revenue", ascending=False)
    market_display = market_df[["country", "total_revenue", "total_orders", "unique_customers"]].copy()
    market_display.columns = ["Country", "Revenue", "Orders", "Customers"]
    market_display["Revenue"] = market_display["Revenue"].apply(lambda x: fmt_currency(x))
    st.dataframe(market_display, use_container_width=True, hide_index=True)
else:
    render_empty_state("Country data not available")

# ── Top Performing Channels ─────────────────────────────────────────────────
render_section_header("Revenue by Channel", icon="📡")

channels = metrics.get("channels", [])
if channels:
    st.plotly_chart(channel_bar_chart(channels), use_container_width=True)

    channel_df = pd.DataFrame(channels).sort_values("total_revenue", ascending=False)
    channel_display = channel_df[["channel", "total_revenue", "total_orders", "unique_customers"]].copy()
    channel_display.columns = ["Channel", "Revenue", "Orders", "Customers"]
    channel_display["Revenue"] = channel_display["Revenue"].apply(lambda x: fmt_currency(x))
    st.dataframe(channel_display, use_container_width=True, hide_index=True)
else:
    render_empty_state("Channel data not available")

# ── Detailed Analysis ───────────────────────────────────────────────────────
render_section_header("Country & Channel Analysis", icon="📋")

col1, col2 = st.columns(2)
with col1:
    if figure_path("country_analysis.png").exists():
        st.image(figure_path("country_analysis.png"), caption="Country Analysis", use_container_width=True)
    else:
        render_empty_state("Country analysis figure not available")
with col2:
    if figure_path("channel_analysis.png").exists():
        st.image(figure_path("channel_analysis.png"), caption="Channel Analysis", use_container_width=True)
    else:
        render_empty_state("Channel analysis figure not available")
