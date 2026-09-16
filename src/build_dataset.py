import pandas as pd
from pathlib import Path

# Project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Load cleaned datasets
calendar = pd.read_csv(data_folder / "calendar_clean.csv")
inventory = pd.read_csv(data_folder / "inventory_clean.csv")
sales = pd.read_csv(data_folder / "sales_clean.csv")
sku_master = pd.read_csv(data_folder / "sku_master_clean.csv")

# Convert dates
calendar["date"] = pd.to_datetime(calendar["date"])
sales["Date"] = pd.to_datetime(sales["Date"])
inventory["Snapshot_Date"] = pd.to_datetime(inventory["Snapshot_Date"])
sku_master["Launch_Date"] = pd.to_datetime(sku_master["Launch_Date"])

# Rename keys for consistency
calendar = calendar.rename(columns={"date": "Date"})

# Merge sales with calendar
dataset = sales.merge(
    calendar,
    on="Date",
    how="left"
)

# Merge with SKU master
dataset = dataset.merge(
    sku_master,
    on="SKU",
    how="left"
)

# Save analysis-ready dataset
output_file = data_folder / "analysis_ready.csv"
dataset.to_csv(output_file, index=False)

print("DATASET BUILD COMPLETED")
print("Final rows:", len(dataset))
print("Final columns:", len(dataset.columns))
print("Saved to:", output_file)
print("\nColumns:")
print(dataset.columns.tolist())