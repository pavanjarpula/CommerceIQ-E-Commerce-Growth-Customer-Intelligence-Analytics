"""Dashboard - Formatting utilities for premium BI presentation."""


def fmt_currency(val, decimals=0):
    """Format as currency with K/M abbreviations. $3,671,066 -> $3.67M"""
    if val is None:
        return "$0"
    if abs(val) >= 1_000_000:
        return f"${val/1_000_000:,.{decimals if decimals else 2}f}M"
    if abs(val) >= 1_000:
        return f"${val/1_000:,.{decimals}f}K"
    return f"${val:,.{decimals}f}"


def fmt_number(val, decimals=0):
    """Format as number with K/M abbreviations. 59,599 -> 59.6K"""
    if val is None:
        return "0"
    if abs(val) >= 1_000_000:
        return f"{val/1_000_000:,.{decimals if decimals else 1}f}M"
    if abs(val) >= 1_000:
        return f"{val/1_000:,.{decimals if decimals else 1}f}K"
    return f"{val:,.{decimals}f}"


def fmt_pct(val, decimals=1):
    """Format as percentage. 0.320 -> 32.0%"""
    if val is None:
        return "0%"
    return f"{val*100:.{decimals}f}%"


def fmt_delta(val):
    """Format as signed percentage delta. +5.2% / -3.1%"""
    if val is None:
        return None
    sign = "+" if val >= 0 else ""
    return f"{sign}{val*100:.1f}%"


def fmt_compact(val, prefix="$"):
    """Format large numbers compactly with tiered precision."""
    if val is None:
        return f"{prefix}0"
    abs_val = abs(val)
    if abs_val >= 1_000_000:
        return f"{prefix}{val/1_000_000:,.2f}M"
    if abs_val >= 100_000:
        return f"{prefix}{val/1_000:,.1f}K"
    if abs_val >= 1_000:
        return f"{prefix}{val/1_000:,.1f}K"
    return f"{prefix}{val:,.0f}"


def fmt_int(val):
    """Format as integer with commas. 12,000"""
    if val is None:
        return "0"
    return f"{int(val):,}"


def fmt_ratio(val, decimals=2):
    """Format as a ratio (e.g., 1.23x)."""
    if val is None:
        return "N/A"
    return f"{val:,.{decimals}f}x"


def fmt_delta_color(val):
    """Return Streamlit delta color string based on value direction."""
    if val is None:
        return "off"
    return "normal" if val >= 0 else "inverse"


def fmt_kpi_value(val, fmt_type="number", prefix="$"):
    """Unified KPI value formatter used by premium KPI components."""
    if fmt_type == "currency":
        return fmt_currency(val)
    elif fmt_type == "pct":
        return fmt_pct(val)
    elif fmt_type == "int":
        return fmt_int(val)
    elif fmt_type == "ratio":
        return fmt_ratio(val)
    else:
        return fmt_number(val)


def fmt_table_currency(val):
    """Table-safe currency formatting."""
    if val is None or val == "":
        return "—"
    try:
        return fmt_currency(float(val))
    except (ValueError, TypeError):
        return str(val)


def fmt_table_pct(val):
    """Table-safe percentage formatting."""
    if val is None or val == "":
        return "—"
    try:
        v = float(val)
        if v < 1 and v > 0:
            return f"{v*100:.1f}%"
        return f"{v:.1f}%"
    except (ValueError, TypeError):
        return str(val)


def fmt_table_number(val):
    """Table-safe number formatting."""
    if val is None or val == "":
        return "—"
    try:
        return fmt_number(float(val))
    except (ValueError, TypeError):
        return str(val)
