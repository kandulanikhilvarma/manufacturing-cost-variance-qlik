# Manufacturing Cost Variance Analysis
**A Qlik Sense Case Study**

Dashboard built on synthetic manufacturing cost data. 12 months, 6 cost
categories, 2 product lines — budget vs. actual, designed to give a controller
one-click answers instead of a 20-minute Excel rebuild.

---

## The problem

Monthly variance reporting in manufacturing controlling usually lives in Excel:
budget vs. actual, manually color-coded, pasted into a slide for the month-end
meeting. When a manager asks "which cost center is running hot this quarter?"
finding the answer takes longer than it should.

This dashboard gives that answer in seconds — by category, by product line, by
month — with a click instead of a pivot table.

---

## Dataset

`data/manufacturing_variance.csv` — 144 rows.

| Column | Type | Description |
|---|---|---|
| Month | YYYY-MM | Reporting month |
| Product_Line | String | Sealing Systems / Welding Components |
| Cost_Category | String | Raw Materials, Direct Labor, Machine Overhead, Packaging, Quality Inspection, Logistics |
| Budget_EUR | Float | Monthly planned cost in EUR |
| Actual_EUR | Float | Actual spend in EUR |
| Variance_EUR | Float | Actual minus Budget |
| Variance_Pct | Float | Variance as % of Budget |
| Over_Budget | Yes/No | Filter flag for conditional coloring |

**Built-in variance patterns (realistic, not random noise):**

| Category | Pattern | Period |
|---|---|---|
| Raw Materials | +8 to +14% over budget | July–September |
| Direct Labor | −3 to −8% under budget | July–December |
| Packaging | ~0.5% monthly cost creep | Full year |
| Logistics | +5 to +11% over budget | October–December |
| Machine Overhead | Flat ±3% | Full year |
| Quality Inspection | Flat ±5% | Full year |

Full year result: **+1.2% over total budget** (€2,536,879 actual vs. €2,508,000 budget).

---

## Dashboard design

One screen. Three components.

**KPI strip (top row)**
Total Budget | Total Actual | Variance EUR | Variance % — color-coded green/red.
All four update instantly when any filter is applied.

**Bar chart — actual vs. budget by cost category**
Side-by-side bars. The gap is visible without reading numbers.
Clicking any bar cross-filters the trend line below it via Qlik's associative model.

**Line chart — monthly variance % trend by category**
Shows whether a category is improving or getting worse over time.
Raw Materials peaks in Q3 and comes back down — that's the story this dashboard tells.

**Filter pane (left side)**
Product Line | Cost Category | Month

One screen by design. A second drill-down sheet would be the natural next step
with real data, but for a demo it adds surface area without adding insight.

---

## What the numbers show

```
Category               Budget (€)   Actual (€)    Var %
----------------------------------------------------------
Direct Labor              624,000      610,644  ▼2.1%
Logistics                 207,600      210,621  ▲1.5%
Machine Overhead          396,000      397,354  ▲0.3%
Packaging                 174,000      178,667  ▲2.7%
Quality Inspection        110,400      110,318  ▼0.1%
Raw Materials             996,000    1,029,275  ▲3.3%
----------------------------------------------------------
TOTAL                   2,508,000    2,536,879  ▲1.2%
```

Raw Materials is the main story: 3.3% over for the year, concentrated in Q3.
Direct Labor savings (2.1% under) offset roughly half of that.
Packaging at 2.7% is the slow-burn problem — small monthly gaps that compound.

---

## How to run

```bash
# Regenerate the dataset
python scripts/generate_data.py

# Validate + print summary
python scripts/prepare_data.py
```

No pip dependencies. Python 3.10+ with stdlib only.

**To open the dashboard:** load `data/manufacturing_variance.csv` into
Qlik Sense Desktop as a new app (free trial at qlik.com).

---

## With real data

Swap the CSV for an SAP export or ERP extract. The data model stays the same.
Natural extensions: cost center dimension, rolling YTD vs. prior year, and
budget input fields to replace the static Budget_EUR column.

---

## Stack

- Qlik Sense Desktop (free — qlik.com/trial)
- Python 3.10+, stdlib only
- Dataset: synthetic, built for this demo
