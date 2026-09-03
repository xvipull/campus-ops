import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pipeline
from pipeline import assert_fresh, assert_no_duplicates, assert_null_threshold, category, decimal, parse_date, pseudonymize, read_raw


class PipelineUnitTests(unittest.TestCase):
    def test_date_standardizes_us_format(self):
        self.assertEqual(parse_date(" 08/25/2026 ", "d"), "2026-08-25")

    def test_invalid_category_fails(self):
        with self.assertRaises(ValueError): category("Maybe", {"YES": "Yes"}, "status")

    def test_negative_range_fails(self):
        with self.assertRaises(ValueError): decimal("-1", "credits")

    def test_pseudonym_is_stable_and_not_identifier(self):
        self.assertEqual(pseudonymize("S-1001"), pseudonymize("S-1001"))
        self.assertNotIn("S-1001", pseudonymize("S-1001"))

    def test_stale_feed_fails(self):
        with self.assertRaises(ValueError): assert_fresh([{"source_updated_at": "2026-01-01"}], "feed", date(2026, 9, 1))

    def test_duplicate_business_key_fails(self):
        with self.assertRaises(ValueError):
            assert_no_duplicates([{"id": "A"}, {"id": "A"}], ["id"], "sample")

    def test_null_threshold_fails(self):
        with self.assertRaises(ValueError):
            assert_null_threshold([{"required": ""}], "sample")

    def test_missing_required_source_column_fails(self):
        original = pipeline.RAW
        with tempfile.TemporaryDirectory() as directory:
            pipeline.RAW = Path(directory)
            (pipeline.RAW / "terms.csv").write_text("term_code\nFALL26\n", encoding="utf-8")
            with self.assertRaises(ValueError): read_raw("terms.csv")
        pipeline.RAW = original


if __name__ == "__main__": unittest.main()
