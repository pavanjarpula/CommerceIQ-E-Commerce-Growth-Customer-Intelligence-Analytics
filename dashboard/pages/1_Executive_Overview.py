"""Executive Overview - CommerceIQ Dashboard."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products, figure_path
from dashboard.utils.theme import inject_global_css, render_page_header, render_section_header, render_empty_state
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct
from dashboard.components.kpi_cards import render_revenue_kpis
from dashboard.components.charts import revenue_trend_chart
from dashboard.components.filters import apply_filters, count_active_filters
from dashboard.components.insights import render_insight_card
from dashboard.components.header import render_app_header

st.set_page_config(page_title="Executive Overview", page_icon="📊", layout="wide")
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
render_page_header("Executive Overview", "How is the business performing?", badge=badge)

# ── KPI Summary ─────────────────────────────────────────────────────────────
revenue = metrics.get("revenue", {})
if revenue:
    render_revenue_kpis(revenue)
else:
    render_empty_state("Revenue KPIs not available")

# ── Revenue Performance ─────────────────────────────────────────────────────
render_section_header("Revenue Performance", icon="📈")

col_trend, col_status = st.columns([3, 2])
with col_trend:
    monthly = metrics.get("monthly", [])
    if monthly:
        st.plotly_chart(revenue_trend_chart(monthly), use_container_width=True)
    else:
        render_empty_state("Monthly revenue data not available")

with col_status:
    if figure_path("status_analysis.png").exists():
        st.image(figure_path("status_analysis.png"), caption="Order Status Breakdown", use_container_width=True)
    else:
        render_empty_state("Status analysis figure not found")

# ── Business Drivers ────────────────────────────────────────────────────────
render_section_header("Business Drivers", icon="⚡")

driver_cols = st.columns(4)
with driver_cols[0]:
    st.markdown(
        '<div class="ciq-card ciq-card-info">'
        '<h4 style="margin:0 0 0.25rem;font-size:0.78rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;">Customers</h4>'
        f'<p style="margin:0;font-size:1.3rem;font-weight:700;color:#0f172a;">{fmt_number(metrics.get("rfm", {}).get("total_customers", 0))}</p>'
        f'<p style="margin:0.15rem 0 0;font-size:0.72rem;color:#64748b;">{fmt_number(metrics.get("rfm", {}).get("active_customers", 0))} active</p>'
        '</div>',
        unsafe_allow_html=True,
    )
with driver_cols[1]:
    channels = metrics.get("channels", [])
    top_channel = max(channels, key=lambda c: c.get("total_revenue", 0)) if channels else {}
    st.markdown(
        '<div class="ciq-card ciq-card-success">'
        '<h4 style="margin:0 0 0.25rem;font-size:0.78rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;">Top Channel</h4>'
        f'<p style="margin:0;font-size:1.3rem;font-weight:700;color:#0f172a;">{top_channel.get("channel", "N/A").title()}</p>'
        f'<p style="margin:0.15rem 0 0;font-size:0.72rem;color:#64748b;">{fmt_currency(top_channel.get("total_revenue", 0))} revenue</p>'
        '</div>',
        unsafe_allow_html=True,
    )
with driver_cols[2]:
    categories = metrics.get("categories", [])
    top_cat = max(categories, key=lambda c: c.get("total_revenue", 0)) if categories else {}
    st.markdown(
        '<div class="ciq-card ciq-card-warning">'
        '<h4 style="margin:0 0 0.25rem;font-size:0.78rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;">Top Category</h4>'
        f'<p style="margin:0;font-size:1.3rem;font-weight:700;color:#0f172a;">{top_cat.get("category", "N/A")}</p>'
        f'<p style="margin:0.15rem 0 0;font-size:0.72rem;color:#64748b;">{fmt_currency(top_cat.get("total_revenue", 0))} revenue</p>'
        '</div>',
        unsafe_allow_html=True,
    )
with driver_cols[3]:
    countries = metrics.get("countries", [])
    top_country = max(countries, key=lambda c: c.get("total_revenue", 0)) if countries else {}
    st.markdown(
        '<div class="ciq-card ciq-card-accent">'
        '<h4 style="margin:0 0 0.25rem;font-size:0.78rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;">Top Market</h4>'
        f'<p style="margin:0;font-size:1.3rem;font-weight:700;color:#0f172a;">{top_country.get("country", "N/A")}</p>'
        f'<p style="margin:0.15rem 0 0;font-size:0.72rem;color:#64748b;">{fmt_currency(top_country.get("total_revenue", 0))} revenue</p>'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Key Findings ────────────────────────────────────────────────────────────
render_section_header("Key Findings", icon="💡")

recs = metrics.get("recommendations", [])
if recs:
    high_recs = [r for r in recs if r.get("priority") == "High"]
    if not high_recs:
        high_recs = recs[:3]
    for rec in high_recs[:3]:
        render_insight_card(
            title=rec.get("category", "General"),
            finding=rec.get("finding", "N/A"),
            impact=rec.get("expected_impact", ""),
            impact_type="success",
        )
else:
    render_empty_state("No recommendations available")
