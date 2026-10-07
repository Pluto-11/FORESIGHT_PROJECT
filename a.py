from train_model import train_df, test_df

import pandas as pd

df = pd.read_csv("data/feature_engineered.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(["SKU", "Date"]).reset_index(drop=True)

features = [
    "Lag_1",
    "Lag_7",
    "Rolling_7",
    "Month",
    "Day_of_Week",
    "Is_Weekend",
    "Promotion",
]

model_df = df.dropna(subset=features + ["Units_Sold"]).copy()

unique_dates = sorted(model_df["Date"].unique())
split_index = int(len(unique_dates) * 0.8)
train_end_date = unique_dates[split_index - 1]

train_df = model_df[model_df["Date"] <= train_end_date]
test_df = model_df[model_df["Date"] > train_end_date]

print("Total:", len(model_df))
print("Train:", len(train_df))
print("Test:", len(test_df))
print("Train dates:", train_df["Date"].min(), "to", train_df["Date"].max())
print("Test dates:", test_df["Date"].min(), "to", test_df["Date"].max())