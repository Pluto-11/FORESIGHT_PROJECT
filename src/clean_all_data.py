import pandas as pd
from pathlib import Path

# Project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Load datasets
calendar = pd.read_csv(data_folder / "calendar.csv")
inventory = pd.read_csv(data_folder / "inventory_snapshots.csv")
sales = pd.read_csv(data_folder / "sales_daily.csv")
sku_master = pd.read_csv(data_folder / "sku_master.csv")

print("DATASETS LOADED SUCCESSFULLY")

# -------------------------
# CLEAN CALENDAR
# -------------------------
calendar["date"] = pd.to_datetime(calendar["date"], errors="coerce")
calendar = calendar.drop_duplicates()

# -------------------------
# CLEAN INVENTORY
# -------------------------
inventory["Snapshot_Date"] = pd.to_datetime(
    inventory["Snapshot_Date"], errors="coerce"
)
inventory = inventory.drop_duplicates()

# -------------------------
# CLEAN SALES
# -------------------------
sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
sales = sales.drop_duplicates()

# Remove rows with essential missing values
sales = sales.dropna(
    subset=["Date", "SKU", "Units_Sold", "Revenue"]
)

# -------------------------
# CLEAN SKU MASTER
# -------------------------
sku_master["Launch_Date"] = pd.to_datetime(
    sku_master["Launch_Date"], errors="coerce"
)
sku_master = sku_master.drop_duplicates()

# -------------------------
# SAVE CLEAN FILES
# -------------------------
calendar.to_csv(data_folder / "calendar_clean.csv", index=False)
inventory.to_csv(data_folder / "inventory_clean.csv", index=False)
sales.to_csv(data_folder / "sales_clean.csv", index=False)
sku_master.to_csv(data_folder / "sku_master_clean.csv", index=False)

print("CLEANING COMPLETED")
print("Calendar rows:", len(calendar))
print("Inventory rows:", len(inventory))
print("Sales rows:", len(sales))
print("SKU Master rows:", len(sku_master))
print("Clean files saved in data folder.")