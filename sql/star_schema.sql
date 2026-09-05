PRAGMA foreign_keys = ON;

-- Dimensions use integer surrogate keys; source codes remain unique business keys.
CREATE TABLE dim_term (
  term_key INTEGER PRIMARY KEY, term_code TEXT NOT NULL UNIQUE, term_name TEXT NOT NULL,
  start_date TEXT NOT NULL, census_date TEXT NOT NULL, term_status TEXT NOT NULL
);
CREATE TABLE dim_academic_org (
  org_key INTEGER PRIMARY KEY, org_code TEXT NOT NULL UNIQUE, org_name TEXT NOT NULL,
  college_name TEXT NOT NULL, org_level TEXT NOT NULL
);
CREATE TABLE dim_student (
  student_key INTEGER PRIMARY KEY, student_business_key TEXT NOT NULL UNIQUE,
  student_level TEXT NOT NULL, residency TEXT NOT NULL
);
-- Grain: one student, term, academic organization, and source snapshot.
CREATE TABLE fact_enrollment (
  enrollment_key INTEGER PRIMARY KEY, student_key INTEGER NOT NULL, term_key INTEGER NOT NULL,
  org_key INTEGER NOT NULL, enrollment_status TEXT NOT NULL, registered_credit_hours REAL NOT NULL,
  snapshot_date TEXT NOT NULL, UNIQUE(student_key,term_key,org_key,snapshot_date),
  FOREIGN KEY(student_key) REFERENCES dim_student(student_key), FOREIGN KEY(term_key) REFERENCES dim_term(term_key), FOREIGN KEY(org_key) REFERENCES dim_academic_org(org_key)
);
-- Grain: one section in one term and source snapshot.
CREATE TABLE fact_course_section (
  course_section_key INTEGER PRIMARY KEY, section_business_key TEXT NOT NULL, term_key INTEGER NOT NULL,
  org_key INTEGER NOT NULL, subject_code TEXT NOT NULL, modality TEXT NOT NULL, available_seats INTEGER NOT NULL,
  enrolled_seats INTEGER NOT NULL, snapshot_date TEXT NOT NULL, UNIQUE(section_business_key,term_key,snapshot_date),
  FOREIGN KEY(term_key) REFERENCES dim_term(term_key), FOREIGN KEY(org_key) REFERENCES dim_academic_org(org_key)
);
-- Grain: one approved planning scenario for a term and academic organization.
CREATE TABLE fact_plan (
  plan_key INTEGER PRIMARY KEY, term_key INTEGER NOT NULL, org_key INTEGER NOT NULL, scenario_version TEXT NOT NULL,
  enrollment_forecast INTEGER NOT NULL, net_tuition_amount REAL NOT NULL, available_sch_forecast REAL NOT NULL,
  UNIQUE(term_key,org_key,scenario_version), FOREIGN KEY(term_key) REFERENCES dim_term(term_key), FOREIGN KEY(org_key) REFERENCES dim_academic_org(org_key)
);
-- Control totals captured at ingest for SQL reconciliation; one row per metric.
CREATE TABLE control_source_totals (
  metric_name TEXT PRIMARY KEY, source_value REAL NOT NULL, tolerance REAL NOT NULL,
  source_snapshot_date TEXT NOT NULL
);
-- Governed scenario inputs; grain: term, academic organization, named scenario.
CREATE TABLE fact_resource_scenario (
  scenario_key INTEGER PRIMARY KEY, term_key INTEGER NOT NULL, org_key INTEGER NOT NULL,
  scenario_name TEXT NOT NULL, demand_growth_pct REAL NOT NULL, planned_sections INTEGER NOT NULL,
  faculty_fte REAL NOT NULL, sch_capacity_per_fte REAL NOT NULL, room_count INTEGER NOT NULL,
  room_slots_per_room INTEGER NOT NULL, room_seats INTEGER NOT NULL,
  UNIQUE(term_key, org_key, scenario_name),
  FOREIGN KEY(term_key) REFERENCES dim_term(term_key), FOREIGN KEY(org_key) REFERENCES dim_academic_org(org_key)
);
-- Persisted decision-support output; calculations remain reproducible in vw_resource_pressure.
CREATE TABLE fact_resource_pressure (
  resource_pressure_key INTEGER PRIMARY KEY, scenario_key INTEGER NOT NULL UNIQUE,
  baseline_enrollment REAL NOT NULL, projected_enrollment REAL NOT NULL, baseline_sch REAL NOT NULL,
  projected_sch REAL NOT NULL, required_sections INTEGER NOT NULL, course_section_pressure REAL NOT NULL,
  faculty_pressure REAL NOT NULL, room_pressure REAL NOT NULL, composite_pressure_score REAL NOT NULL,
  pressure_rank INTEGER NOT NULL,
  FOREIGN KEY(scenario_key) REFERENCES fact_resource_scenario(scenario_key)
);
