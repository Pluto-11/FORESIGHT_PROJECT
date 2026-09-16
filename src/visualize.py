import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project folders
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / "data"
reports_folder = project_folder / "reports"

reports_folder.mkdir(exist_ok=True)

# Load cleaned sales data
file_path = data_folder / "sales_daily_clean.csv"
sales = pd.read_csv(file_path)

# Convert date
sales["Date"] = pd.to_datetime(sales["Date"])

# -----------------------------
# 1. MONTHLY REVENUE TREND
# -----------------------------

sales["Month"] = sales["Date"].dt.to_period("M")

monthly_revenue = sales.groupby("Month")["Revenue"].sum()

plt.figure(figsize=(10, 5))
plt.plot(monthly_revenue.index.astype(str), monthly_revenue.values, marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(reports_folder / "monthly_revenue_trend.png")
plt.show()


# -----------------------------
# 2. TOP 10 SKUs BY UNITS SOLD
# -----------------------------

top_skus = (
    sales.groupby("SKU")["Units_Sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 5))
plt.bar(top_skus.index, top_skus.values)
plt.title("Top 10 SKUs by Units Sold")
plt.xlabel("SKU")
plt.ylabel("Units Sold")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(reports_folder / "top_10_skus.png")
plt.show()


# -----------------------------
# 3. PROMOTION VS REVENUE
# -----------------------------

promotion_revenue = sales.groupby("Promotion")["Revenue"].sum()

plt.figure(figsize=(7, 5))
plt.bar(promotion_revenue.index.astype(str), promotion_revenue.values)
plt.title("Revenue by Promotion")
plt.xlabel("Promotion")
plt.ylabel("Revenue")
plt.tight_layout()

plt.savefig(reports_folder / "promotion_revenue.png")
plt.show()

print("Visualization completed successfully.")
print("Charts saved in the reports folder.")