# CommerceIQ Methodology & Data Quality Report

## Dataset Description

**Source**: LaelaZ/synthetic-ecommerce (Hugging Face)
**License**: MIT
**Generation**: Seed-based (seed=42), reproducible
**Tables**: 5 relational tables, 103,839 total rows

## Data Quality Assessment

### Validation Results: 24/24 checks passed

- Referential integrity: All foreign keys resolve correctly
- Primary key uniqueness: No duplicates in any table
- Null checks: Zero nulls in all critical fields
- Business rules: unit_cost < unit_price for all products, quantity > 0

### Data Cleaning Applied

1. Type casting: order_ts -> datetime, signup_date -> date, numeric fields -> float/int
2. Derived fields: order_date, order_month, line_total, margin_pct
3. No null treatment needed (clean synthetic data)
4. No deduplication needed

## Feature Engineering

### RFM Segmentation
- Recency: Days since last completed order (lower = better)
- Frequency: Total completed orders per customer
- Monetary: Total net revenue per customer
- Scoring: Quintile-based (1-5) using pd.qcut
- Segments: Champions, Loyal Customers, Potential Loyalists, New Customers, At Risk, Lost, Others

### Cohort Analysis
- Cohort month: Customer signup month (YYYY-MM)
- Cohort index: Months since signup
- Retention rate: Unique customers active in month N / cohort size

### Margin Calculation
- Gross margin = (unit_price - unit_cost) * quantity at order-item level
- Product margin = aggregated item margins per product

## Statistical Methods

- **Kruskal-Wallis test**: Non-parametric comparison of AOV across channels/countries
- **Shapiro-Wilk test**: Normality assessment of revenue distribution
- **IQR method**: Anomaly detection (1.5x IQR bounds)
- **Z-score method**: Anomaly detection (3.0 sigma threshold)

## Limitations

1. **Synthetic data**: All patterns are generated, not observed from real transactions
2. **No discounts/shipping**: Dataset lacks discount_pct and shipping_cost fields
3. **No customer demographics**: No age, gender, or income data
4. **No payment methods**: Cannot analyze payment preferences
5. **Cohort based on signup**: Not first purchase (some customers may not purchase immediately)
6. **Small sample**: 12K orders limits statistical power for subgroup analyses
7. **Single year**: 2024-2025 only, no multi-year seasonality
8. **No returns reason**: Cannot analyze why products are returned

## Metric Definitions

| Metric | Definition |
|--------|-----------|
| Gross Revenue | Sum of (quantity x unit_price) for all order items |
| Net Revenue | Same as gross (no discount/shipping fields in this dataset) |
| Gross Margin | Sum of (unit_price - unit_cost) x quantity |
| Margin % | Gross Margin / Gross Revenue |
| AOV | Net Revenue / Completed Orders |
| Completion Rate | Completed Orders / Total Orders |
| Refund Rate | Refunded Orders / Total Orders |
| RFM Score | Sum of R + F + M quintile scores (3-15) |
| Retention Rate | Active customers in month N / Cohort size |