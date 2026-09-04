"""Methodology & Data Quality - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.utils.formatting import fmt_number

st.set_page_config(page_title="Methodology & Data Quality", page_icon="📋", layout="wide")

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
.dataset-card {
    background: linear-gradient(135deg, #f5f7ff 0%, #e8eaf6 100%);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.dataset-card h3 { margin: 0 0 0.5rem; color: #1a237e; font-size: 1.05rem; }
.dataset-card p { margin: 0.2rem 0; font-size: 0.9rem; color: #333; }
.validation-pass { color: #2e7d32; font-weight: 700; }
.validation-fail { color: #c62828; font-weight: 700; }
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

st.markdown('<div class="section-header">Methodology & Data Quality</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="dataset-card">'
    '<h3>Dataset Overview</h3>'
    '<p>This dashboard analyzes e-commerce transaction data covering orders, customers, products, and order items. '
    'All data has been profiled and validated through an automated pipeline.</p>'
    '</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Orders", fmt_number(len(orders)))
with col2:
    st.metric("Customers", fmt_number(len(customers)))
with col3:
    st.metric("Products", fmt_number(len(products)))
with col4:
    st.metric("Tables Profiled", 5)

st.markdown('<div class="section-header">Data Schema</div>', unsafe_allow_html=True)
schema_data = {
    "Table": ["orders", "orders", "orders", "orders", "customers", "customers", "customers", "customers",
              "products", "products", "products", "products", "products", "order_items", "order_items",
              "order_items", "order_items", "order_items"],
    "Column": ["order_id", "customer_id", "order_ts", "status", "customer_id", "signup_date", "channel", "country",
               "product_id", "product_name", "category", "unit_price", "unit_cost",
               "order_item_id", "order_id", "product_id", "quantity", "unit_price"],
    "Type": ["int64", "int64", "datetime64", "object", "int64", "object", "object", "object",
             "int64", "object", "object", "float64", "float64",
             "int64", "int64", "int64", "int64", "float64"],
    "Nulls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}
schema_df = pd.DataFrame(schema_data)
st.dataframe(schema_df, use_container_width=True, hide_index=True)

st.markdown('<div class="section-header">Validation Report</div>', unsafe_allow_html=True)
validation = metrics.get("validation", {})
checks = validation.get("checks", [])
if checks:
    passed = validation.get("passed", 0)
    failed = validation.get("failed", 0)
    total = validation.get("total_checks", 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Checks", total)
    with col2:
        st.metric("Passed", passed, delta=None)
    with col3:
        st.metric("Failed", failed, delta=None)

    check_df = pd.DataFrame(checks)
    check_df.columns = ["Check", "Status", "Detail"]
    st.dataframe(check_df, use_container_width=True, hide_index=True)
else:
    st.markdown('<div class="empty-state">Validation report not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Data Profile Summary</div>', unsafe_allow_html=True)
data_profile = metrics.get("data_profile", {})
for table_name in ["orders", "customers", "products", "order_items", "events"]:
    table_profile = data_profile.get(table_name, {})
    if not table_profile:
        continue
    with st.expander(f"{table_name.upper()} — {table_profile.get('rows', 0)} rows, {table_profile.get('columns', 0)} columns"):
        col_profiles = table_profile.get("column_profiles", {})
        if col_profiles:
            profile_rows = []
            for col_name, col_info in col_profiles.items():
                profile_rows.append({
                    "Column": col_name,
                    "Type": col_info.get("dtype", ""),
                    "Nulls": col_info.get("null_count", 0),
                    "Distinct": col_info.get("distinct", ""),
                    "Memory (MB)": table_profile.get("memory_mb", 0),
                })
            profile_df = pd.DataFrame(profile_rows)
            st.dataframe(profile_df, use_container_width=True, hide_index=True)

if figure_path("correlation_matrix.png").exists():
    st.markdown('<div class="section-header">Correlation Matrix</div>', unsafe_allow_html=True)
    st.image(figure_path("correlation_matrix.png"), caption="Correlation Matrix of Numeric Features", use_container_width=True)

with st.expander("Limitations"):
    st.markdown("""
    - **No Discount Data:** The dataset does not include discount or coupon fields. Margin analysis is based on unit_price vs unit_cost.
    - **No Returns/Refunds Detail:** Refunded orders are flagged by status but detailed refund reasons are not available.
    - **Channel Attribution:** Channel is assigned at customer level, not per-order; some orders may not reflect the actual acquisition channel.
    - **Date Range:** Data covers 2024 only; seasonal patterns may not be fully captured.
    - **Sample Size:** With 12,000 orders and 2,000 customers, some segments have limited observations for statistical power.
    - **Geographic Bias:** US accounts for 43% of revenue; international analysis may have smaller sample sizes.
    - **Event Data:** Web events (views, cart additions) are included but conversion funnel analysis is limited without session-level attribution.
    """)
