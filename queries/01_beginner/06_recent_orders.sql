-- Business question : What are the 10 most recent orders placed?
-- Concept           : ORDER BY date, LIMIT

SELECT order_id, customer_id, order_date, order_status, total_amount
FROM orders
ORDER BY order_date DESC
LIMIT 10;