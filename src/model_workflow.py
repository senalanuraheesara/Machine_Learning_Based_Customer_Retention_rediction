"""Shared data contract; all estimators and searches remain visible in notebooks."""
from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix, brier_score_loss)
SEED = 42
TARGET = 'inactive_in_outcome_window'
FEATURES = ['recency_days','frequency_count','monetary_total','monetary_avg','monetary_std',
 'tenure_days','history_days','purchase_interval_avg','purchase_interval_std','purchase_interval_cv',
 'product_diversity','product_diversity_per_invoice','avg_quantity_per_invoice','return_rate',
 'return_value','country','weekend_ratio','monthly_spend_std','purchase_velocity',
 'spend_per_month','recency_ratio','active_months']
MODEL_NAMES = ['logistic_regression','decision_tree','random_forest','gradient_boosting']

def evaluation_model_names(p):
    """Original four plus completed, frozen classical-ML experiments, if present."""
    folder=p['models'].parent/'accuracy_optimization'
    registry=folder/'candidate_names.json'
    if registry.exists() and (folder/'selection.json').exists():
        names=json.loads(registry.read_text())
        if len(names)!=len(set(names)) or not set(MODEL_NAMES)<=set(names):
            raise ValueError('Invalid optimization candidate registry')
        return names
    return MODEL_NAMES.copy()
RECENT_FEATURES = ['positive_recency_days','positive_invoice_count','positive_order_value',
 'positive_quantity_per_invoice','days_overdue','orders_30d','orders_60d','orders_90d',
 'spend_30d','spend_60d','spend_90d','order_trend','spend_trend']
FEATURES += RECENT_FEATURES

def enrich_snapshots(snapshots, transactions):
    """Past-only positive-invoice signals. Preserve the existing cohort and targets."""
    result = snapshots.drop(columns=RECENT_FEATURES, errors='ignore').copy()
    tx = transactions.copy()
    tx['CustomerID'] = tx.CustomerID.astype(str)
    tx['InvoiceDate'] = pd.to_datetime(tx.InvoiceDate)
    tx = tx[(tx.Quantity > 0) & (tx.UnitPrice > 0) & ~tx.InvoiceNo.astype(str).str.startswith('C')]
    tx['positive_value'] = tx.Quantity * tx.UnitPrice
    frames = []
    for date, part in result.groupby('prediction_date', sort=True):
        date = pd.Timestamp(date)
        past = tx[(tx.InvoiceDate < date) & (tx.InvoiceDate >= date-pd.DateOffset(months=6))]
        invoices = past.groupby(['CustomerID','InvoiceNo']).agg(
            date=('InvoiceDate','min'), value=('positive_value','sum'), quantity=('Quantity','sum')).reset_index()
        stats = invoices.groupby('CustomerID').agg(last=('date','max'), first=('date','min'),
            positive_invoice_count=('InvoiceNo','size'),positive_order_value=('value','mean'),
            positive_quantity_per_invoice=('quantity','mean'))
        stats['positive_recency_days'] = (date-stats['last']).dt.total_seconds()/86400
        interval = (stats['last']-stats['first']).dt.total_seconds()/86400/(stats.positive_invoice_count-1).replace(0,np.nan)
        stats['days_overdue'] = stats.positive_recency_days / interval.clip(lower=1)
        for days in [30,60,90]:
            recent = invoices[invoices.date >= date-pd.Timedelta(days=days)].groupby('CustomerID')
            stats[f'orders_{days}d'] = recent.size().reindex(stats.index,fill_value=0)
            stats[f'spend_{days}d'] = recent.value.sum().reindex(stats.index,fill_value=0)
        stats['order_trend'] = (stats.orders_30d+1)/(stats.orders_60d-stats.orders_30d+1)
        stats['spend_trend'] = (stats.spend_30d+1)/(stats.spend_60d-stats.spend_30d+1)
        part = part.copy()
        part['CustomerID'] = part.CustomerID.astype(str)
        frames.append(part.merge(stats[RECENT_FEATURES],left_on='CustomerID',right_index=True,how='left',validate='one_to_one'))
    return pd.concat(frames,ignore_index=True)

def signed_log1p(values):
    return np.sign(values)*np.log1p(np.abs(values))

MAX_FIT_GAP = .05
MIN_BASELINE_GAIN = .03
MAX_CAPACITY_LOSS = .01

def regularized_refit(results, baseline_accuracy=None):
    """Select competitive CV accuracy subject to explicit fitting-risk limits.

    Never fall back silently to an overfitting or near-baseline configuration.
    These are screening rules, not guarantees of absence of bias/variance.
    """
    if baseline_accuracy is None or not np.isfinite(baseline_accuracy) or not 0<=baseline_accuracy<=1:
        raise ValueError('A valid training-only majority baseline is required for underfitting screening.')
    val = np.asarray(results['mean_test_accuracy'],dtype=float)
    training = np.asarray(results['mean_train_accuracy'],dtype=float)
    gap = training-val
    allowed = np.isfinite(val)&np.isfinite(training)&(gap<=MAX_FIT_GAP)
    allowed &= val >= baseline_accuracy+MIN_BASELINE_GAIN
    allowed &= val >= np.nanmax(val)-MAX_CAPACITY_LOSS
    eligible = np.flatnonzero(allowed)
    if not len(eligible):
        raise ValueError('No candidate passes fit controls: revise features/capacity or collect more data; do not select an unsafe fallback.')
    near = eligible[val[eligible] >= val[eligible].max()-.002]
    return int(min(near, key=lambda i: (max(0,gap[i]), -val[i], i)))

def accuracy_threshold(y, probability):
    rows = pd.DataFrame([metrics('candidate',y,probability,t) for t in np.linspace(.05,.95,91)])
    rows['distance_to_half'] = abs(rows.Threshold-.5)
    chosen = rows.sort_values(['Accuracy','distance_to_half','Threshold'],ascending=[False,True,True]).iloc[0]
    return float(chosen.Threshold), rows

def fit_diagnosis(train_accuracy, cv_accuracy, baseline_accuracy):
    # Screening heuristics, not statistical proof or an arbitrary accuracy target.
    if train_accuracy-cv_accuracy > MAX_FIT_GAP:
        return 'Overfitting warning: train-CV gap > 5 pp'
    if cv_accuracy < baseline_accuracy+MIN_BASELINE_GAIN:
        return 'Possible underfitting / weak signal: CV near baseline'
    return 'Passes fitting screen; no strong overfitting or severe-underfitting signal'
def paths(root):
    result = {'processed':root/'data/processed','models':root/'outputs/models',
              'tables':root/'outputs/tables','figures':root/'outputs/figures/separate_modeling'}
    for p in result.values(): p.mkdir(parents=True,exist_ok=True)
    return result

def load_features(p):
    f = p/'customer_snapshot_features.csv'
    if not f.exists(): raise FileNotFoundError(f'Run 02_preprocessing.ipynb first: missing {f}')
    data = pd.read_csv(f, dtype={'CustomerID':str},parse_dates=['prediction_date'])
    required = FEATURES + [TARGET,'CustomerID','prediction_date','snapshot_id']
    missing = set(required)-set(data)
    if missing: raise ValueError(f'Missing columns: {sorted(missing)}')
    if data[required[-4:]].isna().any().any(): raise ValueError('Missing target or snapshot identifiers')
    if data.duplicated(['CustomerID','prediction_date']).any(): raise ValueError('Duplicate customer snapshots')
    if not set(data[TARGET].unique()) <= {0,1}: raise ValueError('Target must be 0/1')
    data = data.sort_values(['prediction_date','CustomerID']).reset_index(drop=True)
    data['row_id'] = np.arange(len(data))
    data['split'] = 'excluded'
    # Labels from March/April finish by June 30. June labels finish before August 31.
    data.loc[data.prediction_date.isin(pd.to_datetime(['2011-03-31','2011-04-30'])),'split']='train'
    data.loc[data.prediction_date.eq(pd.Timestamp('2011-06-30')),'split']='validation'
    data.loc[data.prediction_date.eq(pd.Timestamp('2011-08-31')),'split']='test'
    for split in ['train','validation','test']:
        part=data[data.split.eq(split)]
        if part.empty or part[TARGET].nunique()!=2: raise ValueError(f'{split} needs both classes and expected dates')
    for a,b in [('train','validation'),('validation','test')]:
        assert (data.loc[data.split.eq(a),'prediction_date']+pd.DateOffset(months=2)).max() <= data.loc[data.split.eq(b),'prediction_date'].min()
    fingerprint = hashlib.sha256(f.read_bytes() + ('v3-accuracy-purged-'+','.join(FEATURES)).encode()).hexdigest()
    return data, fingerprint

def matrix(data):
    return data[FEATURES].replace([np.inf,-np.inf],np.nan)

def preprocess(scale=False):
    steps=[('imputer',SimpleImputer(strategy='median',keep_empty_features=True))]
    if scale:
        steps.extend([('log',FunctionTransformer(signed_log1p,feature_names_out='one-to-one')),('scale',StandardScaler())])
    return ColumnTransformer([
        ('numeric',Pipeline(steps),[f for f in FEATURES if f!='country']),
        ('country',Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),
         ('encode',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),['country'])])

def metrics(name,y,p,threshold=.5):
    pred=(np.asarray(p)>=threshold).astype(int)
    tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    return dict(Model=name,Accuracy=accuracy_score(y,pred),Precision=precision_score(y,pred,zero_division=0),
      Recall=recall_score(y,pred,zero_division=0),F1=f1_score(y,pred,zero_division=0),
      **{'ROC-AUC':roc_auc_score(y,p),'PR-AUC':average_precision_score(y,p),
         'Brier score':brier_score_loss(y,p),'TN':int(tn),'FP':int(fp),'FN':int(fn),'TP':int(tp),'Threshold':float(threshold)})
