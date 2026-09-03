"""Purposeful EDA for enrollment, capacity, and data-health drivers.

Run after src/run_pipeline.py. Outputs are intentionally limited to three decision-ready PNGs.
"""
from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "reports" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(ROOT / "data" / "campus_ops.db") as connection:
    trend = pd.read_sql_query("SELECT * FROM vw_kpi_enrollment_trend ORDER BY start_date, org_code", connection)
    capacity = pd.read_sql_query("SELECT p.*, c.fill_rate_pct FROM vw_kpi_plan_vs_actual p JOIN vw_kpi_course_capacity c ON c.term_code=p.term_code AND c.org_code=p.org_code ORDER BY p.start_date", connection)
    enrollment = pd.read_sql_query("SELECT registered_credit_hours, enrollment_status FROM fact_enrollment", connection)
    reconciliation = pd.read_sql_query("SELECT * FROM vw_reconciliation", connection)

# Trend: primary executive signal, split by academic organization.
fig, ax = plt.subplots(figsize=(8, 4.5))
for org, values in trend.groupby("org_code"):
    ax.plot(values["term_name"], values["active_students"], marker="o", linewidth=2, label=org)
ax.set(title="Active enrollment trend by department", ylabel="Active students", xlabel="Term")
ax.legend(title="Department"); ax.grid(axis="y", alpha=.25); fig.tight_layout()
fig.savefig(FIGURES / "enrollment_trend.png", dpi=160); plt.close(fig)

# Driver view: fill rate versus enrollment variance, sized by planned tuition.
fig, ax = plt.subplots(figsize=(7, 4.5))
for org, values in capacity.groupby("org_code"):
    ax.scatter(values["fill_rate_pct"], values["enrollment_variance_pct"], s=np.maximum(values["net_tuition_amount"] / 50, 40), alpha=.75, label=org)
ax.axhline(0, color="gray", linewidth=.8); ax.set(title="Capacity utilization vs. enrollment-plan variance", xlabel="Course fill rate (%)", ylabel="Enrollment variance (%)")
ax.legend(title="Department"); fig.tight_layout()
fig.savefig(FIGURES / "capacity_plan_driver.png", dpi=160); plt.close(fig)

# Distribution/outlier check. IQR is deliberately recorded, not used to discard data.
q1, q3 = enrollment["registered_credit_hours"].quantile([.25, .75])
iqr = q3 - q1
outliers = int(((enrollment["registered_credit_hours"] < q1 - 1.5 * iqr) | (enrollment["registered_credit_hours"] > q3 + 1.5 * iqr)).sum())
fig, ax = plt.subplots(figsize=(7, 4.5))
for status, values in enrollment.groupby("enrollment_status"):
    ax.hist(values["registered_credit_hours"], bins=np.arange(0, 19, 3), alpha=.65, label=status)
ax.set(title="Registered credit-hour distribution", xlabel="Credit hours", ylabel="Student-term records")
ax.legend(); fig.tight_layout(); fig.savefig(FIGURES / "credit_hour_distribution.png", dpi=160); plt.close(fig)

# Missingness is evaluated from curated SQLite fields; database schema makes required fields non-null.
base_missingness = enrollment.isna().mean()
window_metric_missingness = trend["prior_term_active_students"].isna().mean()
correlation = capacity[["fill_rate_pct", "enrollment_variance_pct", "active_students", "net_tuition_amount"]].corr(numeric_only=True).round(2)
summary = ["# EDA Summary", "", "The data is synthetic; findings validate analytic behavior rather than institutional performance.", "", "## Data health", "", f"- Required fact fields missing: {base_missingness.max():.0%}.", f"- Expected missingness in the prior-term window metric: {window_metric_missingness:.0%}; first observations have no prior period and are not data defects.", f"- IQR credit-hour outliers flagged for review: {outliers}; none are removed by EDA.", f"- Reconciliation controls passing: {(reconciliation.reconciliation_status == 'PASS').sum()}/{len(reconciliation)}.", "", "## Business-driver exploration", "", "- `enrollment_trend.png` shows active enrollment changes by department over time.", "- `capacity_plan_driver.png` compares seat utilization to enrollment-plan variance; marker size represents planned net tuition and color identifies department.", "- Correlations below are directional only because the synthetic sample is deliberately small.", "", "```", correlation.to_string(), "```", ""]
(ROOT / "reports" / "eda_summary.md").write_text("\n".join(summary), encoding="utf-8")
