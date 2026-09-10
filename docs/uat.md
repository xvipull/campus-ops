# User Acceptance Testing

UAT uses the synthetic release dataset and is executed against the SQLite model, Excel companion, and Power BI source package. For production release, repeat each case with role-based access and certified institutional data.

| ID | Persona | Scenario / steps | Expected result | Evidence / status |
| --- | --- | --- | --- | --- |
| UAT-01 | Registrar | Run `python3 src/run_pipeline.py`; compare census/enrollment control totals to `vw_reconciliation`. | Source, curated, and reporting active enrollment, credit hours, and enrolled seats match tolerance; no reconciliation failures. | 3/3 controls PASS in `reports/data_quality.md` and `vw_reconciliation`. |
| UAT-02 | Registrar | Open the Data Quality page/sheet and inspect freshness, required fields, and reconciliation status. | All seven source datasets display successful controls and release data is current within 45 days. | PASS in generated quality report. |
| UAT-03 | Dean | Filter Fall 2026 and compare department enrollment and resource pressure. | Computer Science is shown as the highest-pressure department under baseline and growth scenarios. | CS composite pressure: 1.80 baseline, 1.95 at 10% growth. |
| UAT-04 | Finance | Review forecast versus active enrollment in the exception view. | Material negative enrollment variances are visible and use red conditional formatting. | Four planning exceptions are visible in Excel `Exceptions`. |
| UAT-05 | Department Head | Change an amber growth input in Excel `Scenarios` from 0% to 10%. | Projected enrollment, required sections, and composite pressure recalculate; no source data is overwritten. | Formula-linked scenario cells and validation allow 0%–50%. |
| UAT-06 | Department Head | Drill through from a Power BI department/term visual to detail. | Detail page retains the selected department and term and exposes section/planning/pressure context. | Configured in `powerbi/report_build.md`; validate after Desktop publish. |
| UAT-07 | IRE analyst | Inspect definitions/help and hover a report tooltip. | Metric definition, owner, grain, source date, and prior-period context are available. | DAX/report build specification and Excel Definitions sheet. |
| UAT-08 | Security reviewer | Attempt to locate names/source student IDs in the workbook or report package. | No direct student IDs/names are visible; only pseudonymous keys exist in controlled model data. | Source review PASS; required production RBAC/suppression test remains a go-live gate. |

## Exit criteria

Release acceptance requires all reconciliation controls passing, no severity-1 defects, correct role-scope behavior in production UAT, and at least 90% completion of each persona’s priority scenario. Known limitations and pending production access tests are documented in [assumptions.md](assumptions.md).
