"""
Custom CSS styles for the dashboard.
Modern dark theme with vibrant gradients and glowing accents.
"""
import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styling to the Streamlit application."""
    st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Main color palette - Vibrant Dark Theme */
    :root {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-card: #1e293b;
        --accent-blue: #3b82f6;
        --accent-cyan: #06b6d4;
        --accent-purple: #8b5cf6;
        --accent-pink: #ec4899;
        --accent-green: #10b981;
        --accent-orange: #f59e0b;
        --accent-red: #ef4444;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-color: #334155;
        --glow-blue: rgba(59, 130, 246, 0.5);
        --glow-cyan: rgba(6, 182, 212, 0.5);
    }
    
    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Sidebar styling - Gradient dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #f1f5f9 !important;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown span {
        color: #94a3b8 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: #334155;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Metric cards styling - Glassmorphism effect */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 1.25rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 40px rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4), 0 0 60px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    [data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
        font-weight: 800;
        font-size: 1.75rem !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #10b981 !important;
    }
    
    /* Metric label and value text fix */
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    
    [data-testid="stMetricLabel"] > div {
        color: #94a3b8 !important;
    }
    
    [data-testid="stMetricValue"] > div {
        color: #f1f5f9 !important;
    }
    
    /* Headers - Gradient text effect */
    h1 {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        letter-spacing: -0.02em;
    }
    
    h2 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
    }
    
    h3 {
        background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        font-size: 1.35rem !important;
    }
    
    h4 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    
    /* Paragraph text */
    p, li, span {
        color: #cbd5e1 !important;
    }
    
    strong {
        color: #f1f5f9 !important;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #334155;
    }
    
    [data-testid="stDataFrame"] > div {
        background-color: #1e293b !important;
    }
    
    /* Table text visibility fix */
    [data-testid="stDataFrame"] table {
        color: #f1f5f9 !important;
    }
    
    [data-testid="stDataFrame"] th {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stDataFrame"] td {
        color: #e2e8f0 !important;
        background-color: #1e293b !important;
    }
    
    [data-testid="stDataFrame"] tr:hover td {
        background-color: #334155 !important;
    }
    
    /* Glide data grid (new Streamlit tables) */
    .glideDataEditor {
        --gdg-bg-cell: #1e293b !important;
        --gdg-bg-header: #334155 !important;
        --gdg-text-dark: #f1f5f9 !important;
        --gdg-text-medium: #cbd5e1 !important;
        --gdg-text-light: #94a3b8 !important;
        --gdg-border-color: #475569 !important;
        --gdg-bg-cell-medium: #293548 !important;
        --gdg-accent-color: #3b82f6 !important;
        --gdg-accent-light: rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Table container - ensure horizontal scroll */
    [data-testid="stDataFrame"] > div {
        overflow-x: auto !important;
        min-width: 100% !important;
    }
    
    /* Make sure columns don't get too compressed */
    [data-testid="stDataFrame"] [role="columnheader"] {
        min-width: 80px !important;
        white-space: nowrap !important;
    }
    
    [data-testid="stDataFrame"] [role="gridcell"] {
        min-width: 60px !important;
        white-space: nowrap !important;
    }
    
    /* Data editor cells */
    [data-testid="stDataFrame"] [data-testid="glide-cell"] {
        color: #f1f5f9 !important;
    }
    
    /* Column headers */
    [data-testid="stDataFrame"] [role="columnheader"] {
        color: #f1f5f9 !important;
        background-color: #334155 !important;
    }
    
    /* Grid cells */
    [data-testid="stDataFrame"] [role="gridcell"] {
        color: #e2e8f0 !important;
    }
    
    /* Button styling - Gradient buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.6);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 10px;
        color: #f1f5f9 !important;
    }
    
    /* FORCE all selectbox text to be white */
    .stSelectbox * {
        color: #f1f5f9 !important;
    }
    
    .stSelectbox [data-baseweb="select"] * {
        color: #f1f5f9 !important;
    }
    
    [data-testid="stSelectbox"] * {
        color: #f1f5f9 !important;
    }
    
    /* Selectbox value text */
    .stSelectbox [data-baseweb="select"] span {
        color: #f1f5f9 !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        color: #f1f5f9 !important;
        background-color: #1e293b !important;
    }
    
    .stSelectbox [data-baseweb="select"] input {
        color: #f1f5f9 !important;
    }
    
    /* Selectbox placeholder and value */
    .stSelectbox div[data-baseweb="select"] div[class*="valueContainer"] {
        color: #f1f5f9 !important;
    }
    
    .stSelectbox div[data-baseweb="select"] div[class*="singleValue"] {
        color: #f1f5f9 !important;
    }
    
    /* Target the actual text inside selectbox */
    [data-testid="stSelectbox"] div[data-baseweb="select"] div {
        color: #f1f5f9 !important;
    }
    
    /* SVG icons in selectbox */
    .stSelectbox svg {
        fill: #f1f5f9 !important;
        color: #f1f5f9 !important;
    }
    
    .stSelectbox label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #1e293b !important;
        border-radius: 10px !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
    }
    
    /* Selected value in dropdown */
    .stSelectbox [data-baseweb="select"] span {
        color: #f1f5f9 !important;
    }
    
    /* Dropdown arrow icon */
    .stSelectbox svg {
        fill: #94a3b8 !important;
    }
    
    /* Dropdown menu */
    [data-baseweb="popover"] {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 10px !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #1e293b !important;
    }
    
    [data-baseweb="menu"] li {
        color: #f1f5f9 !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: #334155 !important;
    }
    
    /* Selected option highlight */
    [data-baseweb="menu"] li[aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
        color: #f1f5f9 !important;
    }
    
    .stTextInput label {
        color: #94a3b8 !important;
    }
    
    /* Slider */
    .stSlider label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    
    .stSlider [data-baseweb="slider"] {
        color: #f1f5f9 !important;
    }
    
    /* Slider track */
    .stSlider [data-baseweb="slider"] > div > div {
        background-color: #334155 !important;
    }
    
    /* Slider active track */
    .stSlider [data-baseweb="slider"] > div > div > div {
        background-color: #3b82f6 !important;
    }
    
    /* Slider thumb/handle */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #3b82f6 !important;
        border: 2px solid #f1f5f9 !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.5) !important;
    }
    
    /* Slider value text */
    .stSlider > div > div > div > div {
        color: #f1f5f9 !important;
    }
    
    /* Slider min/max labels */
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }
    
    /* Number input */
    .stNumberInput label {
        color: #94a3b8 !important;
    }
    
    .stNumberInput input {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border-color: #334155 !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 0.75rem 1.25rem;
        background-color: #1e293b;
        color: #94a3b8;
        border: 1px solid #334155;
        border-bottom: none;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%) !important;
        color: white !important;
        border-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 0 12px 12px 12px;
        padding: 1.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        color: #f1f5f9 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-top: none;
        border-radius: 0 0 12px 12px;
    }
    
    /* Info/Warning/Error boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
    }
    
    [data-testid="stAlert"][data-baseweb="notification"] {
        background-color: rgba(59, 130, 246, 0.15);
        border-left: 4px solid #3b82f6;
    }
    
    /* Warning */
    .stAlert [data-baseweb="notification"][kind="warning"] {
        background-color: rgba(245, 158, 11, 0.15) !important;
        border-left: 4px solid #f59e0b;
    }
    
    /* Custom KPI card class - Glassmorphism */
    .kpi-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4), 0 0 40px rgba(59, 130, 246, 0.15);
    }
    
    .kpi-card-title {
        color: #94a3b8;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }
    
    .kpi-card-value {
        background: linear-gradient(135deg, #f1f5f9 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.25rem;
        font-weight: 800;
        line-height: 1.2;
    }
    
    .kpi-card-subtitle {
        color: #64748b;
        font-size: 0.875rem;
        margin-top: 0.5rem;
    }
    
    /* Risk category badges - Glowing effect */
    .risk-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        color: #f87171;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid rgba(239, 68, 68, 0.4);
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
        color: #fbbf24;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid rgba(245, 158, 11, 0.4);
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        color: #34d399;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
    }
    
    /* Cluster badges */
    .cluster-0 {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
        color: #60a5fa;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid rgba(59, 130, 246, 0.4);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
    }
    
    .cluster-1 {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%);
        color: #34d399;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Divider styling */
    hr {
        border-color: #334155;
        margin: 2rem 0;
        opacity: 0.5;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #94a3b8 !important;
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #cbd5e1 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #06b6d4 100%);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Section cards */
    .section-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Glow effect for important elements */
    .glow-blue {
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.4);
    }
    
    .glow-cyan {
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.4);
    }
    
    .glow-green {
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)


def render_kpi_card(title: str, value: str, subtitle: str = None, color: str = "#3b82f6"):
    """Render a styled KPI card with glassmorphism effect."""
    subtitle_html = f'<div class="kpi-card-subtitle">{subtitle}</div>' if subtitle else ''
    return st.markdown(f"""
    <div class="kpi-card" style="border-color: {color}40; background: linear-gradient(135deg, {color}20 0%, {color}10 100%);">
        <div class="kpi-card-title">{title}</div>
        <div class="kpi-card-value">{value}</div>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def render_stat_card(title: str, value: str, icon: str = "📊", trend: str = None, trend_positive: bool = True):
    """Render a compact stat card with icon and optional trend."""
    trend_html = ""
    if trend:
        trend_color = "#10b981" if trend_positive else "#ef4444"
        trend_arrow = "↑" if trend_positive else "↓"
        trend_html = f'<span style="color: {trend_color}; font-size: 0.875rem; font-weight: 600;">{trend_arrow} {trend}</span>'
    
    return st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.75rem;
    ">
        <div style="font-size: 1.75rem;">{icon}</div>
        <div style="flex: 1;">
            <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{title}</div>
            <div style="color: #f1f5f9; font-size: 1.25rem; font-weight: 700;">{value} {trend_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
