"""Dashboard - Premium Methodology & Pipeline Visualization Components."""
import streamlit as st


PIPELINE_STEPS = [
    ("01", "Raw Data"),
    ("02", "Ingestion"),
    ("03", "Validation"),
    ("04", "Cleaning"),
    ("05", "Feature Eng."),
    ("06", "KPI Compute"),
    ("07", "SQL Analytics"),
    ("08", "Statistics"),
    ("09", "Insights"),
]


def render_pipeline_visualization():
    """Render the analytics pipeline as a horizontal step flow."""
    steps_html = ""
    for i, (num, label) in enumerate(PIPELINE_STEPS):
        arrow = '<div class="ciq-pipeline-arrow">&#8594;</div>' if i < len(PIPELINE_STEPS) - 1 else ""
        steps_html += (
            f'<div class="ciq-pipeline-step">'
            f'<div class="ciq-pipeline-node">{num}</div>'
            f'<div class="ciq-pipeline-label">{label}</div>'
            f'</div>'
            f'{arrow}'
        )

    st.markdown(
        f'<div class="ciq-pipeline">{steps_html}</div>',
        unsafe_allow_html=True,
    )


def render_validation_summary(validation: dict):
    """Render a clean validation results summary."""
    checks = validation.get("checks", [])
    passed = validation.get("passed", 0)
    failed = validation.get("failed", 0)
    total = validation.get("total_checks", 0)

    if total == 0:
        st.markdown(
            '<div class="ciq-empty"><h3>No validation data available</h3></div>',
            unsafe_allow_html=True,
        )
        return

    badge_class = "ciq-validation-badge" if failed == 0 else "ciq-validation-badge ciq-validation-badge-fail"
    st.markdown(
        f'<div style="margin-bottom:0.8rem;">'
        f'<div class="{badge_class}">'
        f'&#10003; {passed} / {total} validation checks passed'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if checks:
        check_df = __import__("pandas").DataFrame(checks)
        if len(check_df.columns) >= 3:
            check_df.columns = ["Check", "Status", "Detail"] + list(check_df.columns[3:])
            check_df = check_df[["Check", "Status", "Detail"]]
        st.dataframe(check_df, use_container_width=True, hide_index=True)


def render_dataset_overview_card():
    """Render the dataset overview introduction card."""
    st.markdown(
        '<div class="ciq-card" style="margin-bottom:1rem;">'
        '<h3 style="margin:0 0 0.3rem;color:#0f172a;font-size:0.95rem;font-weight:700;">Dataset Overview</h3>'
        '<p style="margin:0;font-size:0.82rem;color:#475569;line-height:1.55;">'
        'This dashboard analyzes e-commerce transaction data covering orders, customers, products, '
        'and order events. All data has been profiled and validated through an automated analytics pipeline '
        'built with Python, pandas, SQLite, and statistical analysis libraries.</p>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_methodology_step(num: int, title: str, description: str):
    """Render a single methodology step."""
    st.markdown(
        f'<div class="ciq-method-step">'
        f'<div class="ciq-method-num">{num}</div>'
        f'<div class="ciq-method-content">'
        f'<h4>{title}</h4>'
        f'<p>{description}</p>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
