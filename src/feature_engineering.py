import pandas as pd

# Load analysis-ready dataset
df = pd.read_csv("data/analysis_ready.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Sort data by SKU and Date
df = df.sort_values(["SKU", "Date"])

# Calendar features
df["Month"] = df["Date"].dt.month
df["Day_of_Week"] = df["Date"].dt.dayofweek
df["Is_Weekend"] = (df["Day_of_Week"] >= 5).astype(int)

df["Promo_Lag_7"] = df.groupby("SKU")["Promotion"].shift(7)
# Lag features
df["Lag_1"] = df.groupby("SKU")["Units_Sold"].shift(1)
df["Lag_7"] = df.groupby("SKU")["Units_Sold"].shift(7)

# Rolling average
df["Rolling_7"] = (
    df.groupby("SKU")["Units_Sold"]
    .transform(lambda x: x.shift(1).rolling(7).mean())
)

# Save feature-engineered dataset
df.to_csv("data/feature_engineered.csv", index=False)

print("FEATURE ENGINEERING COMPLETED")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Saved to: data/feature_engineered.csv")
print("\nNew Features:")
print(["Month", "Day_of_Week", "Lag_1", "Lag_7", "Rolling_7"])