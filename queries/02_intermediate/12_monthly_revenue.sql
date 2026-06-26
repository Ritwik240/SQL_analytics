-- Business question : What is the total revenue per month over the last two years?
-- Concept           : Date functions, GROUP BY on extracted date parts

SELECT
    YEAR(order_date)  AS year,
    MONTH(order_date) AS month,
    COUNT(order_id)   AS total_orders,
    SUM(total_amount) AS monthly_revenue
FROM orders
WHERE order_status = 'Delivered'
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month;