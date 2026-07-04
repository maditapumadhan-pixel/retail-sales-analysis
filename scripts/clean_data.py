"""
clean_data.py
Cleans the raw retail sales dataset:
 - removes duplicate orders
 - standardizes inconsistent text casing
 - handles missing values in customer_segment and rating
 - adds derived columns (profit_margin_pct, month, year) used in later analysis
"""

import pandas as pd

df = pd.read_csv("data/retail_sales_raw.csv")
print("Raw shape:", df.shape)
print("Duplicate rows:", df.duplicated().sum())
print("Missing values per column:\n", df.isnull().sum())

# 1. Drop exact duplicate orders
df = df.drop_duplicates()

# 2. Standardize text casing (region had inconsistent lowercase entries)
df["region"] = df["region"].str.strip().str.title()
df["category"] = df["category"].str.strip()
df["channel"] = df["channel"].str.strip()

# 3. Handle missing customer_segment -> explicit "Unknown" bucket (preserves row instead of dropping)
df["customer_segment"] = df["customer_segment"].fillna("Unknown")

# 4. Handle missing rating -> keep NaN (no rating submitted) but add a flag column
df["rating_submitted"] = df["rating"].notna()

# 5. Derived columns used across the analysis
df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month_name()
df["profit_margin_pct"] = (df["profit"] / df["revenue"] * 100).round(2)

df.to_csv("data/retail_sales_clean.csv", index=False)

print("\nCleaned shape:", df.shape)
print("Remaining duplicates:", df.duplicated().sum())
print("Remaining nulls (excluding rating):\n", df.drop(columns=["rating"]).isnull().sum())
