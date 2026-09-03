-- Reusable semantic KPI layer. All views use certified fact-table snapshot rows.
CREATE VIEW vw_kpi_enrollment_term_org AS
SELECT t.term_code, t.term_name, t.start_date, o.org_code, o.org_name, o.college_name,
       COUNT(DISTINCT CASE WHEN f.enrollment_status = 'Active' THEN f.student_key END) AS active_students,
       COUNT(DISTINCT CASE WHEN f.enrollment_status = 'Withdrawn' THEN f.student_key END) AS withdrawn_students,
       ROUND(SUM(CASE WHEN f.enrollment_status = 'Active' THEN f.registered_credit_hours ELSE 0 END), 2) AS active_credit_hours,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN f.enrollment_status = 'Withdrawn' THEN f.student_key END) / NULLIF(COUNT(DISTINCT f.student_key), 0), 2) AS withdrawal_rate_pct
FROM fact_enrollment f JOIN dim_term t ON t.term_key = f.term_key JOIN dim_academic_org o ON o.org_key = f.org_key
GROUP BY t.term_key, o.org_key;

CREATE VIEW vw_kpi_enrollment_trend AS
WITH base AS (
  SELECT *, LAG(active_students) OVER (PARTITION BY org_code ORDER BY start_date) AS prior_term_active_students
  FROM vw_kpi_enrollment_term_org
)
SELECT *, active_students - prior_term_active_students AS active_student_change,
       ROUND(100.0 * (active_students - prior_term_active_students) / NULLIF(prior_term_active_students, 0), 2) AS active_student_change_pct
FROM base;

CREATE VIEW vw_kpi_course_capacity AS
SELECT t.term_code, t.term_name, t.start_date, o.org_code, o.org_name, c.modality,
       COUNT(*) AS section_count, SUM(c.available_seats) AS available_seats, SUM(c.enrolled_seats) AS enrolled_seats,
       ROUND(100.0 * SUM(c.enrolled_seats) / NULLIF(SUM(c.available_seats), 0), 2) AS fill_rate_pct
FROM fact_course_section c JOIN dim_term t ON t.term_key = c.term_key JOIN dim_academic_org o ON o.org_key = c.org_key
GROUP BY t.term_key, o.org_key, c.modality;

CREATE VIEW vw_kpi_plan_vs_actual AS
SELECT t.term_code, t.term_name, t.start_date, o.org_code, o.org_name, p.scenario_version,
       p.enrollment_forecast, e.active_students, e.active_credit_hours, p.available_sch_forecast,
       e.active_students - p.enrollment_forecast AS enrollment_variance,
       ROUND(100.0 * (e.active_students - p.enrollment_forecast) / NULLIF(p.enrollment_forecast, 0), 2) AS enrollment_variance_pct,
       e.active_credit_hours - p.available_sch_forecast AS instructional_capacity_gap,
       p.net_tuition_amount
FROM fact_plan p JOIN dim_term t ON t.term_key = p.term_key JOIN dim_academic_org o ON o.org_key = p.org_key
LEFT JOIN vw_kpi_enrollment_term_org e ON e.term_code = t.term_code AND e.org_code = o.org_code;

CREATE VIEW vw_kpi_student_segments AS
SELECT t.term_code, t.term_name, s.student_level, s.residency,
       COUNT(DISTINCT CASE WHEN f.enrollment_status = 'Active' THEN f.student_key END) AS active_students,
       ROUND(AVG(CASE WHEN f.enrollment_status = 'Active' THEN f.registered_credit_hours END), 2) AS avg_active_credit_hours
FROM fact_enrollment f JOIN dim_student s ON s.student_key = f.student_key JOIN dim_term t ON t.term_key = f.term_key
GROUP BY t.term_key, s.student_level, s.residency;

CREATE VIEW vw_kpi_cohort_persistence AS
WITH first_active AS (
  SELECT f.student_key, MIN(t.start_date) AS cohort_start_date
  FROM fact_enrollment f JOIN dim_term t ON t.term_key = f.term_key WHERE f.enrollment_status = 'Active'
  GROUP BY f.student_key
), cohort_terms AS (
  SELECT fa.student_key, t.term_code AS cohort_term, t.start_date AS cohort_start_date,
         (SELECT t2.term_key FROM dim_term t2 WHERE t2.start_date > t.start_date ORDER BY t2.start_date LIMIT 1) AS next_term_key
  FROM first_active fa JOIN dim_term t ON t.start_date = fa.cohort_start_date
)
SELECT ct.cohort_term, COUNT(*) AS cohort_students,
       SUM(CASE WHEN nxt.enrollment_status = 'Active' THEN 1 ELSE 0 END) AS persisted_students,
       ROUND(100.0 * SUM(CASE WHEN nxt.enrollment_status = 'Active' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS persistence_rate_pct
FROM cohort_terms ct LEFT JOIN fact_enrollment nxt ON nxt.student_key = ct.student_key AND nxt.term_key = ct.next_term_key
GROUP BY ct.cohort_term;

CREATE VIEW vw_reconciliation AS
WITH curated AS (
 SELECT 'active_enrollment_rows' AS metric_name, COUNT(*) * 1.0 AS curated_value FROM fact_enrollment WHERE enrollment_status = 'Active'
 UNION ALL SELECT 'active_credit_hours', ROUND(SUM(registered_credit_hours), 2) FROM fact_enrollment WHERE enrollment_status = 'Active'
 UNION ALL SELECT 'enrolled_seats', SUM(enrolled_seats) * 1.0 FROM fact_course_section
), reporting AS (
 SELECT 'active_enrollment_rows' AS metric_name, SUM(active_students) * 1.0 AS reporting_value FROM vw_kpi_enrollment_term_org
 UNION ALL SELECT 'active_credit_hours', ROUND(SUM(active_credit_hours), 2) FROM vw_kpi_enrollment_term_org
 UNION ALL SELECT 'enrolled_seats', SUM(enrolled_seats) * 1.0 FROM vw_kpi_course_capacity
)
SELECT s.metric_name, s.source_value, c.curated_value, r.reporting_value, s.tolerance,
       ROUND(c.curated_value - s.source_value, 4) AS source_to_curated_difference,
       ROUND(r.reporting_value - s.source_value, 4) AS source_to_reporting_difference,
       CASE WHEN ABS(c.curated_value - s.source_value) <= s.tolerance AND ABS(r.reporting_value - s.source_value) <= s.tolerance THEN 'PASS' ELSE 'FAIL' END AS reconciliation_status
FROM control_source_totals s JOIN curated c USING(metric_name) JOIN reporting r USING(metric_name);
