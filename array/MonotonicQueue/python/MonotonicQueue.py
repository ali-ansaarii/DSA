from collections import deque
from typing import Sequence


def sliding_window_maximum(values: Sequence[int], window_size: int) -> list[int]:
    candidate_indices: deque[int] = deque()
    maxima: list[int] = []

    for index, value in enumerate(values):
        while candidate_indices and candidate_indices[0] <= index - window_size:
            candidate_indices.popleft()

        while candidate_indices and values[candidate_indices[-1]] <= value:
            candidate_indices.pop()

        candidate_indices.append(index)

        if index + 1 >= window_size:
            maxima.append(values[candidate_indices[0]])

    return maxima
