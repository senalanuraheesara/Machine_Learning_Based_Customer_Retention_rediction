# Preprocessing decision log

The active classifier input is [customer_snapshot_features.csv](../data/processed/customer_snapshot_features.csv), built by [02_preprocessing.ipynb](../notebooks/02_preprocessing.ipynb). The earlier single-window `customer_features.csv` is the final segmentation input, not the classifier training table. See [population definitions](customer_populations.md).

## Sequential cleaning counts

| Step | Input rows | Removed | Remaining |
| --- | --- | --- | --- |
| Remove exact duplicates | 541,909 | 5,268 | 536,641 |
| Drop missing CustomerID | 536,641 | 135,037 | 401,604 |
| Remove UnitPrice ≤ 0 | 401,604 | 40 | 401,564 |

The raw data has 135,080 missing IDs and 2,517 non-positive prices. Those raw issue counts overlap other filters; they are not the sequential removals above. Earlier generated notes incorrectly reused the raw row count as the input count for later steps.

CustomerID becomes a string join key. Negative quantities and cancellation invoices remain in cleaned data (8,872 rows of each, as reported). Return quantity/value and cancellation indicators are retained. Missing descriptions are not required for the classifier. Net customer-product aggregates are an audit export; the rolling feature builder aggregates transaction lines directly.

## Active rolling snapshots

For prediction date t, features use [t − 6 calendar months, t); labels use [t, t + 2 calendar months). Class 1 means no positive-quantity, non-cancelled purchase during the label window; prices are already positive after cleaning. At least two distinct invoices and 60 days since the first observed invoice in the lookback are required. Return invoices can contribute to this eligibility rule.

| Prediction date | Snapshots | Inactive rate | Classifier use |
| --- | --- | --- | --- |
| 2011-03-31 | 854 | 35.95% | Train |
| 2011-04-30 | 1122 | 39.22% | Train |
| 2011-05-31 | 1412 | 44.33% | Excluded from classifier splits |
| 2011-06-30 | 1460 | 45.68% | Validation |
| 2011-07-31 | 1553 | 42.63% | Excluded from classifier splits |
| 2011-08-31 | 1603 | 38.05% | Test |

Total: 8,004 snapshot rows from 1,994 customers. Classifier partitions contain 1,976 training, 1,460 validation and 1,603 test rows; 2,965 May/July rows are excluded. Repeated customer identities across temporal partitions are allowed. Training CV groups rows by customer.

Each lookback recomputes its positive-quantity 99th percentile, price 99th percentile and five most frequent countries. Quantity is upper-clipped only, so negative return extremes remain. Country grouping and caps use all customers in that past snapshot; they are not fold-fitted transformations. Median imputation and encoding inside the estimator pipeline are fold-fitted.

The earlier exploratory section calculates full-period caps (quantity 120, price 15) and a fixed observation window ending September 2011. Those are not the rolling classifier's caps or target definition. Early six-month lookbacks have less than six months of available data because the source begins on 1 December 2010.

See [project decisions](decision_log.md) and [feature contract](snapshot_feature_contract.md).
