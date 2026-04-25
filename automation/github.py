from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re

from automation.shell import run_command


BOT_LOGIN = "chatgpt-codex-connector[bot]"
CLEAN_REVIEW_RE = re.compile(r"didn['’]?t find any major issues", re.IGNORECASE)


@dataclass(frozen=True)
class ReviewComment:
    path: str | None
    line: int | None
    body: str
    url: str | None
    author: str
    created_at: str | None


@dataclass(frozen=True)
class ReviewStatus:
    state: str
    actionable_comments: list[ReviewComment]
    latest_bot_comment: str | None


def parse_remote_owner_repo(repo_root: Path) -> tuple[str, str]:
    result = run_command(
        ["git", "remote", "get-url", "origin"],
        cwd=repo_root,
    )
    remote = result.stdout.strip()
    ssh_match = re.match(r"git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$", remote)
    https_match = re.match(
        r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
        remote,
    )
    match = ssh_match or https_match
    if not match:
        raise RuntimeError(f"could not parse GitHub remote: {remote}")
    return match.group("owner"), match.group("repo")


def create_pr(
    repo_root: Path,
    *,
    title: str,
    body: str,
    base: str,
    head: str,
) -> tuple[int, str]:
    result = run_command(
        [
            "gh",
            "pr",
            "create",
            "--base",
            base,
            "--head",
            head,
            "--title",
            title,
            "--body",
            body,
        ],
        cwd=repo_root,
    )
    pr_reference = result.stdout.strip().splitlines()[-1].strip()
    details = run_command(
        ["gh", "pr", "view", pr_reference, "--json", "number,url"],
        cwd=repo_root,
    )
    payload = json.loads(details.stdout)
    return int(payload["number"]), payload["url"]


def request_codex_review(repo_root: Path, pr_number: int) -> None:
    run_command(
        ["gh", "pr", "comment", str(pr_number), "--body", "@codex review"],
        cwd=repo_root,
    )


def merge_pr(repo_root: Path, pr_number: int) -> None:
    run_command(
        ["gh", "pr", "merge", str(pr_number), "--squash", "--delete-branch"],
        cwd=repo_root,
    )


def fetch_review_status(repo_root: Path, pr_number: int) -> ReviewStatus:
    owner, repo = parse_remote_owner_repo(repo_root)
    query = """
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100) {
        nodes {
          isResolved
          comments(first: 20) {
            nodes {
              author { login }
              body
              path
              line
              url
              createdAt
            }
          }
        }
      }
      comments(last: 20) {
        nodes {
          author { login }
          body
          createdAt
          url
        }
      }
    }
  }
}
""".strip()
    result = run_command(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={query}",
            "-F",
            f"owner={owner}",
            "-F",
            f"repo={repo}",
            "-F",
            f"number={pr_number}",
        ],
        cwd=repo_root,
    )
    payload = json.loads(result.stdout)
    return parse_review_payload(payload)


def parse_review_payload(payload: dict) -> ReviewStatus:
    pull_request = payload["data"]["repository"]["pullRequest"]
    threads = pull_request["reviewThreads"]["nodes"]
    issue_comments = pull_request["comments"]["nodes"]

    actionable: list[ReviewComment] = []
    for thread in threads:
        if thread.get("isResolved"):
            continue
        comments = thread["comments"]["nodes"]
        bot_comments = [
            comment
            for comment in comments
            if ((comment.get("author") or {}).get("login") == BOT_LOGIN)
        ]
        if not bot_comments:
            continue
        latest = bot_comments[-1]
        actionable.append(
            ReviewComment(
                path=latest.get("path"),
                line=latest.get("line"),
                body=latest["body"],
                url=latest.get("url"),
                author=BOT_LOGIN,
                created_at=latest.get("createdAt"),
            )
        )

    bot_issue_comments = [
        comment
        for comment in issue_comments
        if ((comment.get("author") or {}).get("login") == BOT_LOGIN)
    ]
    latest_bot_comment = bot_issue_comments[-1]["body"] if bot_issue_comments else None

    if actionable:
        return ReviewStatus(
            state="actionable",
            actionable_comments=actionable,
            latest_bot_comment=latest_bot_comment,
        )

    if latest_bot_comment and CLEAN_REVIEW_RE.search(latest_bot_comment):
        return ReviewStatus(
            state="clean",
            actionable_comments=[],
            latest_bot_comment=latest_bot_comment,
        )

    return ReviewStatus(
        state="waiting",
        actionable_comments=[],
        latest_bot_comment=latest_bot_comment,
    )

