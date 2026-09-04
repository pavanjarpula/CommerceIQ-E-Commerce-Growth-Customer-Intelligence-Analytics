"""Dashboard - Premium Insight & Recommendation Card Components."""
import streamlit as st


def render_insight_card(title: str, finding: str, impact: str = "", impact_type: str = "success"):
    """Render a styled insight card with finding and impact."""
    impact_html = ""
    if impact:
        tag_class = f"ciq-tag ciq-tag-{impact_type}"
        impact_html = f'<div class="{tag_class}">{impact}</div>'

    st.markdown(
        f'<div class="ciq-insight">'
        f'<h4>{title}</h4>'
        f'<p>{finding}</p>'
        f'{impact_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_recommendation_card(rec: dict):
    """Render a structured recommendation card: Observation > Evidence > Implication > Action."""
    priority = rec.get("priority", "Medium")
    priority_cls = {"High": "high", "Medium": "medium", "Low": "low"}.get(priority, "medium")
    priority_label_cls = f"rec-label-{priority_cls}"

    sections_html = ""
    if rec.get("finding"):
        sections_html += f'<div class="rec-section"><span class="rec-section-label">Observation</span><p class="rec-body">{rec["finding"]}</p></div>'
    if rec.get("recommendation"):
        sections_html += f'<div class="rec-section"><span class="rec-section-label">Recommended Action</span><p class="rec-body">{rec["recommendation"]}</p></div>'
    if rec.get("expected_impact"):
        sections_html += f'<div class="rec-section"><span class="rec-section-label">Business Impact</span><p class="rec-body" style="color:#059669;font-weight:600;">{rec["expected_impact"]}</p></div>'

    st.markdown(
        f'<div class="ciq-rec ciq-rec-priority-{priority_cls}">'
        f'<div class="rec-label {priority_label_cls}">{priority} Priority</div>'
        f'<h4>{rec.get("category", "General")}</h4>'
        f'{sections_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_anomaly_card(metric: str, count: int, method: str, severity: str = "moderate", details: str = ""):
    """Render a severity-coded anomaly detection card."""
    severity_cls = f"ciq-anomaly ciq-anomaly-{severity}"
    detail_html = f'<div class="ciq-anomaly-detail">{details}</div>' if details else ""

    st.markdown(
        f'<div class="{severity_cls}">'
        f'<div class="ciq-anomaly-title">{metric}</div>'
        f'<div>{count} anomal{"y" if count == 1 else "ies"} detected '
        f'<span style="font-size:0.72rem;color:#64748b;font-weight:500;">({method})</span></div>'
        f'{detail_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_evidence_block(observation: str, evidence: str, implication: str, action: str):
    """Render the full Observation > Evidence > Implication > Action block."""
    st.markdown(
        f'<div class="ciq-card" style="padding:1rem 1.2rem;margin-bottom:0.6rem;">'
        f'<div style="margin-bottom:0.5rem;">'
        f'<span class="rec-section-label" style="color:#64748b;">Observation</span>'
        f'<p style="margin:0.15rem 0 0;font-size:0.82rem;color:#334155;line-height:1.55;">{observation}</p>'
        f'</div>'
        f'<div style="margin-bottom:0.5rem;">'
        f'<span class="rec-section-label" style="color:#64748b;">Evidence</span>'
        f'<p style="margin:0.15rem 0 0;font-size:0.82rem;color:#334155;line-height:1.55;">{evidence}</p>'
        f'</div>'
        f'<div style="margin-bottom:0.5rem;">'
        f'<span class="rec-section-label" style="color:#64748b;">Business Implication</span>'
        f'<p style="margin:0.15rem 0 0;font-size:0.82rem;color:#d97706;font-weight:500;line-height:1.55;">{implication}</p>'
        f'</div>'
        f'<div>'
        f'<span class="rec-section-label" style="color:#64748b;">Recommended Action</span>'
        f'<p style="margin:0.15rem 0 0;font-size:0.82rem;color:#059669;font-weight:500;line-height:1.55;">{action}</p>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
