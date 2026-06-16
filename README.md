# Manufacturing Cost Variance Analysis

> Manufacturing cost variance dashboard built in Qlik Sense using synthetic ERP-style data.

![License](https://img.shields.io/badge/license-MIT-blue)
![Qlik Sense](https://img.shields.io/badge/BI-Qlik%20Sense-green)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![Status](https://img.shields.io/badge/status-Complete-success)

---

## Dashboard Preview

![Full Dashboard](dashboard/screenshots/full_dashboard.png)

---

## Business Problem

Manufacturing controllers frequently rely on Excel-based variance reports to compare budgeted and actual costs.

These reports are:
- Manual
- Time-consuming
- Difficult to explore interactively

This dashboard provides a self-service view of manufacturing cost performance, enabling users to identify overspending categories and variance trends with a few clicks.

---

## Solution

Built a Qlik Sense dashboard that enables:

- Budget vs Actual analysis
- Cost variance monitoring
- Monthly trend analysis
- Product line filtering
- Cost category drill-down

---

## Dataset

Synthetic manufacturing dataset containing:

| Metric | Value |
|----------|----------|
| Months | 12 |
| Product Lines | 2 |
| Cost Categories | 6 |
| Records | 144 |

### Data Fields

| Field | Description |
|---------|---------|
| Month | Reporting month |
| Product_Line | Product family |
| Cost_Category | Cost type |
| Budget_EUR | Planned spend |
| Actual_EUR | Actual spend |
| Variance_EUR | Actual - Budget |
| Variance_Pct | Variance percentage |
| Over_Budget | Yes/No indicator |

---

## Dashboard Components

### KPI Overview

Tracks:

- Total Budget
- Total Actual
- Variance (€)
- Variance (%)

Conditional formatting highlights unfavorable variances.

![KPI Strip](dashboard/screenshots/kpi_strip.png)

---

### Budget vs Actual by Cost Category

Compares planned and actual spending across categories.

![Variance by Category](dashboard/screenshots/variance_by_category.png)

Key finding:

- Raw Materials contributed the largest budget overrun.

---

### Monthly Variance Trend

Shows variance performance over time.

![Monthly Trend](dashboard/screenshots/monthly_trend.png)

Key finding:

- Raw Materials peaked during Q3.
- Direct Labor savings partially offset overspending.

---

## Key Insights

| Insight | Impact |
|----------|----------|
| Raw Materials exceeded budget by 3.3% | Largest variance driver |
| Direct Labor finished 2.1% under budget | Offset part of overrun |
| Packaging increased steadily throughout the year | Emerging risk |
| Total annual variance was +1.2% | Overall budget miss |

---

## Technology Stack

- Qlik Sense
- Python 3.10+
- CSV Data Source
- GitHub

---

## Repository Structure

```text
Manufacturing-Cost-Variance-Analysis/
│
├── data/
│   └── manufacturing_variance.csv
│
├── dashboard/
│   ├── Manufacturing_Cost_Variance_Dashboard.pdf
│   └── screenshots/
│       ├── full_dashboard.png
│       ├── kpi_strip.png
│       ├── variance_by_category.png
│       └── monthly_trend.png
│
├── scripts/
│   ├── generate_data.py
│   └── prepare_data.py
│
├── qlik/
│   └── Manufacturing_Cost_Variance.qvf
│
├── README.md
└── LICENSE
