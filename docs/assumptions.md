# Assumptions, Risks & Dependencies

## Working assumptions

1. The institution has authoritative CRM, SIS, ERP/planning, course-scheduling, and faculty-workload sources and can provide approved extracts or read-only interfaces.
2. Registrar will define the official census calendar, enrollment statuses, eligibility populations, and historical corrections policy.
3. IRE can maintain an effective-dated academic organization hierarchy and crosswalk discontinued/renamed programs.
4. Finance will provide an approved net-tuition allocation method and forecast scenario versions.
5. Source systems expose stable keys sufficient for pseudonymization and historical matching.
6. Initial release uses batch refresh; real-time analytics are not required.
7. Data access is approved through institutional privacy/security governance before onboarding each domain.

## Risks and mitigations

| Risk | Impact | Mitigation | Owner |
| --- | --- | --- | --- |
| Conflicting definitions across offices | Loss of trust and inconsistent decisions | Versioned KPI catalog and cross-functional metric approval | IRE |
| Late or incomplete source feeds | Stale dashboards and missed interventions | Refresh monitoring, data-quality gates, fallback status messaging | Source data owner |
| FERPA/privacy exposure | Regulatory and student harm | RBAC, pseudonymization, suppression, audit logs, secure environments | Information Security / IRE |
| Small cohorts create volatile rates | Misleading comparisons | Suppression, confidence/context flags, multi-term views | IRE |
| Organization changes break historical reporting | Incorrect trend analysis | Effective-dated hierarchy and documented restatement policy | Registrar / Provost |
| Forecast misuse as a commitment | Budget or staffing error | Label scenario version, owner, date, and confidence assumptions | Finance |
| Adoption varies by unit | Continued spreadsheet shadow reporting | Persona UAT, training, office hours, and defined report owners | Product owner |

## Dependencies and open decisions

- Confirm approved small-cell suppression threshold and permitted demographic dimensions.
- Select production data platform, orchestration mechanism, and identity-group mappings.
- Obtain documented retention/completion eligibility rules and historical backfill period.
- Approve budget allocation grain for college/program analysis.
- Establish report release calendar around registration, census, and monthly financial close.
- Validate faculty SCH/FTE capacity, room-slot availability, and organization-level scenario growth inputs before resource-planning publication.
