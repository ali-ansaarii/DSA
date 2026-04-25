from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from automation.checklist import mark_algorithm_done


class ChecklistTests(unittest.TestCase):
    def test_mark_algorithm_done_updates_multiple_occurrences(self) -> None:
        original = """# Checklist

- [ ] Trie
- [x] KMP
## Section
- [ ] Trie
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            checklist_path = Path(temp_dir) / "ALGORITHM_CHECKLIST.md"
            checklist_path.write_text(original, encoding="utf-8")
            updated = mark_algorithm_done(checklist_path, "Trie")
            self.assertEqual(updated, 2)
            self.assertEqual(
                checklist_path.read_text(encoding="utf-8"),
                """# Checklist

- [x] Trie
- [x] KMP
## Section
- [x] Trie
""",
            )


if __name__ == "__main__":
    unittest.main()
