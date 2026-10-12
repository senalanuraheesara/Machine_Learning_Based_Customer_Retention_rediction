# Feature engineering log

The final feature design is the rolling snapshot contract, not the old September-cutoff exploratory export. See the complete [feature definitions](snapshot_feature_contract.md).

| Decision | Implementation | Reason / limit |
| --- | --- | --- |
| Behavioral history | Recency, frequency, monetary, tenure, intervals, diversity and returns | Summarize observed customer behavior. Legacy aggregates include return lines. |
| Exposure normalization | Velocity, spend per month and recency ratio | Account for differing observed history with fixed denominator floors. |
| Positive-only invoice signals | 13 recent/order-level signals added by enrich_snapshots | Separate purchases from cancellations and fix interpretation of order averages. |
| Recent activity | Absolute 30/60/90-day counts and spend are retained in the final input contract | Earlier documentation saying all absolute recent features were excluded is superseded. |
| Compact forest features | 12 numeric columns plus country | Saved Random Forest uses this subset; accepting 35 inputs does not mean all 35 enter each estimator. |
| Deterministic interactions | BehaviorFeatures in optimized Logistic Regression | Computed from past features, with no target fitting. |
| Exclude identifiers/outcomes | Fixed FEATURES allowlist | Prevent direct identity, label or prediction input. |

The older `docs/feature_leakage_checks.csv` describes the single-window export and does not audit every rolling input. Past-only filtering, the rolling code and the final feature allowlist provide the current provenance; this documentation review does not claim a new independent leakage test. Snapshot caps and country groups use the whole past cohort, while estimator imputation/encoding/scaling are fitted within training folds.

See [decision log](decision_log.md), particularly D04–D10, for rationale and alternatives.
