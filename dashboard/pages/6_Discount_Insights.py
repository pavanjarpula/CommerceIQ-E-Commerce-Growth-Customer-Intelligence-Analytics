"""Margin & Pricing Insights - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, load_processed, figure_path
from dashboard.components.charts import margin_by_category_chart
from dashboard.components.kpi_cards import render_kpi_row
from dashboard.components.filters import apply_filters
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct

st.set_page_config(page_title="Margin & Pricing Insights", page_icon="💰", layout="wide")

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

st.markdown('<div class="section-header">Margin & Pricing Insights</div>', unsafe_allow_html=True)

revenue = metrics.get("revenue", {})
if revenue:
    render_kpi_row([
        {"label": "Gross Margin", "value": revenue.get("total_gross_margin", 0), "format": "currency", "icon": "💰"},
        {"label": "Margin %", "value": revenue.get("margin_pct", 0), "format": "pct", "icon": "📊"},
        {"label": "Avg Order Margin", "value": revenue.get("avg_order_margin", 0), "format": "currency", "icon": "📈"},
        {"label": "Avg Items/Order", "value": revenue.get("avg_items_per_order", 0), "format": "number", "icon": "🛒"},
    ])

st.markdown('<div class="section-header">Margin Analysis by Category</div>', unsafe_allow_html=True)
cat_profit = metrics.get("category_profitability", [])
if cat_profit:
    st.plotly_chart(margin_by_category_chart(cat_profit), use_container_width=True)

    cat_df = pd.DataFrame(cat_profit).sort_values("total_margin", ascending=False)
    margin_display = cat_df[["category", "total_revenue", "total_margin", "avg_margin_pct", "revenue_per_product"]]
    margin_display.columns = ["Category", "Revenue", "Margin", "Avg Margin %", "Revenue/Product"]
    margin_display["Revenue"] = margin_display["Revenue"].apply(lambda x: fmt_currency(x))
    margin_display["Margin"] = margin_display["Margin"].apply(lambda x: fmt_currency(x))
    margin_display["Avg Margin %"] = margin_display["Avg Margin %"].apply(lambda x: fmt_pct(x))
    margin_display["Revenue/Product"] = margin_display["Revenue/Product"].apply(lambda x: fmt_currency(x))
    st.dataframe(margin_display, use_container_width=True, hide_index=True)
else:
    st.markdown('<div class="empty-state">Category profitability data not available.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Cost Structure Analysis</div>', unsafe_allow_html=True)
if not products.empty:
    products_df = products.copy()
    products_df["margin_pct"] = (products_df["unit_price"] - products_df["unit_cost"]) / products_df["unit_price"]
    products_df["cost_ratio"] = products_df["unit_cost"] / products_df["unit_price"]

    col1, col2 = st.columns(2)
    with col1:
        fig_margin = px.histogram(products_df, x="margin_pct", nbins=20, title="Product Margin Distribution",
                                  color_discrete_sequence=["#4CAF50"])
        fig_margin.update_layout(xaxis_title="Margin %", yaxis_title="Count", margin=dict(t=40, b=40))
        st.plotly_chart(fig_margin, use_container_width=True)
    with col2:
        fig_cost = px.histogram(products_df, x="cost_ratio", nbins=20, title="Cost-to-Price Ratio Distribution",
                                color_discrete_sequence=["#FF9800"])
        fig_cost.update_layout(xaxis_title="Cost/Price Ratio", yaxis_title="Count", margin=dict(t=40, b=40))
        st.plotly_chart(fig_cost, use_container_width=True)
else:
    st.markdown('<div class="empty-state">Product data not available for cost analysis.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Pricing Tier Analysis</div>', unsafe_allow_html=True)
order_items = load_processed("order_items")
if not products.empty and not order_items.empty:
    item_products = order_items.merge(products[["product_id", "unit_cost"]], on="product_id", how="left")
    item_products["line_revenue"] = item_products["quantity"] * item_products["unit_price"]
    item_products["line_margin"] = item_products["quantity"] * (item_products["unit_price"] - item_products["unit_cost"])

    bins = [0, 20, 40, 60, 80, 120, 500]
    labels = ["<$20", "$20-$40", "$40-$60", "$60-$80", "$80-$120", "$120+"]
    item_products["price_tier"] = pd.cut(item_products["unit_price"], bins=bins, labels=labels, right=False)

    tier_summary = item_products.groupby("price_tier", observed=False).agg(
        total_revenue=("line_revenue", "sum"),
        total_margin=("line_margin", "sum"),
        item_count=("order_item_id", "count"),
    ).reset_index()
    tier_summary["margin_pct"] = tier_summary["total_margin"] / tier_summary["total_revenue"]

    fig_tier = px.bar(tier_summary, x="price_tier", y="total_revenue", title="Revenue by Price Tier",
                      color="margin_pct", color_continuous_scale="Greens")
    fig_tier.update_layout(xaxis_title="Price Tier", yaxis_title="Revenue", margin=dict(t=40, b=40))
    st.plotly_chart(fig_tier, use_container_width=True)
else:
    st.markdown('<div class="empty-state">Insufficient data for pricing tier analysis.</div>', unsafe_allow_html=True)

with st.expander("Methodology & Limitations"):
    st.markdown("""
    - Dataset does not contain explicit discount fields. Margin analysis uses (unit_price - unit_cost) / unit_price.
    - Cost ratio represents unit_cost / unit_price; lower values indicate higher pricing power.
    - Price tiers are defined at unit_price level per order item.
    - Margin anomalies were checked via IQR method; no anomalies detected in the product catalog.
    """)
