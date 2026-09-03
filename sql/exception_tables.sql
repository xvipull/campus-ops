-- Materialized exceptions are rebuilt after each load for operational follow-up.
CREATE TABLE exception_over_capacity AS
SELECT section_business_key, t.term_code, o.org_code, available_seats, enrolled_seats,
       enrolled_seats - available_seats AS seats_over_capacity
FROM fact_course_section c JOIN dim_term t ON t.term_key = c.term_key JOIN dim_academic_org o ON o.org_key = c.org_key
WHERE enrolled_seats > available_seats;

CREATE TABLE exception_plan_variance AS
SELECT * FROM vw_kpi_plan_vs_actual
WHERE ABS(enrollment_variance_pct) > 10.0 OR instructional_capacity_gap > 0;

-- Query expected to return zero rows for a certified run.
SELECT * FROM vw_reconciliation WHERE reconciliation_status = 'FAIL';
