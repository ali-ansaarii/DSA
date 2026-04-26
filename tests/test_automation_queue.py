from __future__ import annotations

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from automation import specs
from automation.run_queue import build_queue_plan
from automation import state
from automation.run_queue import QueueRunner


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
            run_design_statuses={
                "kmp": "ready",
                "trie": "ready",
                "selection-sort": "ready",
            },
            existing_run_states={
                "trie": state.STATE_MANUAL_ATTENTION,
                "selection-sort": state.STATE_DONE,
            },
            existing_local_branches=set(),
            existing_remote_branches=set(),
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
            run_design_statuses={
                "kmp": "ready",
                "merge-sort": "ready",
            },
            existing_run_states={},
            existing_local_branches=set(),
            existing_remote_branches=set(),
            limit=1,
        )
        self.assertEqual(plan[0].status, "runnable")
        self.assertEqual(plan[1].status, "covered_by_alias")
        self.assertEqual(plan[2].status, "deferred_by_limit")

    def test_build_queue_plan_blocks_stale_local_and_remote_branches(self) -> None:
        pending = ["KMP", "Merge Sort"]
        plan = build_queue_plan(
            pending,
            available_run_ids={
                "KMP": "kmp",
                "Merge Sort": "merge-sort",
            },
            run_design_statuses={
                "kmp": "ready",
                "merge-sort": "ready",
            },
            existing_run_states={},
            existing_local_branches={"kmp"},
            existing_remote_branches={"merge-sort"},
            limit=2,
        )
        self.assertEqual(plan[0].status, "blocked_local_branch")
        self.assertEqual(plan[1].status, "blocked_remote_branch")

    def test_build_queue_plan_blocks_non_ready_design_entries(self) -> None:
        pending = ["Manacher", "KMP"]
        plan = build_queue_plan(
            pending,
            available_run_ids={
                "Manacher": "manacher",
                "KMP": "kmp",
            },
            run_design_statuses={
                "manacher": "needs_prompt_refinement",
                "kmp": "ready",
            },
            existing_run_states={},
            existing_local_branches=set(),
            existing_remote_branches=set(),
            limit=2,
        )
        self.assertEqual(plan[0].status, "blocked_design_not_ready")
        self.assertEqual(plan[1].status, "runnable")


class QueueRunnerBehaviorTests(unittest.TestCase):
    def test_run_single_algorithm_refreshes_base_branch_before_worktree(self) -> None:
        with TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            local_root = repo_root / ".local"
            local_root.mkdir()
            (local_root / "ALGORITHM_CHECKLIST.md").write_text("- [ ] Merge Sort\n", encoding="utf-8")
            catalog_path = repo_root / "catalog.json"
            catalog_path.write_text(
                json.dumps(
                    {
                        "Merge Sort": {
                            "checklist_label": "Merge Sort",
                            "topic_path": "sorting/MergeSort",
                            "display_name": "Merge Sort",
                            "algo_id": "MergeSort",
                            "binary_name": "merge-sort",
                            "time_flag": "time-merge-sort",
                            "branch_name": "merge-sort",
                            "pr_title": "Add Merge Sort",
                        },
                    }
                ),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                catalog=str(catalog_path),
                base_branch="main",
                local_root=str(local_root),
                limit=1,
                dry_run=False,
                stop_after=None,
                max_verification_fixes=3,
                max_review_fixes=3,
                max_review_request_attempts=3,
                poll_interval_seconds=120,
                review_request_pickup_timeout_seconds=90,
                review_timeout_seconds=1800,
            )
            runner = QueueRunner(repo_root, args)
            runner.catalog_specs = specs.load_catalog_specs(catalog_path)
            runner.catalog_specs_by_label = specs.load_catalog_specs_by_label(catalog_path)

            with (
                patch("automation.run_queue.git_ops.pull_base_ff_only") as pull_mock,
                patch("automation.run_queue.git_ops.add_detached_worktree"),
                patch("automation.run_queue.run_command") as run_command_mock,
                patch.object(QueueRunner, "_load_run_state", return_value=state.STATE_DONE),
                patch("automation.run_queue.git_ops.remove_worktree"),
                patch("automation.run_queue.shutil.rmtree"),
                patch("automation.run_queue.git_ops.delete_local_branch"),
                patch("automation.run_queue.git_ops.delete_remote_branch"),
            ):
                run_command_mock.return_value.returncode = 0
                run_command_mock.return_value.stdout = ""
                run_command_mock.return_value.stderr = ""
                result = runner._run_single_algorithm(runner.catalog_specs_by_label["Merge Sort"])

            self.assertEqual(result["final_state"], state.STATE_DONE)
            pull_mock.assert_called_once_with(repo_root, "main")

    def test_run_continues_after_blocked_result(self) -> None:
        with TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            local_root = repo_root / ".local"
            local_root.mkdir()
            (local_root / "ALGORITHM_CHECKLIST.md").write_text(
                "- [ ] Merge Sort\n- [ ] Quick Sort\n",
                encoding="utf-8",
            )
            catalog_path = repo_root / "catalog.json"
            catalog_path.write_text(
                json.dumps(
                    {
                        "Merge Sort": {
                            "checklist_label": "Merge Sort",
                            "topic_path": "sorting/MergeSort",
                            "display_name": "Merge Sort",
                            "algo_id": "MergeSort",
                            "binary_name": "merge-sort",
                            "time_flag": "time-merge-sort",
                            "branch_name": "merge-sort",
                            "pr_title": "Add Merge Sort",
                        },
                        "Quick Sort": {
                            "checklist_label": "Quick Sort",
                            "topic_path": "sorting/QuickSort",
                            "display_name": "Quick Sort",
                            "algo_id": "QuickSort",
                            "binary_name": "quick-sort",
                            "time_flag": "time-quick-sort",
                            "branch_name": "quick-sort",
                            "pr_title": "Add Quick Sort",
                        },
                    }
                ),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                catalog=str(catalog_path),
                base_branch="main",
                local_root=str(local_root),
                limit=2,
                dry_run=False,
                stop_after=None,
                max_verification_fixes=3,
                max_review_fixes=3,
                max_review_request_attempts=3,
                poll_interval_seconds=120,
                review_request_pickup_timeout_seconds=90,
                review_timeout_seconds=1800,
            )
            runner = QueueRunner(repo_root, args)
            runner.catalog_specs = specs.load_catalog_specs(catalog_path)
            runner.catalog_specs_by_label = specs.load_catalog_specs_by_label(catalog_path)

            with (
                patch("automation.run_queue.git_ops.ensure_clean_base_branch"),
                patch("automation.run_queue.git_ops.list_local_branches", return_value=set()),
                patch("automation.run_queue.git_ops.list_remote_branches", return_value=set()),
                patch.object(QueueRunner, "_load_existing_run_states", return_value={}),
                patch.object(
                    QueueRunner,
                    "_run_single_algorithm",
                    side_effect=[
                        {
                            "algorithm": "Merge Sort",
                            "final_state": state.STATE_MANUAL_ATTENTION,
                            "outcome": state.STATE_MANUAL_ATTENTION,
                        },
                        {
                            "algorithm": "Quick Sort",
                            "final_state": state.STATE_DONE,
                            "outcome": "success",
                        },
                    ],
                ) as run_single_mock,
            ):
                runner.run()

            self.assertEqual(run_single_mock.call_count, 2)


if __name__ == "__main__":
    unittest.main()
