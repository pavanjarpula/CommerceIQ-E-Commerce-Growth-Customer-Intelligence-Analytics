"""Dashboard - Styled KPI Card Components."""
import streamlit as st
from dashboard.utils.formatting import fmt_currency, fmt_number, fmt_pct


def render_kpi_row(metrics_list: list[dict], cols: int = 4):
    """Render a styled row of KPI cards with icon indicators."""
    columns = st.columns(cols)
    for i, m in enumerate(metrics_list):
        col = columns[i % cols]
        with col:
            fmt = m.get("format", "number")
            icon = m.get("icon", "")

            if fmt == "currency":
                val = fmt_currency(m["value"])
            elif fmt == "pct":
                val = fmt_pct(m["value"])
            else:
                val = fmt_number(m["value"])

            delta = None
            if m.get("delta") is not None:
                delta_val = m["delta"]
                delta = f"{delta_val*100:+.1f}%"

            delta_color = "normal"
            if m.get("delta_color") == "inverse":
                delta_color = "inverse"

            st.metric(
                label=f"{icon} {m['label']}" if icon else m["label"],
                value=val,
                delta=delta,
                delta_color=delta_color,
            )


def render_revenue_kpis(revenue: dict):
    """Render the standard revenue KPI dashboard."""
    render_kpi_row([
        {"label": "Total Orders", "value": revenue.get("total_orders", 0), "format": "number", "icon": "📦"},
        {"label": "Gross Revenue", "value": revenue.get("total_gross_revenue", 0), "format": "currency", "icon": "💰"},
        {"label": "Net Revenue", "value": revenue.get("total_net_revenue", 0), "format": "currency", "icon": "📈"},
        {"label": "Avg Order Value", "value": revenue.get("avg_order_value", 0), "format": "currency", "icon": "🎯"},
    ])
    render_kpi_row([
        {"label": "Gross Margin", "value": revenue.get("total_gross_margin", 0), "format": "currency", "icon": "📊"},
        {"label": "Margin %", "value": revenue.get("margin_pct", 0), "format": "pct", "icon": "⚖️"},
        {"label": "Completion Rate", "value": revenue.get("completion_rate", 0), "format": "pct", "icon": "✅"},
        {"label": "Avg Items / Order", "value": revenue.get("avg_items_per_order", 0), "format": "number", "icon": "🛒"},
    ])


def render_segment_kpis(segments: list[dict], total_customers: int, active_customers: int):
    """Render customer segmentation KPIs."""
    render_kpi_row([
        {"label": "Total Customers", "value": total_customers, "format": "number", "icon": "👥"},
        {"label": "Active Customers", "value": active_customers, "format": "number", "icon": "🟢"},
        {"label": "Activation Rate", "value": active_customers / total_customers if total_customers else 0, "format": "pct", "icon": "📈"},
    ])