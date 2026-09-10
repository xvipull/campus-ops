# Business Insights and Recommendations

## Synthetic-release findings

1. **Computer Science is the highest planning risk.** Its composite pressure is 1.80 in the baseline and 1.95 in the 10% growth scenario. Faculty pressure (4.33 baseline / 4.77 growth) drives the rank, while course-section and room pressure remain below 1.00.
2. **Business Administration has recurring enrollment-plan variance.** It is 50% below the modeled forecast in Fall 2025 and Fall 2026, though its baseline composite pressure is below 1.00. Staffing decisions should not assume the forecast will materialize without demand validation.
3. **Course fill is not the only capacity signal.** The modeled CS fill rate is strong, but faculty SCH capacity creates pressure. Review staffing/workload before adding rooms or sections.
4. **Quality controls are release-ready for the synthetic sample.** All three source-to-curated-to-reporting controls reconcile, and all seven raw datasets retain rows through standardization.

## Recommendations

1. Prioritize a CS faculty-capacity review: validate workload assumptions, qualified adjunct availability, and course release commitments before the next schedule build.
2. Require Business Administration to refresh forecast assumptions before increasing sections or assigning incremental faculty effort.
3. Use the 10% growth scenario as a discussion input, not a forecast commitment; add course-level demand/waitlist data before operational scheduling.
4. Establish a monthly metric-governance review and a term-specific resource-planning checkpoint before registration opens.

## Limitations and next steps

The sample is intentionally small and synthetic. It does not model real applicant behavior, course prerequisites, faculty qualifications, room time conflicts, financial-aid discounting, or causal retention drivers. Next steps are to onboard certified source feeds, approve access/suppression rules, add historical course-demand and waitlist detail, validate scenario capacity assumptions, and perform production persona/RBAC UAT.
