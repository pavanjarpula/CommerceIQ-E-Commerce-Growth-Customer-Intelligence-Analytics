"""CommerceIQ - Pipeline Orchestrator.

Runs the full analytics pipeline end-to-end.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from ingestion import run_ingestion
from validation import run_validation
from cleaning import run_cleaning
from features import run_feature_engineering
from metrics import run_metrics
from sql_engine import run_sql_engine
from analysis import run_analysis
from segmentation import run_segmentation
from cohorts import run_cohorts
from anomaly import run_anomaly_detection
from scenario import run_scenario_analysis
from recommendations import run_recommendations


def main():
    print("\n" + "=" * 60)
    print("  CommerceIQ Analytics Pipeline")
    print("=" * 60 + "\n")

    # Phase 1: Ingestion
    raw_frames = run_ingestion()

    # Phase 2a: Validation
    validation_report = run_validation(raw_frames)

    # Phase 2b: Cleaning
    cleaned = run_cleaning(raw_frames)

    # Phase 3: Feature Engineering
    data = run_feature_engineering(cleaned)

    # Phase 4: Metrics
    metrics = run_metrics(data)

    # Phase 5: SQL Analysis
    run_sql_engine()

    # Phase 6: EDA & Statistical Analysis
    run_analysis(data)

    # Phase 7: Segmentation & Cohorts
    run_segmentation(data)
    run_cohorts(data)

    # Phase 8: Anomaly, Scenarios, Recommendations
    run_anomaly_detection(data)
    run_scenario_analysis(data)
    run_recommendations(data, metrics)

    print("\n" + "=" * 60)
    print("  Pipeline Complete!")
    print("=" * 60)
    print(f"\n  Outputs saved to: outputs/")
    print(f"  Dashboard: streamlit run dashboard/app.py")
    print()


if __name__ == "__main__":
    main()