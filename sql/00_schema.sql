-- CommerceIQ - Schema DDL

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    signup_date TEXT,
    channel TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    unit_price REAL,
    unit_cost REAL,
    margin_pct REAL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_ts TEXT,
    status TEXT,
    order_date TEXT,
    order_month TEXT,
    item_count INTEGER,
    total_quantity INTEGER,
    gross_revenue REAL,
    total_cost REAL,
    gross_margin REAL,
    net_revenue REAL,
    net_margin REAL,
    cost_pct REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    line_total REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY,
    session_id INTEGER,
    customer_id INTEGER,
    event_type TEXT,
    event_ts TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS cohort_orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_ts TEXT,
    status TEXT,
    cohort_month TEXT,
    order_month TEXT,
    cohort_index INTEGER
);

CREATE TABLE IF NOT EXISTS cohort_retention (
    cohort_month TEXT,
    order_month TEXT,
    n_customers INTEGER,
    cohort_size INTEGER,
    retention_rate REAL
);

CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_ts);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_events_customer ON events(customer_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);