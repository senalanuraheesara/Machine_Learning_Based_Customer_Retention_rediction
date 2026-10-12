# Rolling classifier feature contract

The authoritative input order is `FEATURES` in [model_workflow.py](../src/model_workflow.py): 35 columns (34 numeric and country). `matrix()` selects these columns and replaces infinities with missing values.

| Feature(s) | Implemented definition |
| --- | --- |
| recency_days | Days from most recent line to cutoff; can include returns. |
| frequency_count | Distinct invoices in lookback; can include cancellations. |
| monetary_total | Sum of capped line revenue, including negative returns. |
| monetary_avg / monetary_std | Mean / sample standard deviation of capped line revenue, not invoice totals. |
| tenure_days | Last minus first observed line timestamp. |
| history_days | Cutoff minus first observed line timestamp. |
| purchase_interval_avg / purchase_interval_std / purchase_interval_cv | Mean / sample standard deviation / coefficient of variation of intervals between distinct invoice dates; legacy undefined values filled with zero. |
| product_diversity | Number of distinct stock codes. |
| product_diversity_per_invoice | Distinct stock codes divided by distinct invoices. |
| avg_quantity_per_invoice | Legacy name: mean capped quantity per transaction line, not per invoice. |
| return_rate | Negative-quantity line count divided by total line count. |
| return_value | Sum of absolute negative quantity × original positive price; not capped. |
| country | Modal country after snapshot-specific top-five/Other grouping. |
| weekend_ratio | Fraction of lines on Saturday/Sunday. |
| monthly_spend_std | Sample standard deviation of capped revenue summed by active calendar month; inactive months not inserted. |
| purchase_velocity | Invoice count / (history_days clipped to at least 30 / 30). |
| spend_per_month | Capped revenue / (history_days clipped to at least 30 / 30). |
| recency_ratio | recency_days / max(history_days, 1). |
| active_months | Number of calendar months containing observed lines. |
| positive_recency_days | Days since last positive non-cancelled invoice. |
| positive_invoice_count | Count of positive non-cancelled invoices. |
| positive_order_value | Mean original, uncapped invoice value. |
| positive_quantity_per_invoice | Mean original, uncapped invoice quantity. |
| days_overdue | Positive recency / mean positive invoice interval, interval floored at one day. |
| orders_30d / orders_60d / orders_90d | Positive invoice counts in trailing windows. |
| spend_30d / spend_60d / spend_90d | Original positive invoice value in trailing windows. |
| order_trend | (Orders in last 30 days + 1) / (orders in preceding 30 days + 1). |
| spend_trend | (Spend in last 30 days + 1) / (spend in preceding 30 days + 1). |

All inputs use the past six-month lookback. Positive-only signals additionally require Quantity > 0, UnitPrice > 0 and no cancellation prefix. Invoice value/quantity are line sums and invoice time is its earliest line time. Missing positive-only signals remain missing for pipeline median imputation; no outcome activity is used as a predictor.

The final Random Forest uses 12 compact numeric inputs plus country: positive_recency_days, positive_invoice_count, positive_order_value, days_overdue, orders_30d, orders_60d, orders_90d, order_trend, history_days, purchase_interval_cv, return_rate and product_diversity.

The optimized Logistic Regression pipeline includes deterministic `BehaviorFeatures` interactions (recent order/spend shares, order rate, active-month fraction, recent order change, recent order value and spend per product), followed by its fitted column selection, imputation, signed log1p and standard scaling. Decision Tree and standard Gradient Boosting use the shared base preprocessing. The fitted pipeline remains the authority for each model's transformed feature set.

CustomerID, dates, snapshot_id, split, labels and predictions are excluded. Exported helper fields such as monthly_spend_trend (fixed to zero in the rolling builder), days_since_first_purchase and purchases_per_month are not in the classifier FEATURES list. Segmentation uses a separate 16-column list and does include monthly_spend_trend.

Evidence: [preprocessing notebook](../notebooks/02_preprocessing.ipynb), [model helper](../src/model_workflow.py), [derived-feature helper](../src/accuracy_experiments.py), individual model notebooks. See [preprocessing limitations](preprocessing_log.md).
