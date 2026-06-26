-- Business question : Which orders have a total value above 10,000?
-- Concept           : WHERE with numeric filter, ORDER BY

SELECT order_id, customer_id, order_date, total_amount
FROM orders
WHERE total_amount > 10000
ORDER BY total_amount DESC;