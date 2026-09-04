"""Margin & Pricing Insights - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, load_processed, figure_path
from dashboard.utils.theme import inject_global_css, render_page_header, render_section_header, render_empty_state
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct
from dashboard.components.charts import margin_by_category_chart
from dashboard.components.kpi_cards import render_margin_kpis
from dashboard.components.filters import apply_filters, count_active_filters
from dashboard.components.insights import render_insight_card
from dashboard.components.header import render_app_header

st.set_page_config(page_title="Margin & Pricing Insights", page_icon="💰", layout="wide")
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
render_page_header("Margin & Pricing Insights", "Where are we making money?", badge=badge)

# ── Margin KPIs ─────────────────────────────────────────────────────────────
revenue = metrics.get("revenue", {})
if revenue:
    render_margin_kpis(revenue)

# ── Revenue != Profitability Callout ────────────────────────────────────────
render_section_header("Revenue vs Profitability", icon="💰")

render_insight_card(
    title="Revenue \u2260 Profitability",
    finding="High-revenue categories do not always correspond to high-margin categories. Margin % varies significantly across the product catalog, making profitability analysis essential for strategic pricing decisions.",
    impact="Strategic pricing insight",
    impact_type="info",
)

# ── Margin Analysis by Category ─────────────────────────────────────────────
render_section_header("Margin Analysis by Category", icon="📊")

cat_profit = metrics.get("category_profitability", [])
if cat_profit:
    st.plotly_chart(margin_by_category_chart(cat_profit), use_container_width=True)

    cat_df = pd.DataFrame(cat_profit).sort_values("total_margin", ascending=False)
    margin_display = cat_df[["category", "total_revenue", "total_margin", "avg_margin_pct", "revenue_per_product"]].copy()
    margin_display.columns = ["Category", "Revenue", "Margin", "Avg Margin %", "Revenue/Product"]
    margin_display["Revenue"] = margin_display["Revenue"].apply(lambda x: fmt_currency(x))
    margin_display["Margin"] = margin_display["Margin"].apply(lambda x: fmt_currency(x))
    margin_display["Avg Margin %"] = margin_display["Avg Margin %"].apply(lambda x: fmt_pct(x))
    margin_display["Revenue/Product"] = margin_display["Revenue/Product"].apply(lambda x: fmt_currency(x))
    st.dataframe(margin_display, use_container_width=True, hide_index=True)
else:
    render_empty_state("Category profitability data not available")

# ── Cost Structure Analysis ─────────────────────────────────────────────────
render_section_header("Cost Structure Analysis", icon="🔧")

if not products.empty:
    products_df = products.copy()
    products_df["margin_pct"] = (products_df["unit_price"] - products_df["unit_cost"]) / products_df["unit_price"]
    products_df["cost_ratio"] = products_df["unit_cost"] / products_df["unit_price"]

    col1, col2 = st.columns(2)
    with col1:
        fig_margin = px.histogram(products_df, x="margin_pct", nbins=20, title="Product Margin Distribution",
                                  color_discrete_sequence=["#059669"])
        fig_margin.update_layout(xaxis_title="Margin %", yaxis_title="Count", margin=dict(t=40, b=40))
        st.plotly_chart(fig_margin, use_container_width=True)
    with col2:
        fig_cost = px.histogram(products_df, x="cost_ratio", nbins=20, title="Cost-to-Price Ratio Distribution",
                                color_discrete_sequence=["#d97706"])
        fig_cost.update_layout(xaxis_title="Cost/Price Ratio", yaxis_title="Count", margin=dict(t=40, b=40))
        st.plotly_chart(fig_cost, use_container_width=True)
else:
    render_empty_state("Product data not available for cost analysis")

# ── Pricing Tier Analysis ───────────────────────────────────────────────────
render_section_header("Pricing Tier Analysis", icon="💲")

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
    render_empty_state("Insufficient data for pricing tier analysis")
