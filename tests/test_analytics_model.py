import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pipeline import DATABASE, build_database, clean_sources


class AnalyticsModelTests(unittest.TestCase):
    def test_kpi_layer_and_reconciliation_are_queryable(self):
        stage, _, _ = clean_sources()
        build_database(stage)
        with sqlite3.connect(DATABASE) as connection:
            passed, total = connection.execute("SELECT SUM(reconciliation_status = 'PASS'), COUNT(*) FROM vw_reconciliation").fetchone()
            self.assertEqual((passed, total), (3, 3))
            self.assertGreater(connection.execute("SELECT COUNT(*) FROM vw_kpi_enrollment_trend").fetchone()[0], 0)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM exception_over_capacity").fetchone()[0], 0)
            pressure_rows, baseline_rows = connection.execute("SELECT COUNT(*), SUM(scenario_name = 'BASELINE') FROM vw_resource_pressure").fetchone()
            self.assertEqual((pressure_rows, baseline_rows), (6, 3))
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM fact_resource_pressure WHERE composite_pressure_score > 1").fetchone()[0], 2)
            self.assertEqual(connection.execute("SELECT MIN(pressure_rank) FROM fact_resource_pressure").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()
