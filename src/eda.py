import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

file_path = data_folder / "sales_daily_clean.csv"
sales = pd.read_csv(file_path)

sales["Date"] = pd.to_datetime(sales["Date"])

print("\n--- BASIC STATISTICS ---")
print(sales[["Units_Sold", "Revenue", "Price"]].describe())

print("\n--- TOP 10 SKUs BY UNITS SOLD ---")
top_skus = (
    sales.groupby("SKU")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_skus)

print("\n--- REVENUE BY PROMOTION ---")
promotion_revenue = sales.groupby("Promotion")["Revenue"].sum()
print(promotion_revenue)

print("\nEDA analysis completed successfully.")