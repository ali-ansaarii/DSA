from __future__ import annotations

import unittest

from automation.github import BOT_LOGIN, parse_review_payload


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


if __name__ == "__main__":
    unittest.main()
