"""
generate_data.py
Creates manufacturing_variance.csv — synthetic cost data for the variance dashboard.
Run once: python scripts/generate_data.py
"""

import csv
import random
from pathlib import Path

random.seed(42)

MONTHS = [
    "2024-01", "2024-02", "2024-03", "2024-04",
    "2024-05", "2024-06", "2024-07", "2024-08",
    "2024-09", "2024-10", "2024-11", "2024-12",
]

PRODUCT_LINES = ["Sealing Systems", "Welding Components"]

# Monthly budget per category per product line (EUR)
BUDGETS = {
    "Raw Materials":      {"Sealing Systems": 45000, "Welding Components": 38000},
    "Direct Labor":       {"Sealing Systems": 28000, "Welding Components": 24000},
    "Machine Overhead":   {"Sealing Systems": 18000, "Welding Components": 15000},
    "Packaging":          {"Sealing Systems": 8000,  "Welding Components": 6500},
    "Quality Inspection": {"Sealing Systems": 5000,  "Welding Components": 4200},
    "Logistics":          {"Sealing Systems": 9500,  "Welding Components": 7800},
}


def variance_factor(month_idx: int, category: str) -> float:
    """
    Returns a multiplier (actual / budget) per category and month.
    Patterns reflect realistic manufacturing dynamics:
      - Raw Materials: supply pressure in Q3 (Jul–Sep)
      - Direct Labor: efficiency gains H2 (Jul–Dec)
      - Packaging: slow cost creep across the year
      - Logistics: elevated Q4 (Oct–Dec peak)
    """
    if category == "Raw Materials":
        if 6 <= month_idx <= 8:
            return random.uniform(1.08, 1.14)
        return random.uniform(0.97, 1.03)

    if category == "Direct Labor":
        if month_idx >= 6:
            return random.uniform(0.92, 0.97)
        return random.uniform(0.98, 1.04)

    if category == "Machine Overhead":
        return random.uniform(0.98, 1.03)

    if category == "Packaging":
        creep = 1.0 + (month_idx * 0.005)
        return creep + random.uniform(-0.02, 0.02)

    if category == "Quality Inspection":
        return random.uniform(0.95, 1.05)

    if category == "Logistics":
        if month_idx >= 9:
            return random.uniform(1.05, 1.11)
        return random.uniform(0.97, 1.04)

    return 1.0


def build_rows() -> list[dict]:
    rows = []
    for month_idx, month in enumerate(MONTHS):
        for category, pl_budgets in BUDGETS.items():
            for product_line, budget in pl_budgets.items():
                factor = variance_factor(month_idx, category)
                actual = round(budget * factor, 2)
                variance_eur = round(actual - budget, 2)
                variance_pct = round((variance_eur / budget) * 100, 2)
                rows.append({
                    "Month": month,
                    "Product_Line": product_line,
                    "Cost_Category": category,
                    "Budget_EUR": budget,
                    "Actual_EUR": actual,
                    "Variance_EUR": variance_eur,
                    "Variance_Pct": variance_pct,
                    "Over_Budget": "Yes" if variance_eur > 0 else "No",
                })
    return rows


def main():
    output = Path("data/manufacturing_variance.csv")
    output.parent.mkdir(exist_ok=True)
    rows = build_rows()

    fieldnames = [
        "Month", "Product_Line", "Cost_Category",
        "Budget_EUR", "Actual_EUR", "Variance_EUR", "Variance_Pct", "Over_Budget",
    ]

    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Written {len(rows)} rows to {output}")


if __name__ == "__main__":
    main()
