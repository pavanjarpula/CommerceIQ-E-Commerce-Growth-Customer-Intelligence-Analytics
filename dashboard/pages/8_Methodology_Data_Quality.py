"""Methodology & Data Quality - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.utils.theme import inject_global_css, render_page_header, render_section_header, render_empty_state
from dashboard.utils.formatting import fmt_number
from dashboard.components.methodology import render_pipeline_visualization, render_validation_summary, render_dataset_overview_card, render_methodology_step
from dashboard.components.header import render_app_header

st.set_page_config(page_title="Methodology & Data Quality", page_icon="📋", layout="wide")
inject_global_css()

metrics = st.session_state.get("metrics", load_all_metrics())
orders = load_orders()
customers = load_customers()
products = load_products()

render_app_header(metrics)

render_page_header("Methodology & Data Quality", "Can we trust the analysis?")

# ── Dataset Overview ────────────────────────────────────────────────────────
render_dataset_overview_card()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Orders", fmt_number(len(orders)))
with col2:
    st.metric("Customers", fmt_number(len(customers)))
with col3:
    st.metric("Products", fmt_number(len(products)))
with col4:
    st.metric("Tables Profiled", 5)

# ── Pipeline Visualization ──────────────────────────────────────────────────
render_section_header("Analytics Pipeline", icon="⚙️")

st.markdown(
    '<div class="ciq-card" style="margin-bottom:0.5rem;">'
    '<p style="margin:0;font-size:0.82rem;color:#475569;line-height:1.55;">'
    'The CommerceIQ analytics pipeline processes raw data through 9 stages, from ingestion to actionable insights. '
    'Each stage is automated, auditable, and produces intermediate outputs for validation.</p>'
    '</div>',
    unsafe_allow_html=True,
)

render_pipeline_visualization()

# ── Data Schema ─────────────────────────────────────────────────────────────
render_section_header("Data Schema", icon="🗄️")

schema_data = {
    "Table": ["orders", "orders", "orders", "orders", "customers", "customers", "customers", "customers",
              "products", "products", "products", "products", "products", "order_items", "order_items",
              "order_items", "order_items", "order_items", "events", "events", "events", "events", "events"],
    "Column": ["order_id", "customer_id", "order_ts", "status", "customer_id", "signup_date", "channel", "country",
               "product_id", "product_name", "category", "unit_price", "unit_cost",
               "order_item_id", "order_id", "product_id", "quantity", "unit_price",
               "event_id", "session_id", "customer_id", "event_type", "event_ts"],
    "Type": ["int64", "int64", "datetime64", "object", "int64", "object", "object", "object",
             "int64", "object", "object", "float64", "float64",
             "int64", "int64", "int64", "int64", "float64",
             "int64", "int64", "int64", "object", "datetime64"],
    "Nulls": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}
schema_df = pd.DataFrame(schema_data)
st.dataframe(schema_df, use_container_width=True, hide_index=True)

# ── Validation Report ───────────────────────────────────────────────────────
render_section_header("Validation Report", icon="✅")

validation = metrics.get("validation", {})
render_validation_summary(validation)

# ── Data Profile Summary ────────────────────────────────────────────────────
render_section_header("Data Profile Summary", icon="📊")

data_profile = metrics.get("data_profile", {})
for table_name in ["orders", "customers", "products", "order_items", "events"]:
    table_profile = data_profile.get(table_name, {})
    if not table_profile:
        continue
    with st.expander(f"{table_name.upper()} \u2014 {table_profile.get('rows', 0)} rows, {table_profile.get('columns', 0)} columns"):
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

# ── Methodology Steps ───────────────────────────────────────────────────────
render_section_header("Methodology", icon="📐")

methodology_steps = [
    ("Data Ingestion", "Download from HuggingFace, profile raw datasets"),
    ("Validation", "24 automated checks: referential integrity, null handling, type validation, business rules"),
    ("Cleaning", "Type casting, null handling, line_total computation"),
    ("Feature Engineering", "RFM scoring, cohort analysis, margin computation, customer/product features"),
    ("KPI Computation", "Revenue metrics, channel metrics, country metrics, category metrics"),
    ("SQL Analytics", "SQLite-based analytical queries for advanced insights"),
    ("Statistical Analysis", "Kruskal-Wallis, Shapiro-Wilk tests for significance"),
    ("Anomaly Detection", "IQR and Z-score methods on daily metrics and product margins"),
    ("Recommendations", "Evidence-based business recommendations with observation-evidence-implication-action framework"),
]

for i, (title, desc) in enumerate(methodology_steps, 1):
    render_methodology_step(i, title, desc)

# ── Correlation Matrix ──────────────────────────────────────────────────────
if figure_path("correlation_matrix.png").exists():
    render_section_header("Correlation Matrix", icon="🔗")
    st.image(figure_path("correlation_matrix.png"), caption="Correlation Matrix of Numeric Features", use_container_width=True)

# ── Limitations ─────────────────────────────────────────────────────────────
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
