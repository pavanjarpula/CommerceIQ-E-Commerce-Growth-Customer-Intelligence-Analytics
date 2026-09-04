-- CommerceIQ - Core Metric Definitions (SQL with CTEs)

-- Revenue Summary
WITH revenue_summary AS (
    SELECT
        COUNT(*) AS total_orders,
        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_orders,
        SUM(CASE WHEN status = 'refunded' THEN 1 ELSE 0 END) AS refunded_orders,
        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
        ROUND(SUM(gross_revenue), 2) AS total_gross_revenue,
        ROUND(SUM(CASE WHEN status = 'completed' THEN net_revenue ELSE 0 END), 2) AS total_net_revenue,
        ROUND(SUM(CASE WHEN status = 'completed' THEN gross_margin ELSE 0 END), 2) AS total_margin
    FROM orders
),
calculated AS (
    SELECT
        *,
        ROUND(CAST(completed_orders AS REAL) / NULLIF(total_orders, 0), 4) AS completion_rate,
        ROUND(CAST(refunded_orders AS REAL) / NULLIF(total_orders, 0), 4) AS refund_rate,
        ROUND(CAST(cancelled_orders AS REAL) / NULLIF(total_orders, 0), 4) AS cancellation_rate,
        ROUND(total_margin / NULLIF(total_gross_revenue, 0), 4) AS margin_pct,
        ROUND(total_net_revenue / NULLIF(completed_orders, 0), 2) AS avg_order_value,
        ROUND(total_margin / NULLIF(completed_orders, 0), 2) AS avg_order_margin
    FROM revenue_summary
)
SELECT * FROM calculated;

-- Monthly Revenue Trend with Growth
WITH completed_orders AS (
    SELECT * FROM orders WHERE status = 'completed'
),
monthly AS (
    SELECT
        order_month,
        COUNT(*) AS orders,
        ROUND(SUM(gross_revenue), 2) AS gross_revenue,
        ROUND(SUM(net_revenue), 2) AS net_revenue,
        ROUND(AVG(net_revenue), 2) AS avg_order_value,
        ROUND(SUM(gross_margin), 2) AS margin,
        ROUND(SUM(gross_margin) / NULLIF(SUM(gross_revenue), 0), 4) AS margin_pct
    FROM completed_orders
    GROUP BY order_month
    ORDER BY order_month
),
with_growth AS (
    SELECT
        *,
        ROUND((net_revenue - LAG(net_revenue) OVER (ORDER BY order_month))
              / NULLIF(LAG(net_revenue) OVER (ORDER BY order_month), 0), 4) AS revenue_mom_growth,
        ROUND(CAST(orders - LAG(orders) OVER (ORDER BY order_month) AS REAL)
              / NULLIF(LAG(orders) OVER (ORDER BY order_month), 0), 4) AS orders_mom_growth
    FROM monthly
)
SELECT * FROM with_growth;

-- Revenue by Channel
WITH channel_revenue AS (
    SELECT
        c.channel,
        COUNT(*) AS total_orders,
        ROUND(SUM(o.net_revenue), 2) AS total_revenue,
        ROUND(SUM(o.gross_margin), 2) AS total_margin,
        ROUND(AVG(o.net_revenue), 2) AS avg_order_value,
        COUNT(DISTINCT o.customer_id) AS unique_customers
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.channel
)
SELECT
    *,
    ROUND(total_revenue / SUM(total_revenue) OVER (), 4) AS revenue_pct,
    ROUND(total_margin / NULLIF(total_revenue, 0), 4) AS margin_pct
FROM channel_revenue
ORDER BY total_revenue DESC;