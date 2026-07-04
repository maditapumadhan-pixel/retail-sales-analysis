# Retail Sales Performance Analysis

End-to-end data analytics project: raw data generation → cleaning → SQL analysis → EDA & visualization.
Simulates a real retail analytics workflow across regions, product categories, and sales channels (Online vs In-Store).

## Objective
Analyze 2 years of retail transaction data to answer core business questions:
- Which regions and categories drive the most revenue and profit?
- How does profit margin vary by channel and customer segment?
- What's the monthly revenue trend, and are discounts eroding margins?

## Tech Stack
- **Python**: Pandas, NumPy, Matplotlib, Seaborn — data generation, cleaning, EDA
- **SQL (SQLite)**: aggregation, window functions, ranking queries
- **Linux**: shell-based script execution and file handling
- **Git/GitHub**: version control

## Project Structure
```
retail-sales-analysis/
├── data/
│   ├── retail_sales_raw.csv      # synthetic raw data (with intentional data issues)
│   ├── retail_sales_clean.csv    # cleaned dataset
│   └── retail_sales.db           # SQLite database for SQL analysis
├── scripts/
│   ├── generate_data.py          # generates realistic raw transaction data
│   ├── clean_data.py             # data cleaning & preprocessing
│   └── eda_visualize.py          # EDA + chart generation
├── sql/
│   └── analysis_queries.sql      # 8 business-question SQL queries
├── output/
│   └── *.png                     # generated charts
└── README.md
```

## Workflow

**1. Data Cleaning**
- Removed duplicate transaction records
- Standardized inconsistent text casing (e.g. `north` → `North`)
- Handled missing values (`customer_segment` → explicit "Unknown" bucket; `rating` → flagged rather than dropped)
- Added derived fields: `profit_margin_pct`, `month`, `year`

**2. SQL Analysis** (`sql/analysis_queries.sql`)
- Revenue & profit margin by region
- Top 5 products by revenue
- Month-over-month revenue trend
- Category ranking by profit margin (`RANK()` window function)
- Customer segment contribution to revenue
- Channel (Online vs In-Store) comparison
- Discount vs margin risk flagging
- Rolling 3-month revenue average (window function)

**3. EDA & Visualization** (`scripts/eda_visualize.py`)
- Revenue by category
- Monthly revenue trend
- Profit margin % by region
- Online vs In-Store comparison
- Correlation heatmap across key metrics

## Key Findings
- Overall profit margin across all orders: **~31%**
- **Electronics** is the top revenue-generating category
- **South** region delivers the strongest profit margin despite not having the highest raw revenue
- Orders with discounts ≥15% frequently fall below a 20% margin threshold — flagged for pricing review

## How to Run
```bash
pip install pandas numpy matplotlib seaborn
python scripts/generate_data.py
python scripts/clean_data.py
python scripts/eda_visualize.py
```

To explore the SQL layer:
```bash
sqlite3 data/retail_sales.db
.read sql/analysis_queries.sql
```

## Author
Madhan Simha M — [GitHub]([https://github.com/madhansimha](https://github.com/maditapumadhan-pixel)) · [LinkedIn](www.linkedin.com/in/maditapu-madhan-b62a0841b)
