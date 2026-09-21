import pandas as pd
from pathlib import Path
import joblib
import numpy as np

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent

data_folder = project_folder / "data"
model_folder = project_folder / "models"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(
    data_folder / "feature_engineered.csv"
)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values(
    ["SKU", "Date"]
).reset_index(drop=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load(
    model_folder / "demand_model.pkl"
)

features = joblib.load(
    model_folder / "feature_list.pkl"
)

print("FORECAST ENGINE INITIALIZED")

print("Latest historical date:")
print(df["Date"].max())

print("\nNumber of SKUs:")
print(df["SKU"].nunique())

print("\nModel features:")
print(features)



# --------------------------------------------------
# FORECAST SETTINGS
# --------------------------------------------------

forecast_days = 7

last_date = df["Date"].max()

forecast_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=forecast_days,
    freq="D"
)

print("\nForecast period:")
print(forecast_dates.min(), "to", forecast_dates.max())

print("\nForecast days:", len(forecast_dates))





# --------------------------------------------------
# PREPARE HISTORICAL DEMAND
# --------------------------------------------------

history = df[
    ["Date", "SKU", "Units_Sold"]
].copy()

# --------------------------------------------------
# RECURSIVE FORECASTING
# --------------------------------------------------

forecast_results = []

for sku in df["SKU"].unique():

    sku_history = history[
        history["SKU"] == sku
    ].copy()

    demand_history = list(
        sku_history["Units_Sold"].values
    )

    for forecast_date in forecast_dates:

        # Lag 1
        lag_1 = demand_history[-1]

        # Lag 7
        lag_7 = demand_history[-7]

        # Rolling 7-day average
        rolling_7 = np.mean(
            demand_history[-7:]
        )

        # Calendar features
        month = forecast_date.month

        day_of_week = forecast_date.dayofweek

        is_weekend = int(
            day_of_week >= 5
        )

        # Promotion is assumed to be 0
        # because future promotion information
        # is not being supplied yet.
        promotion = 0

        # --------------------------------------------------
        # MODEL INPUT
        # --------------------------------------------------

        X_future = pd.DataFrame({
            "Lag_1": [lag_1],
            "Lag_7": [lag_7],
            "Rolling_7": [rolling_7],
            "Month": [month],
            "Day_of_Week": [day_of_week],
            "Is_Weekend": [is_weekend],
            "Promotion": [promotion]
        })

        # --------------------------------------------------
        # PREDICT
        # --------------------------------------------------

        prediction = model.predict(
            X_future[features]
        )[0]

        prediction = max(
            float(prediction),
            0
        )

        # Add prediction to history
        # so the next day can use it.
        demand_history.append(
            prediction
        )

        forecast_results.append({
            "Date": forecast_date,
            "SKU": sku,
            "Predicted_Demand": prediction
        })

# --------------------------------------------------
# CREATE FORECAST DATAFRAME
# --------------------------------------------------

forecast_df = pd.DataFrame(
    forecast_results
)

print("\nFORECAST GENERATED")

print(
    "Rows:",
    len(forecast_df)
)

print(
    "\nForecast preview:"
)

print(
    forecast_df.head(10)
)


# --------------------------------------------------
# SAVE FORECAST
# --------------------------------------------------

output_folder = project_folder / "outputs"

output_folder.mkdir(exist_ok=True)

forecast_file = output_folder / "forecasts.csv"

forecast_df.to_csv(
    forecast_file,
    index=False
)

print("\nForecast saved to:")
print(forecast_file)