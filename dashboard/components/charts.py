"""Dashboard - Polished Chart Components using Plotly."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ── Brand Palette ───────────────────────────────────────────────────────────
PALETTE = {
    "primary":   "#1a237e",
    "accent":    "#3949ab",
    "success":   "#43a047",
    "warning":   "#fb8c00",
    "danger":    "#e53935",
    "info":      "#039be5",
    "purple":    "#8e24aa",
    "teal":      "#00897b",
}

CHART_COLORS = ["#3949ab", "#43a047", "#fb8c00", "#e53935", "#8e24aa", "#00897b", "#039be5", "#5c6bc0"]

CHART_LAYOUT = dict(
    font=dict(family="Inter, -apple-system, sans-serif", size=12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=50, b=40, l=50, r=20),
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Inter, sans-serif",
        bordercolor="#e8eaf6",
    ),
    xaxis=dict(showgrid=True, gridcolor="#f0f0f5", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#f0f0f5", zeroline=False),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=11),
    ),
)


def _apply_layout(fig, title=None, **kwargs):
    layout = {**CHART_LAYOUT}
    if title:
        layout["title"] = dict(text=title, font=dict(size=15, color="#1a237e", family="Inter, sans-serif"), x=0.01)
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
        marker=dict(size=7, color=PALETTE["success"]),
        hovertemplate="Net: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["order_month"], y=df["gross_revenue"],
        mode="lines+markers", name="Gross Revenue",
        line=dict(color=PALETTE["primary"], width=2, dash="dot"),
        marker=dict(size=6, color=PALETTE["primary"]),
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
        marker_color=PALETTE["warning"],
        marker_line=dict(width=0),
        hovertemplate="Orders: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["order_month"], y=df["orders"],
        mode="lines+markers", name="Trend",
        line=dict(color=PALETTE["danger"], width=2),
        marker=dict(size=5),
    ))
    _apply_layout(fig, title="Monthly Orders")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text="Orders", gridcolor="#f5f5f5")
    return fig


def aov_trend_chart(monthly: list[dict]) -> go.Figure:
    df = pd.DataFrame(monthly)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["order_month"], y=df["avg_order_value"],
        mode="lines+markers",
        line=dict(color=PALETTE["accent"], width=2.5),
        marker=dict(size=8, symbol="diamond", color=PALETTE["accent"]),
        fill="tozeroy",
        fillcolor="rgba(57,73,171,0.08)",
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
        hovertemplate=f"{metric}: %{{x:,.0f}}<extra></extra>",
    ))
    _apply_layout(fig, title=title)
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(tickformat=",.0f", gridcolor="#f5f5f5")
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
        hovertemplate=f"{metric}: %{{x:,.0f}}<extra></extra>",
    ))
    _apply_layout(fig, title=title)
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(tickformat=",.0f", gridcolor="#f5f5f5")
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
        hovertemplate="Revenue: $%{x:,.0f}<extra></extra>",
    ))
    _apply_layout(fig, title="Revenue by Category")
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(tickformat="$,.0f", gridcolor="#f5f5f5")
    fig.update_traces(cliponaxis=False)
    return fig


# ── RFM ─────────────────────────────────────────────────────────────────────
def rfm_pie_chart(segments: list[dict]) -> go.Figure:
    df = pd.DataFrame(segments)
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df["rfm_segment"],
        values=df["customer_count"],
        hole=0.45,
        marker=dict(colors=CHART_COLORS[:len(df)], line=dict(color="white", width=2)),
        textinfo="label+percent",
        textposition="outside",
        textfont=dict(size=11),
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
        hovertemplate="Revenue: $%{x:,.0f}<extra></extra>",
    ))
    _apply_layout(fig, title="Revenue by Customer Segment")
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(tickformat="$,.0f", gridcolor="#f5f5f5")
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
    ))
    fig.add_trace(go.Scatter(
        x=df["category"], y=df["total_revenue"],
        name="Revenue",
        mode="lines+markers",
        line=dict(color=PALETTE["primary"], width=2, dash="dot"),
        marker=dict(size=8),
        yaxis="y2",
    ))
    _apply_layout(fig, title="Margin & Revenue by Category")
    fig.update_layout(
        yaxis=dict(title="Margin ($)", tickformat="$,.0f", gridcolor="#f5f5f5"),
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
            opacity=0.6,
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
    fig.update_yaxes(gridcolor="#f5f5f5")
    return fig