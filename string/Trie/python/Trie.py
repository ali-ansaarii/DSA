from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class _Node:
    children: list[_Node | None] = field(default_factory=lambda: [None] * 26)
    is_word: bool = False


class Trie:
    def __init__(self) -> None:
        self._root = _Node()

    def insert(self, word: str) -> None:
        current = self._root
        for char in word:
            index = self._index(char)
            if current.children[index] is None:
                current.children[index] = _Node()
            current = current.children[index]
        current.is_word = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def _find_node(self, text: str) -> _Node | None:
        current = self._root
        for char in text:
            index = self._index(char)
            child = current.children[index]
            if child is None:
                return None
            current = child
        return current

    @staticmethod
    def _index(char: str) -> int:
        index = ord(char) - ord("a")
        if index < 0 or index >= 26:
            raise ValueError("Trie only supports lowercase English letters")
        return index


def execute_trie_commands(commands: list[tuple[str, str]]) -> list[str]:
    trie = Trie()
    output: list[str] = []

    for operation, value in commands:
        if operation == "insert":
            trie.insert(value)
        elif operation == "search":
            output.append("true" if trie.search(value) else "false")
        elif operation == "starts_with":
            output.append("true" if trie.starts_with(value) else "false")
        else:
            raise ValueError(f"Unknown trie command: {operation}")

    return output
