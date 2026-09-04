-- CommerceIQ - Reconciliation Queries

-- Core Metric Reconciliation
SELECT
    'total_gross_revenue' AS metric,
    ROUND(SUM(gross_revenue), 2) AS sql_value
FROM orders
UNION ALL
SELECT
    'total_net_revenue_completed',
    ROUND(SUM(net_revenue), 2)
FROM orders WHERE status = 'completed'
UNION ALL
SELECT
    'total_margin_completed',
    ROUND(SUM(gross_margin), 2)
FROM orders WHERE status = 'completed'
UNION ALL
SELECT
    'total_orders',
    COUNT(*)
FROM orders
UNION ALL
SELECT
    'completed_orders',
    COUNT(*)
FROM orders WHERE status = 'completed'
UNION ALL
SELECT
    'total_customers',
    COUNT(*)
FROM customers
UNION ALL
SELECT
    'active_customers',
    COUNT(DISTINCT customer_id)
FROM orders WHERE status = 'completed'
UNION ALL
SELECT
    'total_products',
    COUNT(*)
FROM products;

-- Revenue by Channel Reconciliation
SELECT
    c.channel,
    COUNT(*) AS orders,
    ROUND(SUM(o.net_revenue), 2) AS net_revenue,
    ROUND(SUM(o.gross_margin), 2) AS margin
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.channel
ORDER BY net_revenue DESC;

-- Revenue by Country Reconciliation
SELECT
    c.country,
    COUNT(*) AS orders,
    ROUND(SUM(o.net_revenue), 2) AS net_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.country
ORDER BY net_revenue DESC;

-- Revenue by Category Reconciliation
SELECT
    p.category,
    COUNT(*) AS order_items,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.unit_cost)), 2) AS margin
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;