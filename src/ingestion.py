"""CommerceIQ - Data Ingestion & Profiling.

Downloads the LaelaZ/synthetic-ecommerce dataset from Hugging Face,
converts to CSV, and generates a profiling report.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from huggingface_hub import hf_hub_download

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DATA_RAW, METRICS_DIR, DATASET_ID, TABLE_NAMES


def download_dataset() -> dict[str, pd.DataFrame]:
    """Download all tables from Hugging Face and return as DataFrames."""
    frames = {}
    for table in TABLE_NAMES:
        print(f"  Downloading {table}...")
        path = hf_hub_download(
            repo_id=DATASET_ID,
            filename=f"{table}.parquet",
            repo_type="dataset",
        )
        df = pd.read_parquet(path)
        frames[table] = df
        csv_path = DATA_RAW / f"{table}.csv"
        df.to_csv(csv_path, index=False)
        print(f"    Saved {len(df):,} rows to {csv_path.name}")
    return frames


def profile_data(frames: dict[str, pd.DataFrame]) -> dict:
    """Generate profiling report for all tables."""
    report = {}
    for name, df in frames.items():
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        date_cols = [c for c in df.columns if "date" in c.lower() or "ts" in c.lower()]

        col_profiles = {}
        for col in df.columns:
            prof = {
                "dtype": str(df[col].dtype),
                "null_count": int(df[col].isnull().sum()),
                "null_pct": round(df[col].isnull().mean() * 100, 2),
                "distinct": int(df[col].nunique()),
            }
            if col in numeric_cols:
                desc = df[col].describe()
                prof.update({
                    "mean": round(float(desc.get("mean", 0)), 4),
                    "std": round(float(desc.get("std", 0)), 4),
                    "min": round(float(desc.get("min", 0)), 4),
                    "q25": round(float(desc.get("25%", 0)), 4),
                    "median": round(float(desc.get("50%", 0)), 4),
                    "q75": round(float(desc.get("75%", 0)), 4),
                    "max": round(float(desc.get("max", 0)), 4),
                })
            elif col in cat_cols:
                vc = df[col].value_counts()
                prof["top_values"] = {str(k): int(v) for k, v in vc.head(5).items()}
            col_profiles[col] = prof

        report[name] = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_profiles": col_profiles,
            "numeric_columns": numeric_cols,
            "categorical_columns": cat_cols,
            "date_columns": date_cols,
            "memory_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        }
    return report


def save_profile_report(report: dict, path: Path | None = None):
    """Save profiling report as JSON."""
    if path is None:
        path = METRICS_DIR / "data_profile.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"  Profile report saved to {path}")


def run_ingestion() -> dict[str, pd.DataFrame]:
    """Execute full ingestion: download + profile."""
    print("=" * 60)
    print("Phase 1: Data Ingestion & Profiling")
    print("=" * 60)
    print(f"\nDataset: {DATASET_ID}")
    print(f"Tables: {', '.join(TABLE_NAMES)}\n")

    print("Step 1: Downloading data...")
    frames = download_dataset()

    print("\nStep 2: Profiling data...")
    report = profile_data(frames)
    save_profile_report(report)

    print("\nProfiling Summary:")
    for name, info in report.items():
        print(f"  {name}: {info['rows']:,} rows x {info['columns']} cols ({info['memory_mb']} MB)")

    print("\nPhase 1 complete.\n")
    return frames


if __name__ == "__main__":
    run_ingestion()