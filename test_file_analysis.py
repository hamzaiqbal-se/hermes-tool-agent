import os
import unittest
import tempfile
import shutil
from file_analysis_agent import scan_directory, format_report

class TestFileAnalysisAgent(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.files = {
            "a.txt": b"Hello world",
            "b.py": b"print('hi')" * 100,
            "c.md": b"# Title",
            "d": b"",  # no extension
            "sub/e.json": b'{"x":1}',
        }
        for rel_path, content in self.files.items():
            abs_path = os.path.join(self.test_dir, rel_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "wb") as f:
                f.write(content)
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    def test_scan_directory_counts(self):
        result = scan_directory(self.test_dir)
        self.assertEqual(result["total_files"], 5)
        self.assertEqual(result["extensions"], {
            ".txt": 1, ".py": 1, ".md": 1, "(no extension)": 1, ".json": 1
        })
        largest_size, largest_path = result["largest_files"][0]
        self.assertTrue(largest_path.endswith("b.py"))
        self.assertGreater(largest_size, 0)
    def test_format_report(self):
        result = scan_directory(self.test_dir)
        report = format_report(result)
        self.assertIn("Total files: 5", report)
        self.assertIn(".py:", report)
        self.assertIn("Largest files:", report)
    def test_invalid_directory(self):
        with self.assertRaises(ValueError):
            scan_directory("/nonexistent/path/xyz123")
    def test_empty_directory(self):
        empty_dir = tempfile.mkdtemp()
        try:
            result = scan_directory(empty_dir)
            self.assertEqual(result["total_files"], 0)
            self.assertEqual(result["extensions"], {})
            self.assertEqual(result["largest_files"], [])
        finally:
            shutil.rmtree(empty_dir)
if __name__ == "__main__":
    unittest.main()
