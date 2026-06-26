-- Business question : How many orders exist under each status?
-- Concept           : GROUP BY, COUNT

SELECT order_status, COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;