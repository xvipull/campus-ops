-- Demand/capacity scenario engine. Pressure above 1.00 indicates demand exceeds capacity.
CREATE VIEW vw_resource_pressure AS
WITH base AS (
  SELECT s.scenario_key, t.term_code, t.term_name, t.start_date, o.org_code, o.org_name, s.scenario_name,
         s.demand_growth_pct, s.planned_sections, s.faculty_fte, s.sch_capacity_per_fte,
         s.room_count, s.room_slots_per_room, s.room_seats,
         COALESCE(e.active_students, 0) AS baseline_enrollment,
         COALESCE(e.active_credit_hours, 0) AS baseline_sch,
         COALESCE(e.active_students, 0) * (1 + s.demand_growth_pct) AS projected_enrollment,
         COALESCE(e.active_credit_hours, 0) * (1 + s.demand_growth_pct) AS projected_sch
  FROM fact_resource_scenario s JOIN dim_term t ON t.term_key=s.term_key JOIN dim_academic_org o ON o.org_key=s.org_key
  LEFT JOIN vw_kpi_enrollment_term_org e ON e.term_code=t.term_code AND e.org_code=o.org_code
), pressure AS (
  SELECT *,
         CAST(projected_enrollment / room_seats AS INTEGER) + CASE WHEN projected_enrollment > CAST(projected_enrollment / room_seats AS INTEGER) * room_seats THEN 1 ELSE 0 END AS required_sections,
         ROUND((CAST(projected_enrollment / room_seats AS INTEGER) + CASE WHEN projected_enrollment > CAST(projected_enrollment / room_seats AS INTEGER) * room_seats THEN 1 ELSE 0 END) * 1.0 / planned_sections, 4) AS course_section_pressure,
         ROUND(projected_sch / (faculty_fte * sch_capacity_per_fte), 4) AS faculty_pressure,
         ROUND((CAST(projected_enrollment / room_seats AS INTEGER) + CASE WHEN projected_enrollment > CAST(projected_enrollment / room_seats AS INTEGER) * room_seats THEN 1 ELSE 0 END) * 1.0 / (room_count * room_slots_per_room), 4) AS room_pressure
  FROM base
), scored AS (
  SELECT *, ROUND(0.40 * course_section_pressure + 0.35 * faculty_pressure + 0.25 * room_pressure, 4) AS composite_pressure_score
  FROM pressure
)
SELECT *, DENSE_RANK() OVER (PARTITION BY term_code, scenario_name ORDER BY composite_pressure_score DESC) AS pressure_rank
FROM scored;
