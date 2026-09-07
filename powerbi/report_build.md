# Power BI report build

Open `CampusOps.pbip` in Power BI Desktop, use the ODBC connection in `queries/CampusOps_Model.m`, apply `theme.json`, load the tables, create the relationships below, and add the DAX from `dax/Measures.dax`. The package is source-controlled so semantic/report changes can be reviewed alongside SQL definitions.

## Model

Use single-direction relationships from `dim_term` to facts on `term_key`, `dim_academic_org` to facts on `org_key`, and `dim_student` to `fact_enrollment` on `student_key`. Relate `Date[Date]` to `dim_term[start_date]`. Keep all KPI logic in measures; do not add calculated columns for aggregations. Hide surrogate keys from report view. Set default aggregation to **Do not summarize** for keys and **Sum** only for additive measures.

## Pages

| Page | Audience and decision | Visuals and interactions |
| --- | --- | --- |
| Executive overview | Provost, Finance, Deans: are enrollment, capacity, and pressure on plan? | KPI cards: Active Enrollment, Variance %, Course Fill Rate, Highest Resource Pressure. Trend line by term, department variance bar, capacity-pressure scatter, target line at 1.00. Slicers: academic term, college, department, modality, scenario. Pressure card turns amber above 0.85 and red above 1.00. |
| Diagnostic | Registrar and Department Heads: where is intervention needed? | Matrix: term × department with active students, withdrawals, credits, fill rate, variance, pressure rank. Conditional formatting for negative variance and pressure. Tooltip page shows source timestamp, calculation definition, and data-quality status. |
| Trends | Deans and IRE: how is demand changing? | Active enrollment line by department, period-over-period change bar, credit-hour trend, segment matrix for level/residency. Use the Date table for all time axes and show current/prior term comparisons. |
| Detail drill-through | Department Heads: what specific department/term should be reviewed? | Drill-through fields: department and term. Detail table for course sections, planned scenario, capacity gaps, and resource pressure components. Include a back button and department-context card. |
| Data quality | Data stewards: can this release be trusted? | Reconciliation table with source, curated, reporting, tolerance and status; data-quality pass-rate card; refresh timestamp; exception count. Filter only by refresh/term where applicable. |
| Definitions & help | All users: what do metrics mean and how should they be used? | KPI catalog table, calculation/grain/owner/source fields, report navigation, privacy/suppression note, and link to repository documentation. |

## Tooltip and formatting rules

- Use report-page tooltips with metric definition, owner, grain, source date, and preceding-term change.
- Apply `Enrollment Variance %`: green >= 0%, amber between -10% and 0%, red < -10%.
- Apply `Highest Resource Pressure`: green <= 0.85, amber > 0.85 to 1.00, red > 1.00.
- Suppress small cells in accordance with the charter before publishing; do not expose pseudonymous student keys in report views or exports.
