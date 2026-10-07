import pandas as pd
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"
model_folder = project_folder / "models"

model_folder.mkdir(exist_ok=True)

# --------------------------------------------------
# LOAD FEATURE-ENGINEERED DATA
# --------------------------------------------------

file_path = data_folder / "feature_engineered.csv"

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])

# Sort chronologically
df = df.sort_values(["SKU", "Date"]).reset_index(drop=True)

# --------------------------------------------------
# FEATURES
# --------------------------------------------------

features = [
    "Lag_1",
    "Lag_7",
    "Rolling_7",
    "Month",
    "Day_of_Week",
    "Is_Weekend",
    "Promotion",
]

target = "Units_Sold"

# --------------------------------------------------
# REMOVE ROWS WITH MISSING FEATURES
# --------------------------------------------------

model_df = df.dropna(subset=features + [target]).copy()

print("Original rows:", len(df))
print("Rows used for training/evaluation:", len(model_df))

# --------------------------------------------------
# TIME-BASED TRAIN / TEST SPLIT
# --------------------------------------------------

# Use the last 20% of dates as test data.
unique_dates = sorted(model_df["Date"].unique())

split_index = int(len(unique_dates) * 0.8)

train_end_date = unique_dates[split_index - 1]

train_df = model_df[model_df["Date"] <= train_end_date]
test_df = model_df[model_df["Date"] > train_end_date]

print("\nTrain period:")
print(train_df["Date"].min(), "to", train_df["Date"].max())

print("\nTest period:")
print(test_df["Date"].min(), "to", test_df["Date"].max())

print("\nTrain rows:", len(train_df))
print("Test rows:", len(test_df))

# --------------------------------------------------
# PREPARE X AND Y
# --------------------------------------------------

X_train = train_df[features]
y_train = train_df[target]

X_test = test_df[features]
y_test = test_df[target]

# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

model = HistGradientBoostingRegressor(
    max_iter=300,
    learning_rate=0.05,
    max_leaf_nodes=31,
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------------------------------
# PREDICTIONS
# --------------------------------------------------

predictions = model.predict(X_test)

# Demand cannot be negative
predictions = np.maximum(predictions, 0)

# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

# WAPE
wape = (
    np.sum(np.abs(y_test - predictions))
    / np.sum(np.abs(y_test))
) * 100

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"WAPE : {wape:.2f}%")

# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

model_path = model_folder / "demand_model.pkl"

joblib.dump(model, model_path)

# Save feature list
feature_path = model_folder / "feature_list.pkl"

joblib.dump(features, feature_path)

print("\nModel saved to:")
print(model_path)

print("\nFeature list saved to:")
print(feature_path)

print("Train rows:", len(train_df))
print("Test rows:", len(test_df))