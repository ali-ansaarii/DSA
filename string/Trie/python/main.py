from __future__ import annotations

import sys
import time
from pathlib import Path

from Trie import execute_trie_commands


def read_commands(input_path: Path) -> list[tuple[str, str]]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if not tokens:
        raise ValueError("Input file is empty")

    command_count = int(tokens[0])
    expected_tokens = 1 + command_count * 2
    if len(tokens) < expected_tokens:
        raise ValueError("Input file ended before all commands were read")

    commands: list[tuple[str, str]] = []
    index = 1
    for _ in range(command_count):
        operation = tokens[index]
        value = tokens[index + 1]
        commands.append((operation, value))
        index += 2

    return commands


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_trie = False

    for argument in sys.argv[1:]:
        if argument == "--time-trie":
            time_flag_time_trie = True
        else:
            input_path = Path(argument)

    try:
        commands = read_commands(input_path)

        start = time.perf_counter()
        output = execute_trie_commands(commands)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        if output:
            print("\n".join(output))

        if time_flag_time_trie:
            print(f"trie_processing_ms={elapsed_ms:.6f}", file=sys.stderr)
    except Exception as error:  # noqa: BLE001 - command-line runner should report any failure clearly.
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
