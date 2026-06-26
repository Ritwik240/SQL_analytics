-- Business question : How does DuckDB execute the revenue by category query internally?
-- Concept           : EXPLAIN — reading query execution plans to understand performance

EXPLAIN
SELECT
    cat.category_name,
    SUM(oi.line_total) AS total_revenue
FROM categories cat
INNER JOIN products    p  ON cat.category_id = p.category_id
INNER JOIN order_items oi ON p.product_id    = oi.product_id
INNER JOIN orders      o  ON oi.order_id     = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY cat.category_name
ORDER BY total_revenue DESC;