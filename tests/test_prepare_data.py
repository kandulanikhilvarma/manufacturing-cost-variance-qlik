"""
Tests for scripts/prepare_data.py
Run from repo root: pytest tests/ -v
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import prepare_data as pd  # noqa: E402

GOOD_ROW = {
    "Month": "2024-01",
    "Product_Line": "Sealing Systems",
    "Cost_Category": "Raw Materials",
    "Budget_EUR": "45000",
    "Actual_EUR": "45376.45",
    "Variance_EUR": "376.45",
    "Variance_Pct": "0.84",
    "Over_Budget": "Yes",
}


def make_rows(n=2, **overrides):
    rows = []
    for i in range(n):
        row = dict(GOOD_ROW)
        row["Month"] = f"2024-{i + 1:02d}"
        row.update(overrides)
        rows.append(row)
    return rows


# ---------- load() ----------

def test_load_reads_csv_into_list_of_dicts(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(
        "Month,Product_Line,Cost_Category,Budget_EUR,Actual_EUR,"
        "Variance_EUR,Variance_Pct,Over_Budget\n"
        "2024-01,Sealing Systems,Raw Materials,45000,45376.45,376.45,0.84,Yes\n"
    )
    rows = pd.load(csv_path)
    assert len(rows) == 1
    assert rows[0]["Month"] == "2024-01"
    assert rows[0]["Cost_Category"] == "Raw Materials"


def test_load_preserves_row_order(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(
        "Month,Value\n2024-01,a\n2024-02,b\n2024-03,c\n"
    )
    rows = pd.load(csv_path)
    assert [r["Month"] for r in rows] == ["2024-01", "2024-02", "2024-03"]


# ---------- validate() ----------

def test_validate_passes_on_well_formed_rows(capsys):
    rows = make_rows(3)
    pd.validate(rows)  # should not raise
    captured = capsys.readouterr()
    assert "OK" in captured.out
    assert "3 rows" in captured.out


def test_validate_reports_correct_distinct_counts(capsys):
    rows = make_rows(2)
    rows[0]["Cost_Category"] = "Raw Materials"
    rows[1]["Cost_Category"] = "Direct Labor"
    rows[0]["Product_Line"] = "Sealing Systems"
    rows[1]["Product_Line"] = "Welding Components"

    pd.validate(rows)
    out = capsys.readouterr().out
    assert "2 months" in out
    assert "2 categories" in out
    assert "2 product lines" in out


def test_validate_raises_on_missing_column():
    rows = make_rows(1)
    del rows[0]["Variance_Pct"]
    with pytest.raises(ValueError, match="Missing columns"):
        pd.validate(rows)


def test_validate_raises_on_empty_value():
    rows = make_rows(2)
    rows[1]["Budget_EUR"] = ""
    with pytest.raises(ValueError, match="Empty values"):
        pd.validate(rows)


def test_validate_reports_correct_csv_row_number_for_empty_value():
    # rows[1] is CSV row 3 (row 1 = header, row 2 = rows[0], row 3 = rows[1])
    rows = make_rows(3)
    rows[1]["Actual_EUR"] = ""
    with pytest.raises(ValueError, match=r"\[3\]"):
        pd.validate(rows)


# ---------- summarize_by_category() ----------

def test_summarize_prints_grand_total(capsys):
    rows = [
        {**GOOD_ROW, "Cost_Category": "Raw Materials",
         "Budget_EUR": "1000", "Actual_EUR": "1100"},
        {**GOOD_ROW, "Cost_Category": "Direct Labor",
         "Budget_EUR": "2000", "Actual_EUR": "1900"},
    ]
    pd.summarize_by_category(rows)
    out = capsys.readouterr().out
    assert "TOTAL" in out
    # 3000 budget, 3000 actual -> net 0% variance
    assert "3,000" in out


def test_summarize_uses_up_arrow_for_over_budget_category(capsys):
    rows = [{**GOOD_ROW, "Cost_Category": "Raw Materials",
             "Budget_EUR": "1000", "Actual_EUR": "1200"}]
    pd.summarize_by_category(rows)
    out = capsys.readouterr().out
    assert "▲" in out
    assert "20.0%" in out


def test_summarize_uses_down_arrow_for_under_budget_category(capsys):
    rows = [{**GOOD_ROW, "Cost_Category": "Direct Labor",
             "Budget_EUR": "1000", "Actual_EUR": "800"}]
    pd.summarize_by_category(rows)
    out = capsys.readouterr().out
    assert "▼" in out
    assert "20.0%" in out


def test_summarize_aggregates_multiple_rows_in_same_category(capsys):
    rows = [
        {**GOOD_ROW, "Cost_Category": "Logistics",
         "Budget_EUR": "500", "Actual_EUR": "500"},
        {**GOOD_ROW, "Cost_Category": "Logistics",
         "Budget_EUR": "500", "Actual_EUR": "500"},
    ]
    pd.summarize_by_category(rows)
    out = capsys.readouterr().out
    # Combined budget/actual for Logistics should be 1,000 / 1,000
    assert "1,000" in out


# ---------- main() ----------

def test_main_raises_file_not_found_when_csv_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pd, "DATA_FILE", tmp_path / "data" / "manufacturing_variance.csv")
    with pytest.raises(FileNotFoundError, match="generate_data.py"):
        pd.main()


def test_main_runs_end_to_end_against_real_generated_csv(tmp_path, monkeypatch, capsys):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    import generate_data as gd

    monkeypatch.chdir(tmp_path)
    gd.main()  # writes data/manufacturing_variance.csv

    monkeypatch.setattr(pd, "DATA_FILE", tmp_path / "data" / "manufacturing_variance.csv")
    pd.main()  # should not raise

    out = capsys.readouterr().out
    assert "OK  144 rows" in out
    assert "TOTAL" in out
