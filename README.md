# campus-ops

Business intelligence foundation for **University Enrollment, Retention & Resource Planning**. The project turns admissions, student-record, finance, and instructional-capacity data into governed metrics and decision-ready reporting.

## Product outcomes

- Monitor enrollment funnel health, yield, census enrollment, and persistence.
- Identify student cohorts and programs where retention intervention is most needed.
- Align instructional capacity and budget planning with forecast demand.

## Architecture

```text
Admissions / SIS / LMS / Finance / HR
                 |
                 v
           data/raw (restricted extracts)
                 |
                 v
     data/staging + sql transformations
                 |
                 v
      curated semantic model / KPI definitions
                 |
          +------+------+
          |             |
          v             v
       Power BI       Excel exports
          |             |
          +------> reports <------+
```

## Repository guide

| Location | Purpose |
| --- | --- |
| `docs/` | Charter, requirements, KPI definitions, data dictionary, and assumptions |
| `data/raw/` | Access-controlled source extracts; never commit identifiable student data |
| `data/staging/` | Standardized, non-production staging outputs |
| `sql/` | Transformation and validation SQL |
| `src/` | Reusable transformation/application code |
| `notebooks/` | Exploratory and analytical notebooks |
| `tests/` | Data-quality and transformation tests |
| `powerbi/` | Power BI model and report assets |
| `excel/` | Controlled Excel templates and exports |
| `reports/` | Published report artifacts and release notes |

## Documentation

- [Project requirements and charter](docs/requirements.md)
- [KPI catalog](docs/kpi_catalog.md)
- [Data dictionary](docs/data_dictionary.md)
- [Assumptions and risks](docs/assumptions.md)
- [Pipeline, controls, and star model](docs/data_pipeline.md)

## Report screenshots

> Placeholder — Enrollment executive overview

`reports/screenshots/enrollment-overview.png`

> Placeholder — Retention and persistence view

`reports/screenshots/retention-cohorts.png`

> Placeholder — Resource planning view

`reports/screenshots/resource-plan.png`

## Getting started

1. Review the governed definitions in `docs/` before building reports.
2. Store production source extracts only in approved secure locations; use synthetic or de-identified samples locally.
3. Add transformations to `sql/` or `src/` and accompanying checks to `tests/`.

## Data handling

This repository must not contain FERPA-regulated student records, direct identifiers, credentials, or confidential financial data. See the security requirements in the project charter.
