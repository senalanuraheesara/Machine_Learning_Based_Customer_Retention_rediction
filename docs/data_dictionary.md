# Data dictionary

Source: `data/raw/Online Retail.xlsx`, first worksheet; 541,909 rows and eight columns. The saved EDA reports timestamps from 1 December 2010 08:26 to 9 December 2011 12:50, 38 countries, 25,900 invoices and 4,070 stock codes.

| Field | Raw type / interpretation | Use and data quality |
| --- | --- | --- |
| InvoiceNo | Transaction/invoice identifier | Repeated across invoice lines; prefix C indicates cancellation. Used for invoice aggregation, not a model predictor. |
| StockCode | Product identifier | Distinct-product counts; descriptions may vary for the same code. |
| Description | Product text | 1,454 missing values; not used by the final classifier. |
| Quantity | Integer units on a line | 10,624 negative raw rows; returns retained. Large positive and negative values occur. |
| InvoiceDate | Transaction timestamp | Defines lookback/outcome windows and invoice intervals. |
| UnitPrice | Numeric unit price | 2,517 raw non-positive rows; only positive prices survive cleaning. |
| CustomerID | Numeric-looking customer ID, stored as string after cleaning | 135,080 missing raw values (24.927%); required for aggregation and grouped CV, excluded as predictor. |
| Country | Country string | Past-window top-five grouping followed by pipeline one-hot encoding. |

These are raw issue counts, not additive cleaning losses. See [sequential cleaning log](preprocessing_log.md).

| Derived field | Meaning |
| --- | --- |
| prediction_date | Cutoff timestamp for one customer snapshot |
| snapshot_id | Monthly snapshot identifier |
| inactive_in_outcome_window | 1 if no positive non-cancelled purchase in the following two months; otherwise 0 |
| split | Assigned by the helper: train, validation, test or excluded |
| predicted_probability | Model estimate for class 1; not proof of a future outcome |
| predicted_class | Probability ≥ the bundle's frozen threshold |

The [feature contract](snapshot_feature_contract.md) defines the 35 classifier input columns and model-specific feature processing. Identifiers, dates, labels and predictions do not enter that input list.

Evidence: [EDA notebook](../notebooks/01_data_understanding.ipynb). The separate quality and raw dictionary CSV exports are absent from this package; the field definitions are included above. The target definition in this table applies to classification; see [population definitions](customer_populations.md) for the fixed-window segmentation outcome.
