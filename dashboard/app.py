"""CommerceIQ Analytics Dashboard - Premium Landing Page & Executive Command Center."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products
from dashboard.utils.theme import inject_global_css, render_section_header, COLORS
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct
from dashboard.components.filters import render_sidebar_filters
from dashboard.components.header import render_app_header
from dashboard.components.kpi_cards import render_kpi_row

st.set_page_config(
    page_title="CommerceIQ Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

metrics = load_all_metrics()
orders = load_orders()
customers = load_customers()
products = load_products()

render_app_header(metrics)

filters = render_sidebar_filters(orders, customers)
st.session_state["filters"] = filters
st.session_state["metrics"] = metrics

# ── Landing Header ──────────────────────────────────────────────────────────
st.markdown(
    '<div class="ciq-app-header">'
    '<h1>CommerceIQ</h1>'
    '<p class="ciq-subtitle">E-commerce Business Intelligence & Customer Analytics</p>'
    '<div class="ciq-app-header-meta">'
    '<div class="ciq-app-header-meta-item">'
    '<span class="ciq-app-header-meta-dot"></span>'
    'Analysis Period: 2024'
    '</div>'
    '<div class="ciq-app-header-meta-item">'
    'Dataset: 12K orders &middot; 2K customers &middot; 120 products'
    '</div>'
    '<div class="ciq-app-header-meta-item">'
    'Pipeline: 9-stage automated analytics'
    '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Executive KPI Summary ──────────────────────────────────────────────────
revenue = metrics.get("revenue", {})
if revenue:
    net_rev = revenue.get("total_net_revenue", 0)
    gross_rev = revenue.get("total_gross_revenue", 0)
    render_kpi_row([
        {"label": "Total Orders", "value": revenue.get("total_orders", 0), "format": "number"},
        {"label": "Gross Revenue", "value": gross_rev, "format": "currency",
         "context": f"Net: {fmt_currency(net_rev)}"},
        {"label": "Net Revenue", "value": net_rev, "format": "currency",
         "context": f"{net_rev/gross_rev*100:.1f}% of gross revenue"},
        {"label": "Active Customers", "value": metrics.get('rfm', {}).get('total_customers', 0), "format": "number"},
    ])

# ── Analytics Navigation ────────────────────────────────────────────────────
render_section_header("Analytics Modules")

nav_items = [
    ("Executive Overview", "High-level business performance and key recommendations", "How is the business performing?"),
    ("Sales & Growth", "Revenue trends, order patterns, and growth rate analysis", "Where is growth coming from?"),
    ("Customer Intelligence", "RFM segmentation, customer lifecycle, and segment economics", "Who are our most valuable customers?"),
    ("Product Intelligence", "Category performance, product margins, and revenue drivers", "Which products drive revenue and margin?"),
    ("Regional Performance", "Country and channel analysis with market rankings", "Which markets and channels perform best?"),
    ("Margin & Pricing", "Profitability analysis, cost structure, and pricing tiers", "Where are we making money?"),
    ("Insights & Decisions", "Strategic recommendations, anomalies, and scenario analysis", "What should the business investigate or act on?"),
    ("Methodology & Data Quality", "Pipeline architecture, validation, and data governance", "Can we trust the analysis?"),
]

nav_html = '<div class="ciq-nav-grid">'
for title, desc, question in nav_items:
    nav_html += (
        f'<div class="ciq-nav-card">'
        f'<h3>{title}</h3>'
        f'<p>{desc}</p>'
        f'<p style="margin:0.3rem 0 0;font-size:0.72rem;color:#3949ab;font-weight:600;font-style:italic;">{question}</p>'
        f'</div>'
    )
nav_html += '</div>'
st.markdown(nav_html, unsafe_allow_html=True)

# ── Key Business Insights ───────────────────────────────────────────────────
render_section_header("Key Business Insights")

recs = metrics.get("recommendations", [])
if recs:
    high_recs = [r for r in recs if r.get("priority") == "High"]
    if not high_recs:
        high_recs = recs[:3]
    for rec in high_recs[:3]:
        finding = rec.get("finding", "N/A")
        recommendation = rec.get("recommendation", "N/A")
        category = rec.get("category", "General")
        impact = rec.get("expected_impact", "")
        impact_html = f'<span class="ciq-tag ciq-tag-success">{impact}</span>' if impact else ""
        st.markdown(
            f'<div class="ciq-insight">'
            f'<h4>{category}</h4>'
            f'<p><strong>Finding:</strong> {finding}</p>'
            f'<p><strong>Recommendation:</strong> {recommendation}</p>'
            f'{impact_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;padding:1.2rem 0 0.5rem;color:#94a3b8;font-size:0.72rem;">'
    'CommerceIQ Analytics Platform &mdash; End-to-end BI pipeline with SQL, statistical analysis, and ML-driven insights'
    '</div>',
    unsafe_allow_html=True,
)
