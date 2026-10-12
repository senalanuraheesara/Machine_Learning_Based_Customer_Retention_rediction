# Preprocessing Decision Log

All transformations are implemented in this notebook and should be rerun from the raw source.

## Decision: D5: Exact duplicates

**Options considered:** Remove, keep, or investigate

**Chosen:** Remove exact duplicates only

**Justification:** Exact duplicates can inflate revenue and frequency without representing separate purchases.

**Alternatives rejected because:** Keeping duplicates would overstate customer activity.

**Impact:** 541,909 rows before the step; 536,641 rows after the step.

## Decision: D1: Missing CustomerID

**Options considered:** Drop, placeholder, or separate analysis

**Chosen:** Drop from customer-level modeling

**Justification:** A missing customer identifier prevents reliable aggregation and target assignment.

**Alternatives rejected because:** Placeholder identifiers would merge unrelated people.

**Impact:** 541,909 rows before the step; 401,604 rows after the step.

## Decision: D4: Zero or negative UnitPrice

**Options considered:** Remove, impute, or investigate

**Chosen:** Remove from modeling data

**Justification:** Non-positive prices do not have valid revenue meaning for this task.

**Alternatives rejected because:** Median imputation would invent monetary values.

**Impact:** 541,909 rows before the step; 401,564 rows after the step.

## D2/D3: Return and cancellation handling

Negative quantities and cancellation indicators are retained as valid behavior. Net customer-product quantities and values are calculated before customer aggregation; return counts and return value remain explicit features.

## D6: Outlier handling

For modeling features, positive Quantity and UnitPrice are capped at their respective 99th percentiles. Raw values remain available in the cleaned transaction export for auditability.

## D7: Country handling

The five most frequent countries are retained individually and all remaining countries are grouped as Other. This reduces dimensionality while preserving the largest markets.
