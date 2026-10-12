"""
KPI Card components for the dashboard.
Provides styled metric cards with consistent formatting.
"""
import streamlit as st
from typing import Optional, Union


def render_kpi_row(kpis: list):
    """
    Render a row of KPI cards.
    
    Args:
        kpis: List of dictionaries with keys:
            - title: Card title
            - value: Main value to display
            - subtitle: Optional subtitle/description
            - delta: Optional change indicator
            - color: Optional accent color
    """
    cols = st.columns(len(kpis))
    
    for col, kpi in zip(cols, kpis):
        with col:
            render_metric_card(
                title=kpi.get('title', ''),
                value=kpi.get('value', ''),
                subtitle=kpi.get('subtitle'),
                delta=kpi.get('delta'),
                color=kpi.get('color', '#0d9488')
            )


def render_metric_card(
    title: str,
    value: Union[str, int, float],
    subtitle: Optional[str] = None,
    delta: Optional[Union[str, float]] = None,
    color: str = "#0d9488"
):
    """
    Render a single styled metric card.
    
    Args:
        title: Card title
        value: Main value to display
        subtitle: Optional subtitle text
        delta: Optional delta/change value
        color: Accent color for the card border
    """
    # Format value if numeric
    if isinstance(value, float):
        if value < 1 and value > 0:
            formatted_value = f"{value:.1%}"
        else:
            formatted_value = f"{value:,.2f}"
    elif isinstance(value, int):
        formatted_value = f"{value:,}"
    else:
        formatted_value = str(value)
    
    # Build delta HTML if provided
    delta_html = ""
    if delta is not None:
        if isinstance(delta, (int, float)):
            delta_color = "#10b981" if delta >= 0 else "#ef4444"
            delta_symbol = "+" if delta >= 0 else ""
            if isinstance(delta, float) and abs(delta) < 1:
                delta_str = f"{delta_symbol}{delta:.1%}"
            else:
                delta_str = f"{delta_symbol}{delta:,.2f}"
        else:
            delta_color = "#718096"
            delta_str = str(delta)
        
        delta_html = f"""
        <div style="color: {delta_color}; font-size: 0.875rem; font-weight: 500;">
            {delta_str}
        </div>
        """
    
    # Build subtitle HTML
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <div style="color: #718096; font-size: 0.875rem; margin-top: 0.25rem;">
            {subtitle}
        </div>
        """
    
    # Render card
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border-left: 4px solid {color};
        height: 100%;
    ">
        <div style="
            color: #4a5568;
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        ">
            {title}
        </div>
        <div style="
            color: #1a365d;
            font-size: 1.75rem;
            font-weight: 700;
            line-height: 1.2;
        ">
            {formatted_value}
        </div>
        {delta_html}
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def render_stat_highlight(
    label: str,
    value: str,
    icon: str = "",
    color: str = "#0d9488"
):
    """
    Render a compact stat highlight.
    
    Args:
        label: Stat label
        value: Stat value
        icon: Optional icon/emoji
        color: Accent color
    """
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        background: {color}10;
        border-radius: 8px;
    ">
        <div style="font-size: 1.5rem;">{icon}</div>
        <div>
            <div style="color: #718096; font-size: 0.75rem; text-transform: uppercase;">
                {label}
            </div>
            <div style="color: #1a365d; font-size: 1.25rem; font-weight: 600;">
                {value}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_comparison_card(
    title: str,
    items: list,
    highlight_index: Optional[int] = None
):
    """
    Render a comparison card with multiple items.
    
    Args:
        title: Card title
        items: List of dicts with 'label' and 'value' keys
        highlight_index: Index of item to highlight
    """
    items_html = ""
    for i, item in enumerate(items):
        is_highlighted = i == highlight_index
        bg_color = "#0d948810" if is_highlighted else "transparent"
        font_weight = "600" if is_highlighted else "400"
        
        items_html += f"""
        <div style="
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0.75rem;
            background: {bg_color};
            border-radius: 4px;
            margin-bottom: 0.25rem;
        ">
            <span style="color: #4a5568;">{item.get('label', '')}</span>
            <span style="color: #1a365d; font-weight: {font_weight};">
                {item.get('value', '')}
            </span>
        </div>
        """
    
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    ">
        <div style="
            color: #1a365d;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e2e8f0;
        ">
            {title}
        </div>
        {items_html}
    </div>
    """, unsafe_allow_html=True)
