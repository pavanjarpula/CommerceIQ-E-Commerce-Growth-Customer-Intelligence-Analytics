"""Regional Performance - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.components.charts import country_bar_chart, channel_bar_chart
from dashboard.components.kpi_cards import render_kpi_row
from dashboard.components.filters import apply_filters
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct

st.set_page_config(page_title="Regional Performance", page_icon="🌍", layout="wide")

PAGE_CSS = """
<style>
.section-header {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1a237e;
    padding: 0.6rem 0 0.3rem;
    border-bottom: 2px solid #e8eaf6;
    margin-bottom: 0.5rem;
}
.empty-state {
    text-align: center;
    padding: 2rem;
    color: #9e9e9e;
    font-size: 1rem;
}
</style>
"""
st.markdown(PAGE_CSS, unsafe_allow_html=True)

metrics = st.session_state.get("metrics", load_all_metrics())
orders = load_orders()
customers = load_customers()
products = load_products()
filters = st.session_state.get("filters", {})

filtered_orders = apply_filters(orders, filters, customers)

if filtered_orders.empty:
    st.markdown('<div class="empty-state">No orders match the current filters. Try broadening your filter criteria.</div>', unsafe_allow_html=True)
    st.stop()

st.markdown('<div class="section-header">Regional Performance</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Revenue by Country</div>', unsafe_allow_html=True)
countries = metrics.get("countries", [])
if countries:
    st.plotly_chart(country_bar_chart(countries), use_container_width=True)
    total_rev = sum(c.get("total_revenue", 0) for c in countries)
    total_orders = sum(c.get("total_orders", 0) for c in countries)
    total_customers = sum(c.get("unique_customers", 0) for c in countries)
    render_kpi_row([
        {"label": "Total Revenue", "value": total_rev, "format": "currency", "icon": "💰"},
        {"label": "Total Orders", "value": total_orders, "format": "number", "icon": "📦"},
        {"label": "Total Customers", "value": total_customers, "format": "number", "icon": "👥"},
        {"label": "Countries", "value": len(countries), "format": "number", "icon": "🌍"},
    ])
else:
    st.markdown('<div class="empty-state">Country data not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Revenue by Channel</div>', unsafe_allow_html=True)
channels = metrics.get("channels", [])
if channels:
    st.plotly_chart(channel_bar_chart(channels), use_container_width=True)
else:
    st.markdown('<div class="empty-state">Channel data not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Country & Channel Analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if figure_path("country_analysis.png").exists():
        st.image(figure_path("country_analysis.png"), caption="Country Analysis", use_container_width=True)
    else:
        st.markdown('<div class="empty-state">Country analysis figure not available.</div>', unsafe_allow_html=True)
with col2:
    if figure_path("channel_analysis.png").exists():
        st.image(figure_path("channel_analysis.png"), caption="Channel Analysis", use_container_width=True)
    else:
        st.markdown('<div class="empty-state">Channel analysis figure not available.</div>', unsafe_allow_html=True)

with st.expander("Methodology & Limitations"):
    st.markdown("""
    - Country is derived from customer location; orders are attributed to customer's country.
    - Channel is based on the customer's acquisition channel.
    - Revenue share percentages are computed relative to total revenue.
    - 8 countries and 6 channels are represented in the dataset.
    """)
