"""
Retail Customer Analytics Dashboard
AI-Powered Customer Retention & Behavioral Segmentation

Main application entry point.
IT3091 - Machine Learning | SLIIT | Group 2026-DS-60
"""
import streamlit as st
from pathlib import Path
import sys

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from components.styles import apply_custom_styles
from components.sidebar import render_sidebar

# Page configuration
st.set_page_config(
    page_title="Retail Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styles()

# Render sidebar navigation
render_sidebar()

# Hero Section
st.markdown("""
<div style="text-align: center; padding: 2.5rem 2rem; background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.1) 50%, rgba(6, 182, 212, 0.15) 100%); border-radius: 24px; border: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 2rem;">
    <div style="font-size: 3rem; margin-bottom: 1rem; letter-spacing: 0.5rem;">🛒 📊 🎯 👥 📈</div>
    <h1 style="font-size: 2.5rem; margin-bottom: 0.75rem; background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 50%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Retail Customer Analytics</h1>
    <p style="font-size: 1.2rem; margin-bottom: 1.5rem; color: #94a3b8;">AI-Powered Customer Retention Prediction & Behavioral Segmentation Dashboard</p>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
        <span style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); color: #34d399; padding: 0.5rem 1rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600;">✓ 1,696 Customers</span>
        <span style="background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); color: #60a5fa; padding: 0.5rem 1rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600;">✓ 4 ML Models</span>
        <span style="background: rgba(139, 92, 246, 0.2); border: 1px solid rgba(139, 92, 246, 0.4); color: #a78bfa; padding: 0.5rem 1rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600;">✓ 68.6% Accuracy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Dashboard overview
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.05) 100%); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 20px; padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(239, 68, 68, 0.15);">
    <div style="width: 80px; height: 80px; margin: 0 auto 1.25rem auto; background: linear-gradient(135deg, #ef4444 0%, #f87171 100%); border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4);">🎯</div>
    <h3 style="margin-bottom: 0.75rem; font-size: 1.25rem; color: #f1f5f9;">Retention Prediction</h3>
    <p style="font-size: 0.9rem; margin-bottom: 1.25rem; color: #94a3b8;">Identify at-risk customers using Random Forest ML model</p>
    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center;">
        <span style="background: rgba(239, 68, 68, 0.3); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.7rem; color: #fca5a5;">🔮 Risk Scores</span>
        <span style="background: rgba(239, 68, 68, 0.3); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.7rem; color: #fca5a5;">📤 Export</span>
    </div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.05) 100%); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 20px; padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);">
    <div style="width: 80px; height: 80px; margin: 0 auto 1.25rem auto; background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%); border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);">👥</div>
    <h3 style="margin-bottom: 0.75rem; font-size: 1.25rem; color: #f1f5f9;">Customer Segmentation</h3>
    <p style="font-size: 0.9rem; margin-bottom: 1.25rem; color: #94a3b8;">K-Means clustering reveals 2 behavioral groups</p>
    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center;">
        <span style="background: rgba(59, 130, 246, 0.3); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.7rem; color: #93c5fd;">📊 Profiles</span>
        <span style="background: rgba(59, 130, 246, 0.3); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.7rem; color: #93c5fd;">📈 Charts</span>
    </div>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.05) 100%); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 20px; padding: 2rem; text-align: center; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);">
    <div style="width: 80px; height: 80px; margin: 0 auto 1.25rem auto; background: linear-gradient(135deg, #10b981 0%, #34d399 100%); border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);">📊</div>
    <h3 style="margin-bottom: 0.75rem; font-size: 1.25rem; color: #f1f5f9;">Business Insights</h3>
    <p style="font-size: 0.9rem; margin-bottom: 1.25rem; color: #94a3b8;">Model comparison and recommendations</p>
    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center;">
        <span style="background: rgba(16, 185, 129, 0.3); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.7rem; color: #6ee7b7;">🏆 Compare</span>
        <span style="background: rgba(16, 185, 129, 0.3); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.7rem; color: #6ee7b7;">💡 Tips</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ML Pipeline Workflow
st.markdown('<h3 style="text-align: center; margin-bottom: 1.5rem; color: #f1f5f9;">🔄 Machine Learning Pipeline</h3>', unsafe_allow_html=True)

st.markdown("""
<div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 0.75rem; padding: 1rem;">
    <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(139, 92, 246, 0.1) 100%); border: 1px solid rgba(139, 92, 246, 0.4); border-radius: 12px; padding: 1rem; text-align: center; min-width: 100px;">
        <div style="font-size: 1.5rem;">📥</div>
        <div style="font-size: 0.75rem; font-weight: 600; color: #a78bfa;">Data Import</div>
    </div>
    <div style="color: #64748b; font-size: 1.25rem;">→</div>
    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 12px; padding: 1rem; text-align: center; min-width: 100px;">
        <div style="font-size: 1.5rem;">🧹</div>
        <div style="font-size: 0.75rem; font-weight: 600; color: #60a5fa;">Preprocessing</div>
    </div>
    <div style="color: #64748b; font-size: 1.25rem;">→</div>
    <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(6, 182, 212, 0.1) 100%); border: 1px solid rgba(6, 182, 212, 0.4); border-radius: 12px; padding: 1rem; text-align: center; min-width: 100px;">
        <div style="font-size: 1.5rem;">⚙️</div>
        <div style="font-size: 0.75rem; font-weight: 600; color: #22d3ee;">Features</div>
    </div>
    <div style="color: #64748b; font-size: 1.25rem;">→</div>
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(16, 185, 129, 0.1) 100%); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 1rem; text-align: center; min-width: 100px;">
        <div style="font-size: 1.5rem;">🤖</div>
        <div style="font-size: 0.75rem; font-weight: 600; color: #34d399;">Training</div>
    </div>
    <div style="color: #64748b; font-size: 1.25rem;">→</div>
    <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 12px; padding: 1rem; text-align: center; min-width: 100px;">
        <div style="font-size: 1.5rem;">📊</div>
        <div style="font-size: 0.75rem; font-weight: 600; color: #fbbf24;">Evaluation</div>
    </div>
    <div style="color: #64748b; font-size: 1.25rem;">→</div>
    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 12px; padding: 1rem; text-align: center; min-width: 100px;">
        <div style="font-size: 1.5rem;">🎯</div>
        <div style="font-size: 0.75rem; font-weight: 600; color: #f87171;">Prediction</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Key Metrics Row
st.markdown('<h3 style="text-align: center; margin-bottom: 1.5rem; color: #f1f5f9;">📈 Key Performance Metrics</h3>', unsafe_allow_html=True)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(59, 130, 246, 0.05) 100%); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 16px; padding: 1.5rem; text-align: center;">
    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🏆</div>
    <div style="font-size: 2rem; font-weight: 800; color: #60a5fa;">68.6%</div>
    <div style="font-size: 0.8rem; color: #94a3b8;">Validation Accuracy</div>
</div>
""", unsafe_allow_html=True)

with metric_col2:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 16px; padding: 1.5rem; text-align: center;">
    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👥</div>
    <div style="font-size: 2rem; font-weight: 800; color: #34d399;">1,696</div>
    <div style="font-size: 0.8rem; color: #94a3b8;">Customers Analyzed</div>
</div>
""", unsafe_allow_html=True)

with metric_col3:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 16px; padding: 1.5rem; text-align: center;">
    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
    <div style="font-size: 2rem; font-weight: 800; color: #a78bfa;">0.689</div>
    <div style="font-size: 0.8rem; color: #94a3b8;">Silhouette Score</div>
</div>
""", unsafe_allow_html=True)

with metric_col4:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 16px; padding: 1.5rem; text-align: center;">
    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔢</div>
    <div style="font-size: 2rem; font-weight: 800; color: #fbbf24;">K=2</div>
    <div style="font-size: 0.8rem; color: #94a3b8;">Optimal Clusters</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# About Section
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 16px; padding: 2rem;">
    <h3 style="margin-bottom: 1.25rem; color: #f1f5f9;">ℹ️ About This Dashboard</h3>
    <p style="margin-bottom: 1rem; color: #cbd5e1;">This dashboard presents the results of a machine learning project focused on <strong style="color: #f1f5f9;">customer retention prediction</strong> and <strong style="color: #f1f5f9;">behavioral segmentation</strong> for online retail.</p>
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem;">
        <div>
            <p style="color: #cbd5e1;"><strong style="color: #f1f5f9;">🤖 Classification Models:</strong> Four optimized models trained to predict customer inactivity</p>
            <p style="color: #cbd5e1;"><strong style="color: #f1f5f9;">📊 Segmentation:</strong> K-Means clustering to identify customer behavioral groups</p>
        </div>
        <div>
            <p style="color: #cbd5e1;"><strong style="color: #f1f5f9;">📁 Data Source:</strong> UCI Online Retail Dataset (Dec 2010 - Dec 2011)</p>
            <p style="color: #cbd5e1;"><strong style="color: #f1f5f9;">🎯 Best Model:</strong> Random Forest with 68.6% validation accuracy</p>
        </div>
    </div>
    <p style="font-size: 0.875rem; color: #94a3b8;">⚠️ All predictions are decision-support tools based on historical patterns, not definitive predictions.</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem 0; margin-top: 2rem; border-top: 1px solid #334155;">
    <p style="font-size: 0.875rem; margin-bottom: 0.5rem; color: #cbd5e1;"><strong style="color: #f1f5f9;">IT3091 - Machine Learning</strong> | Sri Lanka Institute of Information Technology (SLIIT)</p>
    <p style="font-size: 0.8rem; color: #64748b;">Group: 2026-DS-60 | Customer Retention Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)
