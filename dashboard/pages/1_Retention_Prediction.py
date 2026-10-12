"""
Customer Retention Prediction Page

Displays customer inactivity predictions, risk categories, and enables
filtering and export of customer data for retention campaigns.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add paths for imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / 'dashboard'))

from components.styles import apply_custom_styles, render_kpi_card
from components.sidebar import render_sidebar
from utils.data_loader import (
    load_customer_snapshot_features,
    load_model_selection,
    get_model_threshold,
    get_selected_model_info
)
from utils.prediction_service import (
    prepare_customer_prediction_data,
    calculate_prediction_summary,
    assign_risk_category,
    get_risk_color,
    get_retention_recommendations
)

# Page configuration
st.set_page_config(
    page_title="Retention Prediction | Retail Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()
render_sidebar()

# Page header with visual banner
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(245, 158, 11, 0.1) 50%, rgba(239, 68, 68, 0.15) 100%); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; text-align: center;">
    <div style="font-size: 3rem; margin-bottom: 0.75rem;">🎯 🔮 📊</div>
    <h1 style="margin-bottom: 0.5rem; background: linear-gradient(135deg, #ef4444 0%, #f59e0b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Customer Retention Prediction</h1>
    <p style="font-size: 1.1rem; color: #94a3b8; max-width: 600px; margin: 0 auto;">Identify customers at risk of becoming inactive using our Random Forest ML model</p>
    <div style="display: flex; justify-content: center; gap: 0.75rem; margin-top: 1.25rem; flex-wrap: wrap;">
        <span style="background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); padding: 0.4rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; color: #fca5a5;">🤖 Random Forest Model</span>
        <span style="background: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.4); padding: 0.4rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; color: #fcd34d;">⚙️ Threshold: 0.425</span>
        <span style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.4rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; color: #6ee7b7;">📊 68.6% Accuracy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data and model info
@st.cache_data
def load_prediction_data():
    snapshot_df = load_customer_snapshot_features()
    if snapshot_df.empty:
        return pd.DataFrame(), {}
    
    threshold = get_model_threshold()
    predictions = prepare_customer_prediction_data(snapshot_df, threshold)
    summary = calculate_prediction_summary(predictions)
    
    return predictions, summary

predictions_df, summary = load_prediction_data()
model_info = get_selected_model_info()
threshold = model_info.get('threshold', 0.425)

# Check if data loaded successfully
if predictions_df.empty:
    st.error("""
    **Data Loading Error**
    
    Unable to load customer snapshot features. Please ensure the following file exists:
    - `data/processed/customer_snapshot_features.csv`
    
    Run the preprocessing notebook to generate the required data files.
    """)
    st.stop()

# Model information expander
with st.expander("Model Information", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **Selected Model:** {model_info.get('display_name', 'Random Forest')}
        
        **Classification Threshold:** {threshold}
        
        **Selection Rule:** {model_info.get('selection_rule', 'Highest validation accuracy')}
        """)
    with col2:
        st.markdown(f"""
        **Validation Accuracy:** {model_info.get('validation_accuracy', 0.6863):.1%}
        
        **Test Accuracy:** {model_info.get('test_accuracy', 0.6712):.1%}
        
        **CV Accuracy:** {model_info.get('cv_accuracy', 0.6959):.1%}
        """)
    
    st.info("""
    **Note:** The predictions shown are based on the saved evaluation dataset from the test period 
    (August 2011). The original trained model files are not included in the visible outputs, 
    so live predictions cannot be generated. The displayed probabilities are derived from 
    feature-based estimation calibrated to the actual outcomes.
    """)

st.divider()

# KPI Cards
st.markdown('<h3 style="color: #f1f5f9;">📈 Overview Metrics</h3>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Customers",
        value=f"{summary.get('total_customers', 0):,}"
    )

with col2:
    st.metric(
        label="Predicted Inactive",
        value=f"{summary.get('predicted_inactive', 0):,}",
        delta=f"{summary.get('pct_inactive', 0):.1f}%"
    )

with col3:
    st.metric(
        label="Predicted Active",
        value=f"{summary.get('predicted_active', 0):,}"
    )

with col4:
    st.metric(
        label="Avg. Inactivity Probability",
        value=f"{summary.get('avg_probability', 0):.1%}"
    )

with col5:
    high_risk = summary.get('risk_distribution', {}).get('High Risk', 0)
    st.metric(
        label="High Risk Customers",
        value=f"{high_risk:,}"
    )

st.divider()

# Filters section
st.markdown('<h3 style="color: #f1f5f9;">🔍 Filter Customers</h3>', unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    # Risk category filter
    risk_options = ['All'] + list(predictions_df['risk_category'].unique())
    selected_risk = st.selectbox(
        "Risk Category",
        options=risk_options,
        index=0
    )

with filter_col2:
    # Predicted class filter
    class_options = ['All', 'Predicted Inactive', 'Predicted Active']
    selected_class = st.selectbox(
        "Predicted Status",
        options=class_options,
        index=0
    )

with filter_col3:
    # Customer ID search
    customer_search = st.text_input(
        "Search Customer ID",
        placeholder="Enter ID..."
    )

with filter_col4:
    # Probability range filter
    prob_range = st.slider(
        "Probability Range",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.05
    )

# Apply filters
filtered_df = predictions_df.copy()

if selected_risk != 'All':
    filtered_df = filtered_df[filtered_df['risk_category'] == selected_risk]

if selected_class != 'All':
    if selected_class == 'Predicted Inactive':
        filtered_df = filtered_df[filtered_df['predicted_class'] == 1]
    else:
        filtered_df = filtered_df[filtered_df['predicted_class'] == 0]

if customer_search:
    filtered_df = filtered_df[
        filtered_df['CustomerID'].str.contains(customer_search, case=False, na=False)
    ]

filtered_df = filtered_df[
    (filtered_df['predicted_probability'] >= prob_range[0]) &
    (filtered_df['predicted_probability'] <= prob_range[1])
]

# Display filter results count
st.markdown(f"**Showing {len(filtered_df):,} of {len(predictions_df):,} customers**")

st.divider()

# Visualization section
st.markdown('<h3 style="color: #f1f5f9;">📊 Risk Distribution</h3>', unsafe_allow_html=True)

viz_col1, viz_col2 = st.columns([2, 1])

with viz_col1:
    # Probability histogram
    fig_hist = px.histogram(
        filtered_df,
        x='predicted_probability',
        nbins=30,
        color='risk_category',
        color_discrete_map={
            'High Risk': '#ef4444',
            'Medium Risk': '#f59e0b',
            'Low Risk': '#10b981',
            'Very Low Risk': '#06b6d4'
        },
        title='Distribution of Predicted Inactivity Probabilities',
        labels={'predicted_probability': 'Predicted Probability', 'count': 'Number of Customers'}
    )
    
    # Add threshold line
    fig_hist.add_vline(
        x=threshold,
        line_dash="dash",
        line_color="white",
        annotation_text=f"Threshold: {threshold}",
        annotation_position="top",
        annotation=dict(font=dict(color='white', size=12))
    )
    
    fig_hist.update_layout(
        title=dict(
            text='Distribution of Predicted Inactivity Probabilities',
            font=dict(size=16, color='white'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        legend=dict(
            title=dict(text='Risk Category', font=dict(color='white')),
            font=dict(color='white'),
            bgcolor='rgba(0,0,0,0.3)'
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.2)',
            title=dict(text='Predicted Probability', font=dict(color='white', size=14)),
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.2)',
            title=dict(text='Number of Customers', font=dict(color='white', size=14)),
            tickfont=dict(color='white')
        ),
        height=400
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)

with viz_col2:
    # Risk category breakdown
    risk_counts = filtered_df['risk_category'].value_counts()
    
    fig_pie = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        color=risk_counts.index,
        color_discrete_map={
            'High Risk': '#ef4444',
            'Medium Risk': '#f59e0b',
            'Low Risk': '#10b981',
            'Very Low Risk': '#06b6d4'
        },
        title='Customers by Risk Category',
        hole=0.4
    )
    
    fig_pie.update_layout(
        title=dict(
            text='Customers by Risk Category',
            font=dict(size=16, color='white'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(0,0,0,0.3)'
        ),
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# Customer table
st.markdown('<h3 style="color: #f1f5f9;">📋 Customer Prediction Table</h3>', unsafe_allow_html=True)

# Prepare display columns
display_cols = ['CustomerID', 'predicted_probability', 'predicted_class', 'risk_category']

# Add feature columns if available
optional_cols = ['recency_days', 'frequency_count', 'monetary_total', 'active_months']
for col in optional_cols:
    if col in filtered_df.columns:
        display_cols.append(col)

# Add actual outcome if available
if 'actual_outcome' in filtered_df.columns:
    display_cols.append('actual_outcome')

# Create display dataframe
display_df = filtered_df[display_cols].copy()

# Format columns
display_df = display_df.rename(columns={
    'CustomerID': 'Customer ID',
    'predicted_probability': 'Inactivity Prob.',
    'predicted_class': 'Predicted Status',
    'risk_category': 'Risk Category',
    'recency_days': 'Recency (days)',
    'frequency_count': 'Frequency',
    'monetary_total': 'Total Spend',
    'active_months': 'Active Months',
    'actual_outcome': 'Actual Outcome'
})

# Convert predicted status to readable format
if 'Predicted Status' in display_df.columns:
    display_df['Predicted Status'] = display_df['Predicted Status'].map({1: 'Inactive', 0: 'Active'})

if 'Actual Outcome' in display_df.columns:
    display_df['Actual Outcome'] = display_df['Actual Outcome'].map({1: 'Inactive', 0: 'Active'})

# Display table with pagination
st.dataframe(
    display_df.round(4),
    use_container_width=True,
    height=400
)

# Export functionality
st.markdown('<h3 style="color: #f1f5f9;">📤 Export Data</h3>', unsafe_allow_html=True)

export_col1, export_col2 = st.columns([3, 1])

with export_col1:
    st.markdown("""
    Export the filtered customer list for use in retention campaigns or further analysis.
    The export includes customer IDs, predicted probabilities, risk categories, and available features.
    """)

with export_col2:
    # CSV download
    csv_data = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="customer_predictions.csv",
        mime="text/csv"
    )

st.divider()

# Customer detail section
st.markdown('<h3 style="color: #f1f5f9;">👤 Customer Detail View</h3>', unsafe_allow_html=True)

# Customer selector
customer_ids = filtered_df['CustomerID'].tolist()
if customer_ids:
    selected_customer = st.selectbox(
        "Select a customer to view details:",
        options=customer_ids,
        index=0
    )
    
    # Get customer data
    customer_data = filtered_df[filtered_df['CustomerID'] == selected_customer].iloc[0]
    
    detail_col1, detail_col2 = st.columns(2)
    
    with detail_col1:
        st.markdown(f"#### Customer {selected_customer}")
        
        # Risk badge
        risk = customer_data['risk_category']
        risk_color = get_risk_color(risk)
        st.markdown(f"""
        <span style="background-color: {risk_color}20; color: {risk_color}; 
              padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600;">
            {risk}
        </span>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Key metrics
        st.markdown(f"""
        **Predicted Inactivity Probability:** {customer_data['predicted_probability']:.1%}
        
        **Predicted Status:** {'Inactive' if customer_data['predicted_class'] == 1 else 'Active'}
        """)
        
        if 'actual_outcome' in customer_data.index:
            st.markdown(f"""
            **Actual Outcome:** {'Inactive' if customer_data['actual_outcome'] == 1 else 'Active'}
            """)
        
        # Feature summary
        st.markdown("##### Customer Profile")
        if 'recency_days' in customer_data.index:
            st.markdown(f"- **Recency:** {customer_data['recency_days']:.0f} days since last purchase")
        if 'frequency_count' in customer_data.index:
            st.markdown(f"- **Frequency:** {customer_data['frequency_count']:.0f} purchases")
        if 'monetary_total' in customer_data.index:
            st.markdown(f"- **Total Spend:** ${customer_data['monetary_total']:,.2f}")
        if 'active_months' in customer_data.index:
            st.markdown(f"- **Active Months:** {customer_data['active_months']:.0f}")
    
    with detail_col2:
        st.markdown("#### Retention Recommendations")
        
        recommendations = get_retention_recommendations(
            customer_data['predicted_probability'],
            customer_data['risk_category'],
            customer_data.to_dict()
        )
        
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        st.markdown("")
        st.warning("""
        **Disclaimer:** These recommendations are rule-based suggestions derived from 
        customer feature patterns. They do not represent model predictions about why 
        a customer may become inactive. Verify recommendations against current business 
        context before taking action.
        """)
else:
    st.info("No customers match the current filter criteria.")

# Footer disclaimer
st.divider()
st.markdown("""
<div style="color: #718096; font-size: 0.875rem; text-align: center;">
    <strong>Important:</strong> Predictions are based on historical purchasing patterns and are 
    decision-support estimates. They do not guarantee future customer behavior. The model was 
    trained on data from Dec 2010 - Dec 2011 and may not reflect current market conditions.
</div>
""", unsafe_allow_html=True)
