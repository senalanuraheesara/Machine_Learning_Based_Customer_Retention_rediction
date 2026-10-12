# Retail Customer Analytics Dashboard

**AI-Powered Customer Retention & Behavioral Segmentation**

A professional Streamlit dashboard presenting the results of an IT3091 Machine Learning project focused on customer retention prediction and behavioral segmentation for online retail.

## Overview

This dashboard visualizes the outputs of a machine learning pipeline that:
- Predicts customer inactivity risk using Random Forest classification
- Segments customers into behavioral groups using K-Means clustering
- Provides actionable business insights for retention strategies

## Features

### Page 1: Retention Prediction
- **KPI Overview**: Total customers, predicted inactive/active counts, risk distribution
- **Risk Filters**: Filter by risk category, predicted status, customer ID, probability range
- **Probability Distribution**: Interactive histogram showing prediction distribution
- **Customer Table**: Searchable, sortable table with export functionality
- **Customer Detail View**: Individual customer profiles with retention recommendations

### Page 2: Customer Segmentation
- **Clustering Metrics**: Silhouette score, Davies-Bouldin index, cluster counts
- **Cluster Distribution**: Interactive bar chart of cluster sizes
- **Behavioral Profiles**: Median feature values by cluster
- **Feature Comparison**: Box plots, violin plots, histograms for cluster comparison
- **Inactivity Analysis**: Observed inactivity rates by cluster with statistical context
- **Cluster Explorer**: Browse and export customers by cluster

### Page 3: Business Insights
- **Executive Overview**: Business problem summary and key findings
- **Model Comparison**: Performance metrics across all four models
- **Cross-Validation Analysis**: Fold-by-fold CV results for each model
- **Threshold Analysis**: Accuracy vs threshold curves
- **Business Recommendations**: Actionable retention strategies
- **Limitations & Responsible ML**: Important disclaimers and considerations

## Required Project Files

The dashboard requires these files from the ML project:

### Data Files
```
data/processed/
├── customer_features.csv           # Customer-level feature dataset
└── customer_snapshot_features.csv  # Snapshot features for predictions
```

### Model Outputs
```
outputs/final_four/
├── selection.json                  # Model selection metadata
├── model_comparison.csv            # Model performance comparison
└── accuracy_summary.csv            # Accuracy summary table
```

### Segmentation Outputs
```
outputs/segmentation/
├── customer_segments_kmeans_k2.csv      # Cluster assignments
├── cluster_median_profiles_k2.csv       # Cluster profiles
├── cluster_sizes_k2.csv                 # Cluster sizes
├── cluster_inactivity_summary_k2.csv    # Inactivity by cluster
└── kmeans_cluster_comparison_v3.csv     # K comparison
```

### Evidence Files (Optional)
```
outputs/evidence/cross_validation/
├── random_forest_folds.csv
├── logistic_regression_folds.csv
├── gradient_boosting_folds.csv
└── decision_tree_folds.csv

outputs/reproduction/random_forest/
└── validation_thresholds.csv
```

## Installation

### Prerequisites
- Python 3.10+ (tested with Python 3.14)
- The project's existing virtual environment or dependencies

### Install Dependencies

Using PowerShell:
```powershell
# Navigate to project root
cd D:\Year3\final

# Install dashboard dependencies
python -m pip install streamlit plotly

# Or use requirements if Streamlit not in existing requirements
python -m pip install -r requirements.txt
python -m pip install streamlit plotly
```

### Required Packages
- `streamlit` >= 1.28.0
- `pandas` >= 2.0.0
- `numpy` >= 1.24.0
- `plotly` >= 5.15.0
- `scikit-learn` >= 1.3.0 (for compatibility with project)

## Running the Dashboard

### Start the Application

Using PowerShell:
```powershell
# Navigate to project root
cd D:\Year3\final

# Run Streamlit
python -m streamlit run dashboard/app.py
```

Or from the dashboard directory:
```powershell
cd D:\Year3\final\dashboard
python -m streamlit run app.py
```

### Access the Dashboard
The dashboard will open automatically in your browser at:
- Local URL: `http://localhost:8501`
- Network URL: `http://<your-ip>:8501`

## Dashboard Structure

```
dashboard/
├── app.py                    # Main application entry point
├── pages/
│   ├── 1_Retention_Prediction.py
│   ├── 2_Customer_Segmentation.py
│   └── 3_Business_Insights.py
├── components/
│   ├── __init__.py
│   ├── sidebar.py            # Navigation sidebar
│   ├── styles.py             # Custom CSS styling
│   ├── kpi_cards.py          # KPI card components
│   └── charts.py             # Plotly chart utilities
├── utils/
│   ├── __init__.py
│   ├── data_loader.py        # Data loading with caching
│   └── prediction_service.py # Prediction utilities
└── README.md                 # This file
```

## Model Loading & Prediction Logic

### Current Implementation
The dashboard uses **saved evaluation data** from the project outputs. Since the trained model files (`.joblib`) are not present in the visible outputs directory, the dashboard:

1. Loads customer snapshot features from the test split (August 2011)
2. Uses feature-based probability estimation calibrated to actual outcomes
3. Displays the actual inactivity outcomes alongside estimated probabilities

### For Live Predictions
To enable live predictions with the trained model:

1. Ensure model files are saved in `outputs/final_four/`:
   - `random_forest.joblib`
   - `logistic_regression.joblib`
   - etc.

2. Modify `utils/prediction_service.py` to load and use the model:
   ```python
   import joblib
   
   model_bundle = joblib.load(MODEL_PATH)
   pipeline = model_bundle['pipeline']
   threshold = model_bundle['metadata']['Threshold']
   
   probabilities = pipeline.predict_proba(X)[:, 1]
   predictions = (probabilities >= threshold).astype(int)
   ```

## Data Limitations

1. **Historical Data**: Analysis based on Dec 2010 - Dec 2011 transactions
2. **Reused Holdouts**: Validation and test sets were inspected during development
3. **Missing Customer IDs**: Some transactions lack identifiable customer information
4. **Outcome Definition**: Inactivity defined as no purchase within 2-month window
5. **Segmentation Independence**: Cluster membership not significantly associated with inactivity risk

## Troubleshooting

### Import Errors
If you see import errors, ensure you're running from the project root:
```powershell
cd D:\Year3\final
python -m streamlit run dashboard/app.py
```

### Missing Data Files
If data fails to load:
1. Verify the required CSV files exist in `data/processed/` and `outputs/`
2. Run the preprocessing and modeling notebooks to generate missing files
3. Check file paths in `utils/data_loader.py`

### Style Issues
If styling appears broken:
1. Clear Streamlit cache: `streamlit cache clear`
2. Restart the application

### Performance
For large datasets, the dashboard uses `@st.cache_data` decorators. If data seems stale:
1. Use the "Rerun" button in Streamlit
2. Clear cache via settings menu

## Project Information

- **Module**: IT3091 - Machine Learning
- **Institution**: Sri Lanka Institute of Information Technology (SLIIT)
- **Group**: 2026-DS-60
- **Dataset**: UCI Online Retail Dataset

---

*This dashboard is part of an academic machine learning project. Predictions and recommendations are for educational purposes and should not be used for actual business decisions without proper validation.*
