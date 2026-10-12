"""
Business Insights & Model Performance Page

Displays model comparison, performance metrics, and business recommendations
with appropriate limitations and disclaimers.
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
    load_model_comparison,
    load_model_selection,
    load_accuracy_summary,
    load_cross_validation_results,
    load_validation_thresholds,
    get_selected_model_info,
    get_segmentation_metrics
)

# Page configuration
st.set_page_config(
    page_title="Business Insights | Retail Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()
render_sidebar()

# Page header with visual banner
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.1) 50%, rgba(59, 130, 246, 0.15) 100%); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; text-align: center;">
    <div style="font-size: 3rem; margin-bottom: 0.75rem;">📊 📈 💡</div>
    <h1 style="margin-bottom: 0.5rem; background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Business Insights & Model Performance</h1>
    <p style="font-size: 1.1rem; color: #94a3b8; max-width: 600px; margin: 0 auto;">Machine learning performance analysis, model comparison, and practical business recommendations</p>
</div>
""", unsafe_allow_html=True)

# Executive Overview Section
st.markdown('<h3 style="color: #f1f5f9;">📋 Executive Overview</h3>', unsafe_allow_html=True)

overview_col1, overview_col2 = st.columns([2, 1])

with overview_col1:
    st.markdown("""
    #### Business Problem
    
    **Challenge:** Online retail businesses face customer attrition where previously active 
    customers stop making purchases. Identifying at-risk customers early enables proactive 
    retention interventions.
    
    #### Project Approach
    
    This project addresses customer retention through two complementary analytical tasks:
    
    1. **Customer Retention Prediction (Classification)**
       - Predict which customers are likely to become inactive
       - Four machine learning models optimized and compared
       - Random Forest selected as best-performing model
    
    2. **Customer Behavior Segmentation (Clustering)**
       - Identify distinct customer behavioral groups
       - K-Means clustering with K=2 based on silhouette analysis
       - Behavioral profiles for targeted strategies
    
    #### Key Findings
    
    - **Prediction Model:** Achieves ~67-69% accuracy in identifying potential customer inactivity
    - **Segmentation:** Two behavioral segments identified with distinct purchasing patterns
    - **Integration:** Predictions and segments can inform targeted retention strategies
    """)

with overview_col2:
    model_info = get_selected_model_info()
    seg_metrics = get_segmentation_metrics()
    
    val_acc = model_info.get('validation_accuracy', 0.6863)
    threshold = model_info.get('threshold', 0.425)
    k_val = seg_metrics.get('k', 2)
    silhouette = seg_metrics.get('silhouette', 0.6895)
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
    ">
        <div style="text-align: center; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem;">🏆</span>
            <h4 style="margin: 0.5rem 0 0 0;">Quick Stats</h4>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <span style="opacity: 0.7;">🤖 Model</span>
            <span style="font-weight: 600; color: #a78bfa;">Random Forest</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <span style="opacity: 0.7;">📊 Accuracy</span>
            <span style="font-weight: 600; color: #34d399;">{val_acc:.1%}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <span style="opacity: 0.7;">⚙️ Threshold</span>
            <span style="font-weight: 600; color: #60a5fa;">{threshold}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <span style="opacity: 0.7;">👥 Segments</span>
            <span style="font-weight: 600; color: #fbbf24;">K={k_val}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
            <span style="opacity: 0.7;">🎯 Silhouette</span>
            <span style="font-weight: 600; color: #f87171;">{silhouette:.4f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Model Comparison Section
st.markdown('<h3 style="color: #f1f5f9;">🤖 Classification Model Comparison</h3>', unsafe_allow_html=True)

# Load model comparison data
model_comparison = load_model_comparison()
accuracy_summary = load_accuracy_summary()
model_selection = load_model_selection()

if not model_comparison.empty:
    # Prepare data for display
    display_columns = ['Model', 'Threshold', 'Training accuracy', 'Validation accuracy', 
                       'Test accuracy', 'CV accuracy', 'Selected']
    
    available_columns = [c for c in display_columns if c in model_comparison.columns]
    display_df = model_comparison[available_columns].copy()
    
    # Format percentages
    pct_columns = ['Training accuracy', 'Validation accuracy', 'Test accuracy', 'CV accuracy']
    for col in pct_columns:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2%}" if pd.notnull(x) else "")
    
    # Format model names
    display_df['Model'] = display_df['Model'].apply(lambda x: x.replace('_', ' ').title())
    
    st.markdown("#### Model Performance Summary")
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Selection note
    if model_selection:
        st.info(f"""
        **Selection Rule:** {model_selection.get('rule', 'Highest validation accuracy among fitting-eligible variants')}
        
        **Selected Model:** Random Forest with threshold 0.425
        """)
else:
    st.warning("Model comparison data not available. Please run the model comparison notebook.")

st.divider()

# Model Accuracy Visualization
st.markdown('<h3 style="color: #f1f5f9;">📊 Model Accuracy Comparison</h3>', unsafe_allow_html=True)

if not model_comparison.empty:
    # Prepare data for visualization
    viz_data = []
    for _, row in model_comparison.iterrows():
        model_name = row['Model'].replace('_', ' ').title()
        
        if 'Training accuracy' in row:
            viz_data.append({'Model': model_name, 'Metric': 'Training', 'Accuracy': row['Training accuracy']})
        if 'Validation accuracy' in row:
            viz_data.append({'Model': model_name, 'Metric': 'Validation', 'Accuracy': row['Validation accuracy']})
        if 'Test accuracy' in row:
            viz_data.append({'Model': model_name, 'Metric': 'Test', 'Accuracy': row['Test accuracy']})
    
    viz_df = pd.DataFrame(viz_data)
    
    if not viz_df.empty:
        fig_comparison = px.bar(
            viz_df,
            x='Model',
            y='Accuracy',
            color='Metric',
            barmode='group',
            color_discrete_map={
                'Training': '#3b82f6',
                'Validation': '#10b981',
                'Test': '#f59e0b'
            }
        )
        
        fig_comparison.update_layout(
            title=dict(
                text='Model Accuracy Across Train, Validation, and Test Sets',
                font=dict(size=18, color='white'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.2)',
                title=dict(text='Model', font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12)
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.2)',
                tickformat='.0%',
                range=[0.5, 0.8],
                title=dict(text='Accuracy', font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12)
            ),
            legend=dict(
                title=dict(text='Dataset', font=dict(color='white', size=14)),
                font=dict(color='white', size=12),
                bgcolor='rgba(0,0,0,0.3)'
            ),
            height=450
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)

st.divider()

# Cross-Validation Results
st.markdown('<h3 style="color: #f1f5f9;">🔄 Cross-Validation Analysis</h3>', unsafe_allow_html=True)

cv_tab1, cv_tab2, cv_tab3, cv_tab4 = st.tabs([
    "Random Forest", "Logistic Regression", "Gradient Boosting", "Decision Tree"
])

model_names = ['random_forest', 'logistic_regression', 'gradient_boosting', 'decision_tree']
tabs = [cv_tab1, cv_tab2, cv_tab3, cv_tab4]

for tab, model_name in zip(tabs, model_names):
    with tab:
        cv_folds, provenance = load_cross_validation_results(model_name)
        
        if not cv_folds.empty:
            display_name = model_name.replace('_', ' ').title()
            
            st.markdown(f"#### {display_name} Cross-Validation Results")
            
            # Summary statistics
            if 'cv_accuracy' in cv_folds.columns:
                mean_cv = cv_folds.groupby('threshold')['cv_accuracy'].mean()
                
                # Format CV accuracy values safely
                cv_425 = mean_cv.get(0.425)
                cv_500 = mean_cv.get(0.5)
                cv_425_str = f"{cv_425:.4f}" if cv_425 is not None else "N/A"
                cv_500_str = f"{cv_500:.4f}" if cv_500 is not None else "N/A"
                
                summary_col1, summary_col2 = st.columns(2)
                
                with summary_col1:
                    st.markdown(f"""
                    **Mean CV Accuracy (threshold=0.425):** {cv_425_str}
                    
                    **Mean CV Accuracy (threshold=0.5):** {cv_500_str}
                    
                    **Number of Folds:** {cv_folds['fold'].nunique()}
                    """)
                
                with summary_col2:
                    if provenance:
                        st.markdown(f"""
                        **Status:** {provenance.get('status', 'N/A')}
                        
                        **Limitation:** {provenance.get('limitation', 'N/A')}
                        """)
            
            # Fold-by-fold results
            st.markdown("##### Fold Results")
            st.dataframe(cv_folds.round(4), use_container_width=True, hide_index=True)
        else:
            st.info(f"Cross-validation results for {model_name.replace('_', ' ').title()} not available.")

st.divider()

# Threshold Analysis
st.markdown('<h3 style="color: #f1f5f9;">⚙️ Threshold Analysis</h3>', unsafe_allow_html=True)

st.markdown("""
The classification threshold determines how predicted probabilities are converted to 
binary predictions. A lower threshold increases recall (catches more at-risk customers) 
but may also increase false positives.
""")

# Load threshold data for Random Forest
threshold_data = load_validation_thresholds('random_forest')

if not threshold_data.empty:
    thresh_col1, thresh_col2 = st.columns([2, 1])
    
    with thresh_col1:
        # Accuracy vs Threshold plot
        fig_thresh = go.Figure()
        
        fig_thresh.add_trace(go.Scatter(
            x=threshold_data['Threshold'],
            y=threshold_data['Accuracy'],
            mode='lines+markers',
            name='Accuracy',
            line=dict(color='#3b82f6', width=2)
        ))
        
        # Add selected threshold marker
        selected_thresh = model_info.get('threshold', 0.425)
        selected_row = threshold_data[threshold_data['Threshold'] == selected_thresh]
        if not selected_row.empty:
            fig_thresh.add_trace(go.Scatter(
                x=[selected_thresh],
                y=[selected_row['Accuracy'].values[0]],
                mode='markers',
                name='Selected Threshold',
                marker=dict(color='#ef4444', size=12, symbol='star')
            ))
        
        fig_thresh.update_layout(
            title=dict(
                text='Validation Accuracy vs Classification Threshold',
                font=dict(size=18, color='white'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.2)',
                title=dict(text='Threshold', font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12)
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.2)',
                title=dict(text='Accuracy', font=dict(color='white', size=14)),
                tickfont=dict(color='white', size=12)
            ),
            legend=dict(
                font=dict(color='white', size=12),
                bgcolor='rgba(0,0,0,0.3)'
            ),
            height=400
        )
        
        st.plotly_chart(fig_thresh, use_container_width=True)
    
    with thresh_col2:
        st.markdown("#### Threshold Selection")
        st.markdown(f"""
        **Selected Threshold:** {selected_thresh}
        
        The threshold was selected to maximize validation accuracy 
        while maintaining balanced precision and recall.
        
        **Trade-offs:**
        - Lower threshold → More customers flagged as at-risk
        - Higher threshold → Fewer false positives
        
        The optimal threshold depends on business costs 
        of false positives vs false negatives.
        """)
else:
    st.info("Threshold analysis data not available.")

st.divider()

# Business Recommendations
st.markdown('<h3 style="color: #f1f5f9;">💡 Business Recommendations</h3>', unsafe_allow_html=True)

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.markdown("""
    #### Retention Strategy Recommendations
    
    **1. Prioritize High-Risk Customers**
    - Use model predictions to identify customers with highest inactivity probability
    - Focus resources on customers who historically provided value
    - Implement tiered intervention strategies based on risk level
    
    **2. Early Warning Monitoring**
    - Track customer recency and frequency metrics
    - Set alerts for customers showing declining engagement
    - Act before customers become fully disengaged
    
    **3. Segment-Specific Approaches**
    - Cluster 0 (Main Group): Scalable engagement programs
    - Cluster 1 (Higher-Value): Personalized retention efforts
    - Combine prediction scores with segment profiles
    
    **4. Test and Learn**
    - A/B test retention interventions
    - Measure actual retention impact vs predictions
    - Continuously refine model and strategies
    """)

with rec_col2:
    st.markdown("""
    #### Implementation Considerations
    
    **Data Requirements:**
    - Regular transaction data updates
    - Customer contact information
    - Previous campaign response history
    
    **Resource Planning:**
    - Define capacity for personalized outreach
    - Establish automated vs manual intervention thresholds
    - Train customer service on retention protocols
    
    **Success Metrics:**
    - Customer reactivation rate
    - Retention campaign ROI
    - Customer lifetime value impact
    - Model prediction accuracy over time
    
    **Ongoing Maintenance:**
    - Periodic model retraining with new data
    - Threshold recalibration
    - Feature engineering refinements
    """)

st.divider()

# Limitations and Responsible ML
st.markdown('<h3 style="color: #f1f5f9;">⚠️ Limitations & Responsible ML Practices</h3>', unsafe_allow_html=True)

st.warning("""
**Important Disclaimers for Model Use**

Please consider these limitations when interpreting and applying the model predictions:
""")

limit_col1, limit_col2 = st.columns(2)

with limit_col1:
    st.markdown("""
    #### Data & Methodology Limitations
    
    1. **Historical Data Dependency**
       - Model trained on Dec 2010 - Dec 2011 data
       - Past patterns may not reflect current market conditions
       - Customer behavior evolves over time
    
    2. **Reused Holdout Data**
       - Validation and test sets were inspected during development
       - Reported metrics are not from fully independent evaluation
       - Performance on truly new data may differ
    
    3. **Missing Customer Information**
       - Some transactions lack Customer IDs
       - Incomplete purchase histories affect feature accuracy
       - Anonymous customers cannot be predicted
    
    4. **Definition Constraints**
       - "Inactivity" defined as no purchase in 2-month window
       - Different definitions may yield different results
       - Seasonal effects may impact predictions
    """)

with limit_col2:
    st.markdown("""
    #### Interpretation Cautions
    
    5. **Predictions Are Probabilities**
       - Model outputs are risk estimates, not certainties
       - High probability does not guarantee inactivity
       - Use predictions for prioritization, not absolute decisions
    
    6. **Correlation vs Causation**
       - Features correlate with inactivity; they don't cause it
       - Cannot explain "why" a customer will become inactive
       - Avoid interpreting feature importance as causal
    
    7. **Segmentation Independence**
       - Cluster membership not significantly associated with inactivity
       - Do not treat segments as inherent risk groups
       - Use segmentation for behavioral targeting, not risk prediction
    
    8. **Model Degradation**
       - Prediction quality may decrease over time
       - Regular monitoring and retraining required
       - Validate predictions against actual outcomes
    """)

st.divider()

# Technical Details
with st.expander("Technical Details", expanded=False):
    st.markdown("""
    #### Model Configuration
    
    **Random Forest (Selected Model):**
    - Ensemble of decision trees
    - Handles non-linear relationships
    - Robust to overfitting with proper regularization
    
    **Classification Threshold:** 0.425
    - Selected based on validation accuracy optimization
    - Lower than 0.5 to balance precision and recall
    
    **Feature Set:**
    - RFM features (Recency, Frequency, Monetary)
    - Purchase behavior metrics (intervals, diversity)
    - Temporal features (tenure, active months)
    - Recent activity windows (30/60/90 day features)
    
    #### Evaluation Methodology
    
    - **Temporal Split:** Train (Mar-Apr 2011), Validation (Jun 2011), Test (Aug 2011)
    - **Cross-Validation:** 3-fold stratified group CV on training data
    - **Customer Grouping:** Same customer never appears in both train and test folds
    
    #### Software Versions
    
    - Python 3.14+
    - scikit-learn 1.9.1
    - pandas 3.0+
    - numpy 2.5+
    """)

# Footer
st.divider()
st.markdown("""
<div style="color: #718096; font-size: 0.875rem; text-align: center;">
    <strong>IT3091 - Machine Learning</strong> | Sri Lanka Institute of Information Technology (SLIIT)<br>
    Group: 2026-DS-60 | Dashboard for Customer Retention Analysis
</div>
""", unsafe_allow_html=True)
