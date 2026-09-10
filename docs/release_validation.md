# Release Validation Evidence

## Reproducibility check

Executed on 2026-09-10 from the repository root:

```text
python3 src/run_pipeline.py                 PASS
python3 -m unittest discover -s tests -v    PASS (9 tests)
```

The pipeline rebuilt staging tables, `data/campus_ops.db`, the data-quality report, and the resource-pressure report from checked-in synthetic raw data.

## Reconciliation evidence

| Metric | Source | Curated | Reporting | Tolerance | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Active enrollment rows | 16 | 16 | 16 | 0 | PASS |
| Active credit hours | 192.00 | 192.00 | 192.00 | 0.01 | PASS |
| Enrolled seats | 245 | 245 | 245 | 0 | PASS |

The authoritative generated detail is [reports/data_quality.md](../reports/data_quality.md).

## Performance and edge-case checks

- Pipeline run: sub-second for the checked-in synthetic release sample.
- Representative SQLite KPI/reconciliation queries complete in under one second on the release database.
- Automated tests cover malformed dates, invalid categories, negative numeric ranges, duplicate business keys, null threshold failure, stale feeds, missing required fields, pseudonym stability, KPI-layer queryability, reconciliation, no over-capacity output, scenario row counts, and pressure ranking.

These figures are release smoke-checks, not production capacity benchmarks. Production performance testing should use representative extracts, concurrent Power BI load, refresh-volume SLAs, and the managed data platform.
