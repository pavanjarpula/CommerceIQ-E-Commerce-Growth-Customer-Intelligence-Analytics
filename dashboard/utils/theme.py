"""CommerceIQ Design System - Premium BI Theme, CSS, and Visual Identity."""
import streamlit as st
from datetime import datetime

# ── Color Palette ────────────────────────────────────────────────────────────
COLORS = {
    "primary":       "#0f172a",
    "accent":        "#3949ab",
    "accent_light":  "#5c6bc0",
    "accent_subtle": "#eef2ff",
    "success":       "#059669",
    "success_bg":    "#ecfdf5",
    "success_light": "#d1fae5",
    "warning":       "#d97706",
    "warning_bg":    "#fffbeb",
    "warning_light": "#fef3c7",
    "danger":        "#dc2626",
    "danger_bg":     "#fef2f2",
    "danger_light":  "#fee2e2",
    "info":          "#2563eb",
    "info_bg":       "#eff6ff",
    "info_light":    "#dbeafe",
    "purple":        "#7c3aed",
    "teal":          "#0d9488",
    "bg":            "#f8fafc",
    "surface":       "#ffffff",
    "border":        "#e2e8f0",
    "border_light":  "#f1f5f9",
    "text":          "#0f172a",
    "text_secondary": "#64748b",
    "text_muted":    "#94a3b8",
    "text_inverse":  "#ffffff",
    "sidebar_bg_start": "#1e3a5f",
    "sidebar_bg_end":   "#2c5282",
    "sidebar_text":     "#f7fafc",
    "sidebar_text_muted": "#bee3f8",
}

CHART_COLORS = ["#3949ab", "#059669", "#d97706", "#dc2626", "#7c3aed", "#0d9488", "#2563eb", "#5c6bc0"]

# ── Typography ───────────────────────────────────────────────────────────────
FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

# ── Complete CSS Design System ───────────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════════════════════
   CommerceIQ Premium BI Design System
   Enterprise-grade analytics platform styling
   ═══════════════════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Root Variables ─────────────────────────────────────────────────────── */
:root {
    --ciq-primary: #0f172a;
    --ciq-accent: #3949ab;
    --ciq-accent-light: #5c6bc0;
    --ciq-success: #059669;
    --ciq-warning: #d97706;
    --ciq-danger: #dc2626;
    --ciq-info: #2563eb;
    --ciq-bg: #f8fafc;
    --ciq-surface: #ffffff;
    --ciq-border: #e2e8f0;
    --ciq-border-light: #f1f5f9;
    --ciq-text: #0f172a;
    --ciq-text-secondary: #64748b;
    --ciq-text-muted: #94a3b8;
    --ciq-radius-sm: 6px;
    --ciq-radius: 10px;
    --ciq-radius-lg: 14px;
    --ciq-radius-xl: 18px;
    --ciq-shadow-xs: 0 1px 2px rgba(0,0,0,0.04);
    --ciq-shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --ciq-shadow: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
    --ciq-shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);
    --ciq-shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.08), 0 8px 10px -6px rgba(0,0,0,0.04);
    --ciq-transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Reset & Base ─────────────────────────────────────────────────────── */
.stApp {
    background: var(--ciq-bg);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ── Main Container ────────────────────────────────────────────────────── */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 1400px !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a5f 0%, #2c5282 50%, #1a365d 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #f7fafc !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] label {
    color: #bee3f8 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stDateInput label {
    color: #e2e8f0 !important;
    font-weight: 600;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
section[data-testid="stSidebar"] [data-baseweb="select"] {
    background: rgba(255,255,255,0.1);
    border-color: rgba(255,255,255,0.15);
    border-radius: 8px;
}
section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #f7fafc;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12) !important;
    margin: 0.5rem 0 !important;
}
section[data-testid="stSidebar"] .stCaption {
    color: #90cdf4 !important;
}
section[data-testid="stSidebar"] [data-baseweb="base-input"] {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.12) !important;
}

/* ── Sidebar Brand Block ──────────────────────────────────────────────── */
.ciq-sidebar-brand {
    padding: 0.4rem 0 1rem 0;
}
.ciq-sidebar-brand h1 {
    color: #f7fafc !important;
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    margin: 0 !important;
    letter-spacing: -0.03em !important;
}
.ciq-sidebar-brand p {
    color: #90cdf4 !important;
    font-size: 0.68rem !important;
    margin: 0.15rem 0 0 !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase;
}

/* ── Sidebar Navigation ──────────────────────────────────────────────── */
.ciq-sidebar-section {
    padding: 0.4rem 0 0.2rem;
}
.ciq-sidebar-section-label {
    color: #90cdf4 !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    margin: 0 0 0.3rem 0 !important;
    padding: 0 0.2rem;
}
.ciq-sidebar-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.25rem 0.4rem;
    border-radius: 6px;
    transition: background 0.15s ease;
}
.ciq-sidebar-stat:hover {
    background: rgba(255,255,255,0.05);
}
.ciq-sidebar-stat-label {
    color: #bee3f8;
    font-size: 0.75rem;
    font-weight: 500;
}
.ciq-sidebar-stat-value {
    color: #f7fafc;
    font-size: 0.78rem;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}
.ciq-sidebar-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.12);
    margin: 0.6rem 0;
}
.ciq-sidebar-status {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.4rem;
}
.ciq-sidebar-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #68d391;
    box-shadow: 0 0 6px rgba(104,211,145,0.5);
    animation: ciq-pulse 2s infinite;
}
@keyframes ciq-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.ciq-sidebar-status-text {
    color: #90cdf4;
    font-size: 0.7rem;
    font-weight: 500;
}

/* ── Page Header ──────────────────────────────────────────────────────── */
.ciq-page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 1.5rem;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    border-radius: var(--ciq-radius-lg);
    margin-bottom: 1.5rem;
    color: white;
    box-shadow: var(--ciq-shadow-lg);
    border: 1px solid rgba(255,255,255,0.05);
}
.ciq-page-header .header-content h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: white;
}
.ciq-page-header .header-content p {
    margin: 0.2rem 0 0;
    font-size: 0.82rem;
    color: rgba(255,255,255,0.6);
    font-weight: 400;
}
.ciq-page-header .header-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,255,255,0.1);
    padding: 0.35rem 0.8rem;
    border-radius: 8px;
    font-size: 0.72rem;
    font-weight: 600;
    color: rgba(255,255,255,0.85);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.08);
}

/* ── App Header (Landing) ─────────────────────────────────────────────── */
.ciq-app-header {
    text-align: center;
    padding: 1.5rem 1rem 0.5rem;
    margin-bottom: 0.5rem;
}
.ciq-app-header h1 {
    font-size: 1.8rem;
    font-weight: 900;
    color: var(--ciq-primary);
    margin: 0;
    letter-spacing: -0.04em;
}
.ciq-app-header .ciq-subtitle {
    font-size: 0.88rem;
    color: var(--ciq-text-secondary);
    margin: 0.3rem 0 0;
    font-weight: 500;
    letter-spacing: 0.01em;
}
.ciq-app-header-meta {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 0.7rem;
}
.ciq-app-header-meta-item {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.72rem;
    color: var(--ciq-text-muted);
    font-weight: 500;
}
.ciq-app-header-meta-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--ciq-success);
    box-shadow: 0 0 4px rgba(5,150,105,0.4);
}

/* ── KPI Cards ────────────────────────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: var(--ciq-surface);
    border: 1px solid var(--ciq-border);
    border-radius: var(--ciq-radius);
    padding: 1rem 1.2rem;
    box-shadow: var(--ciq-shadow-xs);
    transition: var(--ciq-transition);
    position: relative;
}
div[data-testid="stMetric"]:hover {
    box-shadow: var(--ciq-shadow);
    border-color: #c7d2fe;
    transform: translateY(-1px);
}
div[data-testid="stMetric"] label {
    color: var(--ciq-text-secondary) !important;
    font-weight: 600 !important;
    font-size: 0.7rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: var(--ciq-primary) !important;
    font-weight: 700 !important;
    font-size: 1.4rem !important;
    line-height: 1.2;
    font-variant-numeric: tabular-nums;
}
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
    font-weight: 600 !important;
    font-size: 0.78rem !important;
}

/* ── Section Headers ──────────────────────────────────────────────────── */
.ciq-section {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--ciq-primary);
    padding: 0.5rem 0 0.3rem;
    border-bottom: 2px solid var(--ciq-border);
    margin: 1.6rem 0 0.7rem 0;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.ciq-section:first-of-type {
    margin-top: 0;
}
.ciq-section-icon {
    font-size: 0.9rem;
}
.ciq-section-gradient {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: white;
    padding: 0.7rem 1.1rem;
    border-radius: var(--ciq-radius);
    margin: 0.8rem 0 1rem 0;
    font-size: 0.92rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    border: 1px solid rgba(255,255,255,0.06);
}

/* ── Cards ────────────────────────────────────────────────────────────── */
.ciq-card {
    background: var(--ciq-surface);
    border: 1px solid var(--ciq-border);
    border-radius: var(--ciq-radius);
    padding: 1.2rem 1.4rem;
    box-shadow: var(--ciq-shadow-xs);
    transition: var(--ciq-transition);
}
.ciq-card:hover {
    box-shadow: var(--ciq-shadow-sm);
}
.ciq-card-accent {
    border-left: 3px solid var(--ciq-accent);
}
.ciq-card-success {
    border-left: 3px solid var(--ciq-success);
    background: #f8fdf9;
}
.ciq-card-warning {
    border-left: 3px solid var(--ciq-warning);
    background: #fffdf8;
}
.ciq-card-danger {
    border-left: 3px solid var(--ciq-danger);
    background: #fef8f8;
}
.ciq-card-info {
    border-left: 3px solid var(--ciq-info);
    background: #f8faff;
}
.ciq-card-purple {
    border-left: 3px solid #7c3aed;
    background: #faf8ff;
}
.ciq-card-teal {
    border-left: 3px solid #0d9488;
    background: #f6fdfc;
}

/* ── Insight Cards ────────────────────────────────────────────────────── */
.ciq-insight {
    background: linear-gradient(135deg, #f8faff 0%, #eef2ff 100%);
    border-left: 3px solid var(--ciq-accent);
    border-radius: var(--ciq-radius);
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.ciq-insight h4 {
    margin: 0 0 0.3rem;
    font-size: 0.88rem;
    color: var(--ciq-primary);
    font-weight: 700;
}
.ciq-insight p {
    margin: 0.15rem 0;
    font-size: 0.82rem;
    color: #334155;
    line-height: 1.55;
}
.ciq-insight .ciq-tag {
    display: inline-block;
    padding: 0.12rem 0.5rem;
    border-radius: 5px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-top: 0.25rem;
}
.ciq-tag-success { background: #d1fae5; color: #065f46; }
.ciq-tag-warning { background: #fef3c7; color: #92400e; }
.ciq-tag-danger  { background: #fee2e2; color: #991b1b; }
.ciq-tag-info    { background: #dbeafe; color: #1e40af; }

/* ── Recommendation Cards ─────────────────────────────────────────────── */
.ciq-rec {
    background: var(--ciq-surface);
    border: 1px solid var(--ciq-border);
    border-radius: var(--ciq-radius);
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: var(--ciq-transition);
}
.ciq-rec:hover {
    box-shadow: var(--ciq-shadow-sm);
}
.ciq-rec-priority-high    { border-left: 3px solid var(--ciq-danger); }
.ciq-rec-priority-medium  { border-left: 3px solid var(--ciq-warning); }
.ciq-rec-priority-low     { border-left: 3px solid var(--ciq-success); }
.ciq-rec .rec-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
}
.ciq-rec .rec-label-high   { color: var(--ciq-danger); }
.ciq-rec .rec-label-medium { color: var(--ciq-warning); }
.ciq-rec .rec-label-low    { color: var(--ciq-success); }
.ciq-rec h4 {
    margin: 0 0 0.35rem;
    font-size: 0.92rem;
    color: var(--ciq-primary);
    font-weight: 700;
}
.ciq-rec .rec-body {
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.55;
}
.ciq-rec .rec-section {
    margin: 0.4rem 0;
}
.ciq-rec .rec-section-label {
    font-weight: 700;
    color: #334155;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ── Anomaly Cards ────────────────────────────────────────────────────── */
.ciq-anomaly {
    border-radius: var(--ciq-radius);
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
    line-height: 1.5;
    border: 1px solid transparent;
}
.ciq-anomaly-normal   { background: #ecfdf5; border-color: #a7f3d0; }
.ciq-anomaly-moderate { background: #fffbeb; border-color: #fde68a; }
.ciq-anomaly-high     { background: #fef2f2; border-color: #fecaca; }
.ciq-anomaly-title {
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--ciq-primary);
    margin-bottom: 0.2rem;
}
.ciq-anomaly-detail {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 0.15rem;
}

/* ── DataFrames / Tables ──────────────────────────────────────────────── */
.stDataFrame {
    border-radius: var(--ciq-radius);
    overflow: hidden;
    border: 1px solid var(--ciq-border);
}
.ciq-table-container {
    background: var(--ciq-surface);
    border: 1px solid var(--ciq-border);
    border-radius: var(--ciq-radius);
    overflow: hidden;
}

/* ── Expanders ────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    color: #334155 !important;
    font-size: 0.88rem !important;
}
.streamlit-expander {
    border: 1px solid var(--ciq-border) !important;
    border-radius: var(--ciq-radius) !important;
    overflow: hidden;
}

/* ── Tabs ─────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 3px;
    background: #f1f5f9;
    border-radius: var(--ciq-radius);
    padding: 3px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.5rem 1.1rem;
    font-weight: 600;
    font-size: 0.82rem;
    color: #64748b;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: var(--ciq-primary) !important;
    box-shadow: var(--ciq-shadow-sm);
}

/* ── Dividers ─────────────────────────────────────────────────────────── */
hr {
    border: none;
    border-top: 1px solid var(--ciq-border);
    margin: 0.8rem 0;
}

/* ── Info/Warning/Success boxes ───────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: var(--ciq-radius);
    font-size: 0.82rem;
}

/* ── Plotly charts ────────────────────────────────────────────────────── */
.stPlotlyChart {
    border-radius: var(--ciq-radius);
    overflow: hidden;
    background: var(--ciq-surface);
    border: 1px solid var(--ciq-border);
    padding: 0.5rem;
}

/* ── Empty States ─────────────────────────────────────────────────────── */
.ciq-empty {
    text-align: center;
    padding: 2.5rem 1rem;
    color: #94a3b8;
}
.ciq-empty-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    opacity: 0.4;
}
.ciq-empty h3 {
    color: #64748b;
    font-size: 0.95rem;
    font-weight: 600;
    margin: 0.3rem 0;
}
.ciq-empty p {
    font-size: 0.82rem;
    color: #94a3b8;
}

/* ── Filter Bar ───────────────────────────────────────────────────────── */
.ciq-filter-bar {
    background: var(--ciq-surface);
    border: 1px solid var(--ciq-border);
    border-radius: var(--ciq-radius);
    padding: 0.6rem 1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    box-shadow: var(--ciq-shadow-xs);
}
.ciq-filter-count {
    background: var(--ciq-accent);
    color: white;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.18rem 0.5rem;
    border-radius: 10px;
    white-space: nowrap;
}
.ciq-filter-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--ciq-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ── Status Indicators ────────────────────────────────────────────────── */
.ciq-status {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.75rem;
    font-weight: 500;
}
.ciq-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}
.ciq-status-ok .ciq-status-dot    { background: var(--ciq-success); box-shadow: 0 0 4px rgba(5,150,105,0.4); }
.ciq-status-warn .ciq-status-dot  { background: var(--ciq-warning); box-shadow: 0 0 4px rgba(217,119,6,0.4); }
.ciq-status-err .ciq-status-dot   { background: var(--ciq-danger); box-shadow: 0 0 4px rgba(220,38,38,0.4); }

/* ── Pipeline Steps ───────────────────────────────────────────────────── */
.ciq-pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    overflow-x: auto;
    padding: 1rem 0;
}
.ciq-pipeline-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 100px;
    text-align: center;
}
.ciq-pipeline-node {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3949ab, #1a237e);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.78rem;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(26,35,126,0.25);
    margin-bottom: 0.35rem;
}
.ciq-pipeline-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: #334155;
    max-width: 85px;
}
.ciq-pipeline-arrow {
    color: #cbd5e1;
    font-size: 1.1rem;
    margin: 0 0.15rem;
    flex-shrink: 0;
}

/* ── Navigation Cards (Landing) ───────────────────────────────────────── */
.ciq-nav-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.8rem;
    margin: 0.8rem 0;
}
.ciq-nav-card {
    background: var(--ciq-surface);
    border: 1px solid var(--ciq-border);
    border-radius: var(--ciq-radius);
    padding: 1.1rem 1.2rem;
    cursor: default;
    transition: var(--ciq-transition);
    text-decoration: none;
    display: block;
}
.ciq-nav-card:hover {
    box-shadow: var(--ciq-shadow);
    border-color: #c7d2fe;
    transform: translateY(-1px);
}
.ciq-nav-card h3 {
    margin: 0 0 0.2rem;
    font-size: 0.88rem;
    color: var(--ciq-primary);
    font-weight: 700;
}
.ciq-nav-card p {
    margin: 0;
    font-size: 0.75rem;
    color: #64748b;
    line-height: 1.4;
}
.ciq-nav-card .nav-icon {
    font-size: 1.2rem;
    margin-bottom: 0.4rem;
    display: block;
}

/* ── Validation Badge ─────────────────────────────────────────────────── */
.ciq-validation-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #ecfdf5;
    color: #065f46;
    padding: 0.45rem 0.9rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.88rem;
    border: 1px solid #a7f3d0;
}
.ciq-validation-badge-fail {
    background: #fef2f2;
    color: #991b1b;
    border-color: #fecaca;
}

/* ── Metric Context ───────────────────────────────────────────────────── */
.ciq-metric-context {
    font-size: 0.72rem;
    color: #64748b;
    margin-top: 0.1rem;
    font-weight: 500;
}

/* ── Sticky table header ──────────────────────────────────────────────── */
.ciq-sticky-table th {
    position: sticky;
    top: 0;
    background: #f8fafc;
    z-index: 1;
    border-bottom: 2px solid var(--ciq-border);
}

/* ── Buttons ──────────────────────────────────────────────────────────── */
.stDownloadButton > button {
    background: var(--ciq-accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    padding: 0.35rem 0.9rem !important;
    transition: var(--ciq-transition) !important;
}
.stDownloadButton > button:hover {
    background: #283593 !important;
    box-shadow: var(--ciq-shadow-sm) !important;
}

/* ── Callout Box ──────────────────────────────────────────────────────── */
.ciq-callout {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: var(--ciq-radius-lg);
    padding: 1.3rem 1.5rem;
    margin: 1rem 0;
    color: white;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: var(--ciq-shadow-lg);
}
.ciq-callout h3 {
    margin: 0 0 0.4rem;
    font-size: 1rem;
    font-weight: 700;
    color: white;
}
.ciq-callout p {
    margin: 0.15rem 0;
    font-size: 0.82rem;
    color: rgba(255,255,255,0.7);
    line-height: 1.5;
}

/* ── KPI Grid ─────────────────────────────────────────────────────────── */
.ciq-kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.8rem;
    margin: 0.6rem 0;
}
.ciq-kpi-item {
    background: var(--ciq-surface);
    border: 1px solid var(--ciq-border);
    border-radius: var(--ciq-radius);
    padding: 1rem 1.1rem;
    transition: var(--ciq-transition);
}
.ciq-kpi-item:hover {
    box-shadow: var(--ciq-shadow-sm);
    border-color: #c7d2fe;
}
.ciq-kpi-label {
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--ciq-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
}
.ciq-kpi-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--ciq-primary);
    font-variant-numeric: tabular-nums;
    line-height: 1.2;
}
.ciq-kpi-context {
    font-size: 0.72rem;
    color: #64748b;
    margin-top: 0.15rem;
}
.ciq-kpi-delta-positive {
    color: var(--ciq-success);
    font-weight: 600;
    font-size: 0.78rem;
}
.ciq-kpi-delta-negative {
    color: var(--ciq-danger);
    font-weight: 600;
    font-size: 0.78rem;
}

/* ── Executive Summary Card ───────────────────────────────────────────── */
.ciq-exec-summary {
    background: linear-gradient(135deg, #f8faff 0%, #eef2ff 50%, #f0fdf4 100%);
    border: 1px solid var(--ciq-border);
    border-radius: var(--ciq-radius-lg);
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
}
.ciq-exec-summary h3 {
    margin: 0 0 0.6rem;
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--ciq-primary);
}
.ciq-exec-summary p {
    margin: 0.15rem 0;
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.55;
}

/* ── Two Column Insight Layout ────────────────────────────────────────── */
.ciq-insight-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin: 0.6rem 0;
}
@media (max-width: 768px) {
    .ciq-insight-grid { grid-template-columns: 1fr; }
}

/* ── Methodology Steps ────────────────────────────────────────────────── */
.ciq-method-step {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    padding: 0.7rem 0;
    border-bottom: 1px solid var(--ciq-border-light);
}
.ciq-method-step:last-child {
    border-bottom: none;
}
.ciq-method-num {
    width: 28px;
    height: 28px;
    min-width: 28px;
    border-radius: 50%;
    background: var(--ciq-accent);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
}
.ciq-method-content h4 {
    margin: 0;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--ciq-primary);
}
.ciq-method-content p {
    margin: 0.1rem 0 0;
    font-size: 0.75rem;
    color: #64748b;
}

/* ── Responsive adjustments ───────────────────────────────────────────── */
@media (max-width: 768px) {
    .ciq-page-header {
        flex-direction: column;
        gap: 0.6rem;
        text-align: center;
    }
    .ciq-pipeline {
        flex-wrap: wrap;
        justify-content: center;
    }
    .ciq-app-header h1 {
        font-size: 1.4rem;
    }
    .ciq-app-header-meta {
        flex-wrap: wrap;
        gap: 0.8rem;
    }
    .ciq-nav-grid {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 480px) {
    .ciq-nav-grid {
        grid-template-columns: 1fr;
    }
}

/* ── Scrollbar Styling ────────────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

/* ── Streamlit Overrides ──────────────────────────────────────────────── */
.stSelectbox > div > div {
    border-radius: 8px !important;
}
.stDateInput > div > div {
    border-radius: 8px !important;
}
.stMultiSelect > div > div {
    border-radius: 8px !important;
}
</style>
"""


def inject_global_css():
    """Inject the complete design system CSS into the page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "", badge: str = ""):
    """Render a compact professional page header."""
    badge_html = ""
    if badge:
        badge_html = f'<div class="header-badge">{badge}</div>'

    subtitle_html = ""
    if subtitle:
        subtitle_html = f"<p>{subtitle}</p>"

    st.markdown(
        f'<div class="ciq-page-header">'
        f'<div class="header-content"><h2>{title}</h2>{subtitle_html}</div>'
        f'{badge_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_section_header(title: str, icon: str = ""):
    """Render a consistent section header with optional icon."""
    icon_html = f'<span class="ciq-section-icon">{icon}</span>' if icon else ""
    st.markdown(f'<div class="ciq-section">{icon_html}{title}</div>', unsafe_allow_html=True)


def render_empty_state(title: str = "No data available", message: str = "Try broadening your filter criteria."):
    """Render a polished empty state."""
    st.markdown(
        f'<div class="ciq-empty">'
        f'<div class="ciq-empty-icon">&#8709;</div>'
        f'<h3>{title}</h3>'
        f'<p>{message}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_filter_indicator(active_count: int):
    """Render an active filter count indicator."""
    if active_count > 0:
        st.markdown(
            f'<span class="ciq-filter-count">{active_count} filter{"s" if active_count > 1 else ""} applied</span>',
            unsafe_allow_html=True,
        )


def render_callout(title: str, body: str):
    """Render a dark executive callout box."""
    st.markdown(
        f'<div class="ciq-callout">'
        f'<h3>{title}</h3>'
        f'<p>{body}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def get_data_status_html() -> str:
    """Return HTML for data status indicator in header."""
    now = datetime.now().strftime("%b %d, %Y %H:%M")
    return (
        f'<div class="ciq-app-header-meta-item">'
        f'<span class="ciq-app-header-meta-dot"></span>'
        f'Data current: 2024'
        f'</div>'
        f'<div class="ciq-app-header-meta-item">'
        f'Last refresh: {now}'
        f'</div>'
    )
