| Variable    | Type     | Business Meaning              | Quality Issues                                          | Modeling Role                        |
|:------------|:---------|:------------------------------|:--------------------------------------------------------|:-------------------------------------|
| InvoiceNo   | string   | Unique transaction identifier | Some values start with 'C' and indicate cancellations   | Identifier / transaction grouping    |
| StockCode   | string   | Product SKU                   | Descriptions may vary for one code                      | Product aggregation                  |
| Description | string   | Product name                  | Missing values occur for some records                   | Optional product context             |
| Quantity    | integer  | Items purchased               | Negative values represent returns; extreme values exist | Aggregated behavioral feature        |
| InvoiceDate | datetime | Transaction timestamp         | Must be validated for range and gaps                    | Temporal features and split design   |
| UnitPrice   | float    | Price per item                | Zeros and negative values are invalid for revenue       | Aggregated monetary feature          |
| CustomerID  | float    | Customer identifier           | Approximately 25% missing                               | Customer-level join key              |
| Country     | string   | Customer country              | Many countries with uneven frequency                    | Context and optional encoded feature |