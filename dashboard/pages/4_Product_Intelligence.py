"""Product Intelligence - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.components.charts import category_bar_chart
from dashboard.components.kpi_cards import render_kpi_row
from dashboard.components.filters import apply_filters
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct

st.set_page_config(page_title="Product Intelligence", page_icon="📦", layout="wide")

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

st.markdown('<div class="section-header">Product Intelligence</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Category Performance</div>', unsafe_allow_html=True)
categories = metrics.get("categories", [])
if categories:
    st.plotly_chart(category_bar_chart(categories), use_container_width=True)
    total_rev = sum(c.get("total_revenue", 0) for c in categories)
    total_margin = sum(c.get("total_margin", 0) for c in categories)
    total_products = sum(c.get("product_count", 0) for c in categories)
    render_kpi_row([
        {"label": "Total Revenue", "value": total_rev, "format": "currency", "icon": "💰"},
        {"label": "Total Margin", "value": total_margin, "format": "currency", "icon": "📊"},
        {"label": "Total Products", "value": total_products, "format": "number", "icon": "📦"},
        {"label": "Avg Margin %", "value": total_margin / total_rev if total_rev else 0, "format": "pct", "icon": "⚖️"},
    ])
else:
    st.markdown('<div class="empty-state">Category data not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
top_products = metrics.get("top_products", {})
products_list = top_products.get("top_products", []) if isinstance(top_products, dict) else []
if products_list:
    prod_df = pd.DataFrame(products_list)
    display_df = prod_df[["product_name", "category", "total_revenue", "total_units_sold", "margin_pct"]].head(10)
    display_df.columns = ["Product", "Category", "Revenue", "Units Sold", "Margin %"]
    display_df["Revenue"] = display_df["Revenue"].apply(lambda x: fmt_currency(x))
    display_df["Margin %"] = display_df["Margin %"].apply(lambda x: fmt_pct(x))
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.markdown('<div class="empty-state">Top products data not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Product Margin Analysis</div>', unsafe_allow_html=True)
if categories:
    margin_df = pd.DataFrame(categories)
    margin_df = margin_df.sort_values("margin_pct", ascending=False)
    margin_display = margin_df[["category", "total_revenue", "total_margin", "margin_pct", "avg_selling_price"]]
    margin_display.columns = ["Category", "Revenue", "Margin", "Margin %", "Avg Price"]
    margin_display["Revenue"] = margin_display["Revenue"].apply(lambda x: fmt_currency(x))
    margin_display["Margin"] = margin_display["Margin"].apply(lambda x: fmt_currency(x))
    margin_display["Margin %"] = margin_display["Margin %"].apply(lambda x: fmt_pct(x))
    margin_display["Avg Price"] = margin_display["Avg Price"].apply(lambda x: fmt_currency(x))
    st.dataframe(margin_display, use_container_width=True, hide_index=True)

st.markdown('<div class="section-header">Category Analysis Detail</div>', unsafe_allow_html=True)
if figure_path("category_analysis.png").exists():
    st.image(figure_path("category_analysis.png"), caption="Category Analysis Overview", use_container_width=True)
else:
    st.markdown('<div class="empty-state">Category analysis figure not available.</div>', unsafe_allow_html=True)

with st.expander("Methodology & Limitations"):
    st.markdown("""
    - Revenue is based on selling price times quantity; margin is (unit_price - unit_cost) * quantity.
    - Margin % is calculated per category as total_margin / total_revenue.
    - Top products are ranked by total revenue across all orders.
    - Product catalog covers 120 SKUs across 6 categories.
    """)
