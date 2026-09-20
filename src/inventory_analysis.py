import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent

data_folder = project_folder / "data"
output_folder = project_folder / "outputs"

# --------------------------------------------------
# LOAD INVENTORY
# --------------------------------------------------

inventory = pd.read_csv(
    data_folder / "inventory_clean.csv"
)

inventory["Snapshot_Date"] = pd.to_datetime(
    inventory["Snapshot_Date"]
)

# --------------------------------------------------
# LOAD FORECAST
# --------------------------------------------------

forecast = pd.read_csv(
    output_folder / "forecasts.csv"
)

forecast["Date"] = pd.to_datetime(
    forecast["Date"]
)

# --------------------------------------------------
# BASIC INFORMATION
# --------------------------------------------------

print("INVENTORY ANALYSIS INITIALIZED")

print("\nInventory rows:")
print(len(inventory))

print("\nInventory columns:")
print(inventory.columns.tolist())

print("\nLatest inventory snapshot:")
print(inventory["Snapshot_Date"].max())

print("\nForecast rows:")
print(len(forecast))

print("\nForecast period:")
print(
    forecast["Date"].min(),
    "to",
    forecast["Date"].max()
)



# --------------------------------------------------
# USE LATEST INVENTORY SNAPSHOT
# --------------------------------------------------

latest_inventory_date = inventory["Snapshot_Date"].max()

current_inventory = inventory[
    inventory["Snapshot_Date"] == latest_inventory_date
].copy()

print("\nLATEST INVENTORY SNAPSHOT SELECTED")

print(
    "Snapshot date:",
    latest_inventory_date
)

print(
    "Inventory rows:",
    len(current_inventory)
)

print(
    "Unique SKUs:",
    current_inventory["SKU"].nunique()
)

print("\nInventory preview:")
print(
    current_inventory.head()
)


# --------------------------------------------------
# CHECK SKU OVERLAP
# --------------------------------------------------

forecast_skus = set(
    forecast["SKU"].unique()
)

inventory_skus = set(
    current_inventory["SKU"].unique()
)

matched_skus = forecast_skus.intersection(
    inventory_skus
)

missing_inventory = forecast_skus - inventory_skus

extra_inventory = inventory_skus - forecast_skus

print("\nSKU MATCHING")

print("Forecast SKUs:", len(forecast_skus))
print("Inventory SKUs:", len(inventory_skus))
print("Matched SKUs:", len(matched_skus))
print("Forecast SKUs without inventory:", len(missing_inventory))
print("Inventory SKUs without forecast:", len(extra_inventory))


# --------------------------------------------------
# AGGREGATE 7-DAY FORECAST
# --------------------------------------------------

forecast_summary = (
    forecast
    .groupby("SKU")["Predicted_Demand"]
    .sum()
    .reset_index()
)

forecast_summary = forecast_summary.rename(
    columns={
        "Predicted_Demand": "Forecast_7_Day_Demand"
    }
)

# --------------------------------------------------
# MERGE INVENTORY WITH FORECAST
# --------------------------------------------------

inventory_analysis = current_inventory.merge(
    forecast_summary,
    on="SKU",
    how="inner"
)

# --------------------------------------------------
# CALCULATE INVENTORY COVERAGE
# --------------------------------------------------

inventory_analysis["Average_Daily_Demand"] = (
    inventory_analysis["Forecast_7_Day_Demand"] / 7
)

inventory_analysis["Days_of_Cover"] = (
    inventory_analysis["Current_Stock"]
    / inventory_analysis["Average_Daily_Demand"]
)

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\nINVENTORY COVERAGE CALCULATED")

print(
    "Analysis rows:",
    len(inventory_analysis)
)

print("\nCoverage preview:")

print(
    inventory_analysis[
        [
            "SKU",
            "Current_Stock",
            "Forecast_7_Day_Demand",
            "Average_Daily_Demand",
            "Days_of_Cover"
        ]
    ].head(10)
)



# --------------------------------------------------
# PROJECTED STOCK AFTER 7 DAYS
# --------------------------------------------------

inventory_analysis["Projected_Stock_7_Day"] = (
    inventory_analysis["Current_Stock"]
    + inventory_analysis["On_Order"]
    - inventory_analysis["Forecast_7_Day_Demand"]
)

# --------------------------------------------------
# STOCK VS SAFETY STOCK
# --------------------------------------------------

inventory_analysis["Stock_Buffer_vs_Safety"] = (
    inventory_analysis["Projected_Stock_7_Day"]
    - inventory_analysis["Safety_Stock"]
)

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\nPROJECTED INVENTORY CALCULATED")

print(
    inventory_analysis[
        [
            "SKU",
            "Current_Stock",
            "On_Order",
            "Forecast_7_Day_Demand",
            "Projected_Stock_7_Day",
            "Safety_Stock",
            "Stock_Buffer_vs_Safety"
        ]
    ].head(10)
)


# --------------------------------------------------
# CALCULATE LEAD-TIME DEMAND
# --------------------------------------------------

inventory_analysis["Lead_Time_Demand"] = (
    inventory_analysis["Average_Daily_Demand"]
    * inventory_analysis["Lead_Time_Days"]
)

# --------------------------------------------------
# CALCULATE STOCK POSITION
# --------------------------------------------------

inventory_analysis["Stock_Position"] = (
    inventory_analysis["Current_Stock"]
    + inventory_analysis["On_Order"]
)

inventory_analysis["Stock_After_Lead_Time"] = (
    inventory_analysis["Stock_Position"]
    - inventory_analysis["Lead_Time_Demand"]
)

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\nLEAD-TIME DEMAND CALCULATED")

print(
    inventory_analysis[
        [
            "SKU",
            "Current_Stock",
            "On_Order",
            "Lead_Time_Days",
            "Average_Daily_Demand",
            "Lead_Time_Demand",
            "Stock_Position",
            "Stock_After_Lead_Time"
        ]
    ].head(10)
)



# --------------------------------------------------
# INVENTORY RISK FLAG
# --------------------------------------------------

inventory_analysis["Lead_Time_Risk"] = (
    inventory_analysis["Stock_After_Lead_Time"] < 0
).astype(int)

print("\nLEAD-TIME RISK IDENTIFIED")

print(
    inventory_analysis[
        [
            "SKU",
            "Lead_Time_Days",
            "Lead_Time_Demand",
            "Stock_Position",
            "Stock_After_Lead_Time",
            "Lead_Time_Risk"
        ]
    ].head(10)
)

print("\nSKUs with lead-time risk:")
print(
    inventory_analysis["Lead_Time_Risk"].sum()
)

# --------------------------------------------------
# REORDER POINT RISK
# --------------------------------------------------

inventory_analysis["Below_Reorder_Point"] = (
    inventory_analysis["Stock_Position"]
    < inventory_analysis["Reorder_Point"]
).astype(int)

print("\nREORDER POINT RISK IDENTIFIED")

print(
    inventory_analysis[
        [
            "SKU",
            "Stock_Position",
            "Reorder_Point",
            "Below_Reorder_Point"
        ]
    ].head(10)
)

print("\nSKUs below reorder point:")
print(
    inventory_analysis["Below_Reorder_Point"].sum()
)



# --------------------------------------------------
# COMBINE RISK SIGNALS
# --------------------------------------------------

inventory_analysis["Risk_Signal_Count"] = (
    inventory_analysis["Lead_Time_Risk"]
    + inventory_analysis["Below_Reorder_Point"]
)

print("\nRISK SIGNAL SUMMARY")

print(
    inventory_analysis[
        [
            "SKU",
            "Lead_Time_Risk",
            "Below_Reorder_Point",
            "Risk_Signal_Count"
        ]
    ].sort_values(
        "Risk_Signal_Count",
        ascending=False
    ).head(10)
)

print("\nRisk signal counts:")
print(
    inventory_analysis["Risk_Signal_Count"]
    .value_counts()
    .sort_index()
)


# --------------------------------------------------
# RISK CATEGORY
# --------------------------------------------------

def classify_risk(row):

    if row["Lead_Time_Risk"] == 1:
        return "High Risk"

    elif row["Below_Reorder_Point"] == 1:
        return "Medium Risk"

    else:
        return "Healthy"


inventory_analysis["Risk_Category"] = (
    inventory_analysis.apply(
        classify_risk,
        axis=1
    )
)

print("\nRISK CATEGORIES")

print(
    inventory_analysis[
        [
            "SKU",
            "Lead_Time_Risk",
            "Below_Reorder_Point",
            "Risk_Category"
        ]
    ].sort_values(
        "Risk_Category"
    )
)

print("\nRisk category counts:")

print(
    inventory_analysis["Risk_Category"]
    .value_counts()
)




# --------------------------------------------------
# SAVE INVENTORY ANALYSIS
# --------------------------------------------------

output_file = output_folder / "inventory_analysis.csv"

inventory_analysis.to_csv(
    output_file,
    index=False
)

print("\nINVENTORY ANALYSIS SAVED")
print("Saved to:")
print(output_file)
print("Rows:", len(inventory_analysis))
print("Columns:", len(inventory_analysis.columns))