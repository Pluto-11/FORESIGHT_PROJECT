import pandas as pd
from pathlib import Path

data_folder = Path("data")

files = [
    "calendar (1).csv",
    "inventory_snapshots (1).csv",
    "sales_daily (1).csv",
    "sku_master (1).csv"
]

for file in files:
    path = data_folder / file
    df = pd.read_csv(path)

    print("\n" + "=" * 50)
    print(file)
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("=" * 50)
    print("Missing values:")
print(df.isnull().sum())

print("Duplicate rows:", df.duplicated().sum())
# Basic sales data summary

sales_path = data_folder / "sales_daily (1).csv"
sales_df = pd.read_csv(sales_path)

print("\n--- SALES DATA SUMMARY ---")
print("Total records:", len(sales_df))
print("Total units sold:", sales_df["Units_Sold"].sum())
print("Total revenue:", sales_df["Revenue"].sum())
print("Average units sold:", sales_df["Units_Sold"].mean())
print("Average revenue:", sales_df["Revenue"].mean())
print("Number of SKUs:", sales_df["SKU"].nunique())
# Check date range

sales_df["Date"] = pd.to_datetime(sales_df["Date"])

print("\n--- DATE INFORMATION ---")
print("Start date:", sales_df["Date"].min())
print("End date:", sales_df["Date"].max())
print("Number of unique dates:", sales_df["Date"].nunique())
# SKU-wise sales summary

sku_sales = (
    sales_df.groupby("SKU")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- TOP 10 SKUs BY UNITS SOLD ---")
print(sku_sales.head(10))
# Monthly revenue trend

sales_df["Month"] = sales_df["Date"].dt.to_period("M")

monthly_revenue = sales_df.groupby("Month")["Revenue"].sum()

print("\n--- MONTHLY REVENUE ---")
print(monthly_revenue)