"""
Tests for scripts/generate_data.py
Run from repo root: pytest tests/ -v
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import generate_data as gd  # noqa: E402

EXPECTED_CATEGORIES = {
    "Raw Materials", "Direct Labor", "Machine Overhead",
    "Packaging", "Quality Inspection", "Logistics",
}
EXPECTED_PRODUCT_LINES = {"Sealing Systems", "Welding Components"}


# ---------- structural constants ----------

def test_twelve_months_defined():
    assert len(gd.MONTHS) == 12
    assert gd.MONTHS[0] == "2024-01"
    assert gd.MONTHS[-1] == "2024-12"


def test_months_are_sequential_and_unique():
    assert len(set(gd.MONTHS)) == 12
    assert gd.MONTHS == sorted(gd.MONTHS)


def test_product_lines_match_expected():
    assert set(gd.PRODUCT_LINES) == EXPECTED_PRODUCT_LINES


def test_budget_table_covers_all_categories_and_product_lines():
    assert set(gd.BUDGETS.keys()) == EXPECTED_CATEGORIES
    for category, pl_budgets in gd.BUDGETS.items():
        assert set(pl_budgets.keys()) == EXPECTED_PRODUCT_LINES, category


def test_all_budgets_are_positive():
    for category, pl_budgets in gd.BUDGETS.items():
        for pl, amount in pl_budgets.items():
            assert amount > 0, f"{category}/{pl} budget must be positive"


# ---------- variance_factor() ----------

def test_raw_materials_spikes_in_q3():
    # month_idx 6,7,8 -> Jul, Aug, Sep
    for idx in (6, 7, 8):
        factor = gd.variance_factor(idx, "Raw Materials")
        assert 1.08 <= factor <= 1.14

    for idx in (0, 1, 5, 9, 11):
        factor = gd.variance_factor(idx, "Raw Materials")
        assert 0.97 <= factor <= 1.03


def test_direct_labor_improves_in_h2():
    for idx in range(6, 12):
        factor = gd.variance_factor(idx, "Direct Labor")
        assert 0.92 <= factor <= 0.97

    for idx in range(0, 6):
        factor = gd.variance_factor(idx, "Direct Labor")
        assert 0.98 <= factor <= 1.04


def test_machine_overhead_stays_flat_all_year():
    for idx in range(12):
        factor = gd.variance_factor(idx, "Machine Overhead")
        assert 0.98 <= factor <= 1.03


def test_packaging_creeps_upward_over_the_year():
    # Compare average factor early year vs late year (random noise means
    # we check the trend, not exact values).
    early = [gd.variance_factor(i, "Packaging") for i in range(3)]
    late = [gd.variance_factor(i, "Packaging") for i in range(9, 12)]
    assert sum(late) / len(late) > sum(early) / len(early)


def test_quality_inspection_within_flat_band():
    for idx in range(12):
        factor = gd.variance_factor(idx, "Quality Inspection")
        assert 0.95 <= factor <= 1.05


def test_logistics_spikes_in_q4():
    for idx in (9, 10, 11):
        factor = gd.variance_factor(idx, "Logistics")
        assert 1.05 <= factor <= 1.11

    for idx in (0, 4, 8):
        factor = gd.variance_factor(idx, "Logistics")
        assert 0.97 <= factor <= 1.04


def test_unknown_category_defaults_to_one():
    assert gd.variance_factor(0, "Nonexistent Category") == 1.0


# ---------- build_rows() ----------

def test_build_rows_row_count_is_months_times_categories_times_lines():
    rows = gd.build_rows()
    expected = len(gd.MONTHS) * len(gd.BUDGETS) * len(gd.PRODUCT_LINES)
    assert len(rows) == expected == 144


def test_build_rows_has_expected_columns():
    rows = gd.build_rows()
    expected_keys = {
        "Month", "Product_Line", "Cost_Category",
        "Budget_EUR", "Actual_EUR", "Variance_EUR",
        "Variance_Pct", "Over_Budget",
    }
    assert set(rows[0].keys()) == expected_keys


def test_build_rows_variance_math_is_internally_consistent():
    rows = gd.build_rows()
    for r in rows:
        expected_variance = round(r["Actual_EUR"] - r["Budget_EUR"], 2)
        assert abs(r["Variance_EUR"] - expected_variance) < 0.01

        expected_pct = round((r["Variance_EUR"] / r["Budget_EUR"]) * 100, 2)
        assert abs(r["Variance_Pct"] - expected_pct) < 0.01


def test_build_rows_over_budget_flag_matches_variance_sign():
    rows = gd.build_rows()
    for r in rows:
        if r["Variance_EUR"] > 0:
            assert r["Over_Budget"] == "Yes"
        else:
            assert r["Over_Budget"] == "No"


def test_build_rows_is_deterministic_given_fixed_seed():
    # generate_data.py seeds random at import time (seed=42), so calling
    # build_rows() twice in the same process should differ (random state
    # advances) — but re-seeding should reproduce the first run exactly.
    import random as random_module

    random_module.seed(42)
    first = gd.build_rows()
    random_module.seed(42)
    second = gd.build_rows()
    assert first == second


def test_build_rows_no_budget_is_referenced_that_doesnt_exist():
    rows = gd.build_rows()
    for r in rows:
        assert r["Cost_Category"] in gd.BUDGETS
        assert r["Product_Line"] in gd.BUDGETS[r["Cost_Category"]]
        assert r["Budget_EUR"] == gd.BUDGETS[r["Cost_Category"]][r["Product_Line"]]


# ---------- main() / file output ----------

def test_main_writes_csv_with_correct_row_count(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    gd.main()

    output = tmp_path / "data" / "manufacturing_variance.csv"
    assert output.exists()

    with open(output, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 144


def test_main_creates_data_directory_if_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert not (tmp_path / "data").exists()
    gd.main()
    assert (tmp_path / "data").is_dir()
