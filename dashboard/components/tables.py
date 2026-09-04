"""Dashboard - Premium Table Components."""
import streamlit as st
import pandas as pd
from dashboard.utils.formatting import fmt_currency, fmt_pct, fmt_number


def render_styled_table(
    df: pd.DataFrame,
    columns: dict = None,
    formatters: dict = None,
    use_container_width: bool = True,
    height: int = None,
    key: str = None,
):
    """Render a professionally styled DataFrame table."""
    display_df = df.copy()

    if columns:
        display_df = display_df[list(columns.keys())]
        display_df.columns = list(columns.values())

    if formatters:
        for col, fmt_fn in formatters.items():
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(fmt_fn)

    st.dataframe(
        display_df,
        use_container_width=use_container_width,
        hide_index=True,
        height=height,
        key=key,
    )


def render_metric_table(
    df: pd.DataFrame,
    metric_cols: list[str],
    prefix: str = "$",
    use_container_width: bool = True,
):
    """Render a table with auto-formatted metric columns."""
    display_df = df.copy()
    for col in metric_cols:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: fmt_currency(x, decimals=0) if prefix == "$" else fmt_number(x))
    st.dataframe(display_df, use_container_width=use_container_width, hide_index=True)


def render_ranked_table(
    df: pd.DataFrame,
    rank_col: str,
    columns: dict = None,
    formatters: dict = None,
    top_n: int = None,
    use_container_width: bool = True,
):
    """Render a table ranked by a specific column with optional top N limit."""
    ranked_df = df.sort_values(rank_col, ascending=False)
    if top_n:
        ranked_df = ranked_df.head(top_n)
    render_styled_table(ranked_df, columns=columns, formatters=formatters, use_container_width=use_container_width)


def render_kpi_table(
    data: list[dict],
    use_container_width: bool = True,
):
    """Render a compact KPI summary table from a list of dicts."""
    if not data:
        return
    rows = []
    for item in data:
        row = {"Metric": item["label"], "Value": item["value"]}
        if item.get("context"):
            row["Context"] = item["context"]
        rows.append(row)
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=use_container_width, hide_index=True)


def render_premium_table(
    df: pd.DataFrame,
    columns: dict = None,
    formatters: dict = None,
    use_container_width: bool = True,
    height: int = None,
    key: str = None,
    caption: str = "",
):
    """Render a premium table with optional caption and formatting."""
    display_df = df.copy()

    if columns:
        available_cols = [c for c in columns.keys() if c in display_df.columns]
        display_df = display_df[available_cols]
        display_df.columns = [columns[c] for c in available_cols]

    if formatters:
        for col, fmt_fn in formatters.items():
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(fmt_fn)

    if caption:
        st.markdown(
            f'<p style="font-size:0.75rem;color:#64748b;margin:0.3rem 0 0.5rem;font-weight:500;">{caption}</p>',
            unsafe_allow_html=True,
        )

    st.dataframe(
        display_df,
        use_container_width=use_container_width,
        hide_index=True,
        height=height,
        key=key,
    )
