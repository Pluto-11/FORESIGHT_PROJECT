# FORESIGHT — Data Quality Report

## 1. Project

Project: FORESIGHT — Demand & Inventory Intelligence

Purpose:
The purpose of this report is to document the data quality checks,
cleaning steps, and preparation of the datasets used for analysis.

---

## 2. Source Datasets

The project uses four main datasets:

1. Sales Daily
2. SKU Master
3. Calendar
4. Inventory Snapshots

The original raw CSV files were kept unchanged.
Cleaned versions were created separately.

---

## 3. Data Quality Summary

| Dataset | Rows | Duplicate Rows | Missing Values |
|---|---:|---:|---:|
| Sales Daily | 36,550 | 0 | 0 |
| SKU Master | 50 | 0 | 0 |
| Calendar | 731 | 0 | 0 |
| Inventory Snapshots | 4,800 | 0 | 0 |

---

## 4. Sales Daily

### Structure

Rows: 36,550

Main columns:

- Date
- SKU
- Units_Sold
- Revenue
- Price
- Promotion

### Quality Checks

- Missing values were checked.
- Duplicate rows were checked.
- Date values were converted to datetime format.
- Rows missing essential fields were removed.
- No duplicate rows were found.
- Final cleaned sales dataset contains 36,550 rows.

### Cleaning Decision

The raw sales data was not modified directly.
A separate cleaned file was created:

`sales_clean.csv`

---

## 5. SKU Master

### Structure

Rows: 50

Important fields include:

- SKU
- Product_Name
- Category
- Subcategory
- Launch_Date
- Cost_Price
- Selling_Price
- Gross_Margin_Per_Unit

### Quality Checks

- Missing values were checked.
- Duplicate rows were checked.
- SKU values were checked for uniqueness.
- No duplicate rows were found.
- No missing values were found.

### Cleaning Decision

The cleaned SKU master was saved separately as:

`sku_master_clean.csv`

---

## 6. Calendar

### Structure

Rows: 731

The calendar dataset covers the daily project period.

### Quality Checks

- Date values were checked.
- Missing values were checked.
- Duplicate rows were checked.
- Date-related fields were prepared for analysis.

### Cleaning Decision

The cleaned calendar data was saved separately as:

`calendar_clean.csv`

---

## 7. Inventory Snapshots

### Structure

Rows: 4,800

Important fields include:

- Snapshot_Date
- SKU
- Current_Stock
- On_Order
- Lead_Time_Days
- Safety_Stock
- Reorder_Point
- Inventory_Value

### Quality Checks

- Missing values were checked.
- Duplicate rows were checked.
- SKU uniqueness was checked.
- There are 200 unique SKUs.
- There are 24 unique inventory snapshot dates.
- No duplicate rows were found.
- No missing values were found.

### Cleaning Decision

The cleaned inventory data was saved separately as:

`inventory_clean.csv`

Inventory snapshots are kept at their snapshot level because
inventory data has a different grain from daily sales data.

---

## 8. Analysis-Ready Dataset

The cleaned sales, calendar, and SKU master data were combined
to create an analysis-ready dataset.

Output file:

`analysis_ready.csv`

Final rows:

36,550

Final columns:

23

The analysis-ready dataset contains sales information together with
calendar features and SKU/product information.

Inventory snapshots are maintained separately because they are
periodic snapshots rather than daily sales records.

---

## 9. Reproducibility

The data preparation process is implemented using Python and pandas.

The main scripts are stored in:

`src/`

Important scripts include:

- `clean_data.py`
- `clean_all_data.py`
- `build_dataset.py`
- `inspect_data.py`

The raw data files remain unchanged, while cleaned and processed
outputs are stored separately in the `data` folder.

---

## 10. Conclusion

The four project datasets were inspected and cleaned.

The main quality checks showed:

- No duplicate rows were identified.
- No missing values were identified in the cleaned datasets.
- Dates and relevant data types were prepared for analysis.
- Cleaned datasets were saved separately from the raw files.
- An analysis-ready dataset was created with 36,550 rows and 23 columns.

The dataset is now ready for the next stage of the project:
Exploratory Data Analysis (EDA) and baseline analysis.