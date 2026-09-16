import pandas as pd
import numpy as np
from pathlib import Path

# Project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"

# Load cleaned sales data
sales = pd.read_csv(data_folder / "sales_clean.csv")

# Fixed random seed so the same values can be reproduced
np.random.seed(42)

# Add Channel column
sales["Channel"] = np.random.choice(
    ["Online", "Offline"],
    size=len(sales)
)

# Add Region column
sales["Region"] = np.random.choice(
    ["North", "South", "East", "West"],
    size=len(sales)
)

# Save updated sales dataset
output_file = data_folder / "sales_updated.csv"
sales.to_csv(output_file, index=False)

print("SALES DATASET UPDATED")
print("Rows:", len(sales))
print("Columns:", len(sales.columns))
print("Added columns: Channel, Region")
print("Saved to:", output_file)