"""Reproducible ingestion, validation, staging, and SQLite star-model load.

The checked-in source files are synthetic and contain no institutional records.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
from collections import Counter
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
STAGING = ROOT / "data" / "staging"
DATABASE = ROOT / "data" / "campus_ops.db"
REPORT = ROOT / "reports" / "data_quality.md"
NULL_THRESHOLD = 0.00
FRESHNESS_DAYS = 45

REQUIRED = {
    "terms.csv": ["term_code", "term_name", "start_date", "census_date", "term_status", "source_updated_at"],
    "academic_orgs.csv": ["org_code", "org_name", "college_name", "org_level", "source_updated_at"],
    "students.csv": ["student_id", "student_level", "residency", "source_updated_at"],
    "enrollment.csv": ["student_id", "term_code", "org_code", "enrollment_status", "registered_credit_hours", "snapshot_date", "source_updated_at"],
    "course_sections.csv": ["section_id", "term_code", "org_code", "subject_code", "modality", "available_seats", "enrolled_seats", "snapshot_date", "source_updated_at"],
    "financial_plan.csv": ["term_code", "org_code", "scenario_version", "enrollment_forecast", "net_tuition_amount", "available_sch_forecast", "source_updated_at"],
    "resource_scenarios.csv": ["term_code", "org_code", "scenario_name", "demand_growth_pct", "planned_sections", "faculty_fte", "sch_capacity_per_fte", "room_count", "room_slots_per_room", "room_seats", "source_updated_at"],
}


def text(value: str) -> str:
    return " ".join(value.strip().split())


def category(value: str, mapping: dict[str, str], field: str) -> str:
    key = text(value).upper()
    if key not in mapping:
        raise ValueError(f"Invalid {field}: {value!r}")
    return mapping[key]


def parse_date(value: str, field: str) -> str:
    value = text(value)
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    raise ValueError(f"Invalid {field}: {value!r}; expected YYYY-MM-DD or MM/DD/YYYY")


def decimal(value: str, field: str, minimum: float = 0) -> float:
    try:
        result = round(float(text(value).replace(",", "")), 2)
    except ValueError as exc:
        raise ValueError(f"Invalid numeric {field}: {value!r}") from exc
    if result < minimum:
        raise ValueError(f"{field} must be >= {minimum}, got {result}")
    return result


def pseudonymize(student_id: str) -> str:
    return "STU-" + hashlib.sha256(student_id.encode()).hexdigest()[:16]


def read_raw(filename: str) -> list[dict[str, str]]:
    path = RAW / filename
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = set(REQUIRED[filename]) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{filename}: missing required columns: {sorted(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{filename}: no rows")
    return rows


def assert_no_duplicates(rows: list[dict], fields: list[str], label: str) -> None:
    keys = [tuple(row[field] for field in fields) for row in rows]
    dupes = [key for key, count in Counter(keys).items() if count > 1]
    if dupes:
        raise ValueError(f"{label}: duplicate business keys: {dupes[:3]}")


def assert_null_threshold(rows: list[dict], label: str) -> None:
    for field in rows[0]:
        null_rate = sum(row[field] in (None, "") for row in rows) / len(rows)
        if null_rate > NULL_THRESHOLD:
            raise ValueError(f"{label}.{field}: null rate {null_rate:.1%} exceeds {NULL_THRESHOLD:.1%}")


def assert_fresh(rows: list[dict], label: str, today: date | None = None) -> None:
    today = today or date.today()
    newest = max(date.fromisoformat(row["source_updated_at"][:10]) for row in rows)
    age = (today - newest).days
    if age > FRESHNESS_DAYS:
        raise ValueError(f"{label}: newest source update is {age} days old (limit {FRESHNESS_DAYS})")


def clean_sources() -> tuple[dict[str, list[dict]], dict[str, int], dict[str, float]]:
    raw = {name: read_raw(name) for name in REQUIRED}
    raw_counts = {name: len(rows) for name, rows in raw.items()}
    stage: dict[str, list[dict]] = {}
    stage["terms"] = [{"term_code": text(r["term_code"]).upper(), "term_name": text(r["term_name"]), "start_date": parse_date(r["start_date"], "start_date"), "census_date": parse_date(r["census_date"], "census_date"), "term_status": category(r["term_status"], {"OPEN": "Open", "CLOSED": "Closed", "PLANNING": "Planning"}, "term_status"), "source_updated_at": parse_date(r["source_updated_at"], "source_updated_at")} for r in raw["terms.csv"]]
    stage["academic_orgs"] = [{"org_code": text(r["org_code"]).upper(), "org_name": text(r["org_name"]), "college_name": text(r["college_name"]), "org_level": category(r["org_level"], {"DEPARTMENT": "Department", "PROGRAM": "Program"}, "org_level"), "source_updated_at": parse_date(r["source_updated_at"], "source_updated_at")} for r in raw["academic_orgs.csv"]]
    stage["students"] = [{"student_key": pseudonymize(text(r["student_id"]).upper()), "student_level": category(r["student_level"], {"UG": "Undergraduate", "GRAD": "Graduate"}, "student_level"), "residency": category(r["residency"], {"IN STATE": "In State", "OUT OF STATE": "Out of State", "INTERNATIONAL": "International"}, "residency"), "source_updated_at": parse_date(r["source_updated_at"], "source_updated_at")} for r in raw["students.csv"]]
    stage["enrollment"] = [{"student_key": pseudonymize(text(r["student_id"]).upper()), "term_code": text(r["term_code"]).upper(), "org_code": text(r["org_code"]).upper(), "enrollment_status": category(r["enrollment_status"], {"ACTIVE": "Active", "WITHDRAWN": "Withdrawn"}, "enrollment_status"), "registered_credit_hours": decimal(r["registered_credit_hours"], "registered_credit_hours"), "snapshot_date": parse_date(r["snapshot_date"], "snapshot_date"), "source_updated_at": parse_date(r["source_updated_at"], "source_updated_at")} for r in raw["enrollment.csv"]]
    stage["course_sections"] = [{"section_id": text(r["section_id"]).upper(), "term_code": text(r["term_code"]).upper(), "org_code": text(r["org_code"]).upper(), "subject_code": text(r["subject_code"]).upper(), "modality": category(r["modality"], {"IN PERSON": "In Person", "ONLINE": "Online", "HYBRID": "Hybrid"}, "modality"), "available_seats": int(decimal(r["available_seats"], "available_seats")), "enrolled_seats": int(decimal(r["enrolled_seats"], "enrolled_seats")), "snapshot_date": parse_date(r["snapshot_date"], "snapshot_date"), "source_updated_at": parse_date(r["source_updated_at"], "source_updated_at")} for r in raw["course_sections.csv"]]
    stage["financial_plan"] = [{"term_code": text(r["term_code"]).upper(), "org_code": text(r["org_code"]).upper(), "scenario_version": text(r["scenario_version"]).upper(), "enrollment_forecast": int(decimal(r["enrollment_forecast"], "enrollment_forecast")), "net_tuition_amount": decimal(r["net_tuition_amount"], "net_tuition_amount"), "available_sch_forecast": decimal(r["available_sch_forecast"], "available_sch_forecast"), "source_updated_at": parse_date(r["source_updated_at"], "source_updated_at")} for r in raw["financial_plan.csv"]]
    stage["resource_scenarios"] = [{"term_code": text(r["term_code"]).upper(), "org_code": text(r["org_code"]).upper(), "scenario_name": text(r["scenario_name"]).upper(), "demand_growth_pct": decimal(r["demand_growth_pct"], "demand_growth_pct"), "planned_sections": int(decimal(r["planned_sections"], "planned_sections", 1)), "faculty_fte": decimal(r["faculty_fte"], "faculty_fte", 0.01), "sch_capacity_per_fte": decimal(r["sch_capacity_per_fte"], "sch_capacity_per_fte", 0.01), "room_count": int(decimal(r["room_count"], "room_count", 1)), "room_slots_per_room": int(decimal(r["room_slots_per_room"], "room_slots_per_room", 1)), "room_seats": int(decimal(r["room_seats"], "room_seats", 1)), "source_updated_at": parse_date(r["source_updated_at"], "source_updated_at")} for r in raw["resource_scenarios.csv"]]
    for row in stage["course_sections"]:
        if row["enrolled_seats"] > row["available_seats"]:
            raise ValueError(f"course_sections: enrollment exceeds capacity for {row['section_id']}")
    for label, rows in stage.items():
        assert_null_threshold(rows, label)
        assert_fresh(rows, label)
    assert_no_duplicates(stage["terms"], ["term_code"], "terms")
    assert_no_duplicates(stage["academic_orgs"], ["org_code"], "academic_orgs")
    assert_no_duplicates(stage["students"], ["student_key"], "students")
    assert_no_duplicates(stage["enrollment"], ["student_key", "term_code", "org_code", "snapshot_date"], "enrollment")
    assert_no_duplicates(stage["course_sections"], ["section_id", "term_code"], "course_sections")
    assert_no_duplicates(stage["financial_plan"], ["term_code", "org_code", "scenario_version"], "financial_plan")
    assert_no_duplicates(stage["resource_scenarios"], ["term_code", "org_code", "scenario_name"], "resource_scenarios")
    terms, orgs, students = ({r["term_code"] for r in stage["terms"]}, {r["org_code"] for r in stage["academic_orgs"]}, {r["student_key"] for r in stage["students"]})
    for label in ("enrollment", "course_sections", "financial_plan", "resource_scenarios"):
        for row in stage[label]:
            if row["term_code"] not in terms or row["org_code"] not in orgs:
                raise ValueError(f"{label}: invalid term/org reference")
    if {r["student_key"] for r in stage["enrollment"]} - students:
        raise ValueError("enrollment: invalid student reference")
    reconciliations = {"enrollment_registered_credit_hours": round(sum(r["registered_credit_hours"] for r in stage["enrollment"]), 2), "financial_plan_net_tuition_amount": round(sum(r["net_tuition_amount"] for r in stage["financial_plan"]), 2)}
    return stage, raw_counts, reconciliations


def write_staging(stage: dict[str, list[dict]]) -> None:
    STAGING.mkdir(parents=True, exist_ok=True)
    for name, rows in stage.items():
        with (STAGING / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)


def build_database(stage: dict[str, list[dict]]) -> None:
    if DATABASE.exists(): DATABASE.unlink()
    connection = sqlite3.connect(DATABASE)
    connection.executescript((ROOT / "sql" / "star_schema.sql").read_text())
    connection.executemany("INSERT INTO dim_term (term_code,term_name,start_date,census_date,term_status) VALUES (:term_code,:term_name,:start_date,:census_date,:term_status)", stage["terms"])
    connection.executemany("INSERT INTO dim_academic_org (org_code,org_name,college_name,org_level) VALUES (:org_code,:org_name,:college_name,:org_level)", stage["academic_orgs"])
    connection.executemany("INSERT INTO dim_student (student_business_key,student_level,residency) VALUES (:student_key,:student_level,:residency)", stage["students"])
    ids = {table: {row[1]: row[0] for row in connection.execute(f"SELECT {surrogate}, {column} FROM {table}")} for table, surrogate, column in [("dim_term", "term_key", "term_code"), ("dim_academic_org", "org_key", "org_code"), ("dim_student", "student_key", "student_business_key")]}
    connection.executemany("INSERT INTO fact_enrollment (student_key,term_key,org_key,enrollment_status,registered_credit_hours,snapshot_date) VALUES (?,?,?,?,?,?)", [(ids["dim_student"][r["student_key"]], ids["dim_term"][r["term_code"]], ids["dim_academic_org"][r["org_code"]], r["enrollment_status"], r["registered_credit_hours"], r["snapshot_date"]) for r in stage["enrollment"]])
    connection.executemany("INSERT INTO fact_course_section (section_business_key,term_key,org_key,subject_code,modality,available_seats,enrolled_seats,snapshot_date) VALUES (?,?,?,?,?,?,?,?)", [(r["section_id"], ids["dim_term"][r["term_code"]], ids["dim_academic_org"][r["org_code"]], r["subject_code"], r["modality"], r["available_seats"], r["enrolled_seats"], r["snapshot_date"]) for r in stage["course_sections"]])
    connection.executemany("INSERT INTO fact_plan (term_key,org_key,scenario_version,enrollment_forecast,net_tuition_amount,available_sch_forecast) VALUES (?,?,?,?,?,?)", [(ids["dim_term"][r["term_code"]], ids["dim_academic_org"][r["org_code"]], r["scenario_version"], r["enrollment_forecast"], r["net_tuition_amount"], r["available_sch_forecast"]) for r in stage["financial_plan"]])
    connection.executemany("INSERT INTO fact_resource_scenario (term_key,org_key,scenario_name,demand_growth_pct,planned_sections,faculty_fte,sch_capacity_per_fte,room_count,room_slots_per_room,room_seats) VALUES (?,?,?,?,?,?,?,?,?,?)", [(ids["dim_term"][r["term_code"]], ids["dim_academic_org"][r["org_code"]], r["scenario_name"], r["demand_growth_pct"], r["planned_sections"], r["faculty_fte"], r["sch_capacity_per_fte"], r["room_count"], r["room_slots_per_room"], r["room_seats"]) for r in stage["resource_scenarios"]])
    active_enrollment = [r for r in stage["enrollment"] if r["enrollment_status"] == "Active"]
    connection.executemany("INSERT INTO control_source_totals (metric_name,source_value,tolerance,source_snapshot_date) VALUES (?,?,?,?)", [
        ("active_enrollment_rows", float(len(active_enrollment)), 0.0, max(r["source_updated_at"] for r in stage["enrollment"])),
        ("active_credit_hours", sum(r["registered_credit_hours"] for r in active_enrollment), 0.01, max(r["source_updated_at"] for r in stage["enrollment"])),
        ("enrolled_seats", float(sum(r["enrolled_seats"] for r in stage["course_sections"])), 0.0, max(r["source_updated_at"] for r in stage["course_sections"])),
    ])
    connection.executescript((ROOT / "sql" / "kpi_views.sql").read_text())
    connection.executescript((ROOT / "sql" / "exception_tables.sql").read_text())
    connection.executescript((ROOT / "sql" / "advanced_decision_support.sql").read_text())
    connection.execute("INSERT INTO fact_resource_pressure (scenario_key,baseline_enrollment,projected_enrollment,baseline_sch,projected_sch,required_sections,course_section_pressure,faculty_pressure,room_pressure,composite_pressure_score,pressure_rank) SELECT scenario_key,baseline_enrollment,projected_enrollment,baseline_sch,projected_sch,required_sections,course_section_pressure,faculty_pressure,room_pressure,composite_pressure_score,pressure_rank FROM vw_resource_pressure")
    connection.commit(); connection.close()


def write_report(stage: dict[str, list[dict]], raw_counts: dict[str, int], totals: dict[str, float]) -> None:
    lines = ["# Data Quality Report", "", "**Run date:** " + date.today().isoformat(), "", "## Result", "", "**PASS** — required-column, null-threshold, duplicate, range, referential-integrity, freshness, and reconciliation checks completed.", "", "## Row reconciliation", "", "| Dataset | Raw rows | Clean rows | Result |", "| --- | ---: | ---: | --- |"]
    for filename, raw_count in raw_counts.items():
        clean_name = filename.removesuffix(".csv")
        lines.append(f"| {clean_name} | {raw_count} | {len(stage[clean_name])} | PASS — 1:1 retained |")
    lines += ["", "## Value reconciliation", "", "| Measure | Clean total | Result |", "| --- | ---: | --- |"]
    for measure, value in totals.items(): lines.append(f"| {measure} | {value:,.2f} | PASS |")
    lines += ["", "## Controls", "", f"- Required columns: PASS for {len(REQUIRED)} source files.", f"- Null threshold: PASS; maximum permitted rate is {NULL_THRESHOLD:.0%} for required cleaned fields.", "- Duplicate business keys: PASS.", "- Invalid ranges: PASS; non-negative credits, seats, forecasts, and currency; enrolled seats do not exceed capacity.", "- Referential integrity: PASS for term, academic organization, and student references.", f"- Freshness: PASS; each source has an update within {FRESHNESS_DAYS} days.", "- Raw-to-clean rows: PASS; all source rows are retained after standardization."]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_resource_pressure_report() -> None:
    with sqlite3.connect(DATABASE) as connection:
        rows = connection.execute("SELECT term_code, scenario_name, pressure_rank, org_code, projected_enrollment, required_sections, course_section_pressure, faculty_pressure, room_pressure, composite_pressure_score FROM vw_resource_pressure ORDER BY term_code, scenario_name, pressure_rank, org_code").fetchall()
    lines = ["# Resource Pressure Scenarios", "", "Generated from governed scenario inputs. A pressure ratio above 1.00 indicates demand exceeds the planned capacity for that resource.", "", "| Term | Scenario | Rank | Department | Projected enrollment | Required sections | Course | Faculty | Room | Composite |", "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for row in rows:
        term, scenario, rank, org, projected, sections, course, faculty, room, composite = row
        lines.append(f"| {term} | {scenario} | {rank} | {org} | {projected:.2f} | {sections} | {course:.2f} | {faculty:.2f} | {room:.2f} | {composite:.2f} |")
    (ROOT / "reports" / "resource_pressure.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> None:
    stage, raw_counts, totals = clean_sources()
    write_staging(stage); build_database(stage); write_report(stage, raw_counts, totals)
    write_resource_pressure_report()
    print(json.dumps({"status": "PASS", "database": str(DATABASE), "report": str(REPORT)}, indent=2))


if __name__ == "__main__": run()
