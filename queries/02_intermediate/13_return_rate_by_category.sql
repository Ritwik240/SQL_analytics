-- Business question : Which product categories have the highest return rate?
-- Concept           : CTE, JOIN, division for percentage

WITH delivered AS (
    SELECT oi.order_item_id, p.category_id
    FROM order_items oi
    INNER JOIN products p ON oi.product_id = p.product_id
    INNER JOIN orders   o ON oi.order_id   = o.order_id
    WHERE o.order_status = 'Delivered'
),
returned AS (
    SELECT oi.order_item_id, p.category_id
    FROM returns r
    INNER JOIN order_items oi ON r.order_item_id = oi.order_item_id
    INNER JOIN products    p  ON oi.product_id   = p.product_id
)
SELECT
    cat.category_name,
    COUNT(DISTINCT d.order_item_id)  AS total_delivered,
    COUNT(DISTINCT rt.order_item_id) AS total_returned,
    ROUND(
        COUNT(DISTINCT rt.order_item_id) * 100.0 /
        NULLIF(COUNT(DISTINCT d.order_item_id), 0), 2
    ) AS return_rate_percent
FROM categories cat
LEFT JOIN delivered d  ON cat.category_id = d.category_id
LEFT JOIN returned  rt ON cat.category_id = rt.category_id
GROUP BY cat.category_name
ORDER BY return_rate_percent DESC;