from __future__ import annotations

from pathlib import Path
from unittest import mock
import unittest

from automation import git_ops


class GitOpsTests(unittest.TestCase):
    def test_ensure_clean_base_branch_allows_detached_head_at_base_commit(self) -> None:
        repo_root = Path("/tmp/fake-repo")

        with (
            mock.patch.object(git_ops, "current_branch", return_value=""),
            mock.patch.object(git_ops, "current_commit", return_value="abc123"),
            mock.patch.object(git_ops, "resolve_ref_commit", return_value="abc123"),
            mock.patch.object(git_ops, "run_command") as run_command_mock,
        ):
            run_command_mock.return_value.stdout = ""
            git_ops.ensure_clean_base_branch(repo_root, "main")
            run_command_mock.assert_called_once()

    def test_ensure_clean_base_branch_rejects_detached_head_at_wrong_commit(self) -> None:
        repo_root = Path("/tmp/fake-repo")

        with (
            mock.patch.object(git_ops, "current_branch", return_value=""),
            mock.patch.object(git_ops, "current_commit", return_value="abc123"),
            mock.patch.object(git_ops, "resolve_ref_commit", return_value="def456"),
        ):
            with self.assertRaisesRegex(RuntimeError, "detached worktree"):
                git_ops.ensure_clean_base_branch(repo_root, "main")


if __name__ == "__main__":
    unittest.main()
