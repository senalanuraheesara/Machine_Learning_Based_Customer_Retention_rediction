"""
Chart components for the dashboard.
Provides consistent Plotly chart styling and common visualizations.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

# Common color palette
COLORS = {
    'primary': '#1a365d',
    'secondary': '#2d3748',
    'accent': '#0d9488',
    'accent_light': '#14b8a6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'gray': '#718096',
    'light_gray': '#e2e8f0',
    'white': '#ffffff'
}

RISK_COLORS = {
    'High Risk': '#ef4444',
    'Medium Risk': '#f59e0b',
    'Low Risk': '#10b981',
    'Very Low Risk': '#06b6d4'
}

CLUSTER_COLORS = {
    0: '#3b82f6',
    1: '#10b981',
    2: '#f59e0b',
    3: '#ef4444'
}


def apply_common_layout(fig, title: str = "", height: int = 400):
    """Apply common layout settings to a Plotly figure with dark theme support."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color='white'),
            x=0.5,
            xanchor='center'
        ) if title else None,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.2)',
            tickfont=dict(color='white'),
            title_font=dict(color='white')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.2)',
            tickfont=dict(color='white'),
            title_font=dict(color='white')
        ),
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(0,0,0,0.3)'
        ),
        height=height,
        margin=dict(l=20, r=20, t=50 if title else 20, b=20)
    )
    return fig


def create_probability_histogram(
    df: pd.DataFrame,
    prob_column: str = 'predicted_probability',
    risk_column: str = 'risk_category',
    threshold: float = 0.5,
    title: str = 'Probability Distribution'
) -> go.Figure:
    """
    Create a histogram of predicted probabilities colored by risk category.
    """
    fig = px.histogram(
        df,
        x=prob_column,
        color=risk_column,
        nbins=30,
        color_discrete_map=RISK_COLORS,
        labels={prob_column: 'Predicted Probability'}
    )
    
    # Add threshold line
    fig.add_vline(
        x=threshold,
        line_dash="dash",
        line_color=COLORS['primary'],
        annotation_text=f"Threshold: {threshold}",
        annotation_position="top"
    )
    
    apply_common_layout(fig, title)
    fig.update_layout(
        legend_title_text='Risk Category',
        barmode='overlay'
    )
    fig.update_traces(opacity=0.8)
    
    return fig


def create_risk_donut(
    risk_counts: pd.Series,
    title: str = 'Risk Distribution'
) -> go.Figure:
    """
    Create a donut chart showing risk category distribution.
    """
    colors = [RISK_COLORS.get(cat, COLORS['gray']) for cat in risk_counts.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        hole=0.4,
        marker_colors=colors
    )])
    
    apply_common_layout(fig, title)
    fig.update_layout(showlegend=True)
    
    return fig


def create_cluster_bar(
    sizes_df: pd.DataFrame,
    title: str = 'Cluster Distribution'
) -> go.Figure:
    """
    Create a bar chart showing cluster sizes.
    """
    colors = [CLUSTER_COLORS.get(c, COLORS['gray']) for c in sizes_df['Cluster']]
    
    fig = go.Figure(data=[go.Bar(
        x=sizes_df['Cluster'].astype(str),
        y=sizes_df['CustomerCount'],
        marker_color=colors,
        text=sizes_df['CustomerPercentage'].apply(lambda x: f"{x:.1f}%"),
        textposition='outside'
    )])
    
    apply_common_layout(fig, title, height=350)
    fig.update_layout(
        xaxis_title='Cluster',
        yaxis_title='Number of Customers'
    )
    
    return fig


def create_model_comparison_bar(
    comparison_df: pd.DataFrame,
    metrics: List[str] = ['Training accuracy', 'Validation accuracy', 'Test accuracy'],
    title: str = 'Model Accuracy Comparison'
) -> go.Figure:
    """
    Create a grouped bar chart comparing model performance.
    """
    metric_colors = {
        'Training accuracy': COLORS['info'],
        'Validation accuracy': COLORS['success'],
        'Test accuracy': COLORS['warning'],
        'CV accuracy': COLORS['accent']
    }
    
    fig = go.Figure()
    
    for metric in metrics:
        if metric in comparison_df.columns:
            fig.add_trace(go.Bar(
                name=metric.replace(' accuracy', ''),
                x=comparison_df['Model'].apply(lambda x: x.replace('_', ' ').title()),
                y=comparison_df[metric],
                marker_color=metric_colors.get(metric, COLORS['gray'])
            ))
    
    apply_common_layout(fig, title, height=450)
    fig.update_layout(
        barmode='group',
        xaxis_title='Model',
        yaxis_title='Accuracy',
        yaxis=dict(tickformat='.0%', range=[0.5, 0.8], gridcolor=COLORS['light_gray']),
        legend_title_text='Dataset'
    )
    
    return fig


def create_threshold_curve(
    threshold_df: pd.DataFrame,
    selected_threshold: float = 0.5,
    title: str = 'Accuracy vs Threshold'
) -> go.Figure:
    """
    Create a line chart showing accuracy across different thresholds.
    """
    fig = go.Figure()
    
    # Accuracy line
    fig.add_trace(go.Scatter(
        x=threshold_df['Threshold'],
        y=threshold_df['Accuracy'],
        mode='lines+markers',
        name='Accuracy',
        line=dict(color=COLORS['info'], width=2)
    ))
    
    # Selected threshold marker
    selected_row = threshold_df[threshold_df['Threshold'] == selected_threshold]
    if not selected_row.empty:
        fig.add_trace(go.Scatter(
            x=[selected_threshold],
            y=[selected_row['Accuracy'].values[0]],
            mode='markers',
            name='Selected',
            marker=dict(color=COLORS['danger'], size=12, symbol='star')
        ))
    
    apply_common_layout(fig, title)
    fig.update_layout(
        xaxis_title='Threshold',
        yaxis_title='Accuracy'
    )
    
    return fig


def create_feature_comparison_box(
    df: pd.DataFrame,
    feature: str,
    cluster_column: str = 'Cluster',
    title: str = None
) -> go.Figure:
    """
    Create a box plot comparing a feature across clusters.
    """
    if title is None:
        title = f'{feature.replace("_", " ").title()} by Cluster'
    
    colors = [CLUSTER_COLORS.get(c, COLORS['gray']) for c in sorted(df[cluster_column].unique())]
    
    fig = px.box(
        df,
        x=cluster_column,
        y=feature,
        color=cluster_column,
        color_discrete_sequence=colors
    )
    
    apply_common_layout(fig, title)
    fig.update_layout(showlegend=False)
    
    return fig


def create_inactivity_comparison_bar(
    inactivity_df: pd.DataFrame,
    title: str = 'Inactivity Rate by Cluster'
) -> go.Figure:
    """
    Create a bar chart comparing inactivity rates across clusters.
    """
    colors = [CLUSTER_COLORS.get(c, COLORS['gray']) for c in inactivity_df['Cluster']]
    
    fig = go.Figure(data=[go.Bar(
        x=inactivity_df['Cluster'].astype(str),
        y=inactivity_df['InactivityRatePct'],
        marker_color=colors,
        text=inactivity_df['InactivityRatePct'].apply(lambda x: f"{x:.1f}%"),
        textposition='outside'
    )])
    
    apply_common_layout(fig, title, height=350)
    fig.update_layout(
        xaxis_title='Cluster',
        yaxis_title='Inactivity Rate (%)',
        yaxis=dict(range=[0, 40], gridcolor=COLORS['light_gray'])
    )
    
    return fig


def create_cv_fold_bar(
    cv_df: pd.DataFrame,
    title: str = 'Cross-Validation Results by Fold'
) -> go.Figure:
    """
    Create a grouped bar chart showing CV results by fold.
    """
    fig = go.Figure()
    
    # Get unique thresholds
    thresholds = cv_df['threshold'].unique()
    
    for thresh in sorted(thresholds):
        subset = cv_df[cv_df['threshold'] == thresh]
        fig.add_trace(go.Bar(
            name=f'Threshold {thresh}',
            x=[f'Fold {f}' for f in subset['fold']],
            y=subset['cv_accuracy'],
            marker_color=COLORS['info'] if thresh == 0.425 else COLORS['success']
        ))
    
    apply_common_layout(fig, title)
    fig.update_layout(
        barmode='group',
        xaxis_title='Fold',
        yaxis_title='CV Accuracy',
        yaxis=dict(tickformat='.0%', gridcolor=COLORS['light_gray'])
    )
    
    return fig
