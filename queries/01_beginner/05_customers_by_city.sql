-- Business question : How many customers are there in each city?
-- Concept           : GROUP BY, COUNT, HAVING

SELECT city, COUNT(*) AS total_customers
FROM customers
GROUP BY city
HAVING COUNT(*) > 10
ORDER BY total_customers DESC;