-- Business question : Which coupons have been used the most and what is their average order value?
-- Concept           : LEFT JOIN, GROUP BY, AVG, COUNT

SELECT
    cp.coupon_code,
    cp.discount_percent,
    COUNT(o.order_id)       AS times_used,
    AVG(o.total_amount)     AS avg_order_value
FROM coupons cp
LEFT JOIN orders o ON cp.coupon_id = o.coupon_id
GROUP BY cp.coupon_id, cp.coupon_code, cp.discount_percent
ORDER BY times_used DESC;