# Data Dictionary

File: `data/manufacturing_variance.csv`

---

## Columns

### Month
Format: `YYYY-MM`  
Range: `2024-01` to `2024-12`

### Product_Line
Two product lines:
- `Sealing Systems` — heat-sealing equipment and components
- `Welding Components` — thermoplastic welding tooling and assemblies

### Cost_Category

| Category | What it covers |
|---|---|
| Raw Materials | Polymer granules, films, adhesive components |
| Direct Labor | Production floor wages and shift premiums |
| Machine Overhead | Depreciation, energy costs, tooling wear |
| Packaging | Cartons, trays, protective materials per shipment |
| Quality Inspection | Testing, calibration, QC personnel time |
| Logistics | Inbound freight, outbound delivery, warehouse handling |

### Budget_EUR
Monthly planned cost in EUR. Set at start of fiscal year, per category and product line.

### Actual_EUR
Actual cost incurred in the month. Rounded to 2 decimal places.

### Variance_EUR
`Actual_EUR - Budget_EUR`  
Positive = over budget. Negative = under budget.

### Variance_Pct
`(Variance_EUR / Budget_EUR) × 100`  
Rounded to 2 decimal places.

### Over_Budget
`Yes` if `Variance_EUR > 0`, otherwise `No`.  
Convenience flag used for Qlik filter pane and conditional coloring.

---

## Monthly budget by category and product line (EUR)

| Category | Sealing Systems | Welding Components |
|---|---|---|
| Raw Materials | 45,000 | 38,000 |
| Direct Labor | 28,000 | 24,000 |
| Machine Overhead | 18,000 | 15,000 |
| Packaging | 8,000 | 6,500 |
| Quality Inspection | 5,000 | 4,200 |
| Logistics | 9,500 | 7,800 |
