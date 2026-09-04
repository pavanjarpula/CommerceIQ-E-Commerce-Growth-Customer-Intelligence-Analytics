"""Customer Intelligence - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.components.charts import rfm_pie_chart, rfm_revenue_bar
from dashboard.components.kpi_cards import render_segment_kpis
from dashboard.components.filters import apply_filters
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct

st.set_page_config(page_title="Customer Intelligence", page_icon="👥", layout="wide")

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

st.markdown('<div class="section-header">Customer Intelligence</div>', unsafe_allow_html=True)

rfm = metrics.get("rfm", {})
if rfm:
    render_segment_kpis(
        segments=rfm.get("segments", []),
        total_customers=rfm.get("total_customers", 0),
        active_customers=rfm.get("active_customers", 0),
    )
else:
    st.markdown('<div class="empty-state">Customer metrics not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">RFM Segment Distribution</div>', unsafe_allow_html=True)
segments = rfm.get("segments", [])
if segments:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(rfm_pie_chart(segments), use_container_width=True)
    with col2:
        st.plotly_chart(rfm_revenue_bar(segments), use_container_width=True)
else:
    st.markdown('<div class="empty-state">RFM segment data not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Segment Details</div>', unsafe_allow_html=True)
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
    st.dataframe(detail_df, use_container_width=True, hide_index=True)
else:
    st.markdown('<div class="empty-state">RFM segment details not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">RFM Distribution</div>', unsafe_allow_html=True)
if figure_path("rfm_distribution.png").exists():
    st.image(figure_path("rfm_distribution.png"), caption="RFM Score Distribution", use_container_width=True)
else:
    st.markdown('<div class="empty-state">RFM distribution figure not available.</div>', unsafe_allow_html=True)

with st.expander("Methodology & Limitations"):
    st.markdown("""
    - RFM segmentation uses Recency (days since last order), Frequency (total orders), and Monetary (total revenue) scores.
    - Segments are assigned based on percentile-based thresholds: Champions, Loyal, Potential Loyalists, New, At Risk, Lost, Others.
    - No Orders segment includes customers with zero orders in the dataset.
    - CLV equals cumulative monetary value per customer.
    """)
