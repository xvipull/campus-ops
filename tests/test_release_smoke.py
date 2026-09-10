"""Release smoke checks for representative analytics-query performance and outcomes."""
import sqlite3
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pipeline import DATABASE, build_database, clean_sources


class ReleaseSmokeTests(unittest.TestCase):
    def test_representative_views_are_fast_and_reconciled(self):
        stage, _, _ = clean_sources()
        build_database(stage)
        with sqlite3.connect(DATABASE) as connection:
            started = time.perf_counter()
            reconciliation = connection.execute("SELECT COUNT(*) FROM vw_reconciliation WHERE reconciliation_status = 'FAIL'").fetchone()[0]
            pressure = connection.execute("SELECT org_code FROM vw_resource_pressure WHERE pressure_rank = 1 ORDER BY scenario_name").fetchall()
            elapsed = time.perf_counter() - started
        self.assertEqual(reconciliation, 0)
        self.assertEqual(pressure, [("CS",), ("CS",)])
        self.assertLess(elapsed, 1.0)


if __name__ == "__main__":
    unittest.main()
