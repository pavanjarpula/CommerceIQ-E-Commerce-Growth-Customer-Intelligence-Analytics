"""Dashboard - Premium Application Header & Sidebar Component."""
import streamlit as st
from datetime import datetime


def render_app_header(metrics: dict = None):
    """Render the global CommerceIQ application header in the sidebar."""
    with st.sidebar:
        st.markdown(
            '<div class="ciq-sidebar-brand">'
            '<h1>CommerceIQ</h1>'
            '<p>E-Commerce BI Platform</p>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="ciq-sidebar-divider">', unsafe_allow_html=True)

        if metrics:
            revenue = metrics.get("revenue", {})
            rfm = metrics.get("rfm", {})

            st.markdown(
                '<p class="ciq-sidebar-section-label">Platform Summary</p>',
                unsafe_allow_html=True,
            )

            stats = [
                ("Orders", f"{revenue.get('total_orders', 0):,}"),
                ("Revenue", f"${revenue.get('total_net_revenue', 0)/1_000_000:.2f}M"),
                ("Customers", f"{rfm.get('total_customers', 0):,}"),
                ("Products", "120"),
            ]
            for label, value in stats:
                st.markdown(
                    f'<div class="ciq-sidebar-stat">'
                    f'<span class="ciq-sidebar-stat-label">{label}</span>'
                    f'<span class="ciq-sidebar-stat-value">{value}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<hr class="ciq-sidebar-divider">', unsafe_allow_html=True)

        now = datetime.now().strftime("%b %d, %H:%M")
        st.markdown(
            f'<div class="ciq-sidebar-status">'
            f'<span class="ciq-sidebar-status-dot"></span>'
            f'<span class="ciq-sidebar-status-text">Data current: 2024 &middot; {now}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def render_page_badge(text: str):
    """Render a small badge in the page header."""
    return f'<div class="header-badge">{text}</div>'
