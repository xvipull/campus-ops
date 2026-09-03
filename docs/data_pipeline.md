# Data Pipeline & Analytics Model

## Dataset

The repository uses a compact **synthetic university operations dataset** that models Registrar, academic-organization, enrollment, course-capacity, and financial-plan extracts. It exists to make the pipeline runnable without FERPA-regulated data. It is not a claim about institutional performance and must be replaced only through approved secure ingestion.

## Runbook

```bash
python3 src/run_pipeline.py
python3 -m unittest discover -s tests -v
```

The pipeline preserves `data/raw/*.csv` unchanged; standardizes into `data/staging/*.csv`; replaces the reproducible SQLite database `data/campus_ops.db`; and regenerates `reports/data_quality.md`.

## Transformation ledger

| Source | Cleaning / standardization | Key handling |
| --- | --- | --- |
| Terms | Trim/case normalize codes; parse ISO or US dates; map term statuses | `term_code` retained as business key; `dim_term.term_key` is surrogate |
| Academic organizations | Trim/case normalize org codes; standardize organization level | `org_code` retained; `dim_academic_org.org_key` is surrogate |
| Students | Standardize level/residency; parse update date | Source ID is SHA-256 pseudonymized before staging; database uses surrogate `student_key` |
| Enrollment | Normalize status; parse dates; numeric credits; reject negatives | Business grain: student/term/org/snapshot |
| Course sections | Normalize section, subject and modality; integer seats; reject over-capacity | Business grain: section/term/snapshot |
| Financial plan | Normalize scenario; parse currency/forecast values | Business grain: term/org/scenario |

## Quality controls

The pipeline fails before database load if any source has missing columns, nulls above 0%, duplicate business keys, invalid category/date/numeric ranges, broken references, an update older than 45 days, or failed row/value reconciliation. The generated report documents each successful run.

## Star model

`fact_enrollment`, `fact_course_section`, and `fact_plan` join through conformed `dim_term` and `dim_academic_org`; enrollment also joins `dim_student`. Schema DDL declares foreign keys, unique business grains, and integer surrogate keys. See `sql/star_schema.sql` for executable definitions.
