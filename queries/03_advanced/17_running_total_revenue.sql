-- Business question : What is the cumulative revenue over time?
-- Concept           : Window function — SUM() OVER (ORDER BY ...) for running total

WITH daily AS (
    SELECT
        order_date,
        SUM(total_amount) AS daily_revenue
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY order_date
)
SELECT
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY order_date) AS cumulative_revenue
FROM daily
ORDER BY order_date;