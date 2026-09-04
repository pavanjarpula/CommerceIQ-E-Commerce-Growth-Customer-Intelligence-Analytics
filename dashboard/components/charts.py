"""Dashboard - Premium Chart Components using Plotly."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ── Brand Palette ───────────────────────────────────────────────────────────
PALETTE = {
    "primary":   "#0f172a",
    "accent":    "#3949ab",
    "success":   "#059669",
    "warning":   "#d97706",
    "danger":    "#dc2626",
    "info":      "#2563eb",
    "purple":    "#7c3aed",
    "teal":      "#0d9488",
}

CHART_COLORS = ["#3949ab", "#059669", "#d97706", "#dc2626", "#7c3aed", "#0d9488", "#2563eb", "#5c6bc0"]

CHART_LAYOUT = dict(
    font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#334155"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=45, b=35, l=50, r=15),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Inter, sans-serif",
        bordercolor="#e2e8f0",
        font_color="#0f172a",
    ),
    xaxis=dict(showgrid=False, zeroline=False, linecolor="#e2e8f0", linewidth=1),
    yaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False, linecolor="#e2e8f0", linewidth=1),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=11, color="#64748b"),
    ),
    dragmode=False,
)


def _apply_layout(fig, title=None, **kwargs):
    layout = {**CHART_LAYOUT}
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(size=13, color="#0f172a", family="Inter, sans-serif", weight=600),
            x=0.01,
            xanchor="left",
        )
    layout.update(kwargs)
    fig.update_layout(**layout)
    return fig


# ── Revenue Charts ──────────────────────────────────────────────────────────
def revenue_trend_chart(monthly: list[dict]) -> go.Figure:
    df = pd.DataFrame(monthly)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["order_month"], y=df["net_revenue"],
        mode="lines+markers", name="Net Revenue",
        line=dict(color=PALETTE["success"], width=2.5),
        marker=dict(size=6, color=PALETTE["success"], line=dict(width=0)),
        hovertemplate="Net: $%{y:,.0f}<extra></extra>",
        fill="tozeroy",
        fillcolor="rgba(5,150,105,0.06)",
    ))
    fig.add_trace(go.Scatter(
        x=df["order_month"], y=df["gross_revenue"],
        mode="lines+markers", name="Gross Revenue",
        line=dict(color=PALETTE["accent"], width=2, dash="dot"),
        marker=dict(size=5, color=PALETTE["accent"]),
        hovertemplate="Gross: $%{y:,.0f}<extra></extra>",
    ))
    _apply_layout(fig, title="Monthly Revenue Trend")
    fig.update_xaxes(title_text=None, showgrid=False)
    fig.update_yaxes(title_text="Revenue ($)", tickformat="$,.0f")
    return fig


def orders_trend_chart(monthly: list[dict]) -> go.Figure:
    df = pd.DataFrame(monthly)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["order_month"], y=df["orders"],
        name="Orders",
        marker_color="rgba(217,119,6,0.7)",
        marker_line=dict(width=0),
        hovertemplate="Orders: %{y}<extra></extra>",
        width=0.6,
    ))
    fig.add_trace(go.Scatter(
        x=df["order_month"], y=df["orders"],
        mode="lines+markers", name="Trend",
        line=dict(color=PALETTE["danger"], width=2),
        marker=dict(size=4),
        showlegend=False,
    ))
    _apply_layout(fig, title="Monthly Orders")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text="Orders", gridcolor="#f1f5f9")
    return fig


def aov_trend_chart(monthly: list[dict]) -> go.Figure:
    df = pd.DataFrame(monthly)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["order_month"], y=df["avg_order_value"],
        mode="lines+markers",
        line=dict(color=PALETTE["accent"], width=2.5),
        marker=dict(size=7, symbol="diamond", color=PALETTE["accent"]),
        fill="tozeroy",
        fillcolor="rgba(57,73,171,0.06)",
        hovertemplate="AOV: $%{y:,.2f}<extra></extra>",
    ))
    _apply_layout(fig, title="Average Order Value Trend")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text="AOV ($)", tickformat="$,.0f")
    return fig


# ── Category / Channel / Country ───────────────────────────────────────────
def channel_bar_chart(channels: list[dict], metric: str = "total_revenue", title: str = "Revenue by Channel") -> go.Figure:
    df = pd.DataFrame(channels).sort_values(metric)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["channel"], x=df[metric],
        orientation="h",
        marker_color=CHART_COLORS[:len(df)],
        marker_line=dict(width=0),
        text=[f"${v:,.0f}" if metric in ("total_revenue", "total_margin", "revenue_per_customer", "margin_per_customer") else f"{v:,.0f}" for v in df[metric]],
        textposition="outside",
        textfont=dict(size=11, color="#334155"),
        hovertemplate=f"{metric}: %{{x:,.0f}}<extra></extra>",
    ))
    _apply_layout(fig, title=title)
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(tickformat=",.0f", gridcolor="#f1f5f9")
    fig.update_traces(cliponaxis=False)
    return fig


def country_bar_chart(countries: list[dict], metric: str = "total_revenue", title: str = "Revenue by Country") -> go.Figure:
    df = pd.DataFrame(countries).sort_values(metric)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["country"], x=df[metric],
        orientation="h",
        marker_color=CHART_COLORS[:len(df)],
        marker_line=dict(width=0),
        text=[f"${v:,.0f}" if metric in ("total_revenue", "total_margin") else f"{v:,.0f}" for v in df[metric]],
        textposition="outside",
        textfont=dict(size=11, color="#334155"),
        hovertemplate=f"{metric}: %{{x:,.0f}}<extra></extra>",
    ))
    _apply_layout(fig, title=title)
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(tickformat=",.0f", gridcolor="#f1f5f9")
    fig.update_traces(cliponaxis=False)
    return fig


def category_bar_chart(categories: list[dict]) -> go.Figure:
    df = pd.DataFrame(categories).sort_values("total_revenue")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["category"], x=df["total_revenue"],
        orientation="h",
        marker_color=CHART_COLORS[:len(df)],
        marker_line=dict(width=0),
        text=[f"${v:,.0f}" for v in df["total_revenue"]],
        textposition="outside",
        textfont=dict(size=11, color="#334155"),
        hovertemplate="Revenue: $%{x:,.0f}<extra></extra>",
    ))
    _apply_layout(fig, title="Revenue by Category")
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(tickformat="$,.0f", gridcolor="#f1f5f9")
    fig.update_traces(cliponaxis=False)
    return fig


# ── RFM ─────────────────────────────────────────────────────────────────────
def rfm_pie_chart(segments: list[dict]) -> go.Figure:
    df = pd.DataFrame(segments)
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df["rfm_segment"],
        values=df["customer_count"],
        hole=0.5,
        marker=dict(colors=CHART_COLORS[:len(df)], line=dict(color="white", width=2)),
        textinfo="label+percent",
        textposition="outside",
        textfont=dict(size=10, color="#334155"),
        hovertemplate="%{label}<br>Customers: %{value}<br>Share: %{percent}<extra></extra>",
    ))
    _apply_layout(fig, title="Customer Segment Distribution")
    fig.update_layout(showlegend=False)
    return fig


def rfm_revenue_bar(segments: list[dict]) -> go.Figure:
    df = pd.DataFrame(segments).sort_values("total_revenue")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["rfm_segment"], x=df["total_revenue"],
        orientation="h",
        marker_color=CHART_COLORS[:len(df)],
        marker_line=dict(width=0),
        text=[f"${v:,.0f}" for v in df["total_revenue"]],
        textposition="outside",
        textfont=dict(size=11, color="#334155"),
        hovertemplate="Revenue: $%{x:,.0f}<extra></extra>",
    ))
    _apply_layout(fig, title="Revenue by Customer Segment")
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(tickformat="$,.0f", gridcolor="#f1f5f9")
    fig.update_traces(cliponaxis=False)
    return fig


# ── Discount / Margin ──────────────────────────────────────────────────────
def margin_by_category_chart(categories: list[dict]) -> go.Figure:
    df = pd.DataFrame(categories).sort_values("total_margin", ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["category"], y=df["total_margin"],
        name="Margin",
        marker_color=PALETTE["success"],
        marker_line=dict(width=0),
        text=[f"${v:,.0f}" for v in df["total_margin"]],
        textposition="outside",
        textfont=dict(size=11, color="#334155"),
    ))
    fig.add_trace(go.Scatter(
        x=df["category"], y=df["total_revenue"],
        name="Revenue",
        mode="lines+markers",
        line=dict(color=PALETTE["primary"], width=2, dash="dot"),
        marker=dict(size=7),
        yaxis="y2",
    ))
    _apply_layout(fig, title="Margin & Revenue by Category")
    fig.update_layout(
        yaxis=dict(title="Margin ($)", tickformat="$,.0f", gridcolor="#f1f5f9"),
        yaxis2=dict(title="Revenue ($)", tickformat="$,.0f", overlaying="y", side="right", showgrid=False),
    )
    fig.update_xaxes(showgrid=False)
    return fig


def anomaly_scatter(daily_data: list[dict], anomalies: list[dict], col: str, title: str) -> go.Figure:
    fig = go.Figure()
    if daily_data:
        df_all = pd.DataFrame(daily_data)
        fig.add_trace(go.Scatter(
            x=df_all.get("order_date", []), y=df_all.get(col, []),
            mode="lines", name="Normal",
            line=dict(color=PALETTE["info"], width=1.5),
            opacity=0.5,
        ))
    if anomalies:
        df_anom = pd.DataFrame(anomalies)
        fig.add_trace(go.Scatter(
            x=df_anom.get("order_date", []), y=df_anom.get(col, []),
            mode="markers", name="Anomaly",
            marker=dict(color=PALETTE["danger"], size=10, symbol="x", line=dict(width=2, color="white")),
        ))
    _apply_layout(fig, title=title)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#f1f5f9")
    return fig


# ── Additional Charts ──────────────────────────────────────────────────────
def revenue_vs_margin_scatter(categories: list[dict]) -> go.Figure:
    """Scatter plot: Revenue vs Margin % by category."""
    df = pd.DataFrame(categories)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["total_revenue"],
        y=df["margin_pct"] * 100 if df["margin_pct"].max() < 1 else df["margin_pct"],
        mode="markers+text",
        text=df["category"],
        textposition="top center",
        textfont=dict(size=11, color="#0f172a"),
        marker=dict(
            size=df.get("product_count", pd.Series([20] * len(df))) * 3,
            color=CHART_COLORS[:len(df)],
            opacity=0.8,
            line=dict(width=1.5, color="white"),
        ),
        hovertemplate="%{text}<br>Revenue: $%{x:,.0f}<br>Margin: %{y:.1f}%<extra></extra>",
    ))
    _apply_layout(fig, title="Revenue vs Margin % by Category")
    fig.update_xaxes(title_text="Revenue ($)", tickformat="$,.0f")
    fig.update_yaxes(title_text="Margin %")
    return fig


def growth_rate_chart(monthly: list[dict]) -> go.Figure:
    """Line chart showing month-over-month growth rates."""
    df = pd.DataFrame(monthly)
    fig = go.Figure()
    if "revenue_mom_growth" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["order_month"],
            y=df["revenue_mom_growth"].fillna(0) * 100,
            mode="lines+markers",
            name="Revenue Growth %",
            line=dict(color=PALETTE["accent"], width=2.5),
            marker=dict(size=6),
            hovertemplate="Rev Growth: %{y:.1f}%<extra></extra>",
        ))
    if "orders_mom_growth" in df.columns:
        fig.add_trace(go.Scatter(
            x=df["order_month"],
            y=df["orders_mom_growth"].fillna(0) * 100,
            mode="lines+markers",
            name="Orders Growth %",
            line=dict(color=PALETTE["warning"], width=2, dash="dot"),
            marker=dict(size=5),
            hovertemplate="Order Growth: %{y:.1f}%<extra></extra>",
        ))
    fig.add_hline(y=0, line_dash="dash", line_color="#cbd5e1", line_width=1)
    _apply_layout(fig, title="Month-over-Month Growth Rates")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text="Growth Rate (%)", ticksuffix="%")
    return fig


def cohort_retention_heatmap(cohort: dict) -> go.Figure:
    """Heatmap for cohort retention analysis."""
    cohort_data = cohort.get("cohort_retention", [])
    if not cohort_data:
        return go.Figure()

    df = pd.DataFrame(cohort_data)
    if "cohort_month" not in df.columns or "retention_rate" not in df.columns:
        return go.Figure()

    pivot = df.pivot_table(
        index="cohort_month",
        columns="order_month",
        values="retention_rate",
        aggfunc="first",
    )

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=[str(i) for i in pivot.index],
        colorscale=[[0, "#f1f5f9"], [0.25, "#bfdbfe"], [0.5, "#60a5fa"], [0.75, "#2563eb"], [1, "#1e3a8a"]],
        text=[[f"{v:.0%}" if pd.notna(v) else "" for v in row] for row in pivot.values],
        texttemplate="%{text}",
        textfont=dict(size=10),
        hovertemplate="Cohort: %{y}<br>Period: %{x}<br>Retention: %{z:.1%}<extra></extra>",
        showscale=True,
        colorbar=dict(title="Retention", tickformat=".0%"),
    ))
    _apply_layout(fig, title="Cohort Retention Heatmap")
    fig.update_xaxes(title_text="Order Month", showgrid=False)
    fig.update_yaxes(title_text="Cohort Month", showgrid=False, autorange="reversed")
    fig.update_layout(margin=dict(t=55, b=55, l=80, r=20))
    return fig
