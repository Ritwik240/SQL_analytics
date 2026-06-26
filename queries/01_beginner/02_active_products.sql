-- Business question : Which products are currently active and what are their prices?
-- Concept           : WHERE filter, ORDER BY

SELECT product_name, price, stock_quantity
FROM products
WHERE is_active = TRUE
ORDER BY price DESC;