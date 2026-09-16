import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

sales_file = data_folder / "sales_daily (1).csv"
sales = pd.read_csv(sales_file)

print("Original rows:", len(sales))

# Remove duplicate records
sales = sales.drop_duplicates()

# Convert date column
sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")

# Remove rows with missing important values
sales = sales.dropna(subset=["Date", "SKU", "Units_Sold", "Revenue"])

print("Rows after cleaning:", len(sales))
print("Missing values:")
print(sales.isnull().sum())

# Save cleaned data separately
output_file = data_folder / "sales_daily_clean.csv"
sales.to_csv(output_file, index=False)

print("\nCleaned file saved successfully:")
print(output_file)