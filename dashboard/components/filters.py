"""Dashboard - Filter Components."""
import streamlit as st
import pandas as pd


def render_sidebar_filters(orders: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """Render sidebar filters and return filter values."""
    st.sidebar.header("Filters")

    # Date range
    orders_sorted = orders.sort_values("order_ts")
    min_date = pd.to_datetime(orders_sorted["order_ts"].iloc[0]).date()
    max_date = pd.to_datetime(orders_sorted["order_ts"].iloc[-1]).date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Country
    countries = ["All"] + sorted(customers["country"].unique().tolist())
    selected_country = st.sidebar.selectbox("Country", countries)

    # Channel
    channels = ["All"] + sorted(customers["channel"].unique().tolist())
    selected_channel = st.sidebar.selectbox("Channel", channels)

    # Status
    statuses = ["All"] + sorted(orders["status"].unique().tolist())
    selected_status = st.sidebar.selectbox("Order Status", statuses)

    return {
        "date_range": date_range,
        "country": selected_country,
        "channel": selected_channel,
        "status": selected_status,
    }


def apply_filters(df: pd.DataFrame, filters: dict, customers_df: pd.DataFrame = None) -> pd.DataFrame:
    """Apply filters to a dataframe."""
    result = df.copy()

    # Date filter
    if "date_range" in filters and len(filters["date_range"]) == 2:
        start, end = filters["date_range"]
        result["order_ts"] = pd.to_datetime(result["order_ts"])
        result = result[result["order_ts"].dt.date >= start]
        result = result[result["order_ts"].dt.date <= end]

    # Status filter
    if filters.get("status") and filters["status"] != "All" and "status" in result.columns:
        result = result[result["status"] == filters["status"]]

    # Country filter (requires join with customers)
    if filters.get("country") and filters["country"] != "All" and customers_df is not None:
        if "customer_id" in result.columns:
            country_customers = customers_df[customers_df["country"] == filters["country"]]["customer_id"]
            result = result[result["customer_id"].isin(country_customers)]

    # Channel filter
    if filters.get("channel") and filters["channel"] != "All" and customers_df is not None:
        if "customer_id" in result.columns:
            channel_customers = customers_df[customers_df["channel"] == filters["channel"]]["customer_id"]
            result = result[result["customer_id"].isin(channel_customers)]

    return result