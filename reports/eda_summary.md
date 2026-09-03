# EDA Summary

The data is synthetic; findings validate analytic behavior rather than institutional performance.

## Data health

- Required fact fields missing: 0%.
- Expected missingness in the prior-term window metric: 33%; first observations have no prior period and are not data defects.
- IQR credit-hour outliers flagged for review: 3; none are removed by EDA.
- Reconciliation controls passing: 3/3.

## Business-driver exploration

- `enrollment_trend.png` shows active enrollment changes by department over time.
- `capacity_plan_driver.png` compares seat utilization to enrollment-plan variance; marker size represents planned net tuition and color identifies department.
- Correlations below are directional only because the synthetic sample is deliberately small.

```
                         fill_rate_pct  enrollment_variance_pct  active_students  net_tuition_amount
fill_rate_pct                     1.00                    -0.16             0.28                0.42
enrollment_variance_pct          -0.16                     1.00             0.27               -0.28
active_students                   0.28                     0.27             1.00                0.84
net_tuition_amount                0.42                    -0.28             0.84                1.00
```
