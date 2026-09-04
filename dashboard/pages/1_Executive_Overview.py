"""Executive Overview - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.components.kpi_cards import render_revenue_kpis
from dashboard.components.charts import revenue_trend_chart
from dashboard.components.filters import apply_filters
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct

st.set_page_config(page_title="Executive Overview", page_icon="📊", layout="wide")

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
.insight-card {
    background: linear-gradient(135deg, #f5f7ff 0%, #e8eaf6 100%);
    border-left: 4px solid #3949ab;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
}
.insight-card h4 { margin: 0 0 0.3rem; font-size: 0.95rem; color: #1a237e; }
.insight-card p { margin: 0.2rem 0; font-size: 0.85rem; color: #333; }
.insight-card .impact {
    display: inline-block;
    background: #e8f5e9;
    color: #2e7d32;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 0.3rem;
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

st.markdown('<div class="section-header">Executive Overview</div>', unsafe_allow_html=True)

revenue = metrics.get("revenue", {})
if revenue:
    render_revenue_kpis(revenue)
else:
    st.markdown('<div class="empty-state">Revenue KPIs not available.</div>', unsafe_allow_html=True)

col_trend, col_status = st.columns([3, 2])
with col_trend:
    monthly = metrics.get("monthly", [])
    if monthly:
        st.plotly_chart(revenue_trend_chart(monthly), use_container_width=True)
    else:
        st.markdown('<div class="empty-state">Monthly revenue data not available.</div>', unsafe_allow_html=True)

with col_status:
    if figure_path("status_analysis.png").exists():
        st.image(figure_path("status_analysis.png"), caption="Order Status Breakdown", use_container_width=True)
    else:
        st.markdown('<div class="empty-state">Status analysis figure not found.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Top Recommendations</div>', unsafe_allow_html=True)
recommendations = metrics.get("recommendations", [])
if recommendations:
    top_insights = [r for r in recommendations if r.get("priority") == "High"]
    if not top_insights:
        top_insights = recommendations[:3]
    cards_cols = st.columns(min(len(top_insights), 3))
    for i, rec in enumerate(top_insights[:3]):
        with cards_cols[i]:
            impact_html = ""
            if rec.get("expected_impact"):
                impact_html = f'<div class="impact">{rec["expected_impact"]}</div>'
            st.markdown(
                f'<div class="insight-card">'
                f'<h4>{rec.get("category", "General")}</h4>'
                f'<p><strong>Finding:</strong> {rec.get("finding", "N/A")}</p>'
                f'<p><strong>Recommendation:</strong> {rec.get("recommendation", "N/A")}</p>'
                f'{impact_html}'
                f'</div>',
                unsafe_allow_html=True,
            )
else:
    st.markdown('<div class="empty-state">No recommendations available.</div>', unsafe_allow_html=True)

with st.expander("Methodology & Limitations"):
    st.markdown("""
    - Data covers orders from 2024.
    - Revenue figures are based on completed and refunded orders; cancellations excluded from net revenue.
    - KPIs are computed at pipeline level from processed data.
    - Charts may update as new data is ingested.
    """)
