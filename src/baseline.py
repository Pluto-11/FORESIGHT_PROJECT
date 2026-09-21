import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

file_path = data_folder / "feature_engineered.csv"

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values(["SKU", "Date"]).reset_index(drop=True)

# --------------------------------------------------
# CREATE SEASONAL NAIVE PREDICTION
# --------------------------------------------------

# Use demand from 7 days earlier
df["Naive_Prediction"] = (
    df.groupby("SKU")["Units_Sold"].shift(7)
)

# Remove rows where previous week's demand is unavailable
evaluation_df = df.dropna(
    subset=["Naive_Prediction", "Units_Sold"]
).copy()

# --------------------------------------------------
# SAME TEST PERIOD AS ML MODEL
# --------------------------------------------------

test_start_date = pd.Timestamp("2025-08-09")

test_df = evaluation_df[
    evaluation_df["Date"] >= test_start_date
].copy()

# --------------------------------------------------
# ACTUAL VS PREDICTED
# --------------------------------------------------

y_true = test_df["Units_Sold"]

y_pred = test_df["Naive_Prediction"]

# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

mae = mean_absolute_error(y_true, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_true, y_pred)
)

wape = (
    np.sum(np.abs(y_true - y_pred))
    / np.sum(np.abs(y_true))
) * 100

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("==============================")
print("SEASONAL NAIVE BASELINE")
print("==============================")

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"WAPE : {wape:.2f}%")

print("\nEvaluation period:")
print(test_df["Date"].min(), "to", test_df["Date"].max())

print("\nEvaluation rows:", len(test_df))