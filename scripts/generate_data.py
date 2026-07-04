"""
generate_data.py
Generates a realistic synthetic retail sales dataset (2 years, multi-region,
multi-category) with intentional data quality issues (duplicates, missing
values, inconsistent casing) to mirror real-world raw data for the
cleaning/EDA stage of the project.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

N_ROWS = 6000
REGIONS = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Grocery", "Beauty"]
PRODUCTS = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch", "Bluetooth Speaker"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress"],
    "Home & Kitchen": ["Mixer Grinder", "Cookware Set", "Vacuum Cleaner", "Air Fryer"],
    "Sports": ["Yoga Mat", "Dumbbells", "Cricket Bat", "Running Shoes"],
    "Grocery": ["Rice 5kg", "Cooking Oil", "Snacks Combo", "Tea Pack"],
    "Beauty": ["Face Wash", "Shampoo", "Lipstick", "Sunscreen"],
}
CHANNELS = ["Online", "In-Store"]
SEGMENTS = ["New Customer", "Returning Customer", "Premium Member"]

BASE_PRICE_RANGE = {
    "Electronics": (1200, 45000),
    "Clothing": (300, 3500),
    "Home & Kitchen": (800, 12000),
    "Sports": (400, 6000),
    "Grocery": (80, 900),
    "Beauty": (150, 1800),
}

dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")

rows = []
order_id = 100000
for _ in range(N_ROWS):
    date = np.random.choice(dates)
    region = np.random.choice(REGIONS, p=[0.28, 0.24, 0.26, 0.22])
    category = np.random.choice(CATEGORIES)
    product = np.random.choice(PRODUCTS[category])
    channel = np.random.choice(CHANNELS, p=[0.62, 0.38])
    segment = np.random.choice(SEGMENTS, p=[0.35, 0.45, 0.20])
    qty = np.random.randint(1, 6)

    low, high = BASE_PRICE_RANGE[category]
    unit_price = round(np.random.uniform(low, high), 2)
    discount_pct = np.random.choice([0, 5, 10, 15, 20], p=[0.4, 0.25, 0.2, 0.1, 0.05])
    revenue = round(unit_price * qty * (1 - discount_pct / 100), 2)
    cost = round(unit_price * qty * np.random.uniform(0.55, 0.75), 2)
    profit = round(revenue - cost, 2)
    rating = np.random.choice([np.nan, 1, 2, 3, 4, 5], p=[0.3, 0.03, 0.05, 0.12, 0.25, 0.25])

    order_id += 1
    rows.append([
        order_id, pd.Timestamp(date).strftime("%Y-%m-%d"), region, category, product,
        channel, segment, qty, unit_price, discount_pct, revenue, cost, profit, rating,
    ])

df = pd.DataFrame(rows, columns=[
    "order_id", "order_date", "region", "category", "product",
    "channel", "customer_segment", "quantity", "unit_price",
    "discount_pct", "revenue", "cost", "profit", "rating",
])

# --- Inject realistic messiness (so cleaning step has genuine work to do) ---
dup_rows = df.sample(50, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)

null_idx = df.sample(120, random_state=2).index
df.loc[null_idx, "customer_segment"] = np.nan

lower_idx = df.sample(80, random_state=3).index
df.loc[lower_idx, "region"] = df.loc[lower_idx, "region"].str.lower()

df.to_csv("data/retail_sales_raw.csv", index=False)
print(f"Generated {df.shape[0]} rows, {df.shape[1]} columns -> data/retail_sales_raw.csv")
