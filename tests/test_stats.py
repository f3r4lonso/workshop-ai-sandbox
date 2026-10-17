import os
import tempfile
import unittest

from csvsummary.stats import format_summary, read_rows, summarize

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "data", "sample.csv")


class StatsTests(unittest.TestCase):
    def test_numeric_columns_only(self):
        summary = summarize(read_rows(SAMPLE))
        self.assertEqual(list(summary), ["price", "volume"])

    def test_values(self):
        price = summarize(read_rows(SAMPLE))["price"]
        self.assertEqual(price["count"], 5)
        self.assertAlmostEqual(price["mean"], 102.0)
        self.assertAlmostEqual(price["median"], 101.5)

    def test_format(self):
        text = format_summary(summarize(read_rows(SAMPLE)))
        self.assertIn("price: count=5 mean=102.00 median=101.50", text)

    def test_column_with_text_is_skipped(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write("a,b\n1,x\n2,3\n")
        try:
            self.assertEqual(list(summarize(read_rows(f.name))), ["a"])
        finally:
            os.unlink(f.name)


if __name__ == "__main__":
    unittest.main()
