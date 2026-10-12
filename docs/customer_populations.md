# Customer populations and eligibility

Both inputs originate in `data/raw/Online Retail.xlsx` through `notebooks/02_preprocessing.ipynb`, after [transaction cleaning](preprocessing_log.md).

| Property | Classification | Final segmentation |
| --- | --- | --- |
| Input | customer_snapshot_features.csv | customer_features.csv |
| Unit | Customer at a prediction date | One customer |
| Count | 8,004 rows; 1,994 distinct customers | 1,696 rows and customers |
| Observation | Six calendar months before March–August 2011 prediction dates; prediction date excluded | 1 December 2010–30 September 2011 inclusive |
| Eligibility | At least two distinct invoices and 60 days since first observed invoice in that lookback | At least three distinct invoices; no separate 60-day rule |
| Outcome | Next two calendar months; inactive means no positive-quantity, non-cancelled purchase | 1 October–9 December 2011 inclusive; inactive means no cleaned transaction, including returns |
| Outcome use | Supervised target | Profiling after clustering only |

Return invoices can contribute to eligibility in both populations. The fixed-window filter removes 1,962 of 3,658 customers, leaving 1,696 (`customer_history_filter.csv`). A return-only outcome customer can count as active in this fixed-window definition. Fixed-window monetary_total uses net product quantities times mean product prices; rolling snapshots sum capped line revenues. Matching column names do not guarantee identical semantics.

Classification uses March/April for training (1,976 rows), June for validation (1,460), August for testing (1,603); May/July's 2,965 rows are excluded from these partitions. Customers recur across dates. Early lookbacks are truncated by the source beginning on 1 December 2010.

Direct CustomerID comparison finds 1,583 shared customers, 113 segmentation-only and 411 snapshot-only customers. Dates, lookbacks and eligibility rules explain why neither is a simple subset of the other. Old segmentation used latest eligible snapshots for 1,994 customers; the final workflow uses the fixed-window table.

## Why return-only activity is treated differently

The fixed-window export retains the earlier broad activity definition: any cleaned transaction shows account activity, including a return. The later rolling classifier uses a purchasing-retention definition: only a positive, non-cancelled purchase demonstrates continued buying. A return records interaction with the retailer but does not demonstrate a new purchase, so it does not count as retention for that classifier.

This is a legacy methodological difference, not a requirement of clustering. Segmentation itself uses neither outcome; the broad fixed-window outcome is joined only for descriptive profiling. Keeping it preserves the provenance of the saved 476/32 inactive counts, but those percentages must not be directly compared with classifier inactivity rates. A common-definition comparison would require rebuilding the fixed-window outcome from positive, non-cancelled purchases and reporting it as a separate sensitivity analysis; silently relabeling the current results would obscure the original definition.
