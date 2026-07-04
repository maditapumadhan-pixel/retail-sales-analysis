"""
eda_visualize.py
Exploratory Data Analysis on the cleaned retail sales dataset.
Produces charts saved to output/ that summarize revenue, category,
regional, and channel performance — the kind of visuals typically
handed off into a BI tool (Power BI/Tableau) for stakeholder reporting.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
df = pd.read_csv("data/retail_sales_clean.csv", parse_dates=["order_date"])

# ---------- 1. Revenue by category ----------
plt.figure(figsize=(9, 5))
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
sns.barplot(x=cat_rev.values, y=cat_rev.index, palette="Blues_r")
plt.title("Total Revenue by Category")
plt.xlabel("Revenue (INR)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("output/revenue_by_category.png", dpi=150)
plt.close()

# ---------- 2. Monthly revenue trend ----------
monthly = (
    df[df["year"] == 2024]
    .groupby(df["order_date"].dt.to_period("M"))["revenue"]
    .sum()
)
plt.figure(figsize=(10, 5))
monthly.index = monthly.index.astype(str)
plt.plot(monthly.index, monthly.values, marker="o", color="#1f3864")
plt.title("Monthly Revenue Trend (2024)")
plt.xlabel("Month")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/monthly_revenue_trend.png", dpi=150)
plt.close()

# ---------- 3. Region-wise profit margin ----------
region_margin = df.groupby("region").apply(
    lambda x: (x["profit"].sum() / x["revenue"].sum()) * 100
).sort_values(ascending=False)
plt.figure(figsize=(8, 5))
sns.barplot(x=region_margin.index, y=region_margin.values, palette="Greens_r")
plt.title("Profit Margin % by Region")
plt.ylabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig("output/profit_margin_by_region.png", dpi=150)
plt.close()

# ---------- 4. Channel comparison ----------
channel_stats = df.groupby("channel")[["revenue", "discount_pct"]].mean()
fig, ax1 = plt.subplots(figsize=(8, 5))
channel_stats["revenue"].plot(kind="bar", ax=ax1, color="#4472C4", position=1, width=0.4)
ax1.set_ylabel("Avg Revenue per Order (INR)")
plt.title("Online vs In-Store: Avg Revenue & Discount")
plt.tight_layout()
plt.savefig("output/channel_comparison.png", dpi=150)
plt.close()

# ---------- 5. Correlation heatmap (numeric fields) ----------
plt.figure(figsize=(7, 6))
num_cols = ["quantity", "unit_price", "discount_pct", "revenue", "cost", "profit", "profit_margin_pct"]
sns.heatmap(df[num_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Matrix — Key Sales Metrics")
plt.tight_layout()
plt.savefig("output/correlation_heatmap.png", dpi=150)
plt.close()

print("Saved 5 charts to output/")
print("\nKey figures:")
print("Total revenue:", round(df["revenue"].sum(), 2))
print("Total profit:", round(df["profit"].sum(), 2))
print("Overall margin %:", round(df["profit"].sum() / df["revenue"].sum() * 100, 2))
print("Best category:", cat_rev.idxmax())
print("Best region by margin:", region_margin.idxmax())
