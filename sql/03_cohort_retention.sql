-- CommerceIQ - Cohort Retention Analysis

-- Monthly cohort retention matrix
WITH cohort_base AS (
    SELECT
        c.customer_id,
        strftime('%Y-%m', c.signup_date) AS cohort_month,
        strftime('%Y-%m', o.order_ts) AS order_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'completed'
),
cohort_period AS (
    SELECT
        customer_id,
        cohort_month,
        order_month,
        ((CAST substr(order_month, 1, 4) AS INTEGER) - (CAST substr(cohort_month, 1, 4) AS INTEGER)) * 12
        + (CAST substr(order_month, 6, 2) AS INTEGER) - (CAST substr(cohort_month, 6, 2) AS INTEGER) AS cohort_index
    FROM cohort_base
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM cohort_period
    WHERE cohort_index = 0
    GROUP BY cohort_month
),
cohort_customers AS (
    SELECT
        cp.cohort_month,
        cp.cohort_index,
        COUNT(DISTINCT cp.customer_id) AS n_customers
    FROM cohort_period cp
    GROUP BY cp.cohort_month, cp.cohort_index
)
SELECT
    cc.cohort_month,
    cc.cohort_index,
    cc.n_customers,
    cs.cohort_size,
    ROUND(CAST(cc.n_customers AS REAL) / NULLIF(cs.cohort_size, 0), 4) AS retention_rate
FROM cohort_customers cc
JOIN cohort_sizes cs ON cc.cohort_month = cs.cohort_month
ORDER BY cc.cohort_month, cc.cohort_index;