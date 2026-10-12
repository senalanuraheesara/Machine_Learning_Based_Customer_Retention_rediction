"""
Customer Behavior Segmentation Page

Displays K-Means clustering results, cluster profiles, and enables
exploration of customer segments.
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
    load_segmentation_assignments,
    load_cluster_profiles,
    load_cluster_sizes,
    load_cluster_inactivity,
    load_clustering_comparison,
    load_customer_features,
    get_segmentation_metrics
)

# Page configuration
st.set_page_config(
    page_title="Customer Segmentation | Retail Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()
render_sidebar()

# Page header with visual banner
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.1) 50%, rgba(6, 182, 212, 0.15) 100%); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; text-align: center;">
    <div style="font-size: 3rem; margin-bottom: 0.75rem;">👥 🎯 📊</div>
    <h1 style="margin-bottom: 0.5rem; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Customer Behavior Segmentation</h1>
    <p style="font-size: 1.1rem; color: #94a3b8; max-width: 600px; margin: 0 auto;">Explore behavioral customer segments identified through K-Means clustering analysis</p>
    <div style="display: flex; justify-content: center; gap: 0.75rem; margin-top: 1.25rem; flex-wrap: wrap;">
        <span style="background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); padding: 0.4rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; color: #93c5fd;">🔬 K-Means Clustering</span>
        <span style="background: rgba(139, 92, 246, 0.2); border: 1px solid rgba(139, 92, 246, 0.4); padding: 0.4rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; color: #c4b5fd;">🎯 K=2 Clusters</span>
        <span style="background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.4rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; color: #6ee7b7;">📈 0.689 Silhouette</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Load all segmentation data
@st.cache_data
def load_all_segmentation_data():
    segments = load_segmentation_assignments()
    profiles = load_cluster_profiles()
    sizes = load_cluster_sizes()
    inactivity = load_cluster_inactivity()
    comparison = load_clustering_comparison()
    features = load_customer_features()
    
    # Merge segments with features for detailed analysis
    if not segments.empty and not features.empty:
        merged = segments.merge(features, on='CustomerID', how='left', suffixes=('', '_feat'))
        # Handle column conflicts
        if 'inactive_in_outcome_window' in merged.columns and 'inactive_in_outcome_window_feat' in merged.columns:
            merged = merged.drop(columns=['inactive_in_outcome_window_feat'])
    else:
        merged = segments
    
    return {
        'segments': segments,
        'profiles': profiles,
        'sizes': sizes,
        'inactivity': inactivity,
        'comparison': comparison,
        'detailed': merged
    }

data = load_all_segmentation_data()
metrics = get_segmentation_metrics()

# Check if data loaded
if data['segments'].empty:
    st.error("""
    **Data Loading Error**
    
    Unable to load segmentation data. Please ensure these files exist:
    - `outputs/segmentation/customer_segments_kmeans_k2.csv`
    - `outputs/segmentation/cluster_median_profiles_k2.csv`
    - `outputs/segmentation/cluster_sizes_k2.csv`
    
    Run the segmentation notebook to generate the required files.
    """)
    st.stop()

# Segmentation overview expander
with st.expander("Segmentation Methodology", expanded=False):
    st.markdown("""
    **Algorithm:** K-Means Clustering
    
    **Features Used:** Customer behavioral metrics including recency, frequency, monetary value, 
    product diversity, purchase intervals, and return rates.
    
    **Cluster Selection:** K=2 was selected based on silhouette score analysis across K=2 to K=6.
    
    **Important Note:** The segmentation identifies purchasing-behavior differences between groups. 
    However, the observed association between cluster membership and customer inactivity was 
    **not statistically significant** (Chi-square p-value = 0.5141). Clusters should not be 
    automatically labeled as "high-risk" or "low-risk" based solely on segment membership.
    """)

st.divider()

# KPI Cards
st.markdown('<h3 style="color: #f1f5f9;">📊 Segmentation Overview</h3>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Customers Segmented",
        value=f"{len(data['segments']):,}"
    )

with col2:
    st.metric(
        label="Number of Clusters",
        value=f"{metrics.get('k', 2)}"
    )

with col3:
    st.metric(
        label="Silhouette Score",
        value=f"{metrics.get('silhouette', 0.6895):.4f}",
        help="Measure of cluster quality (higher is better, range -1 to 1)"
    )

with col4:
    st.metric(
        label="Davies-Bouldin Score",
        value=f"{metrics.get('davies_bouldin', 0.9234):.4f}",
        help="Measure of cluster separation (lower is better)"
    )

st.divider()

# Cluster Distribution
st.markdown('<h3 style="color: #f1f5f9;">📈 Cluster Distribution</h3>', unsafe_allow_html=True)

dist_col1, dist_col2 = st.columns([2, 1])

with dist_col1:
    if not data['sizes'].empty:
        fig_bar = px.bar(
            data['sizes'],
            x='Cluster',
            y='CustomerCount',
            color='Cluster',
            text='CustomerPercentage',
            color_discrete_sequence=['#3b82f6', '#10b981'],
            title='Customer Count by Cluster',
            labels={'CustomerCount': 'Number of Customers', 'CustomerPercentage': 'Percentage'}
        )
        
        fig_bar.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside',
            textfont=dict(color='#f1f5f9', size=14)
        )
        
        fig_bar.update_layout(
            title=dict(
                text='Customer Count by Cluster',
                font=dict(size=18, color='#f1f5f9'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f1f5f9', size=13),
            showlegend=False,
            xaxis=dict(
                tickmode='linear',
                tickvals=[0, 1],
                ticktext=['Cluster 0', 'Cluster 1'],
                tickfont=dict(color='#f1f5f9', size=12),
                title=dict(text='Cluster', font=dict(color='#f1f5f9', size=14))
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.15)',
                tickfont=dict(color='#f1f5f9', size=12),
                title=dict(text='Number of Customers', font=dict(color='#f1f5f9', size=14))
            ),
            height=380,
            margin=dict(t=60, b=60)
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Cluster size data not available")

with dist_col2:
    if not data['sizes'].empty:
        st.markdown("#### 📊 Cluster Summary")
        for _, row in data['sizes'].iterrows():
            cluster = int(row['Cluster'])
            count = int(row['CustomerCount'])
            pct = row['CustomerPercentage']
            
            if cluster == 0:
                color = '#3b82f6'
                icon = '👥'
                label = 'Main Group'
            else:
                color = '#10b981'
                icon = '⭐'
                label = 'High-Value'
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {color}25 0%, {color}10 100%);
                border: 1px solid {color}50;
                padding: 1.25rem;
                border-radius: 16px;
                margin-bottom: 0.75rem;
                text-align: center;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-weight: 700; color: {color}; font-size: 1.1rem; margin-bottom: 0.25rem;">Cluster {cluster}</div>
                <div style="font-size: 0.75rem; opacity: 0.7; margin-bottom: 0.5rem;">{label}</div>
                <div style="font-size: 1.75rem; font-weight: 800; color: #f1f5f9;">{count:,}</div>
                <div style="font-size: 0.85rem; opacity: 0.8;">{pct:.1f}% of customers</div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# Cluster Profiles Comparison
st.markdown('<h3 style="color: #f1f5f9;">👥 Cluster Behavioral Profiles</h3>', unsafe_allow_html=True)

if not data['profiles'].empty:
    # Transpose profiles for better visualization
    profiles_df = data['profiles'].set_index(data['profiles'].columns[0]).T
    profiles_df.columns = [f'Cluster {i}' for i in profiles_df.columns]
    profiles_df.index.name = 'Feature'
    
    # Display profile table at full width first
    st.markdown("#### Median Feature Values by Cluster")
    st.dataframe(
        profiles_df.round(2),
        use_container_width=True,
        height=150
    )
    
    # Key observations in two columns below the table
    obs_col1, obs_col2 = st.columns(2)
    
    with obs_col1:
        st.markdown("""
        **Cluster 0 (Main Customer Group):**
        - Lower median purchase frequency
        - Lower median total spending
        - Higher median purchase intervals
        - Represents the majority of customers
        """)
    
    with obs_col2:
        st.markdown("""
        **Cluster 1 (Higher-Value Group):**
        - Higher median purchase frequency
        - Significantly higher median total spending
        - More product diversity
        - Lower median recency (more recent activity)
        - Smaller segment of customers
        """)
    
    st.info("""
    **Note:** These are behavioral profile differences, not predictive risk labels. 
    Both clusters showed similar observed inactivity rates.
    """)

st.divider()

# Detailed Feature Comparison Charts
st.markdown('<h3 style="color: #f1f5f9;">🔬 Feature Comparison by Cluster</h3>', unsafe_allow_html=True)

if not data['detailed'].empty:
    # Select features to compare
    numeric_features = [
        'frequency_count', 'monetary_total', 'monetary_avg', 'product_diversity',
        'recency_days', 'tenure_days', 'active_months', 'purchase_interval_avg',
        'avg_quantity_per_invoice', 'return_rate'
    ]
    
    available_features = [f for f in numeric_features if f in data['detailed'].columns]
    
    compare_col1, compare_col2 = st.columns(2)
    
    with compare_col1:
        feature_x = st.selectbox(
            "Select Feature for Comparison",
            options=available_features,
            index=available_features.index('monetary_total') if 'monetary_total' in available_features else 0
        )
    
    with compare_col2:
        chart_type = st.selectbox(
            "Chart Type",
            options=['Box Plot', 'Violin Plot', 'Histogram'],
            index=0
        )
    
    # Create comparison chart
    if chart_type == 'Box Plot':
        fig_compare = px.box(
            data['detailed'],
            x='Cluster',
            y=feature_x,
            color='Cluster',
            color_discrete_sequence=['#3b82f6', '#10b981'],
            title=f'{feature_x.replace("_", " ").title()} by Cluster'
        )
    elif chart_type == 'Violin Plot':
        fig_compare = px.violin(
            data['detailed'],
            x='Cluster',
            y=feature_x,
            color='Cluster',
            color_discrete_sequence=['#3b82f6', '#10b981'],
            title=f'{feature_x.replace("_", " ").title()} by Cluster',
            box=True
        )
    else:
        fig_compare = px.histogram(
            data['detailed'],
            x=feature_x,
            color='Cluster',
            color_discrete_sequence=['#3b82f6', '#10b981'],
            title=f'{feature_x.replace("_", " ").title()} Distribution by Cluster',
            barmode='overlay',
            opacity=0.7
        )
    
    fig_compare.update_layout(
        title=dict(
            text=f'{feature_x.replace("_", " ").title()} by Cluster',
            font=dict(size=18, color='#f1f5f9'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f1f5f9', size=13),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.15)',
            tickfont=dict(color='#f1f5f9', size=12),
            title=dict(text='Cluster', font=dict(color='#f1f5f9', size=14)),
            tickvals=[0, 1],
            ticktext=['Cluster 0', 'Cluster 1']
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.15)',
            tickfont=dict(color='#f1f5f9', size=12),
            title=dict(text=feature_x.replace("_", " ").title(), font=dict(color='#f1f5f9', size=14))
        ),
        legend=dict(
            title=dict(text='Cluster', font=dict(color='#f1f5f9', size=13)),
            font=dict(color='#f1f5f9', size=12),
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        height=420,
        margin=dict(t=60, b=60, l=60, r=40)
    )
    
    st.plotly_chart(fig_compare, use_container_width=True)

st.divider()

# Observed Inactivity by Cluster
st.markdown('<h3 style="color: #f1f5f9;">⚡ Observed Inactivity by Cluster</h3>', unsafe_allow_html=True)

if not data['inactivity'].empty:
    inact_col1, inact_col2 = st.columns([2, 1])
    
    with inact_col1:
        fig_inact = px.bar(
            data['inactivity'],
            x='Cluster',
            y='InactivityRatePct',
            color='Cluster',
            color_discrete_sequence=['#3b82f6', '#10b981'],
            title='Observed Inactivity Rate by Cluster',
            labels={'InactivityRatePct': 'Inactivity Rate (%)'}
        )
        
        fig_inact.update_traces(
            texttemplate='%{y:.1f}%',
            textposition='outside',
            textfont=dict(color='#f1f5f9', size=14)
        )
        
        fig_inact.update_layout(
            title=dict(
                text='Observed Inactivity Rate by Cluster',
                font=dict(size=18, color='#f1f5f9'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f1f5f9', size=13),
            showlegend=False,
            xaxis=dict(
                tickmode='linear',
                tickvals=[0, 1],
                ticktext=['Cluster 0', 'Cluster 1'],
                tickfont=dict(color='#f1f5f9', size=12),
                title=dict(text='Cluster', font=dict(color='#f1f5f9', size=14))
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.15)',
                range=[0, 40],
                tickfont=dict(color='#f1f5f9', size=12),
                title=dict(text='Inactivity Rate (%)', font=dict(color='#f1f5f9', size=14))
            ),
            height=380,
            margin=dict(t=60, b=60)
        )
        
        st.plotly_chart(fig_inact, use_container_width=True)
    
    with inact_col2:
        st.markdown("#### Inactivity Summary")
        
        for _, row in data['inactivity'].iterrows():
            cluster = int(row['Cluster'])
            total = int(row['CustomerCount'])
            inactive = int(row['InactiveCount'])
            rate = row['InactivityRatePct']
            
            color = '#3b82f6' if cluster == 0 else '#10b981'
            st.markdown(f"""
            <div style="background-color: {color}15; border-left: 4px solid {color}; 
                        padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="font-weight: 600; color: {color};">Cluster {cluster}</div>
                <div style="color: #1a365d;">
                    <span style="font-size: 1.25rem; font-weight: 700;">{rate:.1f}%</span> inactive
                </div>
                <div style="color: #718096; font-size: 0.875rem;">
                    {inactive:,} of {total:,} customers
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.warning("""
        **Statistical Note:** The difference in inactivity rates between clusters 
        (30.18% vs 26.89%) was **not statistically significant** (Chi-square p-value = 0.5141). 
        This means cluster membership alone should not be used to predict inactivity risk.
        """)

st.divider()

# Cluster Explorer
st.markdown('<h3 style="color: #f1f5f9;">🔎 Cluster Explorer</h3>', unsafe_allow_html=True)

explore_col1, explore_col2 = st.columns([1, 3])

with explore_col1:
    selected_cluster = st.selectbox(
        "Select Cluster",
        options=[0, 1],
        format_func=lambda x: f"Cluster {x}"
    )
    
    customer_search = st.text_input(
        "Search Customer ID",
        placeholder="Enter ID..."
    )
    
    sort_by = st.selectbox(
        "Sort By",
        options=['monetary_total', 'frequency_count', 'recency_days', 'CustomerID'],
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    sort_order = st.radio(
        "Sort Order",
        options=['Descending', 'Ascending']
    )

# Filter data
filtered_cluster = data['detailed'][data['detailed']['Cluster'] == selected_cluster].copy()

if customer_search:
    filtered_cluster = filtered_cluster[
        filtered_cluster['CustomerID'].str.contains(customer_search, case=False, na=False)
    ]

# Sort
ascending = sort_order == 'Ascending'
if sort_by in filtered_cluster.columns:
    filtered_cluster = filtered_cluster.sort_values(sort_by, ascending=ascending)

with explore_col2:
    st.markdown(f"#### Cluster {selected_cluster} Customers ({len(filtered_cluster):,} total)")
    
    # Select display columns
    display_cols = ['CustomerID', 'Cluster']
    optional_cols = [
        'frequency_count', 'monetary_total', 'monetary_avg', 'recency_days',
        'tenure_days', 'product_diversity', 'active_months', 'inactive_in_outcome_window'
    ]
    
    for col in optional_cols:
        if col in filtered_cluster.columns:
            display_cols.append(col)
    
    display_df = filtered_cluster[display_cols].copy()
    display_df = display_df.rename(columns={
        'CustomerID': 'Customer ID',
        'frequency_count': 'Frequency',
        'monetary_total': 'Total Spend',
        'monetary_avg': 'Avg Spend',
        'recency_days': 'Recency (days)',
        'tenure_days': 'Tenure (days)',
        'product_diversity': 'Products',
        'active_months': 'Active Months',
        'inactive_in_outcome_window': 'Became Inactive'
    })
    
    if 'Became Inactive' in display_df.columns:
        display_df['Became Inactive'] = display_df['Became Inactive'].map({1: 'Yes', 0: 'No'})
    
    st.dataframe(
        display_df.round(2),
        use_container_width=True,
        height=400
    )
    
    # Export
    csv_data = filtered_cluster.to_csv(index=False)
    st.download_button(
        label=f"Export Cluster {selected_cluster} Customers",
        data=csv_data,
        file_name=f"cluster_{selected_cluster}_customers.csv",
        mime="text/csv"
    )

st.divider()

# Business Recommendations
st.markdown('<h3 style="color: #f1f5f9;">💡 Segment-Based Business Recommendations</h3>', unsafe_allow_html=True)

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.markdown("""
    #### Cluster 0: Main Customer Group
    
    **Profile:** Represents ~93% of customers with moderate purchasing patterns
    
    **Suggested Actions:**
    - Focus on engagement and activation campaigns
    - Implement loyalty program incentives
    - Send regular product recommendations
    - Monitor for early warning signs of disengagement
    
    **Considerations:**
    - Large group requires scalable retention approaches
    - Segment further by other criteria for targeted campaigns
    """)

with rec_col2:
    st.markdown("""
    #### Cluster 1: Higher-Value Group
    
    **Profile:** Represents ~7% of customers with higher spending and engagement
    
    **Suggested Actions:**
    - Prioritize personalized service and communication
    - Offer exclusive benefits or early access
    - Gather feedback for product development
    - Consider referral program opportunities
    
    **Considerations:**
    - High-value customers warrant individual attention
    - Despite higher engagement, still monitor retention signals
    """)

st.info("""
**Important:** These recommendations are based on behavioral differences between segments, 
not on differential churn risk. Both segments showed similar observed inactivity rates. 
Combine segmentation insights with the retention prediction model for more targeted interventions.
""")

# Footer
st.divider()
st.markdown("""
<div style="color: #718096; font-size: 0.875rem; text-align: center;">
    Segmentation based on K-Means clustering with K=2. 
    Cluster profiles reflect median feature values. 
    Results are descriptive of historical patterns.
</div>
""", unsafe_allow_html=True)
