"""
Sidebar navigation component.
Provides consistent navigation across all dashboard pages.
"""
import streamlit as st
from pathlib import Path


def render_sidebar():
    """Render the sidebar with navigation and project information."""
    with st.sidebar:
        # Dashboard title with gradient effect
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
            <h1 style="
                font-size: 1.35rem; 
                margin-bottom: 0.5rem;
                background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">
                Retail Analytics
            </h1>
            <p style="font-size: 0.8rem; opacity: 0.7; margin: 0;">
                ML Customer Retention
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation section with icons
        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.6; margin-bottom: 0.75rem;">
                📍 Navigation
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
            border-left: 3px solid #ef4444;
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
        ">
            <p style="font-weight: 600; margin: 0; font-size: 0.875rem;">🎯 Retention Prediction</p>
            <p style="font-size: 0.75rem; opacity: 0.7; margin: 0.25rem 0 0 0;">Risk assessment & export</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(59, 130, 246, 0.05) 100%);
            border-left: 3px solid #3b82f6;
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
        ">
            <p style="font-weight: 600; margin: 0; font-size: 0.875rem;">👥 Customer Segmentation</p>
            <p style="font-size: 0.75rem; opacity: 0.7; margin: 0.25rem 0 0 0;">Behavioral clusters</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
            border-left: 3px solid #10b981;
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
        ">
            <p style="font-weight: 600; margin: 0; font-size: 0.875rem;">📊 Business Insights</p>
            <p style="font-size: 0.75rem; opacity: 0.7; margin: 0.25rem 0 0 0;">Model performance</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Model Stats
        st.markdown("""
        <div style="margin-bottom: 0.75rem;">
            <p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.6; margin-bottom: 0.75rem;">
                🤖 Model Stats
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats in compact format
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 12px;
            padding: 1rem;
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-size: 0.75rem; opacity: 0.7;">Algorithm</span>
                <span style="font-size: 0.875rem; font-weight: 600; color: #a78bfa;">Random Forest</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-size: 0.75rem; opacity: 0.7;">Accuracy</span>
                <span style="font-size: 0.875rem; font-weight: 600; color: #34d399;">68.6%</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-size: 0.75rem; opacity: 0.7;">Threshold</span>
                <span style="font-size: 0.875rem; font-weight: 600; color: #60a5fa;">0.425</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 0.75rem; opacity: 0.7;">Clusters</span>
                <span style="font-size: 0.875rem; font-weight: 600; color: #fbbf24;">K=2</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Project badge
        st.markdown("""
        <div style="
            text-align: center;
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.05) 100%);
            border: 1px solid rgba(6, 182, 212, 0.3);
            border-radius: 12px;
            padding: 1rem;
        ">
            <p style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.6; margin-bottom: 0.5rem;">
                IT3091 • Machine Learning
            </p>
            <p style="font-size: 0.875rem; font-weight: 600; margin: 0;">
                SLIIT • Group 2026-DS-60
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size: 0.65rem; opacity: 0.5; text-align: center; margin-top: 1rem; padding: 0 0.5rem;">
            ⚠️ Predictions are decision-support tools based on historical patterns
        </div>
        """, unsafe_allow_html=True)
