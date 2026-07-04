-- ============================================================
-- Retail Sales Analysis — SQL Queries
-- Table: sales (loaded from data/retail_sales_clean.csv)
-- ============================================================

-- 1. Total revenue, profit, and margin by region
SELECT
    region,
    ROUND(SUM(revenue), 2)  AS total_revenue,
    ROUND(SUM(profit), 2)   AS total_profit,
    ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS profit_margin_pct
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;

-- 2. Top 5 best-selling products by revenue
SELECT
    product,
    category,
    SUM(quantity)          AS units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY product, category
ORDER BY total_revenue DESC
LIMIT 5;

-- 3. Month-over-month revenue trend (2024)
SELECT
    month,
    ROUND(SUM(revenue), 2) AS monthly_revenue
FROM sales
WHERE year = 2024
GROUP BY month
ORDER BY MIN(order_date);

-- 4. Category performance ranked by profit margin (window function)
SELECT
    category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS margin_pct,
    RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM sales
GROUP BY category;

-- 5. Customer segment contribution to revenue (excluding Unknown)
SELECT
    customer_segment,
    COUNT(*)                AS num_orders,
    ROUND(SUM(revenue), 2)  AS total_revenue,
    ROUND(AVG(revenue), 2)  AS avg_order_value
FROM sales
WHERE customer_segment != 'Unknown'
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- 6. Online vs In-Store channel comparison
SELECT
    channel,
    COUNT(*)                              AS num_orders,
    ROUND(SUM(revenue), 2)                AS total_revenue,
    ROUND(AVG(discount_pct), 2)           AS avg_discount_pct,
    ROUND(AVG(profit_margin_pct), 2)      AS avg_margin_pct
FROM sales
GROUP BY channel;

-- 7. Orders with high discount but low margin — flag for pricing review
SELECT
    order_id, product, region, discount_pct, profit_margin_pct
FROM sales
WHERE discount_pct >= 15 AND profit_margin_pct < 20
ORDER BY profit_margin_pct ASC
LIMIT 20;

-- 8. Rolling 3-month revenue trend using window function
SELECT
    month,
    monthly_revenue,
    ROUND(AVG(monthly_revenue) OVER (
        ORDER BY month_order
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_3mo_avg
FROM (
    SELECT
        month,
        MIN(order_date) AS month_order,
        SUM(revenue) AS monthly_revenue
    FROM sales
    WHERE year = 2024
    GROUP BY month
);
