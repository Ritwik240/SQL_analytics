-- Business question : Who are the top customers by total spend, ranked within each city?
-- Concept           : Window function — RANK() OVER (PARTITION BY ... ORDER BY ...)

SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    SUM(o.total_amount) AS total_spent,
    RANK() OVER (
        PARTITION BY c.city
        ORDER BY SUM(o.total_amount) DESC
    ) AS city_rank
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city
ORDER BY c.city, city_rank;