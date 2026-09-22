# BrewInsights Data

## Public data policy

The original respondent-level raw survey is not stored in this public repository because the source export can contain direct identifiers.

The dashboard and analytical outputs use the canonical processed dataset:

`data/processed/coffee_cleaned.csv`

A public-safe anonymized survey copy can contain the analytical survey fields without `respondentId` and `email`. Use `scripts/anonymize_public_data.py` when preparing a new public copy.

## Data layers

- `processed/` — cleaned analytical dataset used by the dashboard.
- `coffee_demand_*.csv` — saved demand/forecast artifacts.
- `external_city_data.csv` — city-level supporting data used in market analysis.

For definitions and analytical roles, see [DATA_DICTIONARY.md](../docs/DATA_DICTIONARY.md).
