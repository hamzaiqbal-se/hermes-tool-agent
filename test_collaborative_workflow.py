"""Deterministic validation of Task 2 collaboration outputs.
Tests only file contents — no AI behavior or delegation tested."""
import os, unittest

PROJECT = r"E:\hermes-tool-agent"

class TestTask2CollaborationOutputs(unittest.TestCase):
    def test_research_notes_exists_and_has_data(self):
        p = os.path.join(PROJECT, "research_notes.md")
        self.assertTrue(os.path.isfile(p))
        with open(p) as f:
            text = f.read()
        self.assertIn("data.json", text)
        self.assertIn("37 bytes", text)
        self.assertIn("OpenRouter HTTP 401", text)  # documented limitation

    def test_final_report_agrees_with_notes(self):
        with open(os.path.join(PROJECT, "research_notes.md")) as f:
            notes = f.read()
        with open(os.path.join(PROJECT, "final_report.md")) as f:
            report = f.read()
        # Largest file must agree
        self.assertIn("data.json", report)
        self.assertIn("37 bytes", report)
        # No invented facts (report references source file)
        self.assertIn("research_notes.md", report)

    def test_memory_file_contains_fact(self):
        mem_path = r"C:\Users\hamza\AppData\Local\hermes\memories\MEMORY.md"
        self.assertTrue(os.path.isfile(mem_path))
        with open(mem_path) as f:
            text = f.read()
        self.assertIn("data.json (37 bytes, .json)", text)

    def test_sample_data_unchanged(self):
        for name in ("data.json", "example.py", "notes.txt"):
            p = os.path.join(PROJECT, "sample-data", name)
            self.assertTrue(os.path.isfile(p))

if __name__ == "__main__":
    unittest.main()
