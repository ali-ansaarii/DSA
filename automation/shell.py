from __future__ import annotations

from dataclasses import dataclass
import subprocess
from pathlib import Path
from typing import Mapping


@dataclass
class CommandResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


class CommandError(RuntimeError):
    def __init__(self, message: str, result: CommandResult) -> None:
        super().__init__(message)
        self.result = result


def run_command(
    args: list[str],
    *,
    cwd: Path,
    env: Mapping[str, str] | None = None,
    check: bool = True,
) -> CommandResult:
    completed = subprocess.run(
        args,
        cwd=str(cwd),
        env=dict(env) if env is not None else None,
        capture_output=True,
        text=True,
        check=False,
    )
    result = CommandResult(
        args=args,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
    if check and completed.returncode != 0:
        command_text = " ".join(args)
        raise CommandError(
            f"command failed with exit code {completed.returncode}: {command_text}",
            result,
        )
    return result
