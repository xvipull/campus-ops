# KPI Catalog

All rates use the approved census/snapshot date for the selected term unless stated otherwise. IRE governs definitions; official values require data-owner certification.

| KPI | Definition & formula | Grain / dimensions | Owner | Refresh |
| --- | --- | --- | --- | --- |
| Applications | Distinct submitted applications for an entry term; exclude withdrawn/incomplete applications per policy. | applicant × entry term; campus, program, market | Enrollment Management | Daily |
| Admit rate | `admitted applicants / complete applicants × 100`. | entry term, campus, program, market | Enrollment Management | Daily |
| Yield rate | `enrolled new students / admitted students × 100`. | entry term, campus, program | Enrollment Management / Registrar | Daily |
| Census enrollment | Distinct active students enrolled at official census; follow Registrar enrollment status rules. | student × term; college, department, program, level, modality | Registrar | Certified each term |
| Credit hours | Sum of registered credit hours for active enrollments at snapshot. | student-course × term | Registrar | Daily / census certified |
| Course fill rate | `enrolled seats / available seats × 100`; canceled sections excluded. | section × term; department, subject, modality | Registrar | Daily |
| Fall-to-fall retention | `eligible first-time cohort enrolled next fall / eligible first-time cohort in initial fall × 100`. | entry cohort; college, program, demographics (subject to suppression) | IRE / Registrar | Annually after census |
| Term persistence | `eligible students enrolled in next primary term / eligible students in current primary term × 100`. | student cohort × term | IRE / Registrar | Daily / term certified |
| Completion rate | `cohort members awarded credential within approved time window / cohort members × 100`. | entry cohort, award program | IRE / Registrar | Term close |
| Net tuition revenue | Recognized gross tuition and mandatory fees less institutionally funded discounts; follow Finance close rules. | term/month; college/program where allocated | Finance | Monthly close |
| Enrollment forecast variance | `(actual census enrollment - approved forecast) / approved forecast × 100`. | term, campus, college, program | IRE / Finance | Daily / census certified |
| Instructional capacity gap | `forecast student credit hours - planned available student credit hours`. Positive means planned capacity is short. | term, department, subject, modality | Registrar / Provost Office | Weekly planning |

## Common conventions

- “Student” means a distinct institutional student identifier after de-duplication; no identifier is exposed in public outputs.
- Primary terms are defined by the academic calendar and maintained by the Registrar.
- Program, college, and department attribution uses the effective-dated academic organization mapping for the reporting term.
- All comparisons show the snapshot date and whether figures are preliminary or certified.
