from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import MagicMock, patch

from automation.github import (
    BOT_LOGINS,
    ReviewRequestComment,
    ReviewRequestReceipt,
    fetch_review_request_receipt,
    get_review_token,
    merge_pr,
    parse_review_payload,
    request_codex_review,
)


class GitHubReviewParsingTests(unittest.TestCase):
    def test_bot_login_set_covers_issue_and_review_surfaces(self) -> None:
        self.assertIn("chatgpt-codex-connector[bot]", BOT_LOGINS)
        self.assertIn("chatgpt-codex-connector", BOT_LOGINS)

    def test_clean_review_detected_from_bot_issue_comment(self) -> None:
        payload = {
            "data": {
                "repository": {
                    "pullRequest": {
                        "reviewThreads": {"nodes": []},
                        "comments": {
                            "nodes": [
                                {
                                    "author": {"login": "chatgpt-codex-connector[bot]"},
                                    "body": "Codex Review: Didn't find any major issues. Nice work!",
                                    "createdAt": "2026-04-25T10:00:00Z",
                                    "url": "https://example.test/comment/1",
                                }
                            ]
                        },
                        "reviews": {"nodes": []},
                    }
                }
            }
        }
        status = parse_review_payload(payload)
        self.assertEqual(status.state, "clean")
        self.assertEqual(status.actionable_comments, [])

    def test_alternate_clean_review_phrases_are_detected(self) -> None:
        for body in (
            "Codex Review: No major issues found.",
            "Codex Review: No issues found.",
            "Codex Review: Nothing major to flag here.",
            "Codex Review: Looks good to me.",
            "Codex Review: LGTM",
        ):
            payload = {
                "data": {
                    "repository": {
                        "pullRequest": {
                            "reviewThreads": {"nodes": []},
                            "comments": {
                                "nodes": [
                                    {
                                        "author": {"login": "chatgpt-codex-connector[bot]"},
                                        "body": body,
                                        "createdAt": "2026-04-25T10:00:00Z",
                                        "url": "https://example.test/comment/alt-clean",
                                    }
                                ]
                            },
                            "reviews": {"nodes": []},
                        }
                    }
                }
            }
            status = parse_review_payload(payload)
            self.assertEqual(status.state, "clean", body)
            self.assertEqual(status.actionable_comments, [], body)

    def test_generic_wrapper_comment_is_not_treated_as_clean(self) -> None:
        payload = {
            "data": {
                "repository": {
                    "pullRequest": {
                        "reviewThreads": {"nodes": []},
                        "comments": {
                            "nodes": [
                                {
                                    "author": {"login": "chatgpt-codex-connector[bot]"},
                                    "body": (
                                        "### 💡 Codex Review\n\n"
                                        "Here are some automated review suggestions for this pull request."
                                    ),
                                    "createdAt": "2026-04-25T10:00:00Z",
                                    "url": "https://example.test/comment/wrapper",
                                }
                            ]
                        },
                        "reviews": {"nodes": []},
                    }
                }
            }
        }
        status = parse_review_payload(payload)
        self.assertEqual(status.state, "waiting")
        self.assertEqual(status.actionable_comments, [])

    def test_unresolved_bot_thread_is_actionable(self) -> None:
        payload = {
            "data": {
                "repository": {
                    "pullRequest": {
                        "reviewThreads": {
                            "nodes": [
                                {
                                    "isResolved": False,
                                    "comments": {
                                        "nodes": [
                                            {
                                                "author": {"login": "chatgpt-codex-connector"},
                                                "body": "P2: This parser accepts trailing junk.",
                                                "path": "array/Topic/python/main.py",
                                                "line": 42,
                                                "url": "https://example.test/comment/2",
                                                "createdAt": "2026-04-25T10:01:00Z",
                                            }
                                        ]
                                    },
                                }
                            ]
                        },
                        "comments": {"nodes": []},
                        "reviews": {"nodes": []},
                    }
                }
            }
        }
        status = parse_review_payload(payload)
        self.assertEqual(status.state, "actionable")
        self.assertEqual(len(status.actionable_comments), 1)
        self.assertEqual(status.actionable_comments[0].line, 42)

    def test_stale_thread_is_ignored_after_new_review_request(self) -> None:
        payload = {
            "data": {
                "repository": {
                    "pullRequest": {
                        "reviewThreads": {
                            "nodes": [
                                {
                                    "isResolved": False,
                                    "comments": {
                                        "nodes": [
                                            {
                                                "author": {"login": "chatgpt-codex-connector"},
                                                "body": "P2: old actionable comment",
                                                "path": "sorting/Topic/Makefile",
                                                "line": 10,
                                                "url": "https://example.test/comment/3",
                                                "createdAt": "2026-04-25T18:43:33Z",
                                            }
                                        ]
                                    },
                                }
                            ]
                        },
                        "comments": {
                            "nodes": [
                                {
                                    "author": {"login": "chatgpt-codex-connector[bot]"},
                                    "body": "Codex Review: Didn't find any major issues.",
                                    "createdAt": "2026-04-25T18:55:00Z",
                                    "url": "https://example.test/comment/4",
                                }
                            ]
                        },
                        "reviews": {
                            "nodes": [
                                {
                                    "author": {"login": "chatgpt-codex-connector"},
                                    "body": "Codex Review",
                                    "submittedAt": "2026-04-25T18:55:00Z",
                                    "state": "COMMENTED",
                                }
                            ]
                        },
                    }
                }
            }
        }
        status = parse_review_payload(payload, not_before="2026-04-25T18:51:50+00:00")
        self.assertEqual(status.state, "clean")
        self.assertEqual(status.actionable_comments, [])

    def test_non_clean_bot_review_is_not_treated_as_clean(self) -> None:
        payload = {
            "data": {
                "repository": {
                    "pullRequest": {
                        "reviewThreads": {"nodes": []},
                        "comments": {"nodes": []},
                        "reviews": {
                            "nodes": [
                                {
                                    "author": {"login": "chatgpt-codex-connector"},
                                    "body": "Please address the remaining concerns.",
                                    "submittedAt": "2026-04-25T19:00:00Z",
                                    "state": "CHANGES_REQUESTED",
                                }
                            ]
                        },
                    }
                }
            }
        }
        status = parse_review_payload(payload)
        self.assertEqual(status.state, "actionable")
        self.assertEqual(len(status.actionable_comments), 1)
        self.assertIn("remaining concerns", status.actionable_comments[0].body)

    def test_commented_bot_review_without_clean_signal_is_actionable(self) -> None:
        payload = {
            "data": {
                "repository": {
                    "pullRequest": {
                        "reviewThreads": {"nodes": []},
                        "comments": {"nodes": []},
                        "reviews": {
                            "nodes": [
                                {
                                    "author": {"login": "chatgpt-codex-connector"},
                                    "body": "You still need to address the queue semantics issue.",
                                    "submittedAt": "2026-04-25T19:00:00Z",
                                    "state": "COMMENTED",
                                }
                            ]
                        },
                    }
                }
            }
        }
        status = parse_review_payload(payload)
        self.assertEqual(status.state, "actionable")
        self.assertEqual(len(status.actionable_comments), 1)
        self.assertIn("queue semantics", status.actionable_comments[0].body)


class GitHubReviewRequestTests(unittest.TestCase):
    def test_get_review_token_prefers_explicit_review_token(self) -> None:
        with TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / ".env").write_text(
                "GH_TOKEN=gh-token\nGITHUB_REVIEW_TOKEN=review-token\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(get_review_token(repo_root), "review-token")

    def test_get_review_token_falls_back_to_gh_token(self) -> None:
        with TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / ".env").write_text("GH_TOKEN: gh-token\n", encoding="utf-8")
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(get_review_token(repo_root), "gh-token")

    @patch("automation.github.request.urlopen")
    @patch("automation.github.parse_remote_owner_repo", return_value=("ali-ansaarii", "DSA"))
    def test_request_codex_review_uses_token_api_when_available(
        self,
        parse_remote_owner_repo_mock: MagicMock,
        urlopen_mock: MagicMock,
    ) -> None:
        response = MagicMock()
        response.read.return_value = (
            b'{"id": 12345, "created_at": "2026-04-26T20:14:32Z"}'
        )
        urlopen_mock.return_value.__enter__.return_value = response
        with TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / ".env").write_text("GH_TOKEN=gh-token\n", encoding="utf-8")
            with patch.dict(os.environ, {}, clear=True):
                comment = request_codex_review(repo_root, 25)

        parse_remote_owner_repo_mock.assert_called_once_with(Path(tmp))
        req = urlopen_mock.call_args.args[0]
        self.assertEqual(
            req.full_url,
            "https://api.github.com/repos/ali-ansaarii/DSA/issues/25/comments",
        )
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(req.headers["Authorization"], "token gh-token")
        self.assertEqual(
            comment,
            ReviewRequestComment(comment_id=12345, created_at="2026-04-26T20:14:32Z"),
        )

    @patch("automation.github.request.urlopen")
    @patch("automation.github.parse_remote_owner_repo", return_value=("ali-ansaarii", "DSA"))
    def test_fetch_review_request_receipt_detects_eyes_and_thumbs_up(
        self,
        parse_remote_owner_repo_mock: MagicMock,
        urlopen_mock: MagicMock,
    ) -> None:
        response = MagicMock()
        response.read.return_value = (
            b'[{"content":"eyes","created_at":"2026-04-26T20:14:41Z","user":{"login":"chatgpt-codex-connector[bot]"}}]'
        )
        urlopen_mock.return_value.__enter__.return_value = response
        with TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / ".env").write_text("GH_TOKEN=gh-token\n", encoding="utf-8")
            with patch.dict(os.environ, {}, clear=True):
                receipt = fetch_review_request_receipt(repo_root, comment_id=99)

        parse_remote_owner_repo_mock.assert_called_once_with(Path(tmp))
        self.assertEqual(
            receipt,
            ReviewRequestReceipt(state="acknowledged", seen_at="2026-04-26T20:14:41Z"),
        )

    @patch("automation.github.request.urlopen")
    @patch("automation.github.parse_remote_owner_repo", return_value=("ali-ansaarii", "DSA"))
    def test_fetch_review_request_receipt_detects_clean_thumbs_up(
        self,
        parse_remote_owner_repo_mock: MagicMock,
        urlopen_mock: MagicMock,
    ) -> None:
        response = MagicMock()
        response.read.return_value = (
            b'[{"content":"+1","created_at":"2026-04-26T20:20:00Z","user":{"login":"chatgpt-codex-connector[bot]"}}]'
        )
        urlopen_mock.return_value.__enter__.return_value = response
        with TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / ".env").write_text("GH_TOKEN=gh-token\n", encoding="utf-8")
            with patch.dict(os.environ, {}, clear=True):
                receipt = fetch_review_request_receipt(repo_root, comment_id=100)

        parse_remote_owner_repo_mock.assert_called_once_with(Path(tmp))
        self.assertEqual(
            receipt,
            ReviewRequestReceipt(state="clean", seen_at="2026-04-26T20:20:00Z"),
        )

    @patch("automation.github.run_command")
    def test_merge_pr_omits_delete_branch_when_requested(
        self,
        run_command_mock: MagicMock,
    ) -> None:
        merge_pr(Path("/tmp/repo"), 28, delete_branch=False)
        run_command_mock.assert_called_once_with(
            ["gh", "pr", "merge", "28", "--squash"],
            cwd=Path("/tmp/repo"),
        )

    @patch("automation.github.run_command")
    def test_merge_pr_deletes_branch_by_default(
        self,
        run_command_mock: MagicMock,
    ) -> None:
        merge_pr(Path("/tmp/repo"), 28)
        run_command_mock.assert_called_once_with(
            ["gh", "pr", "merge", "28", "--squash", "--delete-branch"],
            cwd=Path("/tmp/repo"),
        )


if __name__ == "__main__":
    unittest.main()
