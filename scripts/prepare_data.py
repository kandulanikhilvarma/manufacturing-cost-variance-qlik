"""
prepare_data.py
Validates manufacturing_variance.csv and prints a summary by cost category.
Run: python scripts/prepare_data.py
"""

import csv
from collections import defaultdict
from pathlib import Path

DATA_FILE = Path("data/manufacturing_variance.csv")

REQUIRED_COLUMNS = {
    "Month", "Product_Line", "Cost_Category",
    "Budget_EUR", "Actual_EUR", "Variance_EUR", "Variance_Pct", "Over_Budget",
}


def load(path: Path) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def validate(rows: list[dict]) -> None:
    missing_cols = REQUIRED_COLUMNS - set(rows[0].keys())
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    empty_rows = [i + 2 for i, r in enumerate(rows) if any(not r[k] for k in REQUIRED_COLUMNS)]
    if empty_rows:
        raise ValueError(f"Empty values at CSV rows: {empty_rows}")

    print(
        f"OK  {len(rows)} rows | "
        f"{len(set(r['Month'] for r in rows))} months | "
        f"{len(set(r['Cost_Category'] for r in rows))} categories | "
        f"{len(set(r['Product_Line'] for r in rows))} product lines"
    )


def summarize_by_category(rows: list[dict]) -> None:
    totals: dict[str, dict] = defaultdict(lambda: {"budget": 0.0, "actual": 0.0})

    for r in rows:
        cat = r["Cost_Category"]
        totals[cat]["budget"] += float(r["Budget_EUR"])
        totals[cat]["actual"] += float(r["Actual_EUR"])

    print(f"\n{'Category':<22} {'Budget (€)':>12} {'Actual (€)':>12} {'Var %':>8}")
    print("-" * 58)

    grand_budget = grand_actual = 0.0
    for cat in sorted(totals):
        b = totals[cat]["budget"]
        a = totals[cat]["actual"]
        pct = (a - b) / b * 100
        arrow = "▲" if pct > 0 else "▼"
        print(f"{cat:<22} {b:>12,.0f} {a:>12,.0f}  {arrow}{abs(pct):.1f}%")
        grand_budget += b
        grand_actual += a

    total_pct = (grand_actual - grand_budget) / grand_budget * 100
    arrow = "▲" if total_pct > 0 else "▼"
    print("-" * 58)
    print(f"{'TOTAL':<22} {grand_budget:>12,.0f} {grand_actual:>12,.0f}  {arrow}{abs(total_pct):.1f}%")


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"{DATA_FILE} not found — run: python scripts/generate_data.py")

    rows = load(DATA_FILE)
    validate(rows)
    summarize_by_category(rows)


if __name__ == "__main__":
    main()
