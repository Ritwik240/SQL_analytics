-- Business question : What is the total revenue and number of items sold per category?
-- Concept           : Multi-level JOIN, GROUP BY

SELECT
    cat.category_name,
    COUNT(oi.order_item_id) AS total_items_sold,
    SUM(oi.line_total)      AS total_revenue
FROM categories cat
INNER JOIN products p  ON cat.category_id = p.category_id
INNER JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY cat.category_name
ORDER BY total_revenue DESC;