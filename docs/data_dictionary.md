# Data Dictionary

This is a logical dictionary for curated analytics tables. Physical source fields, transformations, and lineage will be maintained alongside each pipeline. No production student data belongs in this repository.

| Entity / field | Type | Definition | Source owner | Sensitivity |
| --- | --- | --- | --- | --- |
| `dim_term.term_key` | string | Stable surrogate key for an academic term. | Registrar | Internal |
| `dim_term.census_date` | date | Official enrollment snapshot date for the term. | Registrar | Internal |
| `dim_academic_org.org_key` | string | Effective-dated college/department/program organization key. | Registrar / Provost | Internal |
| `dim_academic_org.org_level` | string | Organizational level: college, department, or program. | Registrar / Provost | Internal |
| `dim_student.student_key` | string | Pseudonymous analytic key; never a source student ID. | Registrar | FERPA restricted |
| `dim_student.student_level` | string | Approved level, e.g., undergraduate or graduate. | Registrar | FERPA restricted |
| `fact_admission.application_key` | string | Pseudonymous application record key. | Enrollment Management | FERPA restricted |
| `fact_admission.application_status` | string | Standardized funnel status as of snapshot. | Enrollment Management | FERPA restricted |
| `fact_enrollment.enrollment_status` | string | Registrar-defined active/withdrawn/canceled status. | Registrar | FERPA restricted |
| `fact_enrollment.registered_credit_hours` | decimal(6,2) | Credit hours registered at snapshot. | Registrar | FERPA restricted |
| `fact_course_section.available_seats` | integer | Published seat capacity after approved adjustments. | Registrar | Internal |
| `fact_course_section.enrolled_seats` | integer | Active enrolled seats at snapshot. | Registrar | FERPA restricted aggregate |
| `fact_persistence.eligible_flag` | boolean | Indicates inclusion under approved persistence denominator rules. | IRE / Registrar | FERPA restricted |
| `fact_finance.net_tuition_amount` | decimal(18,2) | Finance-certified net tuition amount in institutional currency. | Finance | Confidential |
| `fact_plan.enrollment_forecast` | integer | Approved scenario forecast for census enrollment. | IRE / Finance | Confidential |
| `fact_plan.available_sch_forecast` | decimal(12,2) | Planned available student credit-hour capacity. | Registrar / Provost | Confidential |

## Data-quality rules

- Every enrollment record must map to one valid term and effective-dated academic organization.
- Curated student-term rows must be unique by `student_key`, `term_key`, and official snapshot type.
- Values for seats, credits, and forecast inputs must be non-negative unless an approved accounting adjustment is documented.
- Referential-integrity failures, stale feeds, and missing required values are surfaced before publication.
