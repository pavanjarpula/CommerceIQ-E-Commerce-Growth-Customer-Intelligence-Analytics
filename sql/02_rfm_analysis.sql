-- CommerceIQ - RFM Analysis with Window Functions

-- RFM scores using NTILE
WITH customer_rfm_raw AS (
    SELECT
        c.customer_id,
        c.signup_date,
        c.channel,
        c.country,
        CAST((julianday('now') - julianday(MAX(o.order_ts))) AS INTEGER) AS recency_days,
        COUNT(DISTINCT o.order_id) AS frequency,
        ROUND(SUM(o.net_revenue), 2) AS monetary
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'completed'
    GROUP BY c.customer_id
    HAVING COUNT(DISTINCT o.order_id) > 0
),
rfm_scored AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS rfm_r,
        NTILE(5) OVER (ORDER BY frequency ASC) AS rfm_f,
        NTILE(5) OVER (ORDER BY monetary ASC) AS rfm_m
    FROM customer_rfm_raw
),
rfm_segmented AS (
    SELECT
        *,
        rfm_r + rfm_f + rfm_m AS rfm_score,
        CASE
            WHEN rfm_r >= 4 AND rfm_f >= 4 AND rfm_m >= 4 THEN 'Champions'
            WHEN rfm_r >= 3 AND rfm_f >= 3 AND rfm_m >= 3 THEN 'Loyal Customers'
            WHEN rfm_r >= 4 AND rfm_f <= 2 THEN 'New Customers'
            WHEN rfm_r >= 3 AND rfm_f >= 2 AND rfm_m >= 2 THEN 'Potential Loyalists'
            WHEN rfm_r <= 2 AND rfm_f >= 3 THEN 'At Risk'
            WHEN rfm_r <= 2 AND rfm_f <= 2 THEN 'Lost'
            ELSE 'Others'
        END AS rfm_segment
    FROM rfm_scored
)
SELECT
    rfm_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(recency_days), 0) AS avg_recency,
    ROUND(AVG(frequency), 1) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_monetary,
    ROUND(SUM(monetary), 2) AS total_revenue
FROM rfm_segmented
GROUP BY rfm_segment
ORDER BY total_revenue DESC;