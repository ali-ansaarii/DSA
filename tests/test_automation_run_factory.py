from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from automation import state
from automation.github import ReviewRequestComment
from automation.run_factory import AutomationRunner


class RunFactoryReviewRequestTests(unittest.TestCase):
    def test_request_review_resets_pickup_retries_for_normal_request(self) -> None:
        with TemporaryDirectory() as temp_dir:
            paths = state.RunPaths.create(Path(temp_dir), "binary-search-on-answer")
            store = state.RunStore(paths)
            snapshot = state.RunSnapshot(
                run_id="binary-search-on-answer",
                algorithm_name="Binary Search on Answer",
                checklist_label="Binary Search on Answer",
                branch_name="binary-search-on-answer",
                topic_path="array/BinarySearchOnAnswer",
                display_name="Binary Search on Answer",
                pr_title="Add Binary Search on Answer",
                current_state=state.STATE_PR_OPEN,
                pr_number=33,
                review_request_attempts=2,
                review_request_pickup_retries=2,
            )
            store.initialize(snapshot)

            runner = AutomationRunner.__new__(AutomationRunner)
            runner.repo_root = Path(temp_dir)
            runner.store = store
            runner.snapshot = snapshot
            runner._ensure_run_branch_checked_out = lambda: None

            with patch(
                "automation.run_factory.github.request_codex_review",
                return_value=ReviewRequestComment(
                    comment_id=123,
                    created_at="2026-04-26T20:14:32Z",
                ),
            ):
                runner._request_review()

            self.assertEqual(runner.snapshot.review_request_attempts, 3)
            self.assertEqual(runner.snapshot.review_request_pickup_retries, 0)
            self.assertEqual(runner.snapshot.review_request_comment_id, 123)
            self.assertEqual(runner.snapshot.current_state, state.STATE_REVIEW_REQUESTED)

    def test_request_review_increments_pickup_retries_for_retry_request(self) -> None:
        with TemporaryDirectory() as temp_dir:
            paths = state.RunPaths.create(Path(temp_dir), "binary-search-on-answer")
            store = state.RunStore(paths)
            snapshot = state.RunSnapshot(
                run_id="binary-search-on-answer",
                algorithm_name="Binary Search on Answer",
                checklist_label="Binary Search on Answer",
                branch_name="binary-search-on-answer",
                topic_path="array/BinarySearchOnAnswer",
                display_name="Binary Search on Answer",
                pr_title="Add Binary Search on Answer",
                current_state=state.STATE_REVIEW_WAITING,
                pr_number=33,
                review_request_attempts=3,
                review_request_pickup_retries=1,
            )
            store.initialize(snapshot)

            runner = AutomationRunner.__new__(AutomationRunner)
            runner.repo_root = Path(temp_dir)
            runner.store = store
            runner.snapshot = snapshot
            runner._ensure_run_branch_checked_out = lambda: None

            with patch(
                "automation.run_factory.github.request_codex_review",
                return_value=ReviewRequestComment(
                    comment_id=456,
                    created_at="2026-04-26T20:20:00Z",
                ),
            ):
                runner._request_review(pickup_retry=True)

            self.assertEqual(runner.snapshot.review_request_attempts, 4)
            self.assertEqual(runner.snapshot.review_request_pickup_retries, 2)
            self.assertEqual(runner.snapshot.review_request_comment_id, 456)
            self.assertEqual(runner.snapshot.current_state, state.STATE_REVIEW_REQUESTED)


if __name__ == "__main__":
    unittest.main()
