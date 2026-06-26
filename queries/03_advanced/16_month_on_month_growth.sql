-- Business question : What is the month-on-month revenue growth rate?
-- Concept           : Window function — LAG() to compare current vs previous period

WITH monthly AS (
    SELECT
        YEAR(order_date)  AS year,
        MONTH(order_date) AS month,
        SUM(total_amount) AS revenue
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT
    year,
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY year, month) AS prev_month_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY year, month)) * 100.0 /
        NULLIF(LAG(revenue) OVER (ORDER BY year, month), 0), 2
    ) AS growth_percent
FROM monthly
ORDER BY year, month;