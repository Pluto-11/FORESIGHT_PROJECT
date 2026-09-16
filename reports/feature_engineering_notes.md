# Feature Engineering Notes

## Objective
Feature engineering was performed to create useful time-based and historical demand features for SKU-level forecasting.

## Features Created

- Month: Month number extracted from the Date.
- Day_of_Week: Day of the week extracted from the Date.
- Is_Weekend: Indicates whether the day is Saturday or Sunday.
- Promo_Lag_7: Promotion status from 7 days earlier for the same SKU.
- Lag_1: Units sold by the same SKU on the previous day.
- Lag_7: Units sold by the same SKU 7 days earlier.
- Rolling_7: Seven-day rolling average of previous demand for the same SKU.

## Missing Values

Missing values in lag and rolling features occur at the beginning of each SKU's time series because previous observations are not available.

These values were not blindly replaced with zero because zero would represent actual demand and could distort the historical demand information.

## Output

The feature-engineered dataset contains 36,550 rows and 30 columns.

Output file:
`data/feature_engineered.csv`

## Reproducibility

Feature engineering can be reproduced by running:

`python src/feature_engineering.py`