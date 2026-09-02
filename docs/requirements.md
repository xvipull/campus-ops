# Project Charter & Requirements

## University Enrollment, Retention & Resource Planning BI

**Sponsor:** Provost and Chief Financial Officer

**Product owner:** Institutional Research & Effectiveness (IRE)

**Version:** 0.1 — discovery baseline
**Purpose:** Provide a trusted, governed business-intelligence product for campus leaders to understand enrollment performance, student persistence, and the resource implications of academic demand.

## Business problem

Enrollment, student-success, course-scheduling, and financial planning data are currently spread across admissions, the student information system (SIS), learning systems, departmental spreadsheets, and finance reports. Definitions differ by office and reporting is frequently retrospective. Leaders need a common view of the enrollment pipeline and student progression early enough to adjust recruitment, advising, course capacity, and budget plans.

## Stakeholder personas

| Persona | Primary needs | Decisions enabled |
| --- | --- | --- |
| Registrar | Accurate census enrollment, registrations, withdrawals, and course demand | Section additions/cancellations, registration interventions, official reporting reconciliation |
| Dean | Program, college, and cohort performance with actionable retention signals | Resource allocation, program review, student-success interventions, faculty workload planning |
| Finance leader | Forecast enrollment, net tuition, instructional cost, and budget variance | Revenue assumptions, annual budget allocations, scenario planning |
| Department Head | Major/course demand, capacity, persistence, and student bottlenecks | Course schedule, staffing requests, curriculum and advising actions |

## Decisions the product must support

1. Is the institution on track against term enrollment and net-tuition targets by campus, college, program, and student level?
2. Which recruitment funnel stages, markets, and programs require intervention to improve conversion and yield?
3. Which first-year and continuing-student cohorts are at risk of not persisting, and where should advising/support capacity be targeted?
4. What course sections, seats, faculty effort, and operating resources are required under baseline and approved enrollment scenarios?
5. Where do actual enrollment, instructional capacity, and budget outcomes diverge from plan?

## Scope

### In scope

- Term-level admissions funnel, enrollment, persistence/retention, completions, and course-capacity reporting.
- Governed KPI definitions, source lineage, data-quality checks, and refresh status.
- Drill paths by term, campus, college, department, program, student level, modality, residency, and approved demographic categories.
- Scenario inputs for enrollment and instructional-resource planning.
- Power BI semantic model/report designs and controlled Excel exports.

### Out of scope

- Replacing the SIS, CRM, LMS, finance system, or course scheduling system.
- Individual-level automated intervention decisions, predictive decisions, or student-facing recommendations.
- Admissions application adjudication, financial-aid packaging, payroll, and payroll allocation.
- Unapproved demographic profiling, public release of small-cell results, and real-time operational transaction processing.

## Functional requirements

1. Display actuals, prior term/year, target, and variance for every approved KPI.
2. Support term/census-date controls and preserve official reporting snapshots.
3. Enforce role-based access: institution/college/department levels as authorized.
4. Provide downloadable approved aggregates only; exports must respect security and suppression rules.
5. Show source refresh timestamp, data-quality status, and metric definition link on reports.
6. Retain reproducible transformation SQL/code and test evidence for published metrics.

## Data owners and refresh cadence

| Domain | System of record | Accountable data owner | Planned refresh |
| --- | --- | --- | --- |
| Admissions funnel | CRM / admissions system | VP Enrollment Management | Daily, weekdays at 06:00 local |
| Student enrollment, registration, academic history | SIS | Registrar | Daily at 06:00; official census snapshot per term |
| Retention and completions | SIS / degree audit | Registrar with IRE stewardship | Daily during term; certified after term close |
| Course inventory and capacity | SIS scheduling | Registrar | Daily during registration; weekly otherwise |
| Finance and budget | ERP / planning system | Controller / Budget Office | Monthly close; planning scenarios on approval |
| Faculty workload / instructional capacity | Faculty affairs / workload system | Provost Office | Weekly during planning cycle |

## Security, privacy, and compliance

- Treat student-level data as FERPA-protected. Apply least-privilege role-based access and institutional SSO/MFA.
- Do not store student names, IDs, contact details, or raw transactional extracts in Git. Production storage must be encrypted in transit and at rest.
- Aggregate/suppress results for cells below the institution-approved threshold (default: fewer than 10 students) and restrict sensitive demographic detail.
- Maintain access reviews, audit logs, approved retention schedules, and documented data-sharing agreements.
- Any predictive or risk modeling requires separate governance, bias/privacy review, human oversight, and written sponsor approval.

## Measurable acceptance criteria

| ID | Criterion | Measure |
| --- | --- | --- |
| AC-01 | KPI reconciliation | Census enrollment and registered credits reconcile to Registrar-certified totals within 0.5% for the three latest closed terms. |
| AC-02 | Refresh reliability | At least 95% of scheduled daily refreshes complete by 08:00 local over a rolling 60-day period. |
| AC-03 | Metric consistency | All published KPIs link to an approved catalog definition, owner, source, grain, and calculation. |
| AC-04 | Access control | 100% of test personas can access only their authorized organizational scope; no unauthorized student-level export is possible. |
| AC-05 | Privacy protection | Automated suppression tests pass for every published aggregate containing a small cell. |
| AC-06 | Decision usability | In UAT, each persona completes its three priority decision scenarios with at least 90% task success and no severity-1 defect. |
| AC-07 | Data quality | Required source completeness is at least 99% and duplicate student-term records are zero after certification. |

## Delivery governance

IRE owns metric governance and release sign-off. Registrar certifies official enrollment and academic-history measures. Finance certifies financial/budget measures. The product owner chairs a monthly metric-change review; material definition changes are versioned and communicated before release.
