from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import MagicMock, patch

from automation.github import (
    BOT_LOGIN,
    get_review_token,
    parse_review_payload,
    request_codex_review,
)


class GitHubReviewParsingTests(unittest.TestCase):
    def test_clean_review_detected_from_bot_issue_comment(self) -> None:
        payload = {
            "data": {
                "repository": {
                    "pullRequest": {
                        "reviewThreads": {"nodes": []},
                        "comments": {
                            "nodes": [
                                {
                                    "author": {"login": BOT_LOGIN},
                                    "body": "Codex Review: Didn't find any major issues. Nice work!",
                                    "createdAt": "2026-04-25T10:00:00Z",
                                    "url": "https://example.test/comment/1",
                                }
                            ]
                        },
                    }
                }
            }
        }
        status = parse_review_payload(payload)
        self.assertEqual(status.state, "clean")
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
                                                "author": {"login": BOT_LOGIN},
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
                    }
                }
            }
        }
        status = parse_review_payload(payload)
        self.assertEqual(status.state, "actionable")
        self.assertEqual(len(status.actionable_comments), 1)
        self.assertEqual(status.actionable_comments[0].line, 42)


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
        response.status = 201
        urlopen_mock.return_value.__enter__.return_value = response
        with TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            (repo_root / ".env").write_text("GH_TOKEN=gh-token\n", encoding="utf-8")
            with patch.dict(os.environ, {}, clear=True):
                request_codex_review(repo_root, 25)

        parse_remote_owner_repo_mock.assert_called_once_with(Path(tmp))
        req = urlopen_mock.call_args.args[0]
        self.assertEqual(
            req.full_url,
            "https://api.github.com/repos/ali-ansaarii/DSA/issues/25/comments",
        )
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(req.headers["Authorization"], "token gh-token")


if __name__ == "__main__":
    unittest.main()
