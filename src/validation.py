"""CommerceIQ - Data Validation.

Checks referential integrity, business rules, nulls, and duplicates.
"""
import json
from pathlib import Path

import pandas as pd

from config import METRICS_DIR


def validate_referential_integrity(frames: dict[str, pd.DataFrame]) -> list[dict]:
    """Check foreign key relationships across tables."""
    issues = []

    # orders.customer_id -> customers.customer_id
    if "orders" in frames and "customers" in frames:
        order_cids = set(frames["orders"]["customer_id"].unique())
        customer_cids = set(frames["customers"]["customer_id"].unique())
        orphans = order_cids - customer_cids
        if orphans:
            issues.append({
                "check": "orders.customer_id -> customers.customer_id",
                "status": "FAIL",
                "detail": f"{len(orphans)} orphan customer IDs in orders",
            })
        else:
            issues.append({
                "check": "orders.customer_id -> customers.customer_id",
                "status": "PASS",
                "detail": "All order customer IDs exist in customers",
            })

    # order_items.order_id -> orders.order_id
    if "order_items" in frames and "orders" in frames:
        item_oids = set(frames["order_items"]["order_id"].unique())
        order_oids = set(frames["orders"]["order_id"].unique())
        orphans = item_oids - order_oids
        if orphans:
            issues.append({
                "check": "order_items.order_id -> orders.order_id",
                "status": "FAIL",
                "detail": f"{len(orphans)} orphan order IDs in order_items",
            })
        else:
            issues.append({
                "check": "order_items.order_id -> orders.order_id",
                "status": "PASS",
                "detail": "All order_item order IDs exist in orders",
            })

    # order_items.product_id -> products.product_id
    if "order_items" in frames and "products" in frames:
        item_pids = set(frames["order_items"]["product_id"].unique())
        product_pids = set(frames["products"]["product_id"].unique())
        orphans = item_pids - product_pids
        if orphans:
            issues.append({
                "check": "order_items.product_id -> products.product_id",
                "status": "FAIL",
                "detail": f"{len(orphans)} orphan product IDs in order_items",
            })
        else:
            issues.append({
                "check": "order_items.product_id -> products.product_id",
                "status": "PASS",
                "detail": "All order_item product IDs exist in products",
            })

    return issues


def validate_business_rules(frames: dict[str, pd.DataFrame]) -> list[dict]:
    """Check domain-specific business rules."""
    issues = []

    if "products" in frames:
        prods = frames["products"]
        bad_cost = (prods["unit_cost"] >= prods["unit_price"]).sum()
        issues.append({
            "check": "unit_cost < unit_price for all products",
            "status": "FAIL" if bad_cost > 0 else "PASS",
            "detail": f"{bad_cost} products with cost >= price" if bad_cost else "All products have cost < price",
        })

    if "order_items" in frames:
        items = frames["order_items"]
        bad_qty = (items["quantity"] <= 0).sum()
        issues.append({
            "check": "quantity > 0 for all order items",
            "status": "FAIL" if bad_qty > 0 else "PASS",
            "detail": f"{bad_qty} items with quantity <= 0" if bad_qty else "All quantities positive",
        })

    if "orders" in frames:
        orders = frames["orders"]
        valid_statuses = {"completed", "refunded", "cancelled"}
        invalid = orders[~orders["status"].isin(valid_statuses)]
        issues.append({
            "check": "order status in valid set",
            "status": "FAIL" if len(invalid) > 0 else "PASS",
            "detail": f"{len(invalid)} orders with invalid status" if len(invalid) else "All statuses valid",
        })

    return issues


def validate_nulls(frames: dict[str, pd.DataFrame]) -> list[dict]:
    """Check for unexpected nulls in critical fields."""
    issues = []
    critical_fields = {
        "orders": ["order_id", "customer_id", "order_ts", "status"],
        "order_items": ["order_item_id", "order_id", "product_id", "quantity"],
        "customers": ["customer_id", "signup_date"],
        "products": ["product_id", "unit_price", "unit_cost"],
    }
    for table, fields in critical_fields.items():
        if table in frames:
            for field in fields:
                if field in frames[table].columns:
                    nulls = frames[table][field].isnull().sum()
                    issues.append({
                        "check": f"{table}.{field} not null",
                        "status": "FAIL" if nulls > 0 else "PASS",
                        "detail": f"{nulls} nulls in {table}.{field}",
                    })
    return issues


def validate_duplicates(frames: dict[str, pd.DataFrame]) -> list[dict]:
    """Check for duplicate primary keys."""
    issues = []
    pk_fields = {
        "customers": "customer_id",
        "products": "product_id",
        "orders": "order_id",
        "order_items": "order_item_id",
        "events": "event_id",
    }
    for table, pk in pk_fields.items():
        if table in frames and pk in frames[table].columns:
            dups = frames[table][pk].duplicated().sum()
            issues.append({
                "check": f"{table}.{pk} unique",
                "status": "FAIL" if dups > 0 else "PASS",
                "detail": f"{dups} duplicate {pk} in {table}",
            })
    return issues


def run_validation(frames: dict[str, pd.DataFrame]) -> dict:
    """Execute all validations and save report."""
    print("=" * 60)
    print("Phase 2a: Data Validation")
    print("=" * 60)

    all_checks = []
    all_checks.extend(validate_referential_integrity(frames))
    all_checks.extend(validate_business_rules(frames))
    all_checks.extend(validate_nulls(frames))
    all_checks.extend(validate_duplicates(frames))

    passed = sum(1 for c in all_checks if c["status"] == "PASS")
    failed = sum(1 for c in all_checks if c["status"] == "FAIL")
    total = len(all_checks)

    report = {
        "total_checks": total,
        "passed": passed,
        "failed": failed,
        "checks": all_checks,
    }

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    with open(METRICS_DIR / "validation_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nResults: {passed}/{total} passed, {failed} failed\n")
    for check in all_checks:
        symbol = "âœ“" if check["status"] == "PASS" else "[FAIL]"
        print(f"  {symbol} {check['check']}: {check['detail']}")

    print(f"\nPhase 2a complete. Report saved to outputs/metrics/validation_report.json\n")
    return report