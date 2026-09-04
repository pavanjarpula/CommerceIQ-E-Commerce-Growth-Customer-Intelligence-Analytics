"""Insights & Decisions - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.components.charts import channel_bar_chart
from dashboard.components.filters import apply_filters
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct

st.set_page_config(page_title="Insights & Decisions", page_icon="💡", layout="wide")

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
.rec-high { border-left: 4px solid #e53935; }
.rec-medium { border-left: 4px solid #fb8c00; }
.rec-low { border-left: 4px solid #43a047; }
.empty-state {
    text-align: center;
    padding: 2rem;
    color: #9e9e9e;
    font-size: 1rem;
}
.anomaly-card {
    background: #fff8e1;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
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

st.markdown('<div class="section-header">Insights & Decisions</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Strategic Recommendations</div>', unsafe_allow_html=True)
recs = metrics.get("recommendations", [])
if recs:
    priority_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    priority_cls = {"High": "rec-high", "Medium": "rec-medium", "Low": "rec-low"}
    for rec in recs:
        priority = rec.get("priority", "Medium")
        icon = priority_icons.get(priority, "⚪")
        cls = priority_cls.get(priority, "")
        impact_html = f"<br><em style='color:#2e7d32;font-size:0.85rem'>Expected Impact: {rec['expected_impact']}</em>" if rec.get("expected_impact") else ""
        with st.expander(f"{icon} [{priority}] {rec.get('category', 'General')} — {rec.get('finding', '')[:80]}"):
            st.markdown(f"**Finding:** {rec.get('finding', 'N/A')}")
            st.markdown(f"**Recommendation:** {rec.get('recommendation', 'N/A')}")
            if rec.get("expected_impact"):
                st.success(f"**Expected Impact:** {rec['expected_impact']}")
else:
    st.markdown('<div class="empty-state">No recommendations available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Channel ROI Analysis</div>', unsafe_allow_html=True)
channel_roi = metrics.get("channel_roi", [])
if channel_roi:
    st.plotly_chart(channel_bar_chart(channel_roi, metric="total_revenue", title="Channel Revenue vs Margin"), use_container_width=True)
    roi_df = pd.DataFrame(channel_roi).sort_values("total_revenue", ascending=False)
    roi_display = roi_df[["channel", "total_orders", "total_revenue", "avg_order_value",
                          "unique_customers", "revenue_per_customer"]]
    roi_display.columns = ["Channel", "Orders", "Revenue", "AOV", "Customers", "Rev/Customer"]
    roi_display["Revenue"] = roi_display["Revenue"].apply(lambda x: fmt_currency(x))
    roi_display["AOV"] = roi_display["AOV"].apply(lambda x: fmt_currency(x))
    roi_display["Rev/Customer"] = roi_display["Rev/Customer"].apply(lambda x: fmt_currency(x))
    st.dataframe(roi_display, use_container_width=True, hide_index=True)
else:
    st.markdown('<div class="empty-state">Channel ROI data not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Anomaly Detection Summary</div>', unsafe_allow_html=True)
anomaly = metrics.get("anomaly", {})
daily = anomaly.get("daily", {})

col1, col2, col3 = st.columns(3)
with col1:
    rev_anomaly = daily.get("revenue", {})
    st.metric("Revenue Anomalies (IQR)", rev_anomaly.get("iqr", {}).get("anomaly_count", 0))
with col2:
    st.metric("Revenue Anomalies (Z-Score)", rev_anomaly.get("zscore", {}).get("anomaly_count", 0))
with col3:
    orders_anomaly = daily.get("orders", {})
    st.metric("Order Anomalies (IQR)", orders_anomaly.get("iqr", {}).get("anomaly_count", 0))

aov_anomaly = daily.get("avg_order_value", {})
anomalous_days = aov_anomaly.get("anomalous_days", [])
if anomalous_days:
    st.markdown(
        f'<div class="anomaly-card"><strong>{len(anomalous_days)} anomalous AOV days detected</strong> (IQR method). '
        f'These days show unusually high or low average order values relative to the overall distribution.</div>',
        unsafe_allow_html=True,
    )

products_anomaly = anomaly.get("products", {}).get("margin_anomalies", {})
prod_stats = products_anomaly.get("stats", {})
if prod_stats:
    st.markdown(
        f'<div class="anomaly-card"><strong>Product Margin Anomalies:</strong> '
        f'{prod_stats.get("anomaly_count", 0)} products flagged (IQR method)</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="section-header">Statistical Test Results</div>', unsafe_allow_html=True)
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

with st.expander("Methodology & Limitations"):
    st.markdown("""
    - Recommendations are generated from RFM segmentation, channel analysis, and geographic performance.
    - Scenario analysis models channel ROI using aggregated metrics from the processed dataset.
    - Anomaly detection uses both IQR and Z-score methods on daily aggregated metrics.
    - All insights are derived from historical data; forward-looking predictions require additional modeling.
    """)
