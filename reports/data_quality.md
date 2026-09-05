# Data Quality Report

**Run date:** 2026-09-05

## Result

**PASS** — required-column, null-threshold, duplicate, range, referential-integrity, freshness, and reconciliation checks completed.

## Row reconciliation

| Dataset | Raw rows | Clean rows | Result |
| --- | ---: | ---: | --- |
| terms | 4 | 4 | PASS — 1:1 retained |
| academic_orgs | 3 | 3 | PASS — 1:1 retained |
| students | 8 | 8 | PASS — 1:1 retained |
| enrollment | 19 | 19 | PASS — 1:1 retained |
| course_sections | 9 | 9 | PASS — 1:1 retained |
| financial_plan | 9 | 9 | PASS — 1:1 retained |
| resource_scenarios | 6 | 6 | PASS — 1:1 retained |

## Value reconciliation

| Measure | Clean total | Result |
| --- | ---: | --- |
| enrollment_registered_credit_hours | 201.00 | PASS |
| financial_plan_net_tuition_amount | 160,000.00 | PASS |

## Controls

- Required columns: PASS for 7 source files.
- Null threshold: PASS; maximum permitted rate is 0% for required cleaned fields.
- Duplicate business keys: PASS.
- Invalid ranges: PASS; non-negative credits, seats, forecasts, and currency; enrolled seats do not exceed capacity.
- Referential integrity: PASS for term, academic organization, and student references.
- Freshness: PASS; each source has an update within 45 days.
- Raw-to-clean rows: PASS; all source rows are retained after standardization.
