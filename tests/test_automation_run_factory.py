from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from automation import state
from automation.github import ReviewComment, ReviewRequestComment, ReviewRequestReceipt, ReviewStatus
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

    def test_pickup_timeout_honors_total_request_limit(self) -> None:
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
                review_request_attempts=1,
                review_request_pickup_retries=0,
                review_request_comment_id=123,
                review_request_comment_created_at="2026-04-26T20:00:00+00:00",
            )
            store.initialize(snapshot)
            store.append_progress(
                state.ProgressEntry(
                    step_name="request_review",
                    state_before=state.STATE_PR_OPEN,
                    state_after=state.STATE_REVIEW_REQUESTED,
                    start_timestamp="2026-04-26T20:00:00+00:00",
                    end_timestamp="2026-04-26T20:00:00+00:00",
                    outcome="success",
                    evidence={"pr_number": 33, "request_comment_id": 123},
                    note="requested Codex review",
                )
            )
            store.append_progress(
                state.ProgressEntry(
                    step_name="enter_review_wait",
                    state_before=state.STATE_REVIEW_REQUESTED,
                    state_after=state.STATE_REVIEW_WAITING,
                    start_timestamp="2026-04-26T20:00:00+00:00",
                    end_timestamp="2026-04-26T20:00:00+00:00",
                    outcome="success",
                    evidence={},
                    note="review requested; waiting for Codex response",
                )
            )

            runner = AutomationRunner.__new__(AutomationRunner)
            runner.repo_root = Path(temp_dir)
            runner.store = store
            runner.paths = paths
            runner.snapshot = snapshot
            runner.args = SimpleNamespace(
                max_review_fixes=3,
                max_review_request_attempts=1,
                review_request_pickup_timeout_seconds=90,
                review_timeout_seconds=1800,
                poll_interval_seconds=120,
            )
            runner._ensure_run_branch_checked_out = lambda: None
            runner._ensure_model_client = lambda: None

            with (
                patch(
                    "automation.run_factory.github.fetch_review_request_receipt",
                    return_value=ReviewRequestReceipt(state="waiting", seen_at=None),
                ),
                patch(
                    "automation.run_factory.github.fetch_review_status",
                    return_value=ReviewStatus(
                        state="waiting",
                        actionable_comments=[],
                        latest_bot_comment=None,
                        latest_bot_review_state=None,
                        latest_bot_review_body=None,
                    ),
                ),
                patch("automation.run_factory.datetime") as datetime_mock,
                patch.object(runner, "_request_review") as request_review_mock,
            ):
                real_datetime = __import__("datetime").datetime
                datetime_mock.now.return_value = real_datetime.fromisoformat("2026-04-26T20:02:00+00:00")
                datetime_mock.fromisoformat.side_effect = real_datetime.fromisoformat
                with self.assertRaises(RuntimeError) as ctx:
                    runner._poll_review()

            self.assertIn("did not acknowledge", str(ctx.exception))
            request_review_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
