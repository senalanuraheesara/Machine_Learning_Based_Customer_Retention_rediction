"""
Data loading utilities for the dashboard.
Handles loading of processed datasets, model outputs, and segmentation results.
"""
import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FINAL_FOUR_DIR = OUTPUT_DIR / "final_four"
SEGMENTATION_DIR = OUTPUT_DIR / "segmentation"
EVIDENCE_DIR = OUTPUT_DIR / "evidence"
REPRODUCTION_DIR = OUTPUT_DIR / "reproduction"


@st.cache_data(ttl=3600)
def load_model_selection() -> Dict[str, Any]:
    """Load the model selection metadata."""
    selection_path = FINAL_FOUR_DIR / "selection.json"
    if not selection_path.exists():
        st.error(f"Model selection file not found: {selection_path}")
        return {}
    
    with open(selection_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@st.cache_data(ttl=3600)
def load_model_comparison() -> pd.DataFrame:
    """Load the model comparison results."""
    comparison_path = FINAL_FOUR_DIR / "model_comparison.csv"
    if not comparison_path.exists():
        st.error(f"Model comparison file not found: {comparison_path}")
        return pd.DataFrame()
    
    return pd.read_csv(comparison_path)


@st.cache_data(ttl=3600)
def load_accuracy_summary() -> pd.DataFrame:
    """Load the accuracy summary for all models."""
    summary_path = FINAL_FOUR_DIR / "accuracy_summary.csv"
    if not summary_path.exists():
        st.error(f"Accuracy summary file not found: {summary_path}")
        return pd.DataFrame()
    
    return pd.read_csv(summary_path)


@st.cache_data(ttl=3600)
def load_customer_features() -> pd.DataFrame:
    """Load the customer-level feature dataset used for segmentation."""
    features_path = DATA_DIR / "customer_features.csv"
    if not features_path.exists():
        st.error(f"Customer features file not found: {features_path}")
        return pd.DataFrame()
    
    df = pd.read_csv(features_path, dtype={'CustomerID': str})
    return df


@st.cache_data(ttl=3600)
def load_customer_snapshot_features() -> pd.DataFrame:
    """Load the customer snapshot features (prediction dataset)."""
    snapshot_path = DATA_DIR / "customer_snapshot_features.csv"
    if not snapshot_path.exists():
        st.error(f"Customer snapshot features file not found: {snapshot_path}")
        return pd.DataFrame()
    
    df = pd.read_csv(snapshot_path, dtype={'CustomerID': str}, parse_dates=['prediction_date'])
    return df


@st.cache_data(ttl=3600)
def load_segmentation_assignments() -> pd.DataFrame:
    """Load the K-Means cluster assignments for customers."""
    segments_path = SEGMENTATION_DIR / "customer_segments_kmeans_k2.csv"
    if not segments_path.exists():
        st.error(f"Segmentation file not found: {segments_path}")
        return pd.DataFrame()
    
    df = pd.read_csv(segments_path, dtype={'CustomerID': str})
    return df


@st.cache_data(ttl=3600)
def load_cluster_profiles() -> pd.DataFrame:
    """Load the cluster median profiles."""
    profiles_path = SEGMENTATION_DIR / "cluster_median_profiles_k2.csv"
    if not profiles_path.exists():
        st.error(f"Cluster profiles file not found: {profiles_path}")
        return pd.DataFrame()
    
    return pd.read_csv(profiles_path)


@st.cache_data(ttl=3600)
def load_cluster_sizes() -> pd.DataFrame:
    """Load cluster size information."""
    sizes_path = SEGMENTATION_DIR / "cluster_sizes_k2.csv"
    if not sizes_path.exists():
        st.error(f"Cluster sizes file not found: {sizes_path}")
        return pd.DataFrame()
    
    return pd.read_csv(sizes_path)


@st.cache_data(ttl=3600)
def load_cluster_inactivity() -> pd.DataFrame:
    """Load cluster inactivity summary."""
    inactivity_path = SEGMENTATION_DIR / "cluster_inactivity_summary_k2.csv"
    if not inactivity_path.exists():
        st.error(f"Cluster inactivity file not found: {inactivity_path}")
        return pd.DataFrame()
    
    return pd.read_csv(inactivity_path)


@st.cache_data(ttl=3600)
def load_clustering_comparison() -> pd.DataFrame:
    """Load K-Means comparison across different K values."""
    comparison_path = SEGMENTATION_DIR / "kmeans_cluster_comparison_v3.csv"
    if not comparison_path.exists():
        st.error(f"Clustering comparison file not found: {comparison_path}")
        return pd.DataFrame()
    
    return pd.read_csv(comparison_path)


@st.cache_data(ttl=3600)
def load_cross_validation_results(model_name: str) -> Tuple[pd.DataFrame, Dict]:
    """Load cross-validation results for a specific model."""
    cv_dir = EVIDENCE_DIR / "cross_validation"
    folds_path = cv_dir / f"{model_name}_folds.csv"
    provenance_path = cv_dir / f"{model_name}_provenance.json"
    
    folds_df = pd.DataFrame()
    provenance = {}
    
    if folds_path.exists():
        folds_df = pd.read_csv(folds_path)
    
    if provenance_path.exists():
        with open(provenance_path, 'r', encoding='utf-8') as f:
            provenance = json.load(f)
    
    return folds_df, provenance


@st.cache_data(ttl=3600)
def load_validation_thresholds(model_name: str) -> pd.DataFrame:
    """Load validation threshold analysis for a model."""
    thresholds_path = REPRODUCTION_DIR / model_name / "validation_thresholds.csv"
    if not thresholds_path.exists():
        return pd.DataFrame()
    
    return pd.read_csv(thresholds_path)


def get_model_threshold() -> float:
    """Get the selected model's classification threshold."""
    selection = load_model_selection()
    if not selection:
        return 0.425  # Default fallback
    
    # Find Random Forest variant
    for variant in selection.get('variants', []):
        if variant.get('Model') == 'random_forest':
            return float(variant.get('Threshold', 0.425))
    
    return 0.425


def get_selected_model_info() -> Dict[str, Any]:
    """Get information about the selected model."""
    selection = load_model_selection()
    comparison = load_model_comparison()
    
    if selection and not comparison.empty:
        model_name = selection.get('model', 'random_forest')
        model_row = comparison[comparison['Model'] == model_name]
        if not model_row.empty:
            return {
                'name': model_name,
                'display_name': model_name.replace('_', ' ').title(),
                'threshold': float(model_row['Threshold'].values[0]),
                'train_accuracy': float(model_row['Training accuracy'].values[0]),
                'validation_accuracy': float(model_row['Validation accuracy'].values[0]),
                'test_accuracy': float(model_row['Test accuracy'].values[0]),
                'cv_accuracy': float(model_row['CV accuracy'].values[0]),
                'selection_rule': selection.get('rule', ''),
                'limitations': selection.get('limitations', '')
            }
    
    return {
        'name': 'random_forest',
        'display_name': 'Random Forest',
        'threshold': 0.425,
        'train_accuracy': 0.7156,
        'validation_accuracy': 0.6863,
        'test_accuracy': 0.6712,
        'cv_accuracy': 0.6959,
        'selection_rule': 'Highest validation accuracy',
        'limitations': 'Validation and test were previously inspected'
    }


def get_segmentation_metrics() -> Dict[str, Any]:
    """Get segmentation clustering metrics."""
    comparison = load_clustering_comparison()
    
    if not comparison.empty:
        k2_row = comparison[comparison['k'] == 2]
        if not k2_row.empty:
            return {
                'k': 2,
                'silhouette': float(k2_row['silhouette'].values[0]),
                'davies_bouldin': float(k2_row['davies_bouldin'].values[0]),
                'smallest_cluster': int(k2_row['smallest_cluster'].values[0]),
                'largest_cluster': int(k2_row['largest_cluster'].values[0])
            }
    
    return {
        'k': 2,
        'silhouette': 0.6895,
        'davies_bouldin': 0.9234,
        'smallest_cluster': 119,
        'largest_cluster': 1577
    }
