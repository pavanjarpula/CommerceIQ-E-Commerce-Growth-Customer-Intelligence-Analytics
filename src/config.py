"""CommerceIQ Analytics Pipeline - Configuration."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS = PROJECT_ROOT / "outputs"
METRICS_DIR = OUTPUTS / "metrics"
FIGURES_DIR = OUTPUTS / "figures"
SQL_RESULTS_DIR = OUTPUTS / "sql_results"
REPORTS_DIR = OUTPUTS / "reports"
SQL_DIR = PROJECT_ROOT / "sql"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"

DATASET_ID = "LaelaZ/synthetic-ecommerce"
TABLE_NAMES = ["customers", "products", "orders", "order_items", "events"]

DB_PATH = PROJECT_ROOT / "data" / "commerceiq.db"

RANDOM_SEED = 42