"""Tests for data validation module."""
import sys
import json
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from config import METRICS_DIR


class TestValidation:
    """Test validation report results."""

    def test_validation_report_exists(self):
        assert (METRICS_DIR / "validation_report.json").exists()

    def test_all_checks_passed(self):
        with open(METRICS_DIR / "validation_report.json") as f:
            report = json.load(f)
        assert report["failed"] == 0, f"Failed checks: {report['failed']}"
        assert report["passed"] > 0

    def test_referential_integrity_checks(self):
        with open(METRICS_DIR / "validation_report.json") as f:
            report = json.load(f)
        fk_checks = [c for c in report["checks"] if "FK" in c["check"] or "->" in c["check"]]
        for check in fk_checks:
            assert check["status"] == "PASS", f"FK check failed: {check['check']}"