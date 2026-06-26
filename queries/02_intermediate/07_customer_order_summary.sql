-- Business question : How many orders has each customer placed and what is their total spend?
-- Concept           : JOIN, GROUP BY, aggregate on joined tables

SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(o.order_id)                  AS total_orders,
    SUM(o.total_amount)                AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC;