from __future__ import annotations

import sys
import time
from pathlib import Path

from KMP import kmp


def read_input(input_path: Path) -> tuple[str, str]:
    with input_path.open("r", encoding="utf-8") as file:
        lines = file.read().splitlines()

    if len(lines) < 2:
        raise ValueError("input file must contain a text line and a pattern line")

    return lines[0], lines[1]


def print_matches(matches: list[int]) -> None:
    print(" ".join(str(index) for index in matches))


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_kmp = False

    for argument in sys.argv[1:]:
        if argument == "--time-kmp":
            time_flag_time_kmp = True
        else:
            input_path = Path(argument)

    try:
        text, pattern = read_input(input_path)

        if time_flag_time_kmp:
            start = time.perf_counter()
            matches = kmp(text, pattern)
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            print(f"algorithm_time_ms: {elapsed_ms:.6f}", file=sys.stderr)
        else:
            matches = kmp(text, pattern)

        print_matches(matches)
    except Exception as error:  # noqa: BLE001 - keep runner errors simple for CLI use.
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
