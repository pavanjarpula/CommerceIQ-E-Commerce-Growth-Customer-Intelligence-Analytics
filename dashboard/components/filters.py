"""Dashboard - Premium Filter Components."""
import streamlit as st
import pandas as pd


def render_sidebar_filters(orders: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """Render sidebar filters and return filter values."""
    st.sidebar.markdown(
        '<p class="ciq-sidebar-section-label" style="margin-top:0.5rem;">Filters</p>',
        unsafe_allow_html=True,
    )

    orders_sorted = orders.sort_values("order_ts")
    min_date = pd.to_datetime(orders_sorted["order_ts"].iloc[0]).date()
    max_date = pd.to_datetime(orders_sorted["order_ts"].iloc[-1]).date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    countries = ["All"] + sorted(customers["country"].unique().tolist())
    selected_country = st.sidebar.selectbox("Country", countries)

    channels = ["All"] + sorted(customers["channel"].unique().tolist())
    selected_channel = st.sidebar.selectbox("Channel", channels)

    statuses = ["All"] + sorted(orders["status"].unique().tolist())
    selected_status = st.sidebar.selectbox("Order Status", statuses)

    return {
        "date_range": date_range,
        "country": selected_country,
        "channel": selected_channel,
        "status": selected_status,
    }


def render_global_filters(orders: pd.DataFrame, customers: pd.DataFrame, key_prefix: str = "gf") -> dict:
    """Render a horizontal global filter bar in the main content area."""
    orders_sorted = orders.sort_values("order_ts")
    min_date = pd.to_datetime(orders_sorted["order_ts"].iloc[0]).date()
    max_date = pd.to_datetime(orders_sorted["order_ts"].iloc[-1]).date()

    col1, col2, col3, col4, col5 = st.columns([2.5, 1.2, 1.2, 1.2, 0.8])

    with col1:
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key=f"{key_prefix}_date",
            label_visibility="collapsed",
        )

    with col2:
        countries = ["All"] + sorted(customers["country"].unique().tolist())
        selected_country = st.selectbox("Country", countries, key=f"{key_prefix}_country", label_visibility="collapsed")

    with col3:
        channels = ["All"] + sorted(customers["channel"].unique().tolist())
        selected_channel = st.selectbox("Channel", channels, key=f"{key_prefix}_channel", label_visibility="collapsed")

    with col4:
        statuses = ["All"] + sorted(orders["status"].unique().tolist())
        selected_status = st.selectbox("Status", statuses, key=f"{key_prefix}_status", label_visibility="collapsed")

    with col5:
        active_count = sum(1 for v in [selected_country, selected_channel, selected_status] if v != "All")
        if len(date_range) == 2 and (date_range[0] != min_date or date_range[1] != max_date):
            active_count += 1
        if active_count > 0:
            st.markdown(
                f'<div style="padding-top:0.35rem;">'
                f'<span class="ciq-filter-count">{active_count} filter{"s" if active_count > 1 else ""}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    return {
        "date_range": date_range,
        "country": selected_country,
        "channel": selected_channel,
        "status": selected_status,
    }


def count_active_filters(filters: dict, orders: pd.DataFrame = None) -> int:
    """Count the number of active (non-default) filters."""
    count = 0
    if filters.get("country") and filters["country"] != "All":
        count += 1
    if filters.get("channel") and filters["channel"] != "All":
        count += 1
    if filters.get("status") and filters["status"] != "All":
        count += 1
    if filters.get("date_range") and orders is not None and len(filters["date_range"]) == 2:
        orders_sorted = orders.sort_values("order_ts")
        min_date = pd.to_datetime(orders_sorted["order_ts"].iloc[0]).date()
        max_date = pd.to_datetime(orders_sorted["order_ts"].iloc[-1]).date()
        if filters["date_range"][0] != min_date or filters["date_range"][1] != max_date:
            count += 1
    return count


def apply_filters(df: pd.DataFrame, filters: dict, customers_df: pd.DataFrame = None) -> pd.DataFrame:
    """Apply filters to a dataframe."""
    result = df.copy()

    if "date_range" in filters and len(filters["date_range"]) == 2:
        start, end = filters["date_range"]
        result["order_ts"] = pd.to_datetime(result["order_ts"])
        result = result[result["order_ts"].dt.date >= start]
        result = result[result["order_ts"].dt.date <= end]

    if filters.get("status") and filters["status"] != "All" and "status" in result.columns:
        result = result[result["status"] == filters["status"]]

    if filters.get("country") and filters["country"] != "All" and customers_df is not None:
        if "customer_id" in result.columns:
            country_customers = customers_df[customers_df["country"] == filters["country"]]["customer_id"]
            result = result[result["customer_id"].isin(country_customers)]

    if filters.get("channel") and filters["channel"] != "All" and customers_df is not None:
        if "customer_id" in result.columns:
            channel_customers = customers_df[customers_df["channel"] == filters["channel"]]["customer_id"]
            result = result[result["customer_id"].isin(channel_customers)]

    return result
