from __future__ import annotations

from pathlib import Path

from automation.shell import run_command


def current_branch(repo_root: Path) -> str:
    result = run_command(
        ["git", "branch", "--show-current"],
        cwd=repo_root,
    )
    return result.stdout.strip()


def current_commit(repo_root: Path) -> str:
    result = run_command(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
    )
    return result.stdout.strip()


def resolve_ref_commit(repo_root: Path, ref_name: str) -> str:
    result = run_command(
        ["git", "rev-parse", ref_name],
        cwd=repo_root,
    )
    return result.stdout.strip()


def ensure_clean_base_branch(repo_root: Path, base_branch: str) -> None:
    branch = current_branch(repo_root)
    if branch != base_branch:
        if branch:
            raise RuntimeError(
                f"automation must start from {base_branch}, found branch: {branch}"
            )
        current = current_commit(repo_root)
        expected = resolve_ref_commit(repo_root, base_branch)
        if current != expected:
            raise RuntimeError(
                "automation must start from the base branch tip or a detached worktree at "
                f"that exact commit; expected {base_branch}@{expected}, found {current}"
            )
    result = run_command(
        ["git", "status", "--porcelain"],
        cwd=repo_root,
    )
    if result.stdout.strip():
        raise RuntimeError("automation requires a clean working tree")


def create_branch(repo_root: Path, branch_name: str) -> None:
    run_command(
        ["git", "checkout", "-b", branch_name],
        cwd=repo_root,
    )


def checkout_branch(repo_root: Path, branch_name: str) -> None:
    run_command(
        ["git", "checkout", branch_name],
        cwd=repo_root,
    )


def checkout_base_branch(repo_root: Path, base_branch: str) -> None:
    checkout_branch(repo_root, base_branch)


def stage_paths(repo_root: Path, paths: list[str]) -> None:
    if not paths:
        raise ValueError("no paths to stage")
    run_command(
        ["git", "add", "--", *paths],
        cwd=repo_root,
    )


def commit(repo_root: Path, message: str) -> None:
    run_command(
        ["git", "commit", "-m", message],
        cwd=repo_root,
    )


def push_new_branch(repo_root: Path, branch_name: str) -> None:
    run_command(
        ["git", "push", "-u", "origin", branch_name],
        cwd=repo_root,
    )


def push_current_branch(repo_root: Path) -> None:
    run_command(
        ["git", "push"],
        cwd=repo_root,
    )


def pull_base_ff_only(repo_root: Path, base_branch: str) -> None:
    run_command(
        ["git", "pull", "--ff-only", "origin", base_branch],
        cwd=repo_root,
    )


def delete_local_branch(repo_root: Path, branch_name: str) -> None:
    run_command(
        ["git", "branch", "-D", branch_name],
        cwd=repo_root,
    )


def delete_remote_branch(repo_root: Path, branch_name: str, remote_name: str = "origin") -> None:
    run_command(
        ["git", "push", remote_name, "--delete", branch_name],
        cwd=repo_root,
    )


def list_local_branches(repo_root: Path) -> set[str]:
    result = run_command(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads"],
        cwd=repo_root,
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def list_remote_branches(repo_root: Path, remote_name: str = "origin") -> set[str]:
    result = run_command(
        ["git", "ls-remote", "--heads", remote_name],
        cwd=repo_root,
    )
    branches: set[str] = set()
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        ref = parts[1].strip()
        prefix = "refs/heads/"
        if ref.startswith(prefix):
            branches.add(ref[len(prefix):])
    return branches


def add_detached_worktree(repo_root: Path, worktree_path: Path, start_point: str) -> None:
    run_command(
        [
            "git",
            "worktree",
            "add",
            "--detach",
            str(worktree_path),
            start_point,
        ],
        cwd=repo_root,
    )


def remove_worktree(repo_root: Path, worktree_path: Path, *, force: bool = False) -> None:
    args = ["git", "worktree", "remove"]
    if force:
        args.append("--force")
    args.append(str(worktree_path))
    run_command(
        args,
        cwd=repo_root,
    )
