# Feature Engineering Log

All features are calculated from transactions dated from 2010-12-01 through 2011-09-30. Outcome-window activity is used only for the binary target.

Customers with fewer than three unique invoices are excluded from supervised modeling because their behavioral history is insufficient.

Absolute recent 30-day and 60-day features are retained for audit exploration but excluded from the modeling feature list because their meaning changes with customer age. Tenure-normalized features are used instead.

                      Feature Uses only observation window                                                           Verification method
                 recency_days                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
              frequency_count                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
               monetary_total                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                 monetary_avg                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                 monetary_std                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                  tenure_days                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                 history_days                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
        purchase_interval_avg                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
        purchase_interval_std                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
         purchase_interval_cv                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
            product_diversity                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
product_diversity_per_invoice                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
     avg_quantity_per_invoice                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                  return_rate                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                 return_value                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                      country                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                weekend_ratio                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
            monthly_spend_std                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
          monthly_spend_trend                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
    days_since_first_purchase                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
            purchase_velocity                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
          purchases_per_month                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
              spend_per_month                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                recency_ratio                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation
                active_months                          Yes All source rows filtered to InvoiceDate <= OBSERVATION_END before aggregation

### Target alternatives considered

- No purchase for a fixed number of days: rejected because the outcome window provides a consistent business horizon.
- Revenue below a threshold: rejected because it confounds retention with purchase value.
- Frequency drop: rejected because it requires a customer-specific historical baseline and is less directly actionable.
