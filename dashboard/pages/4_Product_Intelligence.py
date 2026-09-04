"""Product Intelligence - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.utils.theme import inject_global_css, render_page_header, render_section_header, render_empty_state
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct
from dashboard.components.charts import category_bar_chart, revenue_vs_margin_scatter
from dashboard.components.kpi_cards import render_kpi_row
from dashboard.components.filters import apply_filters, count_active_filters
from dashboard.components.tables import render_styled_table
from dashboard.components.header import render_app_header

st.set_page_config(page_title="Product Intelligence", page_icon="📦", layout="wide")
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
render_page_header("Product Intelligence", "Which products and categories drive revenue and margin?", badge=badge)

# ── Category Performance Matrix ─────────────────────────────────────────────
render_section_header("Category Performance", icon="📦")

categories = metrics.get("categories", [])
if categories:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(category_bar_chart(categories), use_container_width=True)
    with col2:
        st.plotly_chart(revenue_vs_margin_scatter(categories), use_container_width=True)

    total_rev = sum(c.get("total_revenue", 0) for c in categories)
    total_margin = sum(c.get("total_margin", 0) for c in categories)
    total_products = sum(c.get("product_count", 0) for c in categories)
    render_kpi_row([
        {"label": "Total Revenue", "value": total_rev, "format": "currency"},
        {"label": "Total Margin", "value": total_margin, "format": "currency"},
        {"label": "Total Products", "value": total_products, "format": "number"},
        {"label": "Avg Margin %", "value": total_margin / total_rev if total_rev else 0, "format": "pct"},
    ])
else:
    render_empty_state("Category data not available")

# ── Top Products ────────────────────────────────────────────────────────────
render_section_header("Top 10 Products by Revenue", icon="🏆")

top_products = metrics.get("top_products", {})
products_list = top_products.get("top_products", []) if isinstance(top_products, dict) else []
if products_list:
    prod_df = pd.DataFrame(products_list).head(10)
    display_df = prod_df[["product_name", "category", "total_revenue", "total_units_sold", "margin_pct"]].copy()
    display_df.columns = ["Product", "Category", "Revenue", "Units Sold", "Margin %"]
    display_df["Revenue"] = display_df["Revenue"].apply(lambda x: fmt_currency(x))
    display_df["Margin %"] = display_df["Margin %"].apply(lambda x: fmt_pct(x))
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    render_empty_state("Top products data not available")

# ── Category Margin Analysis ────────────────────────────────────────────────
render_section_header("Category Margin Analysis", icon="📊")

if categories:
    margin_df = pd.DataFrame(categories).sort_values("margin_pct", ascending=False)
    margin_display = margin_df[["category", "total_revenue", "total_margin", "margin_pct", "avg_selling_price"]].copy()
    margin_display.columns = ["Category", "Revenue", "Margin", "Margin %", "Avg Price"]
    margin_display["Revenue"] = margin_display["Revenue"].apply(lambda x: fmt_currency(x))
    margin_display["Margin"] = margin_display["Margin"].apply(lambda x: fmt_currency(x))
    margin_display["Margin %"] = margin_display["Margin %"].apply(lambda x: fmt_pct(x))
    margin_display["Avg Price"] = margin_display["Avg Price"].apply(lambda x: fmt_currency(x))
    st.dataframe(margin_display, use_container_width=True, hide_index=True)

# ── Category Analysis Detail ────────────────────────────────────────────────
render_section_header("Category Analysis Detail", icon="📋")

if figure_path("category_analysis.png").exists():
    st.image(figure_path("category_analysis.png"), caption="Category Analysis Overview", use_container_width=True)
else:
    render_empty_state("Category analysis figure not available")
