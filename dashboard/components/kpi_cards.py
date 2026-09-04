"""Dashboard - Premium KPI Card Components."""
import streamlit as st
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct, fmt_kpi_value


def render_kpi_row(metrics_list: list[dict], cols: int = 4):
    """Render a styled row of KPI cards with premium presentation."""
    columns = st.columns(cols)
    for i, m in enumerate(metrics_list):
        col = columns[i % cols]
        with col:
            val = fmt_kpi_value(m["value"], m.get("format", "number"))

            delta = None
            delta_color = "normal"
            if m.get("delta") is not None:
                delta_val = m["delta"]
                delta = f"{delta_val*100:+.1f}%"
                if m.get("delta_color") == "inverse":
                    delta_color = "inverse"

            st.metric(
                label=m["label"],
                value=val,
                delta=delta,
                delta_color=delta_color,
            )
            if m.get("context"):
                st.markdown(
                    f'<div class="ciq-metric-context">{m["context"]}</div>',
                    unsafe_allow_html=True,
                )


def render_kpi_strip(metrics_list: list[dict]):
    """Render a compact horizontal KPI strip."""
    cols = st.columns(len(metrics_list))
    for i, m in enumerate(metrics_list):
        with cols[i]:
            val = fmt_kpi_value(m["value"], m.get("format", "number"))

            delta = None
            if m.get("delta") is not None:
                delta = f"{m['delta']*100:+.1f}%"

            st.metric(
                label=m["label"],
                value=val,
                delta=delta,
                delta_color="normal" if m.get("delta_color") != "inverse" else "inverse",
            )
            if m.get("context"):
                st.markdown(
                    f'<div class="ciq-metric-context">{m["context"]}</div>',
                    unsafe_allow_html=True,
                )


def render_revenue_kpis(revenue: dict):
    """Render the standard revenue KPI dashboard with context."""
    render_kpi_row([
        {"label": "Total Orders", "value": revenue.get("total_orders", 0), "format": "number"},
        {"label": "Gross Revenue", "value": revenue.get("total_gross_revenue", 0), "format": "currency",
         "context": "Before refunds & cancellations"},
        {"label": "Net Revenue", "value": revenue.get("total_net_revenue", 0), "format": "currency",
         "context": f"{revenue.get('total_net_revenue', 0)/revenue.get('total_gross_revenue', 1)*100:.1f}% of gross revenue"},
        {"label": "Avg Order Value", "value": revenue.get("avg_order_value", 0), "format": "currency"},
    ])
    render_kpi_row([
        {"label": "Gross Margin", "value": revenue.get("total_gross_margin", 0), "format": "currency"},
        {"label": "Margin %", "value": revenue.get("margin_pct", 0), "format": "pct"},
        {"label": "Completion Rate", "value": revenue.get("completion_rate", 0), "format": "pct",
         "context": f"{revenue.get('completed', 0):,} of {revenue.get('total_orders', 0):,} orders"},
        {"label": "Avg Items / Order", "value": revenue.get("avg_items_per_order", 0), "format": "number"},
    ])


def render_segment_kpis(segments: list[dict], total_customers: int, active_customers: int):
    """Render customer segmentation KPIs with context."""
    render_kpi_row([
        {"label": "Total Customers", "value": total_customers, "format": "number"},
        {"label": "Active Customers", "value": active_customers, "format": "number",
         "context": "With at least 1 order"},
        {"label": "Activation Rate", "value": active_customers / total_customers if total_customers else 0, "format": "pct"},
    ])


def render_margin_kpis(revenue: dict):
    """Render margin-specific KPIs for the Margin & Pricing page."""
    render_kpi_row([
        {"label": "Gross Margin", "value": revenue.get("total_gross_margin", 0), "format": "currency"},
        {"label": "Margin %", "value": revenue.get("margin_pct", 0), "format": "pct"},
        {"label": "Avg Order Margin", "value": revenue.get("avg_order_margin", 0), "format": "currency"},
        {"label": "Avg Items/Order", "value": revenue.get("avg_items_per_order", 0), "format": "number"},
    ])


def render_premium_kpi_card(label: str, value: str, context: str = "", delta: str = "", delta_positive: bool = True):
    """Render a single premium KPI card as HTML."""
    delta_html = ""
    if delta:
        cls = "ciq-kpi-delta-positive" if delta_positive else "ciq-kpi-delta-negative"
        delta_html = f'<div class="{cls}">{delta}</div>'

    context_html = ""
    if context:
        context_html = f'<div class="ciq-kpi-context">{context}</div>'

    st.markdown(
        f'<div class="ciq-kpi-item">'
        f'<div class="ciq-kpi-label">{label}</div>'
        f'<div class="ciq-kpi-value">{value}</div>'
        f'{delta_html}'
        f'{context_html}'
        f'</div>',
        unsafe_allow_html=True,
    )
