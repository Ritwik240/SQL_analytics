-- Business question : How does each product rank in terms of average rating within its category?
-- Concept           : Window functions — DENSE_RANK(), AVG() OVER (PARTITION BY ...)

SELECT
    p.product_name,
    cat.category_name,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    DENSE_RANK() OVER (
        PARTITION BY cat.category_id
        ORDER BY AVG(r.rating) DESC
    ) AS rating_rank_in_category
FROM products p
INNER JOIN reviews    r   ON p.product_id   = r.product_id
INNER JOIN categories cat ON p.category_id  = cat.category_id
GROUP BY p.product_id, p.product_name, cat.category_id, cat.category_name
ORDER BY cat.category_name, rating_rank_in_category;