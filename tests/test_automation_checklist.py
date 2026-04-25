from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from automation.checklist import (
    find_inconsistent_labels,
    list_pending_labels,
    load_label_statuses,
    mark_algorithm_labels_done,
    mark_algorithm_done,
)


class ChecklistTests(unittest.TestCase):
    def test_load_label_statuses_preserves_first_occurrence_and_aggregates_duplicates(self) -> None:
        original = """# Checklist

- [x] Trie
- [ ] KMP
## Section
- [ ] Trie
- [ ] Hash Table
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            checklist_path = Path(temp_dir) / "ALGORITHM_CHECKLIST.md"
            checklist_path.write_text(original, encoding="utf-8")
            statuses = load_label_statuses(checklist_path)
            self.assertEqual([status.label for status in statuses], ["Trie", "KMP", "Hash Table"])
            self.assertTrue(statuses[0].is_inconsistent)
            self.assertEqual(statuses[0].checked_count, 1)
            self.assertEqual(statuses[0].unchecked_count, 1)
            self.assertEqual(statuses[1].first_line_number, 4)

    def test_list_pending_labels_deduplicates_by_label(self) -> None:
        original = """# Checklist

- [x] Trie
- [ ] KMP
## Section
- [ ] Trie
- [ ] Hash Table
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            checklist_path = Path(temp_dir) / "ALGORITHM_CHECKLIST.md"
            checklist_path.write_text(original, encoding="utf-8")
            self.assertEqual(
                list_pending_labels(checklist_path),
                ["Trie", "KMP", "Hash Table"],
            )
            self.assertEqual(find_inconsistent_labels(checklist_path), ["Trie"])

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

    def test_mark_algorithm_labels_done_updates_aliases(self) -> None:
        original = """# Checklist

- [ ] KMP
## String
- [ ] KMP Prefix Function
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            checklist_path = Path(temp_dir) / "ALGORITHM_CHECKLIST.md"
            checklist_path.write_text(original, encoding="utf-8")
            updated = mark_algorithm_labels_done(
                checklist_path,
                ["KMP", "KMP Prefix Function"],
            )
            self.assertEqual(updated, 2)
            self.assertEqual(
                checklist_path.read_text(encoding="utf-8"),
                """# Checklist

- [x] KMP
## String
- [x] KMP Prefix Function
""",
            )


if __name__ == "__main__":
    unittest.main()
