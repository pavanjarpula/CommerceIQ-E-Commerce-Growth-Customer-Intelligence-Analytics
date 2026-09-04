# CommerceIQ Analytics Platform

> End-to-end e-commerce analytics pipeline with interactive Streamlit dashboard.
> Built on the [LaelaZ/synthetic-ecommerce](https://huggingface.co/datasets/LaelaZ/synthetic-ecommerce) dataset (MIT License).

---

## Key Results

| Metric                 | Value                |
| ---------------------- | -------------------- |
| **Total Orders**       | 12,000               |
| **Completed Orders**   | 8,015 (66.8%)        |
| **Gross Revenue**      | $3,671,066           |
| **Net Revenue**        | $2,461,334           |
| **Gross Margin**       | $1,172,816 (32.0%)   |
| **Avg Order Value**    | $307.09              |
| **Refund Rate**        | 16.5%                |
| **Cancellation Rate**  | 16.7%                |
| **Active Customers**   | 1,725 / 2,000        |
| **Product Categories** | 6                    |
| **Countries**          | 8                    |
| **Channels**           | 6                    |

---

## Architecture

```
e-commerce-analysis/
├── data/
│   ├── raw/                    # Downloaded CSVs from HuggingFace
│   └── processed/              # Cleaned & feature-engineered data
│
├── src/                        # Modular Python pipeline
│   ├── ingestion.py            #   Data download & profiling
│   ├── validation.py           #   Referential integrity & business rules
│   ├── cleaning.py             #   Type casting & null handling
│   ├── features.py             #   RFM, cohorts, margin, time features
│   ├── metrics.py              #   KPI definitions & computation
│   ├── sql_engine.py           #   SQLite execution wrapper
│   ├── analysis.py             #   EDA, plots, statistical tests
│   ├── anomaly.py              #   IQR & Z-score detection
│   ├── segmentation.py         #   RFM segment analysis
│   ├── cohorts.py              #   Cohort retention analysis
│   ├── scenario.py             #   Channel ROI & category profitability
│   └── recommendations.py      #   Evidence-based recommendations
│
├── sql/                        # SQL analyses (CTEs, window functions)
├── notebooks/                  # 6 Jupyter notebooks
├── tests/                      # 26 pytest tests
│
├── outputs/
│   ├── metrics/                #   JSON metric files (16 files)
│   ├── figures/                #   PNG visualizations
│   └── sql_results/            #   SQL query results
│
└── dashboard/                  # Streamlit multi-page app
    ├── app.py                  #   Entry point
    ├── pages/                  #   8 dashboard pages
    ├── components/             #   Filters, KPI cards, charts
    └── utils/                  #   Data loader, formatting
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Full Pipeline

```bash
python run_pipeline.py
```

This runs all phases end-to-end:

| Phase | Description |
| ----- | ----------- |
| 1 | Downloads dataset from HuggingFace |
| 2 | Validates referential integrity (24/24 checks pass) |
| 3 | Cleans and type-casts all tables |
| 4 | Engineers RFM scores, cohort assignments, margin calculations |
| 5 | Computes all business metrics |
| 6 | Executes SQL analyses |
| 7 | Generates EDA visualizations and statistical tests |
| 8 | Detects anomalies, runs scenarios, produces recommendations |

### 3. Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Dashboard Pages

| Page | Description |
| ---- | ----------- |
| **Executive Overview** | High-level KPIs, revenue trend, top insights |
| **Sales & Growth** | Monthly trends, growth rates, AOV analysis |
| **Customer Intelligence** | RFM segmentation, customer distribution |
| **Product Intelligence** | Category revenue, top products, margins |
| **Regional Performance** | Country & channel analysis |
| **Margin & Pricing Insights** | Cost structure, pricing tier analysis |
| **Insights & Decisions** | Recommendations, scenarios, anomalies |
| **Methodology & Data Quality** | Schema, validation, data limitations |

---

## Running Tests

```bash
pytest tests/ -v
```

All **26 tests** pass — covering validation logic, metric accuracy, RFM computation, edge cases, and aggregation correctness.

---

## Notebooks

```bash
jupyter notebook notebooks/
```

6 notebooks covering: data profiling, cleaning walkthrough, EDA, cohort analysis, statistical testing, and full pipeline summary.

---

## Dataset

**LaelaZ/synthetic-ecommerce** — 5 tables, MIT License.

| Table         | Rows    | Key Columns                                         |
| ------------- | ------- | --------------------------------------------------- |
| `customers`   | 2,000   | `signup_date`, `channel`, `country`                 |
| `products`    | 120     | `category`, `unit_price`, `unit_cost`               |
| `orders`      | 12,000  | `order_ts`, `status`                                |
| `order_items` | 30,120  | `quantity`, `unit_price` (per line item)            |
| `events`      | 59,599  | Clickstream: view, add_to_cart, checkout, purchase  |

---

## Known Limitations

- **Synthetic data** — findings are illustrative, not business-critical
- No customer demographics (age, gender)
- No `discount_pct` or `shipping_cost` fields on orders
- No payment method data
- Discount analysis replaced with **margin/pricing analysis**
- Cohort analysis based on **signup date** (not first purchase)
- Small dataset (12K orders) — statistical tests may lack power

---

## Tech Stack

| Layer        | Tools                                                |
| ------------ | ---------------------------------------------------- |
| **Language** | Python 3.11                                          |
| **Data**     | Pandas, NumPy, HuggingFace Hub                       |
| **Analysis** | SciPy, Matplotlib, Seaborn, Plotly                   |
| **Dashboard**| Streamlit                                            |
| **Database** | SQLite                                               |
| **Testing**  | Pytest                                               |
| **Notebooks**| Jupyter                                              |
