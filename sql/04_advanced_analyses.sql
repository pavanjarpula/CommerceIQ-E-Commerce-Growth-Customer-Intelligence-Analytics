-- CommerceIQ - Advanced SQL Analyses

-- Top 10 Products by Revenue (RANK window function)
WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        p.unit_price,
        p.unit_cost,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
        SUM(oi.quantity) AS total_units,
        ROUND(SUM(oi.quantity * (oi.unit_price - p.unit_cost)), 2) AS total_margin,
        COUNT(DISTINCT oi.order_id) AS order_count
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY p.product_id
),
ranked AS (
    SELECT
        *,
        RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
        ROUND(total_revenue / NULLIF(SUM(total_revenue) OVER (), 0), 4) AS revenue_share,
        ROUND(total_margin / NULLIF(total_revenue, 0), 4) AS margin_pct
    FROM product_revenue
)
SELECT * FROM ranked WHERE revenue_rank <= 10 ORDER BY revenue_rank;

-- Pareto Analysis: Customer Revenue Distribution
WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(net_revenue) AS total_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id,
        total_revenue,
        ROW_NUMBER() OVER (ORDER BY total_revenue DESC) AS rank_num,
        COUNT(*) OVER () AS total_customers,
        SUM(total_revenue) OVER () AS grand_total
    FROM customer_revenue
),
cumulative AS (
    SELECT
        *,
        ROUND(CAST(rank_num AS REAL) / total_customers, 4) AS customer_pct,
        ROUND(SUM(total_revenue) OVER (ORDER BY rank_num) / grand_total, 4) AS cumulative_revenue_pct
    FROM ranked
)
SELECT
    CASE
        WHEN customer_pct <= 0.20 THEN 'Top 20%'
        WHEN customer_pct <= 0.50 THEN 'Next 30%'
        WHEN customer_pct <= 0.80 THEN 'Next 30%'
        ELSE 'Bottom 20%'
    END AS customer_tier,
    COUNT(*) AS customers,
    ROUND(SUM(total_revenue), 2) AS tier_revenue,
    ROUND(SUM(total_revenue) / (SELECT SUM(net_revenue) FROM orders WHERE status = 'completed'), 4) AS revenue_share
FROM cumulative
GROUP BY customer_tier
ORDER BY tier_revenue DESC;

-- Funnel Conversion from Events
WITH funnel AS (
    SELECT
        event_type,
        COUNT(*) AS event_count,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM events
    GROUP BY event_type
),
ordered_funnel AS (
    SELECT
        event_type,
        event_count,
        unique_customers,
        CASE event_type
            WHEN 'view' THEN 1
            WHEN 'add_to_cart' THEN 2
            WHEN 'checkout' THEN 3
            WHEN 'purchase' THEN 4
        END AS funnel_step
    FROM funnel
)
SELECT
    event_type,
    event_count,
    unique_customers,
    ROUND(CAST(unique_customers AS REAL) / NULLIF(MAX(unique_customers) OVER (), 0), 4) AS overall_conversion,
    ROUND(CAST(unique_customers AS REAL) / NULLIF(LAG(unique_customers) OVER (ORDER BY funnel_step), 0), 4) AS step_conversion
FROM ordered_funnel
ORDER BY funnel_step;

-- Moving Average Revenue Trend
WITH monthly_rev AS (
    SELECT
        order_month,
        SUM(net_revenue) AS net_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY order_month
)
SELECT
    order_month,
    ROUND(net_revenue, 2) AS net_revenue,
    ROUND(AVG(net_revenue) OVER (ORDER BY order_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m,
    ROUND(LAG(net_revenue, 1) OVER (ORDER BY order_month), 2) AS prev_month,
    ROUND(net_revenue - LAG(net_revenue, 1) OVER (ORDER BY order_month), 2) AS mom_change
FROM monthly_rev
ORDER BY order_month;

-- Customer Lifetime Analysis
WITH customer_orders AS (
    SELECT
        customer_id,
        MIN(order_ts) AS first_order,
        MAX(order_ts) AS last_order,
        COUNT(*) AS total_orders,
        SUM(net_revenue) AS total_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN total_orders = 1 THEN 'One-time'
        WHEN total_orders BETWEEN 2 AND 3 THEN 'Occasional'
        WHEN total_orders BETWEEN 4 AND 6 THEN 'Regular'
        ELSE 'Loyal'
    END AS customer_type,
    COUNT(*) AS customers,
    ROUND(AVG(total_revenue), 2) AS avg_revenue,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(AVG(total_orders), 1) AS avg_orders
FROM customer_orders
GROUP BY customer_type
ORDER BY avg_revenue DESC;