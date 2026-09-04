"""CommerceIQ - SQL Engine.

SQLite-based SQL execution with PostgreSQL-compatible syntax.
Splits multi-statement SQL files and executes each statement.
"""
import sqlite3
from pathlib import Path

import pandas as pd

from config import DATA_PROCESSED, SQL_DIR, SQL_RESULTS_DIR, DB_PATH


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def load_tables(conn: sqlite3.Connection):
    table_files = [
        "customers", "products", "orders", "order_items",
        "events", "cohort_orders", "cohort_retention",
    ]
    for name in table_files:
        csv_path = DATA_PROCESSED / f"{name}.csv"
        if not csv_path.exists():
            continue
        df = pd.read_csv(csv_path)
        df.columns = [c.replace(" ", "_").replace("-", "_").lower() for c in df.columns]
        df.to_sql(name, conn, if_exists="replace", index=False)
        print(f"  Loaded {name}: {len(df):,} rows")


def split_sql_statements(sql_text: str) -> list[str]:
    """Split SQL text into individual statements, handling CTEs properly."""
    statements = []
    current = []
    in_cte = 0

    for line in sql_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("--") or not stripped:
            continue

        upper = stripped.upper()
        if "WITH " in upper and in_cte == 0:
            in_cte += 1

        current.append(line)

        if ";" in stripped:
            stmt = "\n".join(current).strip()
            # Remove trailing semicolon
            stmt = stmt.rstrip(";").strip()
            if stmt:
                statements.append(stmt)
            current = []
            in_cte = 0

    # Handle any remaining statement
    if current:
        stmt = "\n".join(current).strip().rstrip(";").strip()
        if stmt:
            statements.append(stmt)

    return statements


def execute_sql_file(conn: sqlite3.Connection, sql_path: Path) -> pd.DataFrame:
    """Execute a SQL file, handling multiple statements."""
    sql_text = sql_path.read_text(encoding="utf-8")
    statements = split_sql_statements(sql_text)

    last_result = pd.DataFrame()
    for i, stmt in enumerate(statements):
        try:
            # Check if it's a SELECT (returns data) or DDL/DML
            first_word = stmt.split()[0].upper() if stmt.split() else ""
            if first_word == "WITH" or first_word == "SELECT":
                result = pd.read_sql_query(stmt, conn)
                last_result = result
            else:
                conn.execute(stmt)
                conn.commit()
        except Exception as e:
            print(f"    Statement {i+1} warning: {e}")

    return last_result


def run_sql_engine():
    print("=" * 60)
    print("Phase 5: SQL Analysis")
    print("=" * 60)

    conn = get_connection()

    print("\nStep 1: Loading tables into SQLite...")
    load_tables(conn)

    print("\nStep 2: Executing SQL files...")
    SQL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    sql_files = sorted(SQL_DIR.glob("*.sql"))
    for sql_file in sql_files:
        name = sql_file.stem
        print(f"\n  Executing {sql_file.name}...")
        result = execute_sql_file(conn, sql_file)
        if not result.empty:
            out_path = SQL_RESULTS_DIR / f"{name}.csv"
            result.to_csv(out_path, index=False)
            print(f"    Result: {len(result)} rows -> {out_path.name}")
            print(f"    Columns: {', '.join(list(result.columns[:5]))}...")
        else:
            print(f"    Executed (DDL or no result set)")

    conn.close()
    print("\nPhase 5 complete.\n")


if __name__ == "__main__":
    run_sql_engine()