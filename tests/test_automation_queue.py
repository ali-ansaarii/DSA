from __future__ import annotations

import unittest

from automation.run_queue import build_queue_plan
from automation import state


class QueuePlanTests(unittest.TestCase):
    def test_build_queue_plan_classifies_missing_existing_and_deferred_items(self) -> None:
        pending = ["KMP", "Hash Table", "Trie", "Selection Sort"]
        plan = build_queue_plan(
            pending,
            available_run_ids={
                "KMP": "kmp",
                "Trie": "trie",
                "Selection Sort": "selection-sort",
            },
            existing_run_states={
                "trie": state.STATE_MANUAL_ATTENTION,
                "selection-sort": state.STATE_DONE,
            },
            limit=1,
        )
        self.assertEqual(
            [(entry.label, entry.status) for entry in plan],
            [
                ("KMP", "runnable"),
                ("Hash Table", "missing_catalog"),
                ("Trie", "blocked_existing_run"),
                ("Selection Sort", "stale_checklist"),
            ],
        )

    def test_build_queue_plan_marks_aliases_as_covered_and_respects_limit(self) -> None:
        pending = ["KMP", "KMP Prefix Function", "Merge Sort"]
        plan = build_queue_plan(
            pending,
            available_run_ids={
                "KMP": "kmp",
                "KMP Prefix Function": "kmp",
                "Merge Sort": "merge-sort",
            },
            existing_run_states={},
            limit=1,
        )
        self.assertEqual(plan[0].status, "runnable")
        self.assertEqual(plan[1].status, "covered_by_alias")
        self.assertEqual(plan[2].status, "deferred_by_limit")


if __name__ == "__main__":
    unittest.main()
