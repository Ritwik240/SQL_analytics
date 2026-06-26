-- Business question : How many days pass between a customer's consecutive orders?
-- Concept           : Window function — LEAD() to find next order date per customer

SELECT
    customer_id,
    order_id,
    order_date,
    LEAD(order_date) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS next_order_date,
    LEAD(order_date) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) - order_date AS days_until_next_order
FROM orders
ORDER BY customer_id, order_date;