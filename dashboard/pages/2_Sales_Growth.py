"""Sales & Growth - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.components.charts import revenue_trend_chart, orders_trend_chart, aov_trend_chart
from dashboard.components.filters import apply_filters
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct

st.set_page_config(page_title="Sales & Growth", page_icon="📈", layout="wide")

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
.growth-positive { color: #2e7d32; font-weight: 600; }
.growth-negative { color: #c62828; font-weight: 600; }
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

st.markdown('<div class="section-header">Sales & Growth</div>', unsafe_allow_html=True)

monthly = metrics.get("monthly", [])
if monthly:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(revenue_trend_chart(monthly), use_container_width=True)
    with col2:
        st.plotly_chart(orders_trend_chart(monthly), use_container_width=True)
    st.plotly_chart(aov_trend_chart(monthly), use_container_width=True)
else:
    st.markdown('<div class="empty-state">Monthly trend data not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Month-over-Month Growth Rates</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="empty-state">Growth rate data not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Moving Average Trends</div>', unsafe_allow_html=True)
if figure_path("monthly_trends.png").exists():
    st.image(figure_path("monthly_trends.png"), caption="Monthly Revenue & Orders with Moving Averages", use_container_width=True)
else:
    st.markdown('<div class="empty-state">Moving average figure not available.</div>', unsafe_allow_html=True)

with st.expander("Methodology & Limitations"):
    st.markdown("""
    - Month-over-month growth is calculated sequentially; first month shows N/A.
    - AOV is computed as gross revenue divided by orders per month.
    - Moving averages smooth short-term fluctuations for trend visibility.
    - Cancellations are excluded from completed order metrics.
    """)
