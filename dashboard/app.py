"""CommerceIQ Analytics Dashboard - Main Entry Point."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from dashboard.utils.data_loader import load_all_metrics, load_orders, load_customers, load_products
from dashboard.components.filters import render_sidebar_filters

st.set_page_config(
    page_title="CommerceIQ Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ─────────────────────────────────────────────────────── */
    .stApp { background: #f8f9fb; }

    /* ── Sidebar ────────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f36 0%, #252b48 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e8eaf6;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: #c5cae9;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stDateInput label {
        color: #c5cae9 !important;
        font-weight: 600;
    }

    /* ── KPI Cards ──────────────────────────────────────────────────── */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e8eaf6;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        box-shadow: 0 4px 16px rgba(33,150,243,0.12);
    }
    div[data-testid="stMetric"] label {
        color: #5c6bc0;
        font-weight: 600;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #1a237e;
        font-weight: 700;
        font-size: 1.55rem;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        font-weight: 600;
    }

    /* ── Section Headers ────────────────────────────────────────────── */
    .section-header {
        background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
        color: white;
        padding: 14px 22px;
        border-radius: 10px;
        margin: 10px 0 18px 0;
        font-size: 1.05rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* ── DataFrames ─────────────────────────────────────────────────── */
    .stDataFrame { border-radius: 10px; overflow: hidden; }

    /* ── Expanders ──────────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #283593;
    }

    /* ── Divider ────────────────────────────────────────────────────── */
    hr { border: none; border-top: 1px solid #e8eaf6; margin: 1.2rem 0; }

    /* ── Tabs ───────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 18px;
        font-weight: 600;
    }

    /* ── Info/Warning boxes ─────────────────────────────────────────── */
    div[data-testid="stAlert"] { border-radius: 10px; }

    /* ── Plotly charts ──────────────────────────────────────────────── */
    .stPlotlyChart { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Data Loading ────────────────────────────────────────────────────────────
metrics = load_all_metrics()
orders = load_orders()
customers = load_customers()
products = load_products()

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## CommerceIQ")
    st.caption("Analytics Dashboard")
    st.markdown("---")

filters = render_sidebar_filters(orders, customers)

st.session_state["filters"] = filters
st.session_state["metrics"] = metrics