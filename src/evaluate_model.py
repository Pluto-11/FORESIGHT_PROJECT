import pandas as pd
from pathlib import Path
import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"
model_folder = project_folder / "models"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(data_folder / "feature_engineered.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values(["SKU", "Date"]).reset_index(drop=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load(model_folder / "demand_model.pkl")

features = joblib.load(model_folder / "feature_list.pkl")

# --------------------------------------------------
# SAME TEST PERIOD
# --------------------------------------------------

test_start_date = pd.Timestamp("2025-08-09")

test_df = df[
    (df["Date"] >= test_start_date)
].dropna(subset=features).copy()

# --------------------------------------------------
# ML MODEL PREDICTIONS
# --------------------------------------------------

X_test = test_df[features]
y_test = test_df["Units_Sold"]

ml_predictions = model.predict(X_test)

ml_predictions = np.maximum(ml_predictions, 0)

# --------------------------------------------------
# SEASONAL NAIVE PREDICTIONS
# --------------------------------------------------

test_df["Naive_Prediction"] = (
    test_df.groupby("SKU")["Units_Sold"].shift(7)
)

# The shift above is not safe after filtering by date,
# so calculate it from the complete dataset.

df["Naive_Prediction"] = (
    df.groupby("SKU")["Units_Sold"].shift(7)
)

test_df = df[
    df["Date"] >= test_start_date
].dropna(subset=features + ["Naive_Prediction"]).copy()

# Recalculate ML predictions for the aligned rows
X_test = test_df[features]
y_test = test_df["Units_Sold"]

ml_predictions = model.predict(X_test)
ml_predictions = np.maximum(ml_predictions, 0)

naive_predictions = test_df["Naive_Prediction"]

# --------------------------------------------------
# METRICS FUNCTION
# --------------------------------------------------

def calculate_metrics(actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    wape = (
        np.sum(np.abs(actual - predicted))
        / np.sum(np.abs(actual))
    ) * 100

    return mae, rmse, wape


# --------------------------------------------------
# CALCULATE METRICS
# --------------------------------------------------

ml_mae, ml_rmse, ml_wape = calculate_metrics(
    y_test,
    ml_predictions
)

naive_mae, naive_rmse, naive_wape = calculate_metrics(
    y_test,
    naive_predictions
)

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("==============================")
print("MODEL COMPARISON")
print("==============================")

print("\nHistGradientBoosting")
print(f"MAE  : {ml_mae:.4f}")
print(f"RMSE : {ml_rmse:.4f}")
print(f"WAPE : {ml_wape:.2f}%")

print("\nSeasonal Naive")
print(f"MAE  : {naive_mae:.4f}")
print(f"RMSE : {naive_rmse:.4f}")
print(f"WAPE : {naive_wape:.2f}%")

# --------------------------------------------------
# IMPROVEMENT
# --------------------------------------------------

wape_improvement = (
    (naive_wape - ml_wape)
    / naive_wape
) * 100

print("\nML WAPE improvement over baseline:")
print(f"{wape_improvement:.2f}%")