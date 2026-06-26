-- Business question : Which suppliers provide the most profitable products on average?
-- Concept           : CASE WHEN, derived columns, GROUP BY

SELECT
    s.supplier_name,
    COUNT(p.product_id)                              AS total_products,
    ROUND(AVG(p.price - p.cost_price), 2)            AS avg_profit_per_unit,
    ROUND(AVG((p.price - p.cost_price) / p.price * 100), 2) AS avg_margin_percent,
    CASE
        WHEN AVG((p.price - p.cost_price) / p.price * 100) >= 50 THEN 'High'
        WHEN AVG((p.price - p.cost_price) / p.price * 100) >= 30 THEN 'Medium'
        ELSE 'Low'
    END AS margin_category
FROM suppliers s
INNER JOIN products p ON s.supplier_id = p.supplier_id
GROUP BY s.supplier_id, s.supplier_name
ORDER BY avg_margin_percent DESC;